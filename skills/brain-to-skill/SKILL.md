---
name: brain-to-skill
description: Convert repeated problem-solving patterns into reusable, reviewable skills.
---

# Brain To Skill

**Version:** 0.2.0 · **Maturity:** Specification, not yet platform-tested. **Provenance:** Chanelle-originated workflow specification.

## Trigger
Use when explicitly requested or necessary to complete a previously authorized task. Do not infer permission to publish, send, or modify accounts from casual mentions.

## Inputs
Repeated task examples, failures, user constraints, desired output, target agent.

## Procedure
1. Cluster recurring requests by trigger and outcome.
2. Extract the successful path.
3. Separate user-owned judgment from automatable steps.
4. Define input/output schemas.
5. Add authorization boundaries.
6. Create three adversarial tests.
7. Compare against existing skills to avoid duplicates.
8. Publish only with provenance..

## Output contract
Return the deliverable, source/evidence references, version, actual completion status, unresolved blockers, and only the decision genuinely required from the user. Never report a proposed action as performed.

## Acceptance scenario
**Given:** A conversation contains three variations of the same complaint: extract one generalizable workflow, not three duplicates.

**Then:** The workflow preserves the facts and produces a checkable result, with any missing evidence labeled explicitly.

## Failure and privacy handling
On tool failure or timeout, inspect destination state before retrying. Keep private data and credentials out of public examples. Preserve source attribution and do not redistribute third-party copyrighted skill content. External actions require the authorization appropriate to their consequences.

## Evaluation
A reviewer should be able to reproduce the steps, inspect the evidence, and distinguish completed work from a draft. Passing this specification review does not constitute a live integration test.
