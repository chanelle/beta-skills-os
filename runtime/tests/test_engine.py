import json
import os
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from beta import db, engine, mock_worker  # noqa: E402
from beta.cli import main as cli  # noqa: E402


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        self.dbpath = self.dir / "s.db"
        self.conn = db.init(self.dbpath)

    def tearDown(self):
        self.conn.close()
        self.tmp.cleanup()

    def art(self, name="out.md"):
        return [{"check": "artifact_nonempty", "path": name}]


class TestHappyPath(Base):
    def test_full_lifecycle(self):
        t = engine.add_task(self.conn, "demo", "write report", acceptance=self.art())
        self.assertEqual(engine.claim(self.conn, "claude"), t)
        (self.dir / "out.md").write_text("real content")
        engine.complete(self.conn, t, "claude", ["out.md"])
        ok, _ = engine.verify_task(self.conn, t, base=self.dir)
        self.assertTrue(ok)
        st = self.conn.execute("SELECT status FROM tasks WHERE id=?", (t,)).fetchone()["status"]
        self.assertEqual(st, "verified")
        ev = self.conn.execute("SELECT * FROM evidence WHERE task_id=?", (t,)).fetchall()
        self.assertEqual(len(ev), 1)
        self.assertIsNotNone(ev[0]["sha256"])

    def test_migration_is_versioned_and_idempotent(self):
        self.assertEqual(db.migrate(self.conn), 1)
        v = self.conn.execute("SELECT v FROM schema_version").fetchone()["v"]
        self.assertEqual(v, len(db.MIGRATIONS))


class TestNegative(Base):
    def _run(self, t, agent="claude"):
        engine.claim(self.conn, agent, t)
        engine.complete(self.conn, t, agent, ["out.md"])
        return engine.verify_task(self.conn, t, base=self.dir)

    def test_missing_artifact_fails(self):
        t = engine.add_task(self.conn, "demo", "x", acceptance=self.art())
        ok, _ = self._run(t)
        self.assertFalse(ok)
        self.assertEqual(self.conn.execute("SELECT status FROM tasks WHERE id=?", (t,)).fetchone()["status"], "failed")

    def test_fake_success_agent_cannot_mark_verified(self):
        t = engine.add_task(self.conn, "demo", "x", acceptance=self.art())
        engine.claim(self.conn, "claude", t)
        engine.complete(self.conn, t, "claude", ["out.md"])  # claims done, wrote nothing
        st = self.conn.execute("SELECT status FROM tasks WHERE id=?", (t,)).fetchone()["status"]
        self.assertEqual(st, "verification")  # a claim is not verified
        with self.assertRaises(engine.TransitionError):
            engine._transition(self.conn, t, "verified", "claude")  # agent tries to self-certify
        ok, _ = engine.verify_task(self.conn, t, base=self.dir)
        self.assertFalse(ok)

    def test_no_criteria_cannot_verify(self):
        t = engine.add_task(self.conn, "demo", "vague task", acceptance=[])
        (self.dir / "out.md").write_text("x")
        ok, res = self._run(t)
        self.assertFalse(ok)
        self.assertIn("no acceptance criteria", res[0]["detail"])

    def test_stale_evidence_checksum_mismatch(self):
        (self.dir / "out.md").write_text("v1")
        import hashlib
        old = hashlib.sha256(b"v1").hexdigest()
        t = engine.add_task(self.conn, "demo", "x", acceptance=[{"check": "checksum", "path": "out.md", "sha256": old}])
        (self.dir / "out.md").write_text("v2 edited after evidence was recorded")
        ok, _ = self._run(t)
        self.assertFalse(ok)

    def test_duplicate_claim_executes_once(self):
        t = engine.add_task(self.conn, "demo", "x", acceptance=self.art())
        winners = []

        def grab(agent):
            c = db.connect(self.dbpath)
            r = engine.claim(c, agent, t)
            if r:
                winners.append(agent)
            c.close()
        ths = [threading.Thread(target=grab, args=(f"agent{i}",)) for i in range(8)]
        [x.start() for x in ths]
        [x.join() for x in ths]
        self.assertEqual(len(winners), 1)
        n = self.conn.execute("SELECT COUNT(*) n FROM executions WHERE task_id=?", (t,)).fetchone()["n"]
        self.assertEqual(n, 1)

    def test_idempotency_key_no_duplicate_task(self):
        a = engine.add_task(self.conn, "demo", "send digest", idempotency_key="digest-2026-11-19", acceptance=self.art())
        b = engine.add_task(self.conn, "demo", "send digest", idempotency_key="digest-2026-11-19", acceptance=self.art())
        self.assertEqual(a, b)

    def test_permission_boundary_requires_approval(self):
        t = engine.add_task(self.conn, "health", "call clinic", permission_scope="external",
                            acceptance=[{"check": "manual_approval"}])
        self.assertIsNone(engine.claim(self.conn, "kai"))  # not claimable until approved
        engine.approve(self.conn, t, "chanelle")
        self.assertEqual(engine.claim(self.conn, "kai"), t)

    def test_verified_dependencies_do_not_bypass_approval(self):
        dependency = engine.add_task(self.conn, "demo", "prepare", acceptance=self.art("prepare.md"))
        engine.claim(self.conn, "claude", dependency)
        (self.dir / "prepare.md").write_text("done")
        engine.complete(self.conn, dependency, "claude", ["prepare.md"])
        engine.verify_task(self.conn, dependency, base=self.dir)
        external = engine.add_task(self.conn, "demo", "publish", permission_scope="external",
                                   acceptance=[{"check": "manual_approval"}], depends_on=[dependency])
        self.assertEqual(self.conn.execute("SELECT status FROM tasks WHERE id=?", (external,)).fetchone()["status"],
                         "needs_approval")
        self.assertIsNone(engine.claim(self.conn, "kai", external))
        engine.approve(self.conn, external, "chanelle")
        self.assertEqual(engine.claim(self.conn, "kai", external), external)

    def test_add_task_unblocks_when_dependencies_already_verified(self):
        dependency = engine.add_task(self.conn, "demo", "prepare", acceptance=self.art("prepare.md"))
        engine.claim(self.conn, "claude", dependency)
        (self.dir / "prepare.md").write_text("done")
        engine.complete(self.conn, dependency, "claude", ["prepare.md"])
        engine.verify_task(self.conn, dependency, base=self.dir)
        dependent = engine.add_task(self.conn, "demo", "next", acceptance=self.art("next.md"), depends_on=[dependency])
        self.assertEqual(self.conn.execute("SELECT status FROM tasks WHERE id=?", (dependent,)).fetchone()["status"],
                         "ready")

    def test_non_lease_holder_cannot_complete(self):
        t = engine.add_task(self.conn, "demo", "x", acceptance=self.art())
        engine.claim(self.conn, "claude", t)
        with self.assertRaises(engine.TransitionError):
            engine.complete(self.conn, t, "chatgpt", ["out.md"])

    def test_interrupted_worker_resumes(self):
        t = engine.add_task(self.conn, "demo", "x", acceptance=self.art())
        engine.claim(self.conn, "kai", t, lease_seconds=0.05)  # kai crashes, no heartbeat
        time.sleep(0.1)
        self.assertEqual(engine.claim(self.conn, "claude"), t)  # lease expired, re-claimed
        row = self.conn.execute("SELECT retry_count, owner FROM tasks WHERE id=?", (t,)).fetchone()
        self.assertEqual(row["retry_count"], 1)
        self.assertEqual(row["owner"], "claude")
        hist = [h["note"] for h in self.conn.execute("SELECT note FROM transitions WHERE task_id=?", (t,))]
        self.assertTrue(any("lease expired" in h for h in hist))

    def test_illegal_transition_rejected(self):
        t = engine.add_task(self.conn, "demo", "x", acceptance=self.art())
        with self.assertRaises(engine.TransitionError):
            engine._transition(self.conn, t, "verified", "anyone")


class TestDependenciesAndParallel(Base):
    def test_dependency_unblocks_on_verify(self):
        a = engine.add_task(self.conn, "demo", "a", acceptance=self.art("a.md"))
        b = engine.add_task(self.conn, "demo", "b", acceptance=self.art("b.md"), depends_on=[a])
        self.assertEqual(self.conn.execute("SELECT status FROM tasks WHERE id=?", (b,)).fetchone()["status"], "blocked")
        engine.claim(self.conn, "claude", a)
        (self.dir / "a.md").write_text("x")
        engine.complete(self.conn, a, "claude", ["a.md"])
        engine.verify_task(self.conn, a, base=self.dir)
        self.assertEqual(self.conn.execute("SELECT status FROM tasks WHERE id=?", (b,)).fetchone()["status"], "ready")

    def test_parallel_mock_workers(self):
        for i in range(9):
            engine.add_task(self.conn, f"stream{i % 3}", f"job {i}", acceptance=self.art(f"out/{i}.md"))
        res = mock_worker.main(["--db", str(self.dbpath), "--workdir", str(self.dir), "--agents", "claude", "kai", "chatgpt"])
        self.assertEqual(len(res), 9)
        self.assertTrue(all(ok for _, _, ok in res))
        self.assertEqual(len({tid for _, tid, _ in res}), 9)  # no task done twice


class TestCLI(Base):
    def test_cli_round_trip(self):
        d = str(self.dbpath)
        cwd = os.getcwd()
        os.chdir(self.dir)
        try:
            self.assertEqual(cli(["--db", d, "init"]), 0)
            cli(["--db", d, "task", "add", "demo", "cli job", "--accept", json.dumps(self.art())])
            tid = self.conn.execute("SELECT id FROM tasks").fetchone()["id"]
            self.assertEqual(cli(["--db", d, "task", "claim", "claude"]), 0)
            Path("out.md").write_text("x")
            cli(["--db", d, "task", "complete", tid, "claude", "--evidence", "out.md"])
            self.assertEqual(cli(["--db", d, "task", "verify", tid]), 0)
            cli(["--db", d, "export", "--out", "export.json"])
            data = json.loads(Path("export.json").read_text())
            self.assertEqual(data["tasks"][0]["status"], "verified")
        finally:
            os.chdir(cwd)


if __name__ == "__main__":
    unittest.main()
