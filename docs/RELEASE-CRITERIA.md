# Release criteria for Beta Skills OS

## Maturity levels
- **Concept:** named problem, no complete workflow.
- **Specification:** trigger, inputs, steps, output contract, guardrails, and acceptance scenarios.
- **Tested:** dated execution records demonstrate that acceptance scenarios pass on a named platform.
- **Integrated:** an authorized connector or runtime performs the workflow end-to-end, with recovery and audit logging.
- **Production-ready:** operational security review, regression coverage, monitoring, and documented rollback.

No skill is production-ready merely because a `SKILL.md` file exists.

## Definition of done for each skill
- [ ] Unique name and specific trigger
- [ ] Required and optional inputs with missing-data behavior
- [ ] Deterministic decision procedure or explicit judgment criteria
- [ ] Machine-readable or inspectable output example
- [ ] At least one success, partial-success, and failure scenario
- [ ] Evidence and provenance handling
- [ ] Authorization, privacy, and irreversible-action boundaries
- [ ] Named owner, version, and last verification date
- [ ] Real test record before any “tested” badge

## Release gates
1. Validate repository links, filenames, and SKILL.md frontmatter.
2. Run the relevant acceptance scenarios and archive dated results.
3. Review authorship and third-party dependencies before licensing.
4. Check that README claims match actual verified evidence.
5. Tag a release only after the checklist is satisfied.

## Cross-agent handoff contract
Each handoff should include: `case_id`, `goal`, `current_state`, `last_verified_at`, `evidence_refs`, `completed_actions`, `pending_actions`, `authorization_scope`, `blocked_reason`, `next_actor`. Unknown fields must be explicit rather than invented.

## Ownership and licensing
Copyright in original material remains with its respective owners. Public visibility alone does not grant a reuse license. External-source adaptations require provenance and permission review before redistribution.
