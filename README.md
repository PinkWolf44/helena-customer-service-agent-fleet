# Multi-Market Customer-Service Agent Fleet

## Outcome

I architected a human-in-the-loop customer-service agent system for several markets. The agents classified requests, gathered verified information from business tools, prepared replies, added operational notes and tags, escalated exceptions and supported scheduled monitoring—while preserving a hard rule that a human sent the final customer message.

This case study is based on implementation files and a live configuration snapshot captured on 13 September 2026. The public examples are sanitised and synthetic.

## The problem

Customer-service work was spread across markets, languages, products, logistics providers and internal systems. A useful agent needed more than a friendly prompt: it had to understand local policy, retrieve the correct records, avoid inventing facts, read enough conversation history, prepare operational actions and know when to stop.

## The system I designed

I separated the control layer into reusable components:

| Component | Purpose |
|---|---|
| `SOUL.md` | Identity, tone, hard safety boundaries and execution discipline |
| Market `SKILL.md` | Classification, tool use, workflow steps, drafting and escalation |
| Reference files | Product, logistics, claims and market-specific knowledge |
| `BASELINE.md` | Regression tests that block unsafe changes |
| Health Card | Current status, connections, risks and ownership |
| Stability Protocol | Controlled change, testing, rollback and incident handling |
| Scheduled monitors | Recurring operational checks and alerts |

The core flow is:

> classify → retrieve → verify → draft → record actions → escalate when required → human review

See [Architecture](docs/ARCHITECTURE.md) for the full topology.

## My role

I owned the product and behavioural architecture, authored the control and evaluation files, transformed operational source material into executable Markdown, performed initial testing and commissioning, designed scheduled workflows and handled major corrections and cross-agent governance.

Market specialists supplied local knowledge and examples, reviewed live output, trained their assigned agents and made smaller local corrections. Infrastructure specialists created hosts and connected the runtime to customer-support, internal-data and team-messaging systems. They did not design or train the agents.

See [Ownership and collaboration](docs/OWNERSHIP.md).

## What made the work technical

- The agent had multiple control layers with explicit precedence and scope.
- Claims about orders, carriers and products required source verification.
- Human approval was enforced as an operational boundary, not a suggestion.
- Production failures became rules and deployment-blocking regression tests.
- Agents could modify their own workspace only after an authorised operator gave a bounded instruction; the result was then tested.
- Scheduled jobs connected inbox signals to internal alert workflows.
- Token-saving strategies had to be balanced against thread completeness and reference availability.

## Evidence-backed lessons

1. A polished response can still be operationally wrong if its facts are not grounded.
2. Progressive reference loading reduces context, but missing files can silently remove critical rules.
3. Thread compression needs precedence rules; “read everything” and “read only the latest messages” cannot both be absolute.
4. Evaluation suites are most valuable when they preserve lessons from actual incidents.
5. Deployment status, adoption and integration status must be reported separately.

## Repository contents

- [Architecture](docs/ARCHITECTURE.md)
- [Ownership and collaboration](docs/OWNERSHIP.md)
- [Evaluation and governance](docs/EVALUATION_AND_GOVERNANCE.md)
- [Incident-driven improvement](docs/INCIDENT_DRIVEN_IMPROVEMENT.md)
- [Evidence and sanitisation](docs/EVIDENCE_AND_SANITISATION.md)
- [Sample SOUL](examples/SOUL.sample.md)
- [Sample market skill](examples/SKILL.sample.md)
- [Sample baseline suite](examples/BASELINE.sample.md)
- [Sample Health Card](examples/HEALTH_CARD.sample.md)
- [Sample Stability Protocol](examples/STABILITY_PROTOCOL.sample.md)
- [Hourly dispute monitor specification](automations/DISPUTE_MONITOR.spec.md)

## Honest boundaries

This is not the production repository. Exact commercial policies, live endpoints, customer records, company identifiers and proprietary source files have been removed. No impact numbers are claimed until reliable measurements can be attached.
