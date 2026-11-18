---
name: ux-copy
description: Adapt UX writing review principles with clear third-party attribution.
---

# Ux Copy

**Version:** 0.2.0 · **Maturity:** Specification, not yet platform-tested. **Provenance:** Adaptation candidate; provenance review required.

## Trigger
Use when explicitly requested or necessary to complete a previously authorized task. Do not infer permission to publish, send, or modify accounts from casual mentions.

## Inputs
Interface screenshots, user goal, content, locale, accessibility requirements, source attribution.

## Procedure
1. Inventory user-facing strings and states.
2. Test clarity and information scent.
3. Evaluate error recovery and accessible labels.
4. Propose concise variants preserving meaning.
5. Flag coercive or guilt-inducing wording.
6. Verify against actual interface constraints.
7. Document any borrowed framework and licensing..

## Output contract
Return the deliverable, source/evidence references, version, actual completion status, unresolved blockers, and only the decision genuinely required from the user. Never report a proposed action as performed.

## Acceptance scenario
**Given:** An error message blames the user but offers no recovery: replace with actionable, nonjudgmental guidance.

**Then:** The workflow preserves the facts and produces a checkable result, with any missing evidence labeled explicitly.

## Failure and privacy handling
On tool failure or timeout, inspect destination state before retrying. Keep private data and credentials out of public examples. Preserve source attribution and do not redistribute third-party copyrighted skill content. External actions require the authorization appropriate to their consequences.

## Evaluation
A reviewer should be able to reproduce the steps, inspect the evidence, and distinguish completed work from a draft. Passing this specification review does not constitute a live integration test.
