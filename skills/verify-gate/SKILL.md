---
name: verify-gate
description: Require inspectable evidence before consequential claims or external actions.
---

# Verify Gate

> Status: Starter draft; not validated in production. Version 0.1.0.

## Purpose
Require inspectable evidence before consequential claims or external actions.

## Trigger
Use when the user explicitly requests this workflow or when it directly reduces work on an authorized task.

## Inputs
Claims, citations, source artifacts, and proposed action.

## Procedure
Classify each claim as verified, inferred, disputed, or unknown; cross-check sources; block unsupported assertions; document uncertainty.

## Output contract
Provide a concise result, evidence or provenance, unresolved questions, and exactly one next action when needed. Distinguish completed work from suggestions.

## Guardrails
- Do not invent sources, integrations, approvals, outcomes, or prior execution.
- Do not publish, send, purchase, modify permissions, or contact third parties without appropriate authorization.
- Keep private data and credentials out of public examples.
- When uncertain, label uncertainty and preserve original source material.

## Evaluation
- Output is grounded in supplied inputs.
- A reviewer can inspect the provenance and reproduce the workflow.
- The result reduces user effort without suppressing user agency.
