---
name: publish-pipeline
description: Move approved ideas through drafting, editorial QA, and channel-specific publishing.
---

# Publish Pipeline

**Version:** 0.2.0 · **Maturity:** Specification, not yet platform-tested. **Provenance:** Chanelle-originated workflow specification.

## Trigger
Use when explicitly requested or necessary to complete a previously authorized task. Do not infer permission to publish, send, or modify accounts from casual mentions.

## Inputs
Approved thesis, evidence, channels, voice rubric, links, rights.

## Procedure
1. Recover existing draft and version.
2. Verify factual claims.
3. Produce channel-specific variants.
4. Inspect link and media rights.
5. Run voice and accessibility checks.
6. Stage publication with metadata.
7. Request approval for public posting.
8. Verify the live URL and capture outcome metrics when available..

## Output contract
Return the deliverable, source/evidence references, version, actual completion status, unresolved blockers, and only the decision genuinely required from the user. Never report a proposed action as performed.

## Acceptance scenario
**Given:** An agent creates a LinkedIn draft but does not post: mark staged, not published.

**Then:** The workflow preserves the facts and produces a checkable result, with any missing evidence labeled explicitly.

## Failure and privacy handling
On tool failure or timeout, inspect destination state before retrying. Keep private data and credentials out of public examples. Preserve source attribution and do not redistribute third-party copyrighted skill content. External actions require the authorization appropriate to their consequences.

## Evaluation
A reviewer should be able to reproduce the steps, inspect the evidence, and distinguish completed work from a draft. Passing this specification review does not constitute a live integration test.
