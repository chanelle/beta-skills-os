---
name: chanelle-voice
description: Preserve Chanelle Henry’s editorial voice and brand intent.
---

# Chanelle Voice

**Version:** 0.2.0 · **Maturity:** Specification, not yet platform-tested. **Provenance:** Chanelle-originated workflow specification.

## Trigger
Use when explicitly requested or necessary to complete a previously authorized task. Do not infer permission to publish, send, or modify accounts from casual mentions.

## Inputs
Consented user-authored samples, audience, medium, message, tone constraints.

## Procedure
1. Extract distinctive syntax, rhythm, metaphors and argument structure from actual samples.
2. Create a concise style rubric.
3. Draft without invented personal experiences.
4. Compare against the original meaning.
5. Flag clichés and unrequested AI rhetoric.
6. Present substantive alterations for approval.
7. Do not train or publish private samples without consent..

## Output contract
Return the deliverable, source/evidence references, version, actual completion status, unresolved blockers, and only the decision genuinely required from the user. Never report a proposed action as performed.

## Acceptance scenario
**Given:** A draft adds invented credentials or an unearned testimonial: remove the claim and flag it.

**Then:** The workflow preserves the facts and produces a checkable result, with any missing evidence labeled explicitly.

## Failure and privacy handling
On tool failure or timeout, inspect destination state before retrying. Keep private data and credentials out of public examples. Preserve source attribution and do not redistribute third-party copyrighted skill content. External actions require the authorization appropriate to their consequences.

## Evaluation
A reviewer should be able to reproduce the steps, inspect the evidence, and distinguish completed work from a draft. Passing this specification review does not constitute a live integration test.
