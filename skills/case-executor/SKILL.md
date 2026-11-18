---
name: case-executor
description: Move an authorized real-world case from remembered context through evidence gathering, preparation, handoffs, and verified resolution.
---

# Case Executor

**Version:** 0.1.0 · **Maturity:** Specification; platform integration and test runs pending.

## Purpose
Move an authorized real-world case from remembered context through evidence gathering, preparation, handoffs, and verified resolution.

## Trigger
Invoke when the user requests the workflow or a previously authorized task requires it. Casual mentions do not authorize external actions.

## Inputs
Case ID; desired outcome; current verified state; source records; constraints; deadlines; authorization scope; responsible parties.

## Procedure
1. Recover the existing case and its last verified event before asking questions.
2. Separate verified facts, user reports, and open hypotheses; create a dated chronology.
3. Define the exact outcome and externally observable completion criteria.
4. Enumerate required actions and dependencies; execute all reversible, authorized steps available through connected tools.
5. Prepare correspondence, forms, attachments and evidence packets without inventing identifiers.
6. For any external communication, consequential submission, or irreversible step, check authorization and obtain approval where required.
7. Verify each resulting action in the destination system; capture receipts, timestamps, or confirmations.
8. On failure or timeout, reconcile actual state before retrying; avoid duplicate submissions.
9. Persist updated case state and schedule follow-up only when an authorized scheduling mechanism exists.
10. Return one concise decision or approval request only when necessary. Otherwise return the verified outcome.

## Output contract
`case_id`, `goal`, `status`, `last_verified_event`, `completed_actions`, `evidence_refs`, `blocked_reason`, `next_actor`, `approval_needed`, `next_check`.

## Acceptance scenarios
- A user mentions an existing case in passing: recover context without assuming authorization to contact anyone.
- A police agency previously requested a letter: prepare a draft and supporting checklist; do not claim submission.
- A submission times out: check for confirmation before retrying.
- A case has a verified closure notice: mark resolved with evidence, not merely because an email was sent.

## Guardrails
Never invent facts, approvals, tool access, legal conclusions, or outcomes. Keep sensitive case data out of public repositories. Distinguish completed work, prepared work, and planned work. Do not assert that a background process exists without a configured runtime.
