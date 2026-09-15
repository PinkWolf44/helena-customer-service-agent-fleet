# Evaluation and Governance

The baseline suite converts failure history into a repeatable release gate.

## Severity model

| Severity | Meaning | Release effect |
|---|---|---|
| Critical | Could send an unsupported operational claim, violate approval boundaries or expose internal systems | Blocks release |
| High | Could misroute work, ignore relevant history or create a harmful promise | Blocks release until resolved |
| Medium | Degrades consistency, tone or formatting | Fix or record an explicit exception |

## Test anatomy

Each regression test records:

- the incident class it protects against;
- a synthetic input;
- the authoritative data available to the agent;
- required behaviours;
- forbidden behaviours;
- observable pass criteria;
- severity and owner.

## Change gate

1. Capture the current files and Health Card.
2. Define the intended change and its blast radius.
3. Apply the smallest bounded edit.
4. Run the full baseline, not only a happy-path example.
5. Run live-tool smoke checks without sending external messages.
6. Record evidence and update the Health Card.
7. Roll back if any critical test fails.

## What the tests protect

- Unsupported carrier or tracking claims
- Fabricated product facts
- Thread blindness
- Wrong market or language
- Unauthorised external sending
- False follow-up promises
- Internal path or system disclosure
- Incorrect aftercare handoff
- Formatting that breaks the support workflow

See the [synthetic baseline example](../examples/BASELINE.sample.md).
