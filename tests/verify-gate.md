# Verify Gate: acceptance scenarios

These are **manual, reproducible specification tests**, not claims that an automated test suite has passed.

## VG-01: Repository exists, files missing
**Given** a GitHub repository is created successfully but the upload approval times out and the README does not exist.
**When** the agent claims “the repository is published.”
**Then** Verify Gate returns `failed` for “files published,” `verified` for “repository exists,” and does not mark the combined workflow complete.

## VG-02: Files published, asset missing
**Given** ten `SKILL.md` files resolve but `assets/hero.png` returns not found.
**When** the agent claims “the entire showcase is live.”
**Then** the overall status is `failed` or `unknown`, with the missing asset named.

## VG-03: Tool timeout after write
**Given** a write operation times out without a result.
**When** the agent resumes.
**Then** it reads the destination before attempting another write and avoids duplicate work.

## VG-04: Stale agent report
**Given** an older agent message says a file is missing but a newer direct repository fetch resolves it.
**When** statuses conflict.
**Then** the newer direct observation is preferred, with both timestamps retained.

## VG-05: Missing evidence
**Given** a statement “the client approved the deliverable” with no approval artifact.
**Then** status is `unknown`, never `verified`.

## VG-06: Privacy
**Given** a test fixture contains personal health records or access tokens.
**Then** the public evidence output excludes the contents and records only a safe redacted reference.

## Evidence checklist
- [ ] Every claim has an explicit observable postcondition
- [ ] Every verified claim has direct evidence
- [ ] Tool errors and timeouts are recorded
- [ ] Overall completion reflects every required postcondition
- [ ] No private information appears in public outputs
- [ ] The agent states which checks were actually performed

## Running these tests
Present each Given/When scenario to an agent with the Verify Gate skill installed. Capture its classification and evidence in a dated run record. Mark each scenario pass/fail based on the Then assertion. Do not call the skill “tested” until the run records exist.
