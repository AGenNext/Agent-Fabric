# Agent-Fabric SDK

Agent-Fabric SDK is the developer-facing interface for building Fabric participants, tools, controllers, dashboards, agents, and Fabric Boxes.

The SDK exposes Fabric as a simple operational contract:

```text
observe
propose
validate
authorize
approve
reject
commit
challenge
reconcile
project
query
notify
```

## Decision

Agent-Fabric should be delivered as SDKs first.

```text
SDK first.
Kernel inside.
Adapters later.
```

The Rust crates remain the correctness core, but developers should experience Fabric through SDKs, not internal kernel plumbing.

## SDK layers

```text
Agent-Fabric SDK
├── Rust SDK        # correctness, embedded kernel, edge runtime
├── Go SDK          # operators, controllers, adapters, fleet services
├── TypeScript SDK  # apps, dashboards, browser surfaces, Horizon UI
└── Python SDK      # agents, notebooks, experiments, research workflows
```

## Developer mental model

```text
Fabric::new()
  .observe(event)
  .propose(proposal)
  .validate()
  .authorize()
  .reconcile()
  .project()
```

## Rust SDK

Rust SDK owns:

```text
canonical types
message envelope
validation contracts
authority contracts
reconciliation contracts
projection contracts
embedded memory store
kernel facade
WASM-friendly core later
```

Primary users:

```text
kernel developers
edge runtimes
embedded Fabric Boxes
Snapcraft packaged participants
high-integrity services
```

## Go SDK

Go SDK owns:

```text
controller helpers
operator loops
HTTP clients
Landscape adapter
Ubuntu Core adapter
Snapcraft/snapd adapter
OPA/OpenFGA/AuthZEN adapters
OpenTelemetry adapter
CloudEvents adapter
```

Primary users:

```text
orchestrators
operators
controllers
fleet integrations
cloud-native services
```

## TypeScript SDK

TypeScript SDK owns:

```text
Fabric message client
Horizon UI client
query helpers
state projection viewer helpers
agent dashboard integrations
browser-safe schemas
```

Primary users:

```text
web apps
dashboards
admin panels
Horizon UI
browser-based operators
```

## Python SDK

Python SDK owns:

```text
agent helper APIs
notebook workflows
research experiments
LLM/agent integrations
simple observe/propose/query helpers
```

Primary users:

```text
agent builders
researchers
data scientists
prototype builders
notebook users
```

## SDK surface

All SDKs should expose the same conceptual API.

```text
create_node
create_relationship
observe
propose
validate
authorize
approve
reject
commit
challenge
reconcile
project
query
notify
```

## Non-goals

SDKs should not hide Fabric governance.

They must not silently:

```text
activate state
bypass validation
bypass authority
bypass reconciliation
hide trace requirements
invent predicates
ignore lifecycle
```

## Repository layout

```text
sdk/
├── rust/
├── go/
├── typescript/
└── python/

crates/
├── fabric-core/
├── fabric-message/
├── fabric-validate/
├── fabric-authority/
├── fabric-reconcile/
├── fabric-project/
├── fabric-store-memory/
└── fabric-kernel/
```

## One-line definition

Agent-Fabric SDK is the developer-facing contract that lets builders create Fabric participants while preserving validation, authority, reconciliation, traceability, and projected state.
