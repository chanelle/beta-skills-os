"""Verification checks. A model's self-report is never evidence; these are.

Each check returns (passed: bool, detail: str, sha256: str|None).
Checks are declared per task in acceptance_criteria as JSON, e.g.
  [{"check": "artifact_nonempty", "path": "out/report.md"},
   {"check": "checksum", "path": "out/report.md", "sha256": "..."},
   {"check": "command_exit", "cmd": ["python", "-m", "unittest"], "expect": 0},
   {"check": "required_fields", "path": "out/data.json", "fields": ["id", "title"]},
   {"check": "url_status", "url": "https://...", "expect": 200},
   {"check": "manual_approval"}]
"""
import hashlib
import json
import subprocess
import urllib.request
from pathlib import Path


def _sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def artifact_exists(spec, ctx):
    p = Path(ctx["base"]) / spec["path"]
    return p.exists(), f"exists={p.exists()} {p}", _sha(p) if p.is_file() else None


def artifact_nonempty(spec, ctx):
    p = Path(ctx["base"]) / spec["path"]
    ok = p.is_file() and p.stat().st_size > 0
    return ok, f"size={p.stat().st_size if p.exists() else 'missing'}", _sha(p) if ok else None


def checksum(spec, ctx):
    p = Path(ctx["base"]) / spec["path"]
    if not p.is_file():
        return False, "missing", None
    actual = _sha(p)
    return actual == spec["sha256"], f"expected={spec['sha256'][:12]} actual={actual[:12]}", actual


def command_exit(spec, ctx):
    r = subprocess.run(spec["cmd"], cwd=ctx["base"], capture_output=True, text=True, timeout=spec.get("timeout", 300))
    expect = spec.get("expect", 0)
    tail = (r.stdout + r.stderr)[-400:]
    return r.returncode == expect, f"exit={r.returncode} expect={expect} :: {tail}", None


def required_fields(spec, ctx):
    p = Path(ctx["base"]) / spec["path"]
    try:
        data = json.loads(p.read_text())
    except Exception as e:
        return False, f"unreadable: {e}", None
    missing = [f for f in spec["fields"] if f not in data or data[f] in (None, "")]
    return not missing, f"missing={missing}", _sha(p)


def url_status(spec, ctx):
    if not ctx.get("network"):
        return False, "network checks disabled (pass --network to enable)", None
    try:
        with urllib.request.urlopen(spec["url"], timeout=20) as r:
            code = r.status
    except urllib.error.HTTPError as e:
        code = e.code
    except Exception as e:
        return False, f"error: {e}", None
    return code == spec.get("expect", 200), f"status={code}", None


def manual_approval(spec, ctx):
    ok = bool(ctx.get("approved"))
    return ok, "approval recorded" if ok else "no approval on file", None


CHECKS = {f.__name__: f for f in
          (artifact_exists, artifact_nonempty, checksum, command_exit, required_fields, url_status, manual_approval)}


def run_checks(criteria, ctx):
    """Return list of dicts. Empty criteria is a FAILURE: nothing to verify means not verified."""
    if not criteria:
        return [{"check": "acceptance_criteria", "passed": False,
                 "detail": "task has no acceptance criteria; cannot verify", "sha256": None}]
    results = []
    for spec in criteria:
        fn = CHECKS.get(spec.get("check"))
        if fn is None:
            results.append({"check": spec.get("check"), "passed": False, "detail": "unknown check", "sha256": None})
            continue
        try:
            passed, detail, sha = fn(spec, ctx)
        except Exception as e:
            passed, detail, sha = False, f"check raised: {e}", None
        results.append({"check": spec["check"], "passed": passed, "detail": detail, "sha256": sha,
                        "ref": spec.get("path") or spec.get("url") or " ".join(spec.get("cmd", []))})
    return results
