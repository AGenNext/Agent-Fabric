# Existing Literature and Protocols

This document maps Agent-Fabric concepts to existing literature, standards, and protocols.

Agent-Fabric should not invent new words where mature concepts already exist.
It should compose existing concepts into a coherent operational fabric for agents, humans, tools, runtimes, policies, contracts, traces, and state.

## Summary

| Fabric concept | Existing grounding |
|---|---|
| Node | W3C PROV Entity/Agent, schema.org Thing, JSON-LD node identifiers |
| Relationship | RDF triples, JSON-LD, PROV relations, schema.org properties |
| Identity | W3C DID Core, W3C Verifiable Credentials, issuer-holder-verifier trust model |
| Trace | W3C PROV, OpenTelemetry traces, audit logs |
| Event | CNCF CloudEvents, ActivityStreams, Linked Data Notifications |
| Contract | Contract Net Protocol, multi-agent commitments, service contracts |
| Commitment | Commitment-based multi-agent systems, debtor-creditor obligations |
| Authority | OPA/Rego, XACML, OpenFGA/ReBAC, AuthZEN, approval workflows |
| Policy | OPA/Rego, XACML, Cedar-style authorization, policy-as-code |
| Time | RFC 3339, ISO 8601, bitemporal modeling, event sourcing |
| Intent | BDI agents, goal-oriented requirements, objectives and constraints |
| Validation | JSON Schema, SHACL, schema.org validation literature |
| Reconciliation | Kubernetes controllers, GitOps/Flux/ArgoCD, control theory, event sourcing |
| State | Event-sourced projections, Kubernetes desired/observed state, digital twins |
| Vocabulary | SKOS, schema.org, RDF vocabularies, controlled taxonomies |

---

## 1. Node

Fabric Node maps to existing concepts:

- `prov:Entity` for things produced, used, or transformed.
- `prov:Agent` for people, software agents, organizations, or systems with responsibility.
- `schema:Thing` as the broad web vocabulary root.
- JSON-LD `@id` for stable linked-data identifiers.

Fabric extension:

```text
A Fabric Node is any addressable operational thing that can participate in relationships, authority, validation, reconciliation, and state projection.
```

Existing protocols:

- W3C PROV
- JSON-LD
- RDF
- schema.org

---

## 2. Relationship

Fabric Relationship maps directly to RDF-style subject-predicate-object triples.

```text
subject predicate object
```

Example:

```text
agent:x runsOn runtime:y
```

Existing grounding:

- RDF triples
- JSON-LD linked data
- schema.org properties
- PROV relations such as `wasGeneratedBy`, `used`, `wasAssociatedWith`, `wasDerivedFrom`

Fabric extension:

```text
A Fabric Relationship must carry status, evidence, risk, authority, and lifecycle.
```

This is stricter than plain RDF because operational systems need governance and reconciliation, not just semantic linkage.

---

## 3. Identity

Fabric Identity maps to:

- W3C Decentralized Identifiers (DID Core)
- W3C Verifiable Credentials
- issuer-holder-verifier trust model
- enterprise IAM and lifecycle identity concepts

DID gives persistent, verifiable identifiers.
VC gives signed claims about subjects.

Fabric extension:

```text
Every actor node must have identity, issuer, lifecycle, and verification status before it can hold authority.
```

Existing protocols:

- W3C DID Core
- W3C Verifiable Credentials Data Model
- SCIM for identity lifecycle provisioning
- OpenID Connect and SAML for enterprise authentication

---

## 4. Trace and Provenance

Fabric Trace is grounded in provenance and observability.

Existing grounding:

- W3C PROV models provenance through Entity, Activity, Agent, and relations such as generation, usage, derivation, attribution, and association.
- OpenTelemetry models traces, spans, metrics, logs, baggage, and context propagation for observability.
- Audit logs provide compliance evidence.

Fabric extension:

```text
A Fabric Trace is evidence that supports a claim, event, proposal, decision, or reconciliation.
```

Rule:

```text
No claim without trace.
```

Existing protocols:

- W3C PROV-O
- OpenTelemetry
- audit log standards and SIEM event models

---

## 5. Event

Fabric Event is grounded in event-driven architecture.

Existing grounding:

- CNCF CloudEvents standardizes event metadata across systems.
- ActivityStreams 2.0 represents activities and social/event objects in JSON-LD.
- Linked Data Notifications defines HTTP-based linked-data notification exchange.

Fabric extension:

```text
A Fabric Event records an observed change that may trigger validation, gap filling, reconciliation, or state projection.
```

Existing protocols:

- CloudEvents
- ActivityStreams 2.0
- Linked Data Notifications
- Webhooks
- Event sourcing patterns

---

## 6. Contract

Fabric Contract is grounded in service contracts, legal contracts, and multi-agent contract protocols.

Existing grounding:

- Contract Net Protocol: a classic multi-agent task allocation protocol where a manager issues a call for proposals and contractors respond with proposals or refusals.
- Service-level agreements and API contracts.
- Legal and commercial contract concepts.

Fabric extension:

```text
A Fabric Contract binds parties, scope, obligations, authority, and lifecycle into a governed operational relationship.
```

Existing literature:

- Reid G. Smith, Contract Net Protocol, 1980
- FIPA Contract Net Interaction Protocol
- Service contracts and SLAs

---

## 7. Commitment

Commitment is the deeper primitive under contract.

Existing multi-agent literature treats commitments as social relationships, commonly involving:

```text
Debtor commits to creditor to bring about condition under context.
```

Typical commitment lifecycle:

```text
create
detach
discharge
cancel
release
assign
delegate
violate
expire
```

Fabric extension:

```text
A Fabric Commitment records what was promised, by whom, to whom, under which conditions, with what evidence, authority, deadline, and fulfillment state.
```

Existing grounding:

- Commitment-based multi-agent systems
- Tosca: operationalizing commitments over information protocols
- Contract Net Protocol
- Commitment devices in economics

Important distinction:

```text
Cryptographic commitment schemes are not the same as social or operational commitments.
```

Cryptographic commitments hide and later reveal values.
Fabric commitments model obligations and fulfillment.

---

## 8. Authority

Fabric Authority is grounded in access control, policy decision systems, and governance workflows.

Existing grounding:

- XACML: OASIS policy language for authorization decisions.
- OPA/Rego: policy-as-code and general-purpose policy decision point.
- OpenFGA/ReBAC: relationship-based authorization.
- AuthZEN: modern authorization API work under OpenID Foundation.
- Enterprise approval workflows and separation of duties.

Fabric extension:

```text
Fabric Authority records the decision chain: observer, proposer, validator, reviewer, approver, reconciler, projector, accountable authority.
```

Rule:

```text
No fabric change becomes stable state without an authority chain.
```

---

## 9. Policy

Policy in Fabric should not be invented as loose natural language.

Existing grounding:

- OPA/Rego for executable policy-as-code.
- XACML for access control policies.
- OpenFGA for relationship-based access control.
- AuthZEN for authorization request/response interoperability.
- Cedar-style policy systems for principal-action-resource-context authorization.

Fabric extension:

```text
Policy constrains intent, validates authority, gates relationships, and can trigger reconciliation.
```

Policy should answer:

```text
Can subject perform action on object in context?
```

---

## 10. Time

Fabric Time is grounded in standard timestamp formats and bitemporal modeling.

Existing grounding:

- RFC 3339 profile of ISO 8601 for internet timestamps.
- Event sourcing distinguishes event time and processing time.
- Bitemporal databases distinguish valid time and transaction/recorded time.

Fabric extension:

```text
Fabric separates observedAt, recordedAt, effectiveAt, validFrom, validTo, reconciledAt, and projectedAt.
```

This lets Fabric answer:

```text
What was true then?
What did Fabric know then?
When did Fabric learn it?
Which projection changed after late evidence arrived?
```

---

## 11. Intent

Intent is grounded in agent theory and goal-oriented modeling.

Existing grounding:

- BDI agent model: beliefs, desires, intentions.
- Goal-oriented requirements engineering.
- Planning systems: goals, constraints, actions, outcomes.
- Business process management objectives and constraints.

Fabric extension:

```text
Fabric Intent binds autonomous action to accountable purpose, objective, constraints, success criteria, and outcome.
```

Rule:

```text
No autonomous action without explicit intent.
```

---

## 12. Validation

Fabric Validation is grounded in schema validation and semantic validation.

Existing grounding:

- JSON Schema validates JSON structure.
- SHACL validates RDF graph constraints.
- schema.org validation literature discusses semantic consistency and completeness checks.
- OpenAPI validates API contracts.

Fabric extension:

```text
Fabric Validator combines schema validation, vocabulary validation, reference validation, evidence validation, authority validation, cycle validation, orphan validation, and state reachability validation.
```

Existing protocols:

- JSON Schema Draft 2020-12
- SHACL
- OpenAPI schemas
- schema.org validation patterns

---

## 13. Reconciliation

Fabric Reconciliation is grounded in control loops and desired-state systems.

Existing grounding:

- Kubernetes controllers compare desired and observed state and reconcile resources.
- GitOps tools such as Flux and ArgoCD reconcile declared desired state with cluster state.
- Event sourcing projects state from event history.
- Control theory uses feedback loops to reduce error between target and observed state.

Fabric extension:

```text
Fabric Reconciliation compares desired state, observed state, evidence, policy, authority, risk, and validation results before projecting stable state.
```

Rule:

```text
No stable state without reconciliation.
```

---

## 14. State

Fabric State is grounded in state machines, event sourcing, and digital twin patterns.

Existing grounding:

- Event-sourced projections.
- Kubernetes resource status.
- Digital twin state representations.
- CQRS read models.

Fabric extension:

```text
Fabric State is a versioned, replayable projection derived from accepted events, traces, proposals, authority records, and reconciliations.
```

State is not hand-written.
State is projected.

---

## 15. Vocabulary

Fabric Vocabulary is grounded in controlled vocabularies and semantic web practice.

Existing grounding:

- SKOS for controlled vocabularies, taxonomies, thesauri, and concept schemes.
- schema.org for web-scale vocabulary.
- RDF/OWL vocabularies.

Fabric extension:

```text
Fabric Vocabulary defines the canonical predicates and relationship language used by all AGenNext repos.
```

Rule:

```text
If no predicate exists, emit VocabularyGapProposal instead of inventing a casual edge.
```

---

## Protocol fit map

| Need | Best-fit existing protocol | Fabric use |
|---|---|---|
| Linked identifiers | JSON-LD, RDF | Node and relationship representation |
| Public semantic vocabulary | schema.org | Base entity/action vocabulary |
| Controlled vocabulary | SKOS | Fabric predicates and type system |
| Provenance | W3C PROV-O | Evidence, trace, derivation |
| Event metadata | CloudEvents | Fabric event envelope |
| Distributed notification | Linked Data Notifications | Fabric inbox/outbox messages |
| Identity | DID Core | Stable verifiable identifiers |
| Claims | Verifiable Credentials | Signed authority, role, capability, delegation claims |
| Policy | OPA/Rego, XACML | Machine-enforced constraints |
| Authorization | OpenFGA, AuthZEN | Relationship and request-time authz |
| Schema validation | JSON Schema | JSON fabric record validation |
| Graph validation | SHACL | Semantic graph constraint validation |
| Time | RFC 3339, ISO 8601 | Temporal fields |
| Desired state | Kubernetes API/controller model | Reconciliation loop |
| GitOps | Flux/ArgoCD | Declarative reconciliation inspiration |
| Observability | OpenTelemetry | Traces, spans, correlation |
| Commitments | MAS commitment literature | Obligations, fulfillment, violation |
| Task allocation | Contract Net Protocol | Offers, proposals, acceptance |

---

## What Fabric should reuse directly

Fabric should reuse these as much as possible:

```text
JSON-LD for linked data shape
schema.org for common web entity types
SKOS for vocabulary governance
W3C PROV-O for provenance
CloudEvents for event envelopes
OpenTelemetry for traces and correlation
DID Core for persistent verifiable identifiers
Verifiable Credentials for signed claims
JSON Schema for record validation
SHACL for graph constraints
RFC 3339 timestamps
OPA/Rego for policy decisions
OpenFGA/AuthZEN for authorization
Kubernetes/GitOps reconciliation pattern
Commitment-based MAS literature for obligation lifecycle
Contract Net Protocol for offers/proposals/acceptance
```

## What Fabric should define itself

Fabric should define only what is missing between these systems:

```text
canonical fabric primitives
canonical relationship vocabulary
fabric authority chain
fabric reconciliation record
fabric gap-fill proposal
fabric commitment record
fabric state projection contract
cross-repo ownership boundaries
```

## Avoid

Fabric should avoid pretending to replace:

- RDF
- JSON-LD
- schema.org
- DID/VC
- OPA
- OpenFGA
- CloudEvents
- OpenTelemetry
- Kubernetes
- GitOps
- SHACL
- JSON Schema

Fabric should compose them.

## One-line definition

Agent-Fabric is a governed operational fabric that composes linked data, provenance, identity, events, policy, commitments, validation, and reconciliation into replayable stable state for human-agent work.
