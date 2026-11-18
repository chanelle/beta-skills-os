"""Task state engine: validated transitions, leased claims, evidence-gated verification."""
import json
from . import db, verify

STATUSES = ("queued", "ready", "running", "blocked", "needs_approval", "verification", "verified", "failed")

# Allowed transitions. Note: nothing reaches 'verified' except via verify_task().
ALLOWED = {
    "queued": {"ready", "blocked", "needs_approval", "failed"},
    "ready": {"running", "blocked", "needs_approval", "failed"},
    "running": {"verification", "blocked", "failed", "ready"},  # ready = lease expired, re-queued
    "blocked": {"ready", "failed"},
    "needs_approval": {"ready", "failed"},
    "verification": {"verified", "failed", "running"},
    "verified": set(),
    "failed": {"ready"},  # explicit retry
}

LEASE_SECONDS = 15 * 60


class TransitionError(Exception):
    pass


def _transition(conn, task_id, to, actor, note="", extra_sql="", extra_args=(), _gate=False):
    if to == "verified" and not _gate:
        raise TransitionError(f"{task_id}: only the verification gate can mark a task verified")
    row = conn.execute("SELECT status FROM tasks WHERE id=?", (task_id,)).fetchone()
    if row is None:
        raise TransitionError(f"no such task {task_id}")
    frm = row["status"]
    if to not in ALLOWED[frm]:
        raise TransitionError(f"{task_id}: {frm} -> {to} not allowed")
    sets = "status=?, updated_at=?" + (", " + extra_sql if extra_sql else "")
    cur = conn.execute(f"UPDATE tasks SET {sets} WHERE id=? AND status=?",
                       (to, db.now(), *extra_args, task_id, frm))
    if cur.rowcount != 1:
        raise TransitionError(f"{task_id}: concurrent modification")
    conn.execute("INSERT INTO transitions (task_id, from_status, to_status, actor, at, note) VALUES (?,?,?,?,?,?)",
                 (task_id, frm, to, actor, db.now(), note))
    return frm


def add_project(conn, name):
    pid = db.new_id("prj")
    conn.execute("INSERT INTO projects (id, name, created_at) VALUES (?,?,?)", (pid, name, db.now()))
    return pid


def project_id(conn, name):
    r = conn.execute("SELECT id FROM projects WHERE name=?", (name,)).fetchone()
    return r["id"] if r else None


def add_task(conn, project, title, *, priority=3, acceptance=None, permission_scope="reversible",
             idempotency_key=None, depends_on=(), owner=None):
    pid = project_id(conn, project) or add_project(conn, project)
    if idempotency_key:
        existing = conn.execute("SELECT id FROM tasks WHERE idempotency_key=?", (idempotency_key,)).fetchone()
        if existing:
            return existing["id"]  # idempotent: same key, same task, no duplicate
    tid = db.new_id("tsk")
    t = db.now()
    status = "needs_approval" if permission_scope != "reversible" else "ready"
    conn.execute("BEGIN IMMEDIATE")
    try:
        conn.execute(
            """INSERT INTO tasks (id, project_id, title, owner, status, priority, created_at, updated_at,
               idempotency_key, permission_scope, acceptance_criteria) VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
            (tid, pid, title, owner, "queued", priority, t, t, idempotency_key, permission_scope,
             json.dumps(acceptance or [])))
        for d in depends_on:
            conn.execute("INSERT INTO task_dependencies VALUES (?,?)", (tid, d))
        _transition(conn, tid, "blocked" if depends_on else status, "system",
                    "waiting on dependencies" if depends_on else "created")
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise
    return tid


def approve(conn, task_id, by, scope=""):
    conn.execute("BEGIN IMMEDIATE")
    try:
        conn.execute("INSERT INTO approvals VALUES (?,?,?,?,?)", (db.new_id("apr"), task_id, by, scope, db.now()))
        st = conn.execute("SELECT status FROM tasks WHERE id=?", (task_id,)).fetchone()["status"]
        if st == "needs_approval":
            _transition(conn, task_id, "ready", by, "approved")
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise


def release_expired_leases(conn):
    """Crash recovery: a running task whose lease expired goes back to ready (state preserved)."""
    rows = conn.execute("SELECT id, lease_owner FROM tasks WHERE status='running' AND lease_expires_at < ?",
                        (db.now(),)).fetchall()
    for r in rows:
        conn.execute("BEGIN IMMEDIATE")
        try:
            _transition(conn, r["id"], "ready", "watchdog", f"lease expired (was {r['lease_owner']})",
                        "lease_owner=NULL, lease_expires_at=NULL, retry_count=retry_count+1")
            conn.execute("COMMIT")
        except TransitionError:
            conn.execute("ROLLBACK")
    return [r["id"] for r in rows]


def _unblock(conn):
    rows = conn.execute("""SELECT t.id FROM tasks t WHERE t.status='blocked' AND NOT EXISTS (
        SELECT 1 FROM task_dependencies d JOIN tasks u ON u.id=d.depends_on
        WHERE d.task_id=t.id AND u.status!='verified')
        AND EXISTS (SELECT 1 FROM task_dependencies d WHERE d.task_id=t.id)""").fetchall()
    for r in rows:
        _transition(conn, r["id"], "ready", "system", "dependencies verified")


def claim(conn, agent, task_id=None, lease_seconds=LEASE_SECONDS):
    """Atomically claim one ready task. Two agents can never hold the same task."""
    release_expired_leases(conn)
    conn.execute("BEGIN IMMEDIATE")
    try:
        if task_id:
            row = conn.execute("SELECT id FROM tasks WHERE id=? AND status='ready'", (task_id,)).fetchone()
        else:
            row = conn.execute("SELECT id FROM tasks WHERE status='ready' ORDER BY priority, created_at LIMIT 1").fetchone()
        if row is None:
            conn.execute("ROLLBACK")
            return None
        _transition(conn, row["id"], "running", agent, "claimed",
                    "owner=?, lease_owner=?, lease_expires_at=?", (agent, agent, db.now() + lease_seconds))
        conn.execute("INSERT INTO executions (id, task_id, agent, started_at, idempotency_key) VALUES (?,?,?,?,?)",
                     (db.new_id("exe"), row["id"], agent, db.now(), f"{row['id']}:{db.now()}"))
        conn.execute("COMMIT")
        return row["id"]
    except Exception:
        conn.execute("ROLLBACK")
        raise


def heartbeat(conn, task_id, agent, lease_seconds=LEASE_SECONDS):
    cur = conn.execute("UPDATE tasks SET lease_expires_at=? WHERE id=? AND lease_owner=? AND status='running'",
                       (db.now() + lease_seconds, task_id, agent))
    return cur.rowcount == 1


def complete(conn, task_id, agent, output_refs):
    """Agent says it's done. That is a CLAIM, so the task moves to 'verification', not 'verified'."""
    row = conn.execute("SELECT lease_owner FROM tasks WHERE id=?", (task_id,)).fetchone()
    if row is None or row["lease_owner"] != agent:
        raise TransitionError(f"{agent} does not hold the lease on {task_id}")
    conn.execute("BEGIN IMMEDIATE")
    try:
        _transition(conn, task_id, "verification", agent, "agent reported completion",
                    "output_refs=?, lease_owner=NULL, lease_expires_at=NULL", (json.dumps(output_refs),))
        conn.execute("UPDATE executions SET finished_at=?, outcome='claimed_done' WHERE task_id=? AND finished_at IS NULL",
                     (db.now(), task_id))
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise


def verify_task(conn, task_id, base=".", network=False, verifier="verify-gate"):
    t = conn.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
    if t["status"] != "verification":
        raise TransitionError(f"{task_id} is {t['status']}, not awaiting verification")
    approved = conn.execute("SELECT 1 FROM approvals WHERE task_id=?", (task_id,)).fetchone() is not None
    results = verify.run_checks(json.loads(t["acceptance_criteria"]),
                                {"base": base, "network": network, "approved": approved})
    ok = all(r["passed"] for r in results)
    conn.execute("BEGIN IMMEDIATE")
    try:
        for r in results:
            conn.execute("INSERT INTO evidence VALUES (?,?,?,?,?,?,?,?,?)",
                         (db.new_id("evd"), task_id, "check", r.get("ref"), r.get("sha256"), db.now(),
                          r["check"], int(r["passed"]), r["detail"]))
        if ok:
            _transition(conn, task_id, "verified", verifier, "all checks passed", _gate=True)
            _unblock(conn)
        else:
            failed = "; ".join(f"{r['check']}: {r['detail']}" for r in results if not r["passed"])
            _transition(conn, task_id, "failed", verifier, "verification failed", "last_error=?", (failed[:1000],))
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise
    return ok, results


def fail(conn, task_id, actor, error):
    conn.execute("BEGIN IMMEDIATE")
    try:
        _transition(conn, task_id, "failed", actor, "reported failure",
                    "last_error=?, lease_owner=NULL, lease_expires_at=NULL", (error,))
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise


def retry(conn, task_id, actor):
    conn.execute("BEGIN IMMEDIATE")
    try:
        _transition(conn, task_id, "ready", actor, "retry", "retry_count=retry_count+1")
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise


def export(conn):
    def rows(sql, *a):
        return [dict(r) for r in conn.execute(sql, a).fetchall()]
    tasks = rows("""SELECT t.*, p.name AS project FROM tasks t JOIN projects p ON p.id=t.project_id
                    ORDER BY p.name, t.priority, t.created_at""")
    for t in tasks:
        t["evidence"] = rows("SELECT check_name, ref, sha256, passed, detail, observed_at FROM evidence WHERE task_id=? ORDER BY observed_at", t["id"])
        t["history"] = rows("SELECT from_status, to_status, actor, at, note FROM transitions WHERE task_id=? ORDER BY id", t["id"])
        t["last_verified_at"] = max((h["at"] for h in t["history"] if h["to_status"] == "verified"), default=None)
    return {"exported_at": db.now(), "tasks": tasks,
            "needs_you": [t["id"] for t in tasks if t["status"] == "needs_approval"],
            "corrections": rows("SELECT * FROM corrections ORDER BY created_at DESC")}
