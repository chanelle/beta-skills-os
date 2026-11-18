---
name: council-protocol
description: Coordinate ChatGPT, Claude, Kai, and other authorized agents through shared state, delegated tasks, approval boundaries, and evidence-based handoffs.
---

# Council Protocol

**Version:** 0.1.0 · **Maturity:** Specification; platform integration and test runs pending.

## Purpose
Coordinate ChatGPT, Claude, Kai, and other authorized agents through shared state, delegated tasks, approval boundaries, and evidence-based handoffs.

## Trigger
Invoke when the user requests the workflow or a previously authorized task requires it. Casual mentions do not authorize external actions.

## Inputs
User objective; canonical case record; available agent capabilities; permissions; constraints; required deliverables; latest verified status.

## Procedure
1. Recover the canonical project record and current versions before delegating.
2. Break the objective into independently verifiable deliverables with dependencies.
3. Assign work by actual tool access and competency, not assumed agent capabilities.
4. Parallelize independent, reversible tasks; serialize dependent writes to the same artifact.
5. Use a shared handoff contract and record which agent owns each action.
6. Prevent duplicate execution with task IDs, idempotency keys where available, and destination-state checks.
7. Require Verify Gate evidence for all completion claims.
8. When one agent is blocked, reroute supported work rather than waiting unnecessarily.
9. Request human input only for genuine judgment, missing consent, or an unavailable capability.
10. Reconcile versions and return a single coherent progress report.

## Handoff contract
`task_id`, `project_id`, `goal`, `assigned_agent`, `input_refs`, `permissions`, `dependencies`, `deliverable`, `status`, `evidence_refs`, `next_actor`, `last_verified_at`.

## Acceptance scenarios
- Claude writes a document while Kai checks source links: independent work runs concurrently.
- Two agents try to edit the same file: one write owner; second agent reviews a diff.
- Kai reports “published” but destination is empty: Verify Gate blocks completion.
- A user mentions a case in casual conversation: retrieve context, do not initiate unauthorized contact.

## Guardrails
Never invent facts, approvals, tool access, legal conclusions, or outcomes. Keep sensitive case data out of public repositories. Distinguish completed work, prepared work, and planned work. Do not assert that a background process exists without a configured runtime.

## Output contract
Return the objective, actions actually performed, artifact or evidence references, verification result, unresolved blockers, and next authorized action. Label unverified outcomes explicitly; never report a specification as an executed integration.
