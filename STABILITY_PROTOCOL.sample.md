# Bot Stability Protocol — Synthetic Example

## Before a change

1. Record the purpose, owner and expected outcome.
2. Save the current stable files and Health Card.
3. Identify affected markets, references, tools and scheduled jobs.
4. Define the test that would prove the change works.

## Apply

1. Make the smallest bounded edit.
2. Review the diff for deleted or contradictory rules.
3. Confirm the mandatory startup set and reference dependencies.
4. Do not combine an infrastructure migration with a behavioural rewrite unless the rollback paths are independent.

## Verify

1. Run the complete baseline suite.
2. Run draft-only smoke tests against non-production or synthetic cases.
3. Verify source retrieval and evidence reporting.
4. Check that scheduled jobs use the intended cadence and destination.
5. Update the Health Card with observed status, not assumed status.

## Release or rollback

- Release only when all Critical and High tests pass.
- Roll back when the agent is unresponsive, loses required references or violates a hard boundary.
- Escalate runtime and connector failures to the infrastructure owner.
- Escalate structural behaviour failures to the behavioural architect.

## After an incident

1. Preserve the failing input and available sources in sanitised form.
2. Identify the missing or conflicting rule.
3. Add a regression test before or with the correction.
4. Apply the fix and rerun the entire suite.
5. Record the outcome and new baseline version.
