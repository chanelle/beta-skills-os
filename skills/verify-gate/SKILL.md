---
name: verify-gate
description: Verify claims of completed agent work against inspectable evidence before reporting success or taking consequential follow-up action.
---

# Verify Gate

**Version:** 0.2.0 · **Maturity:** Specification with reproducible acceptance scenarios; integration not yet certified.

## When to invoke
Before reporting that an external action succeeded, a document was published, a payment was made, a task was completed, or an agent handoff finished. Also invoke when a source contradicts an earlier status.

## Required inputs
- **Claim:** precise statement being evaluated, with actor and timestamp.
- **Expected result:** observable postcondition that would make the claim true.
- **Evidence:** tool results, URLs, commit IDs, receipts, artifacts, or other inspectable sources.
- **Scope:** environment, repository, account, date, and permissions.
- **Evidence freshness:** when each observation was made.

If any required input is absent, mark it `unknown`, not `verified`.

## Workflow
1. **Decompose:** Split compound statements into independently testable claims. “Repository created and published” requires separate checks.
2. **Specify postconditions:** Define what must exist in the target system. Example: GitHub repository exists; expected file paths resolve on `main`; assets load.
3. **Gather primary evidence:** Prefer target-system reads over agent self-report. Record exact path, identifier, timestamp, and what was observed. Never invent a check.
4. **Reconcile:** Compare evidence against each postcondition. Detect stale reads, partial successes, conflicting results, and untested claims.
5. **Classify:** Use exactly one of `verified`, `inferred`, `disputed`, `unknown`, or `failed` per claim.
6. **Gate:** Do not label the overall workflow complete while a required postcondition is `unknown`, `disputed`, or `failed`. Do not take irreversible actions without appropriate authorization.
7. **Report:** State the outcome, supporting evidence, unresolved gaps, and the smallest next action only if one remains.
8. **Persist:** Update the case ledger or handoff with evidence references and last-verified time, if an authorized writable system exists.

## Classification rules
| Status | Meaning |
|---|---|
| verified | Direct evidence demonstrates the exact postcondition |
| inferred | Evidence supports a conclusion but does not demonstrate it directly |
| disputed | Credible evidence conflicts and cannot yet be reconciled |
| unknown | Necessary evidence is missing or inaccessible |
| failed | Direct evidence demonstrates the required postcondition is false |

**Never promote inferred or unknown to verified solely because another agent reported success.**

## Output schema
```json
{
  "claim": "README and ten skills published to main",
  "status": "verified",
  "checked_at": "ISO-8601 timestamp of actual check",
  "postconditions": [
    {"requirement": "README.md resolves", "status": "verified", "evidence": "GitHub file fetch"},
    {"requirement": "10 SKILL.md paths resolve", "status": "verified", "evidence": "10 individual file fetches"}
  ],
  "limitations": [],
  "next_action": null
}
```
The JSON above is a **format example**, not a report of a performed check. Replace example values with real evidence.

## Failure handling
- **Timeout:** Re-read the target state before retrying. Do not assume either success or failure.
- **Partial success:** Preserve completed steps and resume only missing steps.
- **Stale source:** Recheck and annotate timestamps.
- **Conflicting reports:** Preserve both, then prioritize a newer direct observation.
- **Unavailable integration:** State exactly which postcondition could not be inspected.
- **Sensitive evidence:** Store only redacted references in public outputs.

## Evaluation
Pass only if the operator can (a) identify the claim, (b) inspect evidence, (c) reproduce the classification, and (d) detect a partial completion. Run the scenarios in `tests/verify-gate.md`.

## Boundaries
This skill is an instruction contract, not a background daemon or an assurance of cross-platform execution. The host agent must have appropriate tools and permissions.
