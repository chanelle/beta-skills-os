---
name: deep-research
description: Run structured, skeptical research with traceable sources.
---

# Deep Research

**Version:** 0.2.0 · **Maturity:** Specification, not yet platform-tested. **Provenance:** Adaptation candidate; provenance review required.

## Trigger
Use when explicitly requested or necessary to complete a previously authorized task. Do not infer permission to publish, send, or modify accounts from casual mentions.

## Inputs
Research question, decision, timeframe, sources, evidence threshold.

## Procedure
1. Translate the question into falsifiable subquestions.
2. Search primary and recent sources.
3. Log publication dates and jurisdiction.
4. Cross-check consequential claims independently.
5. Seek disconfirming evidence.
6. Separate fact from inference.
7. Identify unanswered questions.
8. Deliver a sourced decision with confidence and limitations..

## Output contract
Return the deliverable, source/evidence references, version, actual completion status, unresolved blockers, and only the decision genuinely required from the user. Never report a proposed action as performed.

## Acceptance scenario
**Given:** Two news articles repeat one press release: count as one underlying source, not independent corroboration.

**Then:** The workflow preserves the facts and produces a checkable result, with any missing evidence labeled explicitly.

## Failure and privacy handling
On tool failure or timeout, inspect destination state before retrying. Keep private data and credentials out of public examples. Preserve source attribution and do not redistribute third-party copyrighted skill content. External actions require the authorization appropriate to their consequences.

## Evaluation
A reviewer should be able to reproduce the steps, inspect the evidence, and distinguish completed work from a draft. Passing this specification review does not constitute a live integration test.
