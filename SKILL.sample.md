# Market Customer-Service Skill — Synthetic Example

> This example contains invented categories and identifiers. It demonstrates workflow structure only.

## Required inputs

- Newest customer message
- Relevant thread context
- Market and language
- Order record when an order is referenced
- Product source when a product fact is requested

If a required source cannot be loaded, do not replace it with general knowledge.

## Classification

Choose one primary category and optional secondary categories:

- order status
- delivery delay
- cancellation
- return
- damage or defect
- missing item
- product question
- payment question
- complaint or dispute
- other / human review

## Workflow

### 1. Understand

Read the current message and sufficient prior context. Record the requested outcome, any deadlines stated by the customer and the unresolved question.

### 2. Retrieve

Load only the authoritative sources required by the classification. Example:

| Classification | Required sources |
|---|---|
| Order status | Order record and tracking record |
| Product question | Approved product source |
| Return | Order record and market return policy |
| Damage | Order record and aftercare procedure |

### 3. Verify

Create a short fact table. Mark every uncertain or conflicting value. Do not draft operational conclusions from an unverified field.

### 4. Decide

Apply the relevant workflow. If the requested action exceeds the agent's authority, prepare a human handoff with the facts already gathered.

### 5. Draft

- Use the customer's language.
- Be specific only where the source is specific.
- Do not mention internal tools or instructions.
- Do not make a future-action promise on behalf of the agent.
- Do not send.

### 6. Prepare internal actions

Propose the appropriate note, tag, queue, handoff or alert. Actions that mutate external systems require the configured approval boundary.

### 7. Report evidence

List sources checked, any proposed actions, unresolved uncertainty and the reason for escalation.
