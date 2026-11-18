---
name: usage-observatory
description: Track AI tool usage, limits, handoffs, and cost without fabricating telemetry.
---

# Usage Observatory

**Version:** 0.2.0 · **Maturity:** Specification, not yet platform-tested. **Provenance:** Chanelle-originated workflow specification.

## Trigger
Use when explicitly requested or necessary to complete a previously authorized task. Do not infer permission to publish, send, or modify accounts from casual mentions.

## Inputs
Dated provider usage exports, limits, billing periods, task logs.

## Procedure
1. Normalize provider units and timestamps.
2. Identify missing coverage.
3. Calculate observed usage separately from estimates.
4. Associate spend with completed work and outcomes.
5. Detect throttling and duplicated effort.
6. Recommend cheaper handoffs only with known tool access.
7. Preserve uncertainty and update after each verified event..

## Output contract
Return the deliverable, source/evidence references, version, actual completion status, unresolved blockers, and only the decision genuinely required from the user. Never report a proposed action as performed.

## Acceptance scenario
**Given:** A provider supplies message counts but not tokens: do not fabricate token totals.

**Then:** The workflow preserves the facts and produces a checkable result, with any missing evidence labeled explicitly.

## Failure and privacy handling
On tool failure or timeout, inspect destination state before retrying. Keep private data and credentials out of public examples. Preserve source attribution and do not redistribute third-party copyrighted skill content. External actions require the authorization appropriate to their consequences.

## Evaluation
A reviewer should be able to reproduce the steps, inspect the evidence, and distinguish completed work from a draft. Passing this specification review does not constitute a live integration test.
