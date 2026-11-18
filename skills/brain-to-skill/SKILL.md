---
name: brain-to-skill
description: Convert repeated problem-solving patterns into reusable, reviewable skills.
---

# Brain To Skill

> Status: Starter draft; not validated in production. Version 0.1.0.

## Purpose
Convert repeated problem-solving patterns into reusable, reviewable skills.

## Trigger
Use when the user explicitly requests this workflow or when it directly reduces work on an authorized task.

## Inputs
A repeated task, prior attempts, constraints, and successful outputs.

## Procedure
Extract a repeatable procedure; identify inputs, permissions, failure modes, and evaluation criteria; draft a skill; test with a real case.

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
