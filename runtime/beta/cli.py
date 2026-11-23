"""beta CLI. Run as: python -m beta <command>  (from runtime/), or the `beta` script.

DB path: $BETA_DB or ./.beta/state.db
"""
import argparse
import json
import os
import sys
from datetime import datetime

from . import db, engine

STATE = os.environ.get("BETA_DB", ".beta/state.db")


def _close_and_return(conn, code=0):
    conn.close()
    return code


def _ts(x):
    return datetime.fromtimestamp(x).strftime("%Y-%m-%d %H:%M") if x else "-"


def main(argv=None):
    ap = argparse.ArgumentParser(prog="beta")
    ap.add_argument("--db", default=STATE)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init")
    pa = sub.add_parser("project"); psub = pa.add_subparsers(dest="sub", required=True)
    p = psub.add_parser("add"); p.add_argument("name")
    ta = sub.add_parser("task"); tsub = ta.add_subparsers(dest="sub", required=True)
    p = tsub.add_parser("add"); p.add_argument("project"); p.add_argument("title")
    p.add_argument("--priority", type=int, default=3)
    p.add_argument("--accept", default="[]", help="JSON list of checks")
    p.add_argument("--scope", default="reversible", help="reversible | external | irreversible")
    p.add_argument("--key", help="idempotency key"); p.add_argument("--depends", nargs="*", default=[])
    p = tsub.add_parser("list"); p.add_argument("--status")
    p = tsub.add_parser("claim"); p.add_argument("agent"); p.add_argument("--id")
    p = tsub.add_parser("heartbeat"); p.add_argument("id"); p.add_argument("agent")
    p = tsub.add_parser("complete"); p.add_argument("id"); p.add_argument("agent")
    p.add_argument("--evidence", nargs="+", required=True, help="output artifact refs")
    p = tsub.add_parser("verify"); p.add_argument("id"); p.add_argument("--base", default=".")
    p.add_argument("--network", action="store_true")
    p = tsub.add_parser("fail"); p.add_argument("id"); p.add_argument("actor"); p.add_argument("error")
    p = tsub.add_parser("retry"); p.add_argument("id"); p.add_argument("actor")
    p = tsub.add_parser("approve"); p.add_argument("id"); p.add_argument("by")
    sub.add_parser("status")
    p = sub.add_parser("export"); p.add_argument("--out", default="-")
    a = ap.parse_args(argv)

    conn = db.init(a.db)
    if a.cmd == "init":
        print(f"initialized {a.db}")
    elif a.cmd == "project":
        print(engine.add_project(conn, a.name))
    elif a.cmd == "task":
        if a.sub == "add":
            print(engine.add_task(conn, a.project, a.title, priority=a.priority, acceptance=json.loads(a.accept),
                                  permission_scope=a.scope, idempotency_key=a.key, depends_on=a.depends))
        elif a.sub == "list":
            q = "SELECT id, status, priority, owner, title FROM tasks"
            rows = conn.execute(q + (" WHERE status=?" if a.status else "") + " ORDER BY priority, created_at",
                                (a.status,) if a.status else ()).fetchall()
            for r in rows:
                print(f"{r['id']}  {r['status']:<14} p{r['priority']}  {r['owner'] or '-':<10} {r['title']}")
        elif a.sub == "claim":
            tid = engine.claim(conn, a.agent, a.id)
            print(tid or "nothing ready"); return _close_and_return(conn, 0 if tid else 3)
        elif a.sub == "heartbeat":
            ok = engine.heartbeat(conn, a.id, a.agent); print("ok" if ok else "lease lost"); return _close_and_return(conn, 0 if ok else 4)
        elif a.sub == "complete":
            engine.complete(conn, a.id, a.agent, a.evidence); print("awaiting verification")
        elif a.sub == "verify":
            ok, res = engine.verify_task(conn, a.id, base=a.base, network=a.network)
            for r in res:
                print(f"  [{'PASS' if r['passed'] else 'FAIL'}] {r['check']}: {r['detail']}")
            print("VERIFIED" if ok else "FAILED"); return _close_and_return(conn, 0 if ok else 1)
        elif a.sub == "fail":
            engine.fail(conn, a.id, a.actor, a.error); print("failed")
        elif a.sub == "retry":
            engine.retry(conn, a.id, a.actor); print("ready")
        elif a.sub == "approve":
            engine.approve(conn, a.id, a.by); print("approved")
    elif a.cmd == "status":
        engine.release_expired_leases(conn)
        for r in conn.execute("SELECT status, COUNT(*) n FROM tasks GROUP BY status ORDER BY status"):
            print(f"{r['status']:<14} {r['n']}")
        last = conn.execute("SELECT MAX(at) m FROM transitions WHERE to_status='verified'").fetchone()["m"]
        print(f"last verified: {_ts(last)}")
    elif a.cmd == "export":
        data = json.dumps(engine.export(conn), indent=2, default=str)
        if a.out == "-":
            print(data)
        else:
            with open(a.out, "w") as out:
                out.write(data)
            print(f"wrote {a.out}")
    return _close_and_return(conn)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except engine.TransitionError as e:
        print(f"error: {e}", file=sys.stderr); sys.exit(2)
