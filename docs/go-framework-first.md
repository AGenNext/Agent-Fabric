# Go Framework First

Agent-Fabric should start as a Go framework, not a database-bound implementation.

SurrealDB, Postgres, SQLite, Badger, Pebble, NATS, Kafka, RDF stores, and object stores should be adapters.
The Fabric Kernel should remain portable.

## Decision

```text
Build Fabric Kernel as a Go framework first.
Make storage pluggable.
Use in-memory storage for tests and bootstrap.
Add database adapters later.
```

## Why

A database-first implementation would couple the protocol to one persistence model too early.

A Go framework-first implementation gives:

- stable interfaces,
- deterministic tests,
- embeddable kernel,
- edge and air-gapped readiness,
- CLI/server flexibility,
- pluggable storage,
- clean controller loops,
- stronger type safety,
- easier future Kubernetes/native integration.

## Principle

```text
Fabric Kernel owns behavior.
Storage adapters persist records.
Databases do not define the protocol.
```

## Architecture

```text
Go Fabric Kernel
├── core/          # canonical types and interfaces
├── message/       # Fabric Protocol Messages
├── validate/      # schema, semantic, and rule validation
├── authority/     # authority chain evaluation
├── reconcile/     # reconciliation engine
├── project/       # state projection engine
├── graph/         # relationship resolver
├── temporal/      # time and replay rules
├── commitment/    # commitment lifecycle
├── store/         # storage interfaces
├── store/memory/  # in-memory adapter
├── policy/        # policy adapter interface
├── trace/         # trace adapter interface
├── runtime/       # participant runtime contract
├── api/           # optional HTTP API
└── cmd/fabricd/   # optional daemon
```

## First storage model

The first storage implementation should be memory-backed.

```text
store/memory
```

It must support:

- unit tests,
- replay tests,
- reconciliation tests,
- deterministic examples,
- CLI demos,
- embedded runtime.

## Store interfaces

The kernel should define interfaces, not database tables.

```go
type NodeStore interface {
    PutNode(ctx context.Context, node Node) error
    GetNode(ctx context.Context, id string) (Node, error)
    ListNodes(ctx context.Context, filter NodeFilter) ([]Node, error)
}

type RelationshipStore interface {
    PutRelationship(ctx context.Context, rel Relationship) error
    GetRelationship(ctx context.Context, id string) (Relationship, error)
    RelationshipsFor(ctx context.Context, nodeID string) ([]Relationship, error)
}

type EventStore interface {
    AppendEvent(ctx context.Context, event Event) error
    EventsAfter(ctx context.Context, cursor string) ([]Event, error)
}

type ProjectionStore interface {
    PutState(ctx context.Context, state State) error
    GetState(ctx context.Context, id string) (State, error)
    StateAsOf(ctx context.Context, subject string, asOf time.Time) (State, error)
}
```

## Adapter path

Adapters can be added without changing the kernel.

```text
store/memory   -> first
store/sqlite   -> local durable
store/postgres -> enterprise relational
store/surreal  -> graph/native relation adapter
store/pebble   -> embedded event log
store/rdf      -> semantic graph adapter
```

## Kernel loop in Go

```text
Receive Fabric Message
  -> Verify Identity
  -> Validate Envelope
  -> Append Event
  -> Attach Trace
  -> Validate Record
  -> Resolve Graph
  -> Evaluate Authority
  -> Detect Gap or Drift
  -> Reconcile
  -> Project State
  -> Notify
  -> Audit
```

## First executable milestone

```text
M1: Go framework kernel
```

Must include:

```text
go.mod
cmd/fabricd/main.go
internal or pkg core types
memory store
message envelope
validator interface
reconciler interface
projector interface
basic tests
README quickstart
```

## M1 non-goals

Do not include yet:

- SurrealDB adapter,
- database migrations,
- Kubernetes controller,
- distributed consensus,
- full RDF engine,
- full OPA integration,
- production identity provider,
- UI.

## M1 success test

The framework must pass this loop in memory:

```text
Create node
Create observed event
Create gap-fill proposal
Validate proposal
Create authority chain
Reconcile proposal
Project state
Query state
Replay state from events
```

## Positioning

```text
Agent-Fabric is a Go-native operational fabric kernel with pluggable storage and protocol adapters.
```

## One-line definition

Go framework first means the Fabric Kernel is defined by typed behavior and interfaces, while databases remain replaceable persistence adapters.
