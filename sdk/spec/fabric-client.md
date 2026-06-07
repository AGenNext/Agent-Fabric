# Fabric Client SDK Contract

This is the language-neutral SDK contract for Agent-Fabric.

Every SDK must expose the same conceptual surface even if language idioms differ.

## FabricClient

The FabricClient is the developer-facing entry point for Fabric operations.

```text
FabricClient
├── create_node
├── create_relationship
├── observe
├── propose
├── validate
├── authorize
├── approve
├── reject
├── commit
├── challenge
├── reconcile
├── project
├── query
└── notify
```

## Rule

```text
SDKs may simplify usage, but must not bypass validation, authority, reconciliation, traceability, or lifecycle.
```

## Required operations

### create_node

Creates a Fabric node record.

```text
create_node(input) -> Node
```

### create_relationship

Creates a proposed Fabric relationship.

```text
create_relationship(input) -> Relationship
```

### observe

Records an observation as a Fabric message/event.

```text
observe(event) -> Envelope
```

### propose

Creates a candidate change.

```text
propose(proposal) -> Envelope
```

### validate

Validates a record or message.

```text
validate(target) -> ValidationReport
```

### authorize

Evaluates authority for an action.

```text
authorize(request) -> AuthorityResult
```

### approve

Approves a proposal within authority scope.

```text
approve(target, authority) -> Envelope
```

### reject

Rejects a proposal with reason.

```text
reject(target, reason) -> Envelope
```

### commit

Creates or accepts a commitment.

```text
commit(commitment) -> Envelope
```

### challenge

Challenges a record, state, authority, or relationship.

```text
challenge(target, reason) -> Envelope
```

### reconcile

Produces a reconciliation plan or outcome.

```text
reconcile(input) -> ReconciliationOutcome
```

### project

Projects stable state from accepted records.

```text
project(input) -> State
```

### query

Queries Fabric state or history.

```text
query(request) -> QueryResult
```

### notify

Emits a Fabric notification.

```text
notify(notification) -> Envelope
```

## SDK language roles

| SDK | Primary role |
|---|---|
| Rust | correctness, embedded kernel, WASM-ready core |
| Go | operators, controllers, adapters, fleet services |
| TypeScript | apps, dashboards, Horizon UI, browser surfaces |
| Python | agents, notebooks, experiments, research workflows |

## Minimal chain

Every SDK must make this chain easy:

```text
observe
  -> propose
  -> validate
  -> authorize
  -> reconcile
  -> project
```

## One-line definition

FabricClient is the common developer-facing SDK contract for creating, validating, authorizing, reconciling, projecting, and querying Fabric state.
