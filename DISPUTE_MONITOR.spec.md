# Hourly Dispute Monitor — Sanitised Specification

## Purpose

Surface support conversations that contain a dispute signal so the operations team can review them promptly.

## Attribution pattern

- The behavioural/operations owner defines the trigger, cadence, destination and acceptance test.
- The agent runtime creates or updates the scheduled job after an explicit instruction.
- A platform administrator may create the destination channel when admin permission is required.
- Creating the channel does not constitute authorship of the monitoring workflow.

## Schedule

Run at the start of every hour:

```cron
0 * * * *
```

## Inputs

- Read-only access to the support queue
- Search term: `dispute` (case-insensitive)
- Persistent checkpoint for the last completed scan
- Approved internal alert destination

## Logic

```text
load last successful checkpoint
search conversations updated after checkpoint
select conversations containing the configured dispute term
deduplicate by conversation identifier and update timestamp
post a minimal internal alert for each new match
store the new checkpoint only after the scan succeeds
record counts, execution time and errors
```

## Safety requirements

- Do not send a customer message.
- Do not copy unnecessary customer content into the alert.
- Do not expose credentials or internal URLs in logs.
- Do not advance the checkpoint after a failed or partial scan.
- Prevent duplicate alerts after retries.
- Send a health warning when repeated executions fail.

## Acceptance tests

1. A new synthetic conversation containing `dispute` produces one alert.
2. A case-insensitive match produces one alert.
3. An unrelated conversation produces no alert.
4. Re-running the same scan does not duplicate the alert.
5. A simulated API failure preserves the earlier checkpoint.
6. The job creates no external customer action.

This is a portfolio specification, not the production job or its live configuration.
