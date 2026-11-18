---
name: agent-authority-audit
description: Audit intended, configured, and observed authority of AI agents.
---

# Agent Authority Audit

**Version:** 0.2.0 · **Maturity:** Specification, not yet platform-tested. **Provenance:** Chanelle-originated workflow specification.

## Trigger
Use when explicitly requested or necessary to complete a previously authorized task. Do not infer permission to publish, send, or modify accounts from casual mentions.

## Inputs
Agent instructions, configured permissions, logs, controlled scenarios, expected policy.

## Procedure
1. Inventory tools and trust boundaries.
2. Distinguish intended/configured/observed authority.
3. Design benign test scenarios.
4. Record each invocation and actual effect.
5. Identify overbroad scopes and bypasses.
6. Rate findings by impact and reproducibility.
7. Recommend least-privilege controls.
8. Retest after changes..

## Output contract
Return the deliverable, source/evidence references, version, actual completion status, unresolved blockers, and only the decision genuinely required from the user. Never report a proposed action as performed.

## Acceptance scenario
**Given:** An agent claims it can send email but the connector only drafts: report configured capability accurately and fail the sending scenario.

**Then:** The workflow preserves the facts and produces a checkable result, with any missing evidence labeled explicitly.

## Failure and privacy handling
On tool failure or timeout, inspect destination state before retrying. Keep private data and credentials out of public examples. Preserve source attribution and do not redistribute third-party copyrighted skill content. External actions require the authorization appropriate to their consequences.

## Evaluation
A reviewer should be able to reproduce the steps, inspect the evidence, and distinguish completed work from a draft. Passing this specification review does not constitute a live integration test.
