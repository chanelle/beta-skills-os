"""No-network mock worker + scheduler demo.

Simulates N parallel agents pulling from one queue. It does NOT mean Claude, Kai or
ChatGPT are running in the background; it proves the queue mechanics they would use.

  python -m beta.mock_worker --db /tmp/demo.db --workdir /tmp/demo --agents claude kai chatgpt
"""
import argparse
import json
import threading
from pathlib import Path

from . import db, engine


def work_one(dbpath, agent, workdir, results):
    conn = db.connect(dbpath)
    try:
        while True:
            tid = engine.claim(conn, agent)
            if tid is None:
                return
            t = conn.execute("SELECT title, acceptance_criteria FROM tasks WHERE id=?", (tid,)).fetchone()
            outputs = []
            for spec in json.loads(t["acceptance_criteria"]):
                if "path" in spec and spec["check"].startswith("artifact"):
                    p = Path(workdir) / spec["path"]
                    p.parent.mkdir(parents=True, exist_ok=True)
                    p.write_text(f"# {t['title']}\nproduced by mock agent {agent}\n")
                    outputs.append(str(p))
            engine.heartbeat(conn, tid, agent)
            engine.complete(conn, tid, agent, outputs)
            ok, _ = engine.verify_task(conn, tid, base=workdir)
            results.append((agent, tid, ok))
    finally:
        conn.close()


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", required=True)
    ap.add_argument("--workdir", required=True)
    ap.add_argument("--agents", nargs="+", default=["claude", "kai", "chatgpt"])
    a = ap.parse_args(argv)
    bootstrap = db.init(a.db)
    bootstrap.close()
    results = []
    threads = [threading.Thread(target=work_one, args=(a.db, ag, a.workdir, results)) for ag in a.agents]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    for agent, tid, ok in results:
        print(f"{agent:<8} {tid} {'verified' if ok else 'FAILED verification'}")
    return results


if __name__ == "__main__":
    main()
