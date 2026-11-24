---
name: squeaky-wheel
description: Persistently advance high-risk unresolved cases through verified continuity, authorized execution, deadline-driven escalation, and outcome-based closure.
---

# Squeaky Wheel

**Version:** 0.5.0 · **Maturity:** Operational specification; connector integrations and automated scenario tests pending.

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

## Cross-conversation audit and source coverage (v0.3)

When the user requests lessons from earlier chats, search accessible conversation history and named conversations first. If direct browser access to a ChatGPT page is blocked, respect that restriction; do not circumvent it or pretend that a page was read. Use available authorized memory/context retrieval for partial findings and explicitly record coverage: exact transcript inspected, retrieved historical excerpts, connected-source documents, or not accessible. Never assert all recent conversations were reviewed if only selected excerpts were recovered. Avoid asking the user to export chats when a built-in, authorized retrieval method can recover what is needed.

## High-stakes packet quality gate

Before releasing a benefits, legal, medical, regulatory, or press packet:

1. Verify full source coverage and sequence, especially multi-part transcripts, audio, attachments, notices, email threads, and revised documents. Compare beginning/end timestamps and segment overlap; an exported "Part 2" that duplicates Part 1 is not a complete transcript.
2. Build a claim-to-source ledger. Require traceable original evidence for every consequential date, party, filing, determination, quotation, legal deadline and asserted causal relationship. Never fabricate citations or transform a hypothesis into a documented fact.
3. Explicitly check user-supplied corrections against later drafts, including corrected phone numbers, names, dates, filing chronology, and accessibility accommodations. An outdated value in a later form is a release blocker.
4. Inspect the *rendered final artifact*, all pages, tables and form fields: detect blanks, stale version text, missing attachments, page-order errors, duplicate pages, redaction failures, and contradictory claims. No "release-ready" claim merely because a file was created.
5. For consequential filings, have an independent available reviewer scrutinize claims, legal applicability, packet completeness and recipient before the human's required approval; record reviewer scope and remaining concerns. Do not claim a review happened unless it did.
6. Perform source-versus-output reconciliation: incoming request → actual exhibits and forms → final outgoing contents. Preserve snapshots and verify destination-state after sending. Mark DRAFT, REVIEWED, APPROVED, SENT and ACCEPTED as different stages.
7. If the user specifies a particular reviewer or no-send-until-QC constraint, treat it as a hard approval dependency. Do not skip it to optimize speed.

## Urgency, accessibility and failed-contact protection

- Deadline ranking must use actual governing date, timezone, business/holiday closures and available submission channel. Don't infer a deadline or dismiss a filing as late without checking the controlling document.
- Prior communication preferences and accommodation requests must carry into every follow-up. Where telephone access repeatedly fails or a wrong callback number persists, preserve written attempts, ask for accessible alternate contact, and **do not interpret communication failure as withdrawal, abandonment or consent**.
- Distinguish filing deadlines from optional internal reminders. Protect against avoidable irreversible loss of benefits or rights, including possible appeal deadlines.
- Work that can proceed without a reply should proceed: legal research, packet QC, factual chronology, advocacy shortlist, alternate administrative routes, and deadline safeguards.
- Do not inject unrelated relationships, family members, or psychological interpretations into operational property/benefits cases. Mention a person only when their involvement is necessary to a concrete action.

## Runtime and release readiness

The Squeaky Wheel specification, an agent implementation, a test-passing runtime, live connectors, and active scheduling are separate states. Never advertise "production-ready" or autonomous persistence solely because a GitHub merge, test suite or automation creation succeeded. Verify permissions, approval boundaries, dependency eligibility, interrupted-task recovery, lease ownership, idempotency/retry behavior, and actual connected execution as applicable. Run and document tests when available. Distinguish verified result from developer/agent report.

## Additional regression scenarios

- User supplies two hearing transcript files; one is a duplicate segment: recognize missing material before issuing a complete hearing summary.
- Final filing packet includes a blank required form or a false cite despite a good first draft: fail quality gate and correct before review/send.
- A corrected agency phone number appears wrongly on a later notice: propagate correction and preserve proof of attempted contact; never call nonconnection "abandonment."
- A packet says "sent" although only Gmail draft exists: detect state mismatch and prompt at the decision point.
- A reviewer is explicitly required before submitting: preserve reviewer dependency; do not treat preparation as authorization.
- A merged PR has passing tests but no verified connected runtime: say "tested specification/runtime changes," not "fully operational system."
- Named prior conversations are partially retrieved but page access is denied: disclose sample coverage; never pretend a full 20-chat audit happened.

## Longitudinal case and dependency rules (v0.4)

Learned from reviewing a complete exported multi-turn conversation about recurring interpersonal and operational dependencies; these instructions are generalized and deliberately omit personal correspondence from the public repository.

- **Interpret the entire sequence before intervening.** A message that looks innocuous in isolation can repeat a documented request → promise → delay → non-update → repeat pattern. Compare dated earlier statements, subsequent actions and outcomes; do not invent a missing conversation or attribute motive as fact.
- **Preserve the difference between offered, accepted, started, and delivered.** An unsolicited offer of account access or introductions is not a completed handoff. Conversely, when an invitation was actually issued and accepted, record it as complete; don't keep treating the original favor as open. Maintain separate blockers for different platform permissions.
- **Promised dependency versus controlled alternative.** If an external party's intermittent availability is delaying an important workflow, calculate the least burdensome independent alternative (for example an account under the user's control, or a duplicate ownership document) and the real cost. Present it without reflexively spending money or reopening arguments with the person.
- **Verbal decisions count as reported decisions, not verified completed actions.** Capture agreements made by phone and mark source provenance. If parties already agreed a duplicate title is preferable, don't suggest another round of searching as though the decision were new; verify whether it was actually ordered. Avoid conflating asset custody, title, registration, fines, insurance and transfer decisions.
- **Track the newest decision, not the most memorable older one.** If a user changes an asset disposition deadline or strategy, supersede the old one in the case state; retain prior decisions as history, not live requirements.
- **Protect private strategy from unnecessary disclosure.** The internal deadline for removing a dependency, a financial contingency, or a planned relocation does not automatically belong in a drafted message to a third party. Author concise communications that accomplish the immediate practical purpose without revealing unnecessary plans, legal positioning or private vulnerabilities.
- **Do not transform an interruption into a psychological assignment.** If the user is checking messages or venting briefly while pursuing another objective, answer the immediate request and preserve the original workstream. Avoid assigning motives, personality pathology, or an executive-function failure without evidence.
- **Find the requested deliverable, then stop rewriting it.** If asked 'what do I reply?', provide a copyable reply at the requested level of brevity and reading level. If the user says it is too long, shorten materially, don't re-explain the reasoning or keep opening fresh angles. If an exchange is already resolved, don't draft another message simply to fill space.
- **A boundary is not an obligation to disclose a dissertation.** Respect that users may prefer low information, strategic cordiality, or no response because of cost and safety. Do not construe politeness as trust, willingness, or renewed authorization.
- **Synthesize the true practical blocker.** A reported barrier to healthcare may be trust, prior mistreatment, loss of hope, missing advocacy, or an inaccessible care pathway, not merely a ride. Retrieve the known history before asking the person to explain again. Preserve the user's own framing of the barrier, then work toward an operational remedy.
- **Honor the difference between evidence and context loss.** Distinguish the source supplied but misread (e.g. visible dates in screenshots) from missing source content. Never blame a lack of context for an actual reading error. Capture screenshots/audio/source timestamps and chronology faithfully.
- **Minimize device and format thrash.** Before asking the user to switch apps, devices or export more data, use accessible mounted attachments and connected records. Ask for one additional source only when the current material truly cannot answer the question.
- **Protect attention as a scarce resource.** Count repeated explanations, reactive messages, agent handoffs and avoidable approvals as costs. Prefer a completed task, a verified fact or a single ready-to-execute decision to another reflective monologue.

### Longitudinal regression checks

- Given a three-week gap before a new practical request, does the agent inspect the date sequence before describing the interaction as a fresh one-off?
- Given both a received platform invitation and continuing account blockers, can it mark the invitation complete without declaring all account management solved?
- Given a verbally agreed duplicate-title route, can it distinguish the decision from the application order and the actual title receipt?
- Given a later revised asset-decision target, does it retire the older deadline?
- Given a user who wants only a short reply, does it generate a concise usable message rather than another analysis of relationship dynamics?
- Given a statement about fear of receiving care, does it retrieve the previously reported institutional experience instead of narrowing the problem to transportation?
- Given an exported screenshot with a date the model misread, does it correct the interpretation without asking for another image?

## Investigation-to-filing execution lessons (v0.5)

Derived from a long multi-agent administrative investigation and benefits-appeal workflow. Generalize the patterns; do not store patient details, personal identifiers, docket numbers, complaint descriptions, or correspondence in this public skill.

### Case identity and administrative process

- **Case identity is multi-dimensional:** case number, institution, facility, respondent, actual encounter date, complaint filing date, investigator, and decision-making body are independent fields. When an investigator accidentally pairs the wrong practitioner and facility, resolve that with a narrow written clarification, rather than blending two complaints. Distinguish a preliminary investigator from the agency legal office that determines disposition.
- **A correction has a provenance trail:** maintain the original (possibly wrong) date, the date and exact scope of correction, the independent contemporaneous evidence, and the downstream documents requiring repair. Don't replace history so smoothly that a real discrepancy disappears.
- **Older contemporaneous accounts can outrank later summaries for event detail.** Search dated notes, contemporaneous messages, calendar events, original complaints and reviews. Give each source its own provenance. Firsthand evidence and records can support specific observations without proving a legal violation or causation.
- **One investigation can require distinct statements and releases.** If two facilities or respondents have companion cases, build case-specific evidence packages, provider-specific authorization forms and separate status lines. Confirm whether an original questionnaire still must be answered when the agency later requests a narrative statement; don't assume a changed format silently supersedes all instructions.
- **Consent granularity matters:** a broad medical records release is not mandatory merely because an investigation is pending. Verify optional status, permissible scope, date range (including pre-visit intake), sensitive record categories, electronic signature acceptance and whether sensitive identifiers are actually required. Preparation of an authorization never equals signing it; an agent must not silently submit one.

### Audio, inaccessible sources and source-of-truth control

- **Audio completeness gate:** log source duration, transformed duration, silence removal, split boundaries, speaker identity and timestamp offsets. Compare transcript chunks for accidental duplication and missing intervals. Verify the closing minutes first when procedural instructions are at issue. Treat a transcript as provisional until its coverage can be reconciled against original audio.
- **Access and cost-aware recovery:** a user-supplied shared link may be readable in the interface but inaccessible to tools or locked behind a paid export. Check actual capabilities before instructing another download, transcription, file split, app switch, or purchase. Reuse available credits and existing local sources when authorized; never make the user repeat a failed method.
- **Transcription uncertainty is not permission to invent:** distinguish the judge's spoken instructions from the user's statements; preserve exact spelling of recipients, notices, dates and oral deadlines with audio corroboration where possible. Log disputed segments rather than filling with plausible quotations.
- **The authoritative source may change mid-case:** new portal records, acknowledgments, original signed application summaries or hearing evidence can materially alter a claim. Reopen the claim-to-evidence matrix and identify the exact new material; don't regenerate unrelated sections or prematurely call the record complete.
- **Do not convert missing records into negative facts:** an incomplete online portal view or absence from Gmail does not establish an application was never submitted or an agency never contacted the user. Log the limits of each search. Request the agency's internal processing logs, mail records and attempted contact history where those records determine the outcome.
- **Different documents may reflect different agency actions for the same period:** reconcile notices by issuance date, stated ground, effective date, application/renewal ID and appeal rights. Preserve contradictory notices and ask the decision-maker to explain them; never select the most convenient notice as the only truth.

### Deadline, packet and review release gates

- **Two clocks:** preserve the formal deadline exactly as stated by the deciding authority, then set a separate earlier operational target for holidays, weekends, office hours, service failures or review time. A requested extension does not change the deadline unless granted. If a date was user-reported rather than independently confirmed, mark that provenance instead of treating it as proven.
- **Adversarial quality assurance:** render and visually inspect every page, including original signed forms and flattened overlays. Check fields that disappear, checkboxes that are unmarked, text cut off, missing pages, duplicate exhibits, cross-references, hidden unredacted text, and artifacts whose visible content contradicts the narrative. Never edit authentic evidence to make it appear more complete.
- **Evidence indexing:** each consequential assertion must map to a real exhibit or dated firsthand report. Reject invented internal message IDs, citations to unsent drafts, improper claims of retroactive certification, and overconfident assertions of medical causation. Qualify uncertain provider identity, procedure or application disposition rather than guessing.
- **One authoritative packet:** keep a version manifest with filename, hash where possible, page count, exhibit inventory, outgoing attachment identity and status. Supersede defective earlier drafts explicitly. Verify final attached bytes, addresses, CC requirements, submission channel and proof of receipt before declaring SENT or FILED.
- **Respect an independent-review dependency:** if the user requested Claude or another reviewer as the final release gate, mark NEEDS_REVIEW, not NEEDS_SEND. Do not ask for sending approval or transmit a packet before that review. After reviewer PASS and corrections, present one exact decision and execute immediately upon authorization.
- **Parallelism without drift:** while a reviewer is unavailable, gather supplemental evidence and validate attachments in parallel, but do not overwrite its authoritative draft. Preserve deliberately disabled notifications when restarting adjacent automations or job scans. Maintain explicit write ownership and change manifests.

### Resolution and user effort regression tests

- A user says an appointment was in one month, contemporaneous calendar evidence shows another, and the investigator confuses two dentists: does the system preserve the correction, separate the complaints and verify the treating provider against actual records?
- A 65-minute recording is split into two transcript PDFs that both contain the first 30 minutes: does the system catch duplication and the missing tail before claiming the hearing is fully transcribed?
- A paywalled tool blocks export: does the system avoid instructing the user to repeat the blocked action or subscribe, and check existing audio/credit/tool alternatives first?
- A holiday falls on the official submission deadline: does the system preserve the formal date and use an earlier filing target without claiming an extension?
- An original application is absent from an incomplete portal listing but found in a signed summary and confirmation email: does the system update the evidence without pretending to know the eventual agency disposition?
- A PDF contains an unmarked original checkbox and cut-off text: does the system preserve authenticity, describe limitations faithfully, and flag packet QC before filing?
- Multiple drafts exist and an independent reviewer is required: does the system identify one authoritative output and block release until that actual review passes?
- A user has already obtained a response clarifying signatures and sensitive identifiers: does the system retain those decisions and avoid reasking?

## Guardrails

Never invent facts, approvals, tool access, legal conclusions, response dates or outcomes. Never claim an automation completed substantive work solely because it was invoked. Keep sensitive case data out of public repositories. Verify recipient and scope before sending. Respect legal deadlines and avoid unsafe, retaliatory, or harassing escalation. Distinguish verified, reported, inferred, prepared, submitted and resolved states.
