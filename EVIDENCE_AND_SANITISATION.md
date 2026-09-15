# Evidence and Sanitisation

## Evidence base

The internal audit used a configuration snapshot retrieved directly from a live agent workspace on 13 September 2026. The snapshot contained four substantive control files:

- an identity and behavioural boundary file;
- a market customer-service workflow skill;
- a legacy global aftercare workflow skill;
- a versioned baseline regression suite.

The current source agent still carries both the market workflow and the older aftercare scope. That fact is recorded as configuration evidence only; it is not used to imply that a separate aftercare deployment was fully connected or operational.

Additional attribution was confirmed directly by the system architect and checked against handoff documents. Where an earlier AI-generated summary conflicted with direct confirmation, the direct confirmation controls.

## Why the production files are not published

The source snapshot contains confidential operating details, including private policies, internal system names, organisation-specific workflows, colleague names, machine paths and realistic business identifiers. It contains no detected credentials, but absence of credentials does not make the rest suitable for publication.

## Transformation rules

The examples in this repository:

- preserve architectural patterns but not production wording;
- replace brands, tools, people and agent names with role descriptions;
- replace order, product and logistics data with synthetic examples;
- omit exact commercial thresholds and operational destinations;
- avoid claims about deployments that lacked required integrations or adoption;
- separate verified facts from remaining evidence gaps.

This approach makes the work inspectable without turning a portfolio into a production-data leak.
