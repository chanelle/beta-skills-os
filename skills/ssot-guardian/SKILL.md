---
name: ssot-guardian
description: Reconcile project state and contradictions across agents and conversations.
---

# Ssot Guardian

**Version:** 0.2.0 · **Maturity:** Specification, not yet platform-tested. **Provenance:** Chanelle-originated workflow specification.

## Trigger
Use when explicitly requested or necessary to complete a previously authorized task. Do not infer permission to publish, send, or modify accounts from casual mentions.

## Inputs
Project identifier, dated records, source reliability, current artifact versions.

## Procedure
1. Inventory all competing records.
2. Normalize timestamps.
3. Rank direct recent evidence over old summaries.
4. Detect contradictions.
5. Preserve disputed facts.
6. Propose a canonical state with source pointers.
7. Write only to authorized source of truth.
8. Propagate version and handoff updates.
9. Re-read after writing..

## Output contract
Return the deliverable, source/evidence references, version, actual completion status, unresolved blockers, and only the decision genuinely required from the user. Never report a proposed action as performed.

## Acceptance scenario
**Given:** An older chat says a repo is empty but a current GitHub fetch shows files: prefer the fetch and retain historical context.

**Then:** The workflow preserves the facts and produces a checkable result, with any missing evidence labeled explicitly.

## Failure and privacy handling
On tool failure or timeout, inspect destination state before retrying. Keep private data and credentials out of public examples. Preserve source attribution and do not redistribute third-party copyrighted skill content. External actions require the authorization appropriate to their consequences.

## Evaluation
A reviewer should be able to reproduce the steps, inspect the evidence, and distinguish completed work from a draft. Passing this specification review does not constitute a live integration test.
