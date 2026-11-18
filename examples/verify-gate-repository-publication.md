# Verify Gate showcase: the repository that existed before its files did

**Type:** Real workflow pattern, anonymized and limited to publicly verifiable repository state. This is a retrospective case study, not a recorded execution of the skill.

## The failure mode
1. A public GitHub repository was created successfully.
2. A file upload was interrupted or its approval expired.
3. The repository existed but the expected files had not been published.
4. A subsequent authorized retry uploaded the text files and hero image.

## The incorrect shortcut
> "The repository exists, therefore the project is published."

That statement conflates **resource creation** with **deliverable completion**.

## Verify Gate postconditions
| Check | Evidence required | Outcome |
|---|---|---|
| Repository exists | GitHub repository read | Independently observable |
| README published | Fetch README.md from main | Independently observable |
| All skill files published | Fetch each required SKILL.md | Must check individually |
| Hero published | Fetch assets/hero.png | Independently observable |
| All acceptance tests passed | Dated test run records | Not established by publication |

## What changes
The agent reports partial success when only the repository exists. It retries only after checking destination state, then reports publication only when the expected paths resolve. It does not claim that skill workflows have passed integration tests.

## What remains unverified
Production reliability, compatibility across agent platforms, and the runtime behavior of the skills. Those require separate dated tests.

See [Verify Gate](../skills/verify-gate/SKILL.md) and [test scenarios](../tests/verify-gate.md).
