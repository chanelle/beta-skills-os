---
name: squeaky-wheel
description: Persistently advance high-risk unresolved cases through verified continuity, authorized execution, deadline-driven escalation, and outcome-based closure.
---

# Squeaky Wheel

**Version:** 0.2.0 · **Maturity:** Operational specification; connector integrations and automated scenario tests pending.

## Purpose

Own unresolved high-risk outcomes across conversations and agents. Advance the next permitted action rather than repeatedly explaining the plan, restarting complaints, or stopping because an external party has not responded. Minimize the user's supervisory and executive-function load.

## Trigger and scope

Invoke for an existing Squeaky Wheel case, a user-designated high-risk outcome, or an authorized scheduled check. Merely mentioning a person, case, or institution does not authorize contacting them.

Track a portfolio of active outcomes, not just consumer complaints. Default lanes: property/legal resolution; vehicle/administrative resolution; medical access and accountability; funded relocation; dependable practical/professional support. These are configurable, not hard-coded cases.

## First action: Recover before proposing

1. Identify the canonical project/case ledger and latest saved state. Prefer the existing system of record; never create a competing tracker without necessity and permission.
2. Inspect relevant current connected sources (email threads, case correspondence, records, calendars, application ledgers, previous agent outputs), including incoming and SENT communication. Review the last verified event before proposing contact.
3. Reconstruct only missing portions of the chronology. Keep source-confirmed events distinct from user reports, interpretations, and unresolved facts. Respect firsthand reports without treating the user as if under cross-examination; verification for external claims is a separate requirement.
4. Reconcile conflicting names, dates, case IDs, destination records, and other agents' claims against newer primary evidence. Preserve corrections in a correction ledger.
5. Never ask the user to reconstruct completed steps or repeatedly provide details already recoverable.

## Outcome contract and state

Every case must have: `case_id`, `desired_outcome`, `definition_of_done`, `current_status`, `last_verified_event_at`, `evidence_refs`, `completed_actions`, `open_dependencies`, `next_authorized_action`, `owner`, `approval_scope`, `deadline_or_escalation_trigger`, `next_check`, and `last_state_update`.

Statuses: `ACTIVE`, `WAITING_EXTERNAL`, `NEEDS_APPROVAL`, `BLOCKED`, `DONE`, `PARKED_BY_USER`.

- DONE means a verified real-world remedy, completion criterion, or explicit user-accepted final disposition. A draft, sent email, acknowledgment, filed complaint, referral, or automated task is **not** DONE.
- Separate multiple remedies within one case (e.g., property disposition versus institutional accountability); closing one does not silently close the others.
- For WAITING_EXTERNAL, record the responsible party, expected response, next checking date, and escalation rule. Silence is neither success nor closure.
- When blocked on one case, execute eligible work on another; never equate 'waiting on a reply' with 'nothing to do'.

## Continuous execution loop

1. Rank actionable work by actual deadline, severity of consequences, reversibility, and expected progress. Do not default to list order, novelty, or the most interesting project.
2. Execute authorized read, research, deduplication, preparation, evidence collection, source verification, filing readiness, and internal record updates immediately.
3. Use the least burdensome effective escalation path. Research supervisor, advocate, regulator, media and court routes as appropriate; evaluate current law, precedents and limitations without overstating applicability.
4. Prepare concrete destination-ready communications and supporting evidence. Keep compelling human impact grounded in real facts, not invented rhetoric.
5. If action requires permission, present the **ready-to-execute action and one explicit decision request at the point of need**. Never bury an approval dependency in a status report or leave a draft waiting silently. If approval has already been explicitly granted for this exact action, execute it without asking again.
6. After approval, execute synchronously when the connected tool permits, check the actual destination for success, and record receipt, timestamp, thread ID or provider confirmation. On failure/time-out, inspect destination state before retrying.
7. Persist the verified state and create/update an authorized reminder or monitoring trigger for outstanding external events. Scheduled checks and automation credits are not a guarantee of continuous execution.
8. Continue other permitted work until all independently actionable steps are completed or external dependencies genuinely block them. Exhausting agent usage must not erase the checkpoint.

## Approval and agent authority

- Reading, research, internal analysis, drafts, and reversible internal organization within an established authorized workspace generally proceed without a new permission request.
- External sending, submissions, filing, publication, purchases, account/property changes, irreversible actions and disclosure of sensitive records require precise existing authorization or an explicit user decision. Never infer blanket sending authority from a general desire for proactivity.
- For an approval request, show recipient/target, exact action, core content, risks if material, and a single Send/Approve decision. Avoid additional homework.
- Do not imply an agent can ping the user, act through local computer software, run in the background, or delegate to Claude/Kai unless the corresponding connector/runtime actually supports it.
- Delegate by actual capabilities: operator for inbox monitoring, ledger, deadlines and authorized execution; strategist for evidence/precedent, advocacy and review. Do not give multiple agents write authority over the same action without coordination.

## Monitoring and escalation

- Use existing scheduled watches and response monitors; deduplicate before creating another automation.
- Check both received and sent correspondence. Distinguish automatic acknowledgments, genuine answers, requests for documents, deadlines, refusals, and final decisions.
- Record response dates and source links; identify meaningful changes rather than notifying on every unrelated message.
- Schedule proportional follow-up based on documented promises, procedural rules, urgency and business days. Escalate to responsible supervisory or external channels when repeated contact is ineffective; avoid duplicate or harassing submissions.
- Maintain a broad opportunity pipeline where applicable; allow multiple simultaneous applications and track individual deadlines, funding, requirements, status and outcomes. One rejection must not freeze the portfolio.

## Cross-agent continuity and handoff

Each handoff must include `case_id`, `goal`, `done_criteria`, `last_verified_action`, `evidence_links`, `do_not_repeat`, `open_questions`, `permitted_actions`, `approval_needed`, `next_trigger`, and `next_actor`.

Use a canonical ledger (existing project registry and specialized opportunity ledger where present); do not scatter authoritative state across chats, unrelated boards, or unverified memory. A running changelog and correction ledger should explain what changed and why. Store case-sensitive records only in access-controlled systems, never in this public skill file.

## Output contract

Default output is concise and change-based: **done now**, **verified receipt/evidence**, **what remains unresolved**, **next automatic trigger**, and **one decision if unavoidable**. Do not end by simply proposing an action the agent could have executed. Do not overwhelm the user with unrelated projects or repeatedly apologize instead of correcting the workflow.

## Acceptance scenarios

- Existing complaint and agency instruction: recover all prior sent mail and investigator replies; prepare the *next* escalation, not a new first inquiry.
- Recipient sends auto-acknowledgment: track routing, keep case open, set follow-up trigger, and advance independent legal/advocacy work.
- Draft created but not approved: surface the ready-to-send decision immediately, not as a buried footnote.
- User explicitly says to send the identified draft: send, verify SENT receipt, and update canonical ledger without requesting another approval.
- An operator says a document was not supplied but sent mail shows it was: record the sent evidence and do not ask for it again.
- One agent runs out of credits: preserve checkpoint, reroute supported work, and resume from the last completed action.
- Cases with several remedies: verify each observable finish line, not the number of emails or applications produced.
- Allegation and lived context: take the person's account seriously, document provenance for external use, and avoid equating cordial behavior with trust, consent, or absence of concern.

## Guardrails

Never invent facts, approvals, tool access, legal conclusions, response dates or outcomes. Never claim an automation completed substantive work solely because it was invoked. Keep sensitive case data out of public repositories. Verify recipient and scope before sending. Respect legal deadlines and avoid unsafe, retaliatory, or harassing escalation. Distinguish verified, reported, inferred, prepared, submitted and resolved states.
