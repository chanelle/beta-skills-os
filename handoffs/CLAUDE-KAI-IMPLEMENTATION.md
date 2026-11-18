# EXECUTION HANDOFF: Beta Skills OS → Working Council Runtime
**Owner:** Chanelle Henry. **Status:** implementation assignment, not evidence of completion. **Date:** 2026-11-18.

## Instructions to Claude and Kai
You are receiving an implementation assignment, not a request for another architecture diagram, strategy memo, or reassurance. Read this repository first. Proceed with authorized reversible work without asking for stepwise permission. If one workstream is blocked, continue other independent workstreams. Do not claim background execution unless an actual worker is running. Do not contact clinics, send marketing, spend money, deploy publicly, publish private data, or modify external accounts without explicit authorization. Do not ask Chanelle to reconstruct context that is already present in repository, Notion, or agent history.

**Definition of done:** executable software in this repository or a clearly linked implementation repo; repeatable setup instructions; passing tests with captured output; real sample run with redacted artifacts; a dashboard or CLI that shows actual task state; cross-agent adapter examples; documented failures; evidence of verified actions. A README, specification, wireframe, screenshot, or prompt alone is not done.

## Source of truth and starting facts
Repository: https://github.com/chanelle/beta-skills-os
Read README.md, docs/ARCHITECTURE.md, docs/ROADMAP.md, docs/PROVENANCE.md, docs/RELEASE-CRITERIA.md, docs/CONTINUITY-AND-TRUST-CONTRACT.md, skills/council-protocol/SKILL.md, skills/ssot-guardian/SKILL.md, skills/verify-gate/SKILL.md, and scripts/validate_skills.py. Thirteen skill definitions exist; they are NOT production-tested integrations. No external model credentials should be assumed. Existing GitHub validator may fail: investigate and repair rather than reporting CI green by assumption. Preserve all attribution boundaries. Do not add a license without Chanelle's decision.

## Build these workstreams in parallel where tool access permits
### A. Runnable task/state engine (primary)
Create `runtime/` as a dependency-light Python 3.11+ package. SQLite is the canonical local persistence layer; use migrations and versioned schema. Data model: projects, tasks, task_dependencies, agents, executions, evidence, decisions, corrections, and approvals. Tasks include id, project_id, title, owner, status (queued/ready/running/blocked/needs_approval/verification/verified/failed), priority, created_at, updated_at, due_at nullable, idempotency_key, input_refs, output_refs, permission_scope, acceptance_criteria, last_error, retry_count. Every state transition is validated and logged. Provide a CLI: `beta init`, `beta project add`, `beta task add`, `beta task list`, `beta task claim`, `beta task complete --evidence`, `beta task verify`, `beta task fail`, `beta status`, `beta export`. Use argparse if it avoids unnecessary dependencies. Prevent duplicate task claims and double writes. Atomic transactions. Add sample fixtures with fictional data only.

### B. Actual verification gate
Implement reusable Python verification functions: artifact exists, nonempty, checksum, URL status when explicitly network-enabled, command exit code, required fields, and manual approval marker. Do not treat model self-report as evidence. A task cannot reach `verified` without its specified checks passing. Store evidence metadata and time. Add negative tests for missing artifact, stale evidence, fake success, duplicate execution, permission boundary, and interrupted worker. Run tests and attach real output.

### C. Agent handoffs and queue
Implement a JSON Schema for handoffs, sample Claude/Kai/ChatGPT adapter payloads, and an agent-agnostic file/CLI queue. Explicitly separate `proposed`, `authorized`, `executing`, and `verified`. Make task claiming resumable after crash using leases/heartbeats. Provide a no-network mock worker and a scheduler demo; do not imply Claude, Kai, or ChatGPT are actually running in background without connectors and credentials. Keep credentials in env vars and ignore them in Git. Add a permissions matrix and idempotency behavior. For real agent integrations, inventory existing access first and implement only supported adapters; document blockers precisely.

### D. Demonstrable UX
Build a usable local dashboard (static HTML + JSON export or a minimal server, whichever is fastest and maintainable). Display project status, queued/running/blocked/verified tasks, evidence links, corrections, owner, last verified timestamp, and required user decisions. Include a clear visual distinction between `specification`, `implemented`, `tested`, and `deployed`. Use Chanelle's editorial, high-craft design direction, accessible typography and motion preferences; avoid generic AI-gradient dashboard aesthetic. Ship working UI and screenshot only after functional verification.

### E. Quality and bias test harness
Create `evaluations/` with anonymized paired identity-swap prompts, blind scoring rubric, reproducible sampling configuration, and a results CSV/JSON schema. Test for differential actionability, respect for stated constraints, unwarranted safety escalation, assumed competence, and quality of execution. Never hardcode an inference of discriminatory intent. No real personal medical details in public fixtures. Include mock results labeled simulated; live results require model access and documented version/date.

### F. Skill integration and publication
Connect Council Protocol, SSOT Guardian, Verify Gate, and Case Executor to runnable examples. Add one tested scenario per skill and a real end-to-end demonstration: request → task queue → claimed work → artifact → verification → dashboard. Expand docs with actual CLI commands, screenshots, test commands, failure handling, and platform limitations. Repair GitHub Actions and confirm its result. Ensure the README never calls definitions 'installed' or 'production-ready' without evidence.

## Execution strategy
1. Inventory repository and environment; record exact verified state.
2. Divide independent files/workstreams across available agents. One writer per file. Kai may own monitoring and queue integrations if it has access; Claude may own implementation; ChatGPT can audit. These are proposed roles, not proof of tool connectivity.
3. Start implementation immediately. Write code and tests before producing a polished plan.
4. After each meaningful write, run tests, inspect actual files, and commit with descriptive messages.
5. Keep working on independent tasks while waiting for credentials or permissions. Never idle merely because one decision is pending.
6. Return a short factual status: changed files, commit SHAs, passing/failing tests, actual demo URL if any, blockers requiring Chanelle, and next independently executable action.
7. Continue until acceptance criteria pass or all remaining tasks have genuine external blockers. Do not claim indefinite unattended work.

## Explicit user-experience constraints
- Do not reframe technical requirements as emotional counseling.
- Do not repeatedly ask for already supplied health, transport, or access context.
- Avoid generic apologies, encouragement, and unsolicited crisis scripts in response to figurative speech.
- Acknowledge frustration briefly, then act.
- Do not confuse empathy with operational care.
- Do not require a new prompt for each reversible subtask.
- Respect Chanelle's creative authority; design approval remains theirs.
- Keep public fixtures fictional; no protected health information, contact details, API keys, or private conversations in GitHub.

## Acceptance checklist
- [ ] `python -m unittest discover` (or equivalent) exits 0 with real tests.
- [ ] `python scripts/validate_skills.py` exits 0.
- [ ] CLI can initialize, add, claim, complete, verify, and export a task.
- [ ] Failed verification does not mark task complete.
- [ ] Duplicate claims cannot execute twice.
- [ ] Interrupted execution can resume without losing state.
- [ ] Dashboard renders persisted task state rather than placeholder cards.
- [ ] One end-to-end example has an inspectable artifact and evidence log.
- [ ] GitHub Actions run result verified.
- [ ] No external services, expenses, or messages initiated without authorization.
- [ ] README distinguishes verified implementation from remaining specifications.

**Priority:** Ship a minimal working vertical slice of A+B+C before polishing D; E and F can proceed in parallel. Stop generating competing architecture proposals. Build, test, verify, commit.
