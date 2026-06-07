# Rust Kernel, Go Orchestration

Agent-Fabric should use Rust for the kernel core and Go for orchestration.

This gives the system a strict correctness boundary without making the whole platform unnecessarily complex.

## Decision

```text
Rust = Fabric Kernel
Go   = Fabric Orchestration
```

## Why Rust for the kernel

The Fabric Kernel owns correctness.

It must enforce:

- typed records,
- safe state transitions,
- validation gates,
- authority gates,
- temporal rules,
- reconciliation invariants,
- replayability,
- deterministic projection,
- memory-safe embedded execution.

Rust is the right fit for this layer because the kernel should make invalid state difficult to represent.

## Why Go for orchestration

The orchestration layer owns integration and operations.

It must handle:

- HTTP APIs,
- controllers,
- workers,
- adapters,
- Kubernetes integration,
- CloudEvents routing,
- OpenTelemetry export,
- OPA/OpenFGA/AuthZEN adapters,
- storage adapters,
- CLI/daemon lifecycle,
- deployment operations.

Go is the right fit for this layer because it is simple, operational, and excellent for controllers and cloud-native services.

## Boundary rule

```text
Rust decides what is valid.
Go decides where it runs.
```

## Layering

```text
Agent-Fabric
├── Rust Kernel
│   ├── core types
│   ├── validation
│   ├── authority checks
│   ├── commitment lifecycle
│   ├── reconciliation engine
│   ├── projection engine
│   ├── temporal replay rules
│   └── in-memory reference store
│
└── Go Orchestration
    ├── API server
    ├── controller loops
    ├── storage adapters
    ├── policy adapters
    ├── identity adapters
    ├── trace adapters
    ├── event bus adapters
    └── deployment/runtime ops
```

## Rust workspace

```text
crates/
├── fabric-core/          # canonical types and invariants
├── fabric-message/       # protocol message envelope and message types
├── fabric-validate/      # validation engine
├── fabric-authority/     # authority chain checks
├── fabric-commitment/    # commitment lifecycle
├── fabric-reconcile/     # reconciliation engine
├── fabric-project/       # projection engine
├── fabric-store-memory/  # in-memory reference store
└── fabric-kernel/        # composed kernel facade
```

## Go workspace

```text
go/
├── cmd/fabricd/          # daemon / API server
├── internal/controller/  # control loops
├── internal/adapters/    # storage/policy/identity/trace adapters
├── internal/api/         # HTTP handlers
├── internal/events/      # CloudEvents routing
└── pkg/client/           # Go client for Fabric Kernel/API
```

## Kernel API boundary

The Rust kernel should expose a small stable surface:

```text
validate(record) -> ValidationResult
check_authority(change, chain) -> AuthorityResult
reconcile(input) -> ReconciliationRecord
project(input) -> State
replay(events) -> State
```

Go should call this boundary, not reimplement it.

## First implementation profile

M1 should build only the Rust kernel.

```text
M1: Rust Kernel
```

Includes:

- Cargo workspace,
- core record structs,
- message envelope,
- in-memory store,
- validator trait,
- reconciler trait,
- projector trait,
- basic end-to-end test.

M1 test:

```text
Create node
Create relationship proposal
Validate proposal
Attach authority chain
Reconcile
Project state
Replay state
```

## M2: Go orchestration

```text
M2: Go Orchestrator
```

Includes:

- API server,
- controller loop,
- CloudEvents ingress,
- OpenTelemetry adapter,
- OPA/OpenFGA/AuthZEN adapter shell,
- storage adapter shell,
- calls into Rust kernel through CLI, FFI, WASM, or service boundary.

## Integration options

| Option | Use |
|---|---|
| Rust binary + Go process call | simplest early integration |
| Rust HTTP/gRPC service | clean service boundary |
| Rust compiled to WASM | embeddable policy/kernel evaluation |
| Rust FFI | fast but more operational complexity |
| Pure Rust daemon first | simplest correctness-first path |

Preferred first path:

```text
Pure Rust kernel binary first.
Go orchestration second.
```

## Repository shape

```text
Agent-Fabric/
├── crates/
│   ├── fabric-core/
│   ├── fabric-message/
│   ├── fabric-validate/
│   ├── fabric-authority/
│   ├── fabric-reconcile/
│   ├── fabric-project/
│   ├── fabric-store-memory/
│   └── fabric-kernel/
├── go/
│   ├── cmd/fabricd/
│   └── internal/
├── docs/
├── schemas/
├── contexts/
├── examples/
└── tests/
```

## Non-overlap rule

Rust must not own:

- deployment orchestration,
- Kubernetes controllers,
- external policy engines,
- external identity providers,
- long-running ops glue unless required.

Go must not own:

- canonical type invariants,
- reconciliation correctness,
- projection correctness,
- authority-chain invariants,
- temporal replay semantics.

## One-line definition

Agent-Fabric uses Rust as the correctness kernel and Go as the cloud-native orchestration layer.
