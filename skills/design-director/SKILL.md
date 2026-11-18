---
name: design-director
description: Direct visual work through a coherent design system and measurable QA.
---

# Design Director

**Version:** 0.2.0 · **Maturity:** Specification, not yet platform-tested. **Provenance:** Chanelle-originated workflow specification.

## Trigger
Use when explicitly requested or necessary to complete a previously authorized task. Do not infer permission to publish, send, or modify accounts from casual mentions.

## Inputs
Design brief, device constraints, reference images, brand tokens, target audience.

## Procedure
1. Audit existing implementation before redesign.
2. Identify hierarchy, accessibility and viewing-distance problems.
3. Define visual tokens and layout constraints.
4. Generate variants only when comparison improves a decision.
5. Test realistic content, overscan, navigation and low-light readability.
6. Preserve working functionality.
7. Document changes and screenshots..

## Output contract
Return the deliverable, source/evidence references, version, actual completion status, unresolved blockers, and only the decision genuinely required from the user. Never report a proposed action as performed.

## Acceptance scenario
**Given:** A Samsung Tizen TV interface looks good on desktop but controls are unreadable from a couch: fail review until on-device readability is tested.

**Then:** The workflow preserves the facts and produces a checkable result, with any missing evidence labeled explicitly.

## Failure and privacy handling
On tool failure or timeout, inspect destination state before retrying. Keep private data and credentials out of public examples. Preserve source attribution and do not redistribute third-party copyrighted skill content. External actions require the authorization appropriate to their consequences.

## Evaluation
A reviewer should be able to reproduce the steps, inspect the evidence, and distinguish completed work from a draft. Passing this specification review does not constitute a live integration test.
