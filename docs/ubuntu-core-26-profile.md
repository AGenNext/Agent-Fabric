# Ubuntu Core 26 Fabric Node Profile

Ubuntu Core 26 is the sealed node substrate for Agent-Fabric deployments.

Snapcraft is the packaging trick.

It turns the Rust kernel, Go orchestrator, adapters, validators, reconcilers, projectors, and agents into sealed Fabric participants that can be signed, confined, refreshed, rolled back, and distributed through channels.

## Definition

A Fabric Node on Ubuntu Core 26 is a sealed, updateable, recoverable, snap-based appliance that runs Fabric participants under explicit confinement, signed trust, transactional updates, and rollback.

```text
Source Code
  -> Snapcraft
  -> Snap
  -> Assertion
  -> Channel
  -> Ubuntu Core 26
  -> Fabric Box
```

## Core rule

```text
No unmanaged services on a Fabric Box.
Everything active is packaged by Snapcraft, confined by snapd, signed by assertions, refreshed transactionally, and recoverable.
```

## Snapcraft role

Snapcraft is the build and packaging layer for Fabric participants.

It owns:

```text
snapcraft.yaml
build parts
Rust build step
Go build step
runtime staging
service declaration
interfaces/plugs/slots
confinement declaration
version metadata
channel publishing
```

It converts:

```text
Rust Fabric Kernel      -> fabric-kernel snap
Go Fabric Orchestrator  -> fabric-orchestrator snap
Gap Filler Agent        -> fabric-agent-gap-filler snap
Validator Wrapper       -> fabric-validator snap
Reconciler Wrapper      -> fabric-reconciler snap
Projector Wrapper       -> fabric-projector snap
Policy Adapter          -> fabric-policy-adapter snap
Identity Adapter        -> fabric-identity-adapter snap
Trace Adapter           -> fabric-trace-adapter snap
Store Adapter           -> fabric-store-* snap
```

## Fabric Box

```text
Fabric Box
├── Ubuntu Core 26
├── kernel snap
├── gadget snap
├── base snap
├── snapd
├── fabric-kernel snap
├── fabric-orchestrator snap
├── fabric-agent snaps
├── fabric-policy snap
├── fabric-identity snap
├── fabric-trace snap
├── fabric-store snap
└── recovery system
```

## Ubuntu Core feature mapping

| Ubuntu Core feature | Agent-Fabric use |
|---|---|
| Immutable base | Stable node substrate |
| Snapcraft | Build Fabric participants as snaps |
| Snaps | Package Fabric kernel, agents, tools, adapters, and services |
| Strict confinement | Isolate agents, tools, stores, and adapters |
| Interfaces | Declare explicit capability grants between snaps |
| Assertions | Signed trust statements for model, account, snap, and validation |
| Transactional updates | Safe upgrade path for Fabric components |
| Rollback | Recover failed kernel/orchestrator/agent releases |
| Channels | Release rings: edge, beta, candidate, stable |
| Validation sets | Approved combinations of Fabric snaps |
| Gadget snap | Hardware and device model contract |
| Kernel snap | Controlled Linux kernel boundary |
| Base snap | Minimal runtime base |
| Recovery system | Restore broken node state |
| Remodeling | Transition device model or role under signed authority |
| Brand store | Controlled enterprise distribution of Fabric snaps |

## Snap boundaries

```text
snaps/
├── fabric-kernel/             # Rust correctness kernel
├── fabric-orchestrator/       # Go control plane and API server
├── fabric-agent-gap-filler/   # gap detection and proposal agent
├── fabric-validator/          # validation service wrapper
├── fabric-reconciler/         # reconciliation controller wrapper
├── fabric-projector/          # state projection service wrapper
├── fabric-policy-adapter/     # OPA/OpenFGA/AuthZEN adapter
├── fabric-identity-adapter/   # DID/VC/OIDC/SCIM adapter
├── fabric-trace-adapter/      # OpenTelemetry/provenance adapter
├── fabric-store-memory/       # local test/dev store
└── fabric-store-durable/      # durable storage adapter
```

## Snapcraft build rule

Each participant must have a `snap/snapcraft.yaml`.

Minimum required metadata:

```yaml
name: fabric-kernel
base: core24
version: git
grade: stable
confinement: strict
summary: Agent-Fabric Rust correctness kernel
description: |
  Fabric Kernel validates, reconciles, projects, and replays Fabric state.
```

Rule:

```text
If it participates in Fabric, it gets a snapcraft.yaml.
```

## Rust kernel snap

The `fabric-kernel` snap contains the Rust kernel.

Owns:

```text
canonical types
validation invariants
authority invariants
commitment lifecycle
reconciliation invariants
projection invariants
replay rules
```

## Go orchestrator snap

The `fabric-orchestrator` snap contains the Go orchestration layer.

Owns:

```text
HTTP API
controller loops
event ingress
message routing
storage adapters
policy adapters
identity adapters
trace adapters
health reporting
snap-aware lifecycle hooks
```

## Participant snap contract

Every participant snap must declare:

```text
identity
capabilities
accepted message types
emitted message types
authority boundary
required interfaces
health endpoint
trace behavior
update channel
```

## Interface model

Use snap interfaces as the OS-level capability boundary.

Rule:

```text
No hidden side channel. Every connection is declared.
```

## Release channels

```text
edge
beta
candidate
stable
```

Fabric interpretation:

| Channel | Use |
|---|---|
| edge | experimental builds and internal testing |
| beta | integration testing |
| candidate | release candidate with validation set |
| stable | production-approved Fabric component |

## Validation sets

Validation sets define approved combinations of Fabric snaps.

Rule:

```text
A Fabric Box is valid only when its installed snap set matches an approved validation set.
```

## Assertions and trust

Ubuntu Core assertions become OS-level trust anchors.

Fabric maps them to:

```text
model assertion       -> Fabric Box model identity
account assertion     -> publisher identity
snap declaration      -> allowed snap capabilities
snap revision         -> signed component version
validation assertion  -> approved component combination
serial assertion      -> device identity
```

## Transactional update and rollback

Update flow:

```text
Snapcraft builds snap
Snap is signed and released to channel
Device refreshes snap
Health check runs
Revision accepted or rolled back
Fabric emits update event
Fabric reconciles node state
```

## Security rules

```text
No apt on production Fabric Boxes.
No unmanaged daemon.
No hidden sidecar.
No unconfined participant by default.
No mutable base assumption.
No update without health check.
No rollback without event.
No interface connection without declared purpose.
No production snap outside approved validation set.
```

## One-line definition

Snapcraft is the build spell that turns Agent-Fabric code into sealed Ubuntu Core participants; Ubuntu Core 26 is the substrate that runs them as recoverable Fabric Boxes.
