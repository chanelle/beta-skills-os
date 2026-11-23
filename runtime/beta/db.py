"""SQLite persistence with versioned migrations. Stdlib only."""
import sqlite3
import time
import uuid
from pathlib import Path

MIGRATIONS = [
    # v1
    """
    CREATE TABLE projects (
        id TEXT PRIMARY KEY, name TEXT NOT NULL UNIQUE, created_at REAL NOT NULL);
    CREATE TABLE agents (
        id TEXT PRIMARY KEY, name TEXT NOT NULL UNIQUE, kind TEXT, permission_scope TEXT DEFAULT '');
    CREATE TABLE tasks (
        id TEXT PRIMARY KEY,
        project_id TEXT NOT NULL REFERENCES projects(id),
        title TEXT NOT NULL,
        owner TEXT,
        status TEXT NOT NULL DEFAULT 'queued',
        priority INTEGER NOT NULL DEFAULT 3,
        created_at REAL NOT NULL, updated_at REAL NOT NULL, due_at REAL,
        idempotency_key TEXT UNIQUE,
        input_refs TEXT DEFAULT '[]', output_refs TEXT DEFAULT '[]',
        permission_scope TEXT DEFAULT 'reversible',
        acceptance_criteria TEXT DEFAULT '[]',
        last_error TEXT, retry_count INTEGER NOT NULL DEFAULT 0,
        lease_owner TEXT, lease_expires_at REAL);
    CREATE TABLE task_dependencies (
        task_id TEXT REFERENCES tasks(id), depends_on TEXT REFERENCES tasks(id),
        PRIMARY KEY (task_id, depends_on));
    CREATE TABLE executions (
        id TEXT PRIMARY KEY, task_id TEXT REFERENCES tasks(id), agent TEXT,
        started_at REAL, finished_at REAL, outcome TEXT, idempotency_key TEXT UNIQUE);
    CREATE TABLE evidence (
        id TEXT PRIMARY KEY, task_id TEXT REFERENCES tasks(id), kind TEXT, ref TEXT,
        sha256 TEXT, observed_at REAL, check_name TEXT, passed INTEGER, detail TEXT);
    CREATE TABLE decisions (
        id TEXT PRIMARY KEY, task_id TEXT, question TEXT, answer TEXT, decided_at REAL);
    CREATE TABLE corrections (
        id TEXT PRIMARY KEY, task_id TEXT, what_was_wrong TEXT, fix TEXT, created_at REAL);
    CREATE TABLE approvals (
        id TEXT PRIMARY KEY, task_id TEXT REFERENCES tasks(id), approved_by TEXT,
        scope TEXT, approved_at REAL);
    CREATE TABLE transitions (
        id INTEGER PRIMARY KEY AUTOINCREMENT, task_id TEXT, from_status TEXT,
        to_status TEXT, actor TEXT, at REAL, note TEXT);
    """,
]


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


def now() -> float:
    return time.time()


def connect(path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(path), isolation_level=None, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def migrate(conn: sqlite3.Connection) -> int:
    conn.execute("CREATE TABLE IF NOT EXISTS schema_version (v INTEGER NOT NULL)")
    row = conn.execute("SELECT v FROM schema_version").fetchone()
    current = row["v"] if row else 0
    for i, sql in enumerate(MIGRATIONS[current:], start=current + 1):
        conn.execute("BEGIN IMMEDIATE")
        try:
            for stmt in [s for s in sql.split(";") if s.strip()]:
                conn.execute(stmt)
            if row:
                conn.execute("UPDATE schema_version SET v=?", (i,))
            else:
                conn.execute("INSERT INTO schema_version (v) VALUES (?)", (i,))
                row = {"v": i}
            conn.execute("COMMIT")
        except Exception:
            conn.execute("ROLLBACK")
            raise
    return len(MIGRATIONS)


def init(path) -> sqlite3.Connection:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    conn = connect(path)
    migrate(conn)
    return conn
