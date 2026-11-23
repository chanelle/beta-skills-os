# Beta runtime (v0.1.0): task state engine + verification gate

**Status: implemented and tested locally.** It is not deployed and not wired to live agents yet.

Stdlib-only Python 3.11+. SQLite is the canonical store. The Notion Agent Relay is meant to be a synced *view* of this database, not a second source of truth.

## Try it
```bash
cd runtime
python -m unittest discover -s tests         # 15 tests
python -m beta init
python -m beta task add demo "write report" --accept '[{"check":"artifact_nonempty","path":"out.md"}]'
python -m beta task claim claude
echo "real content" > out.md
python -m beta task complete <task_id> claude --evidence out.md
python -m beta task verify <task_id>          # runs the checks; only this can mark a task verified
python -m beta status
python -m beta export --out state.json
python -m beta.mock_worker --db .beta/state.db --workdir . --agents claude kai chatgpt   # parallel demo, no network
```

## Guarantees (each one has a test)
| Guarantee | Test |
|---|---|
| An agent saying "done" moves the task to `verification`, never to `verified` | test_fake_success_agent_cannot_mark_verified |
| No acceptance criteria means the task can't be verified | test_no_criteria_cannot_verify |
| A missing artifact or a stale checksum fails the task | test_missing_artifact_fails, test_stale_evidence_checksum_mismatch |
| Eight agents racing for one task produce exactly one execution | test_duplicate_claim_executes_once |
| The same idempotency key never creates a duplicate task | test_idempotency_key_no_duplicate_task |
| External/irreversible tasks can't be claimed until Chanelle approves | test_permission_boundary_requires_approval |
| A crashed worker's lease expires and another agent resumes the task | test_interrupted_worker_resumes |
| Dependencies unblock only when the upstream task is *verified* | test_dependency_unblocks_on_verify |

## Not done yet (honest list)
- Dashboard (workstream D): `beta export` produces the JSON it would render, but there's no UI yet.
- Real agent adapters: `handoff.schema.json` defines the contract, but Claude, Kai and ChatGPT aren't connected. `mock_worker` only proves the queue mechanics.
- Notion Relay sync.
- Network checks (`url_status`) are off unless you pass `--network`.
