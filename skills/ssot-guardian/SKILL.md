---
name: ssot-guardian
description: Reconcile project state and contradictions across agents and conversations.
---

# Ssot Guardian

> Status: Starter draft; not validated in production. Version 0.1.0.

## Purpose
Reconcile project state and contradictions across agents and conversations.

## Trigger
Use when the user explicitly requests this workflow or when it directly reduces work on an authorized task.

## Inputs
Current project state, dated sources, previous decisions, and updates.

## Procedure
Prioritize latest verified evidence; list conflicts with timestamps; propose canonical state; never silently overwrite or invent progress.

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
