# Fabric Federation Model

Fabric Federation Model defines the canonical topology for Agent-Fabric operations.

It connects the logical Fabric model to Ubuntu Horizon, Ubuntu Landscape, Ubuntu Core, Snapcraft-built participants, and real operational boundaries.

## Definition

A Fabric Federation is a governed collection of domains, clusters, boxes, and participants that exchange Fabric Protocol Messages while preserving identity, authority, trust, reconciliation, and failure boundaries.

```text
Fabric Federation
└── Fabric Domain
    └── Fabric Cluster
        └── Fabric Box
            └── Fabric Participant
```

## Core rule

```text
Topology is authority-bearing.
```

A topology boundary is not just visual grouping.
It affects ownership, trust, update policy, failure containment, reconciliation scope, and command authority.

---

## 1. Fabric Federation

A Federation is the highest trust and governance boundary.

It represents a connected operating world where domains agree to exchange Fabric messages under shared protocol rules.

Examples:

```text
AGenNext managed federation
enterprise federation
partner federation
sovereign deployment federation
air-gapped federation
```

A Federation owns:

```text
federation identity
root trust policy
accepted protocol versions
domain admission rules
cross-domain message rules
federation-wide vocabulary governance
root audit policy
```

A Federation does not own every local decision inside every domain.

Rule:

```text
Federation defines interoperability. Domains retain local authority within scope.
```

---

## 2. Fabric Domain

A Domain is a governed operational boundary inside a federation.

Examples:

```text
tenant
organization
business unit
factory
region
air-gapped site
regulated environment
customer environment
```

A Domain owns:

```text
domain identity
domain authority
domain policies
domain validation sets
domain Landscape groups
domain Horizon views
domain commitments
domain audit scope
domain reconciliation scope
```

Rule:

```text
A domain is the first real authority boundary.
```

---

## 3. Fabric Cluster

A Cluster is a group of Fabric Boxes managed together.

It may map to:

```text
Landscape computer group
site group
availability group
update group
factory line
edge group
workload group
```

A Cluster owns:

```text
cluster health
cluster update policy
cluster failure domain
cluster reconciliation backlog
cluster validation set compliance
cluster participant placement
cluster timing profile
```

Rule:

```text
A cluster is a failure and update boundary.
```

---

## 4. Fabric Box

A Box is a physical or virtual node that runs Fabric participants.

In the Canonical-aligned profile, a Box is usually:

```text
Ubuntu Core 26 device
Ubuntu Core 26 + PREEMPT_RT device
Ubuntu Server managed by Landscape
```

A Box owns:

```text
box identity
model assertion
serial assertion
installed snaps
snap revisions
interface connections
health status
recovery status
local traces
local participant inventory
```

Rule:

```text
A box is the sealed execution boundary.
```

---

## 5. Fabric Participant

A Participant is an active component running in or represented by a Box.

Examples:

```text
fabric-kernel
fabric-orchestrator
gap-filler agent
validator
reconciler
projector
policy adapter
identity adapter
trace adapter
store adapter
tool adapter
human operator identity
```

A Participant owns:

```text
participant identity
capabilities
accepted messages
emitted messages
authority boundary
health status
trace behavior
commitments
runtime contract
```

Rule:

```text
A participant is the smallest active Fabric actor.
```

---

## Canonical topology record

```json
{
  "id": "federation:agennext",
  "type": "FabricFederation",
  "domains": ["domain:customer-a"],
  "authority": "authority:federation:agennext",
  "status": "active"
}
```

```json
{
  "id": "domain:customer-a",
  "type": "FabricDomain",
  "federation": "federation:agennext",
  "clusters": ["cluster:customer-a:edge"],
  "authority": "authority:domain:customer-a",
  "status": "active"
}
```

```json
{
  "id": "cluster:customer-a:edge",
  "type": "FabricCluster",
  "domain": "domain:customer-a",
  "boxes": ["box:factory-gateway-001"],
  "profile": "realtime",
  "status": "active"
}
```

```json
{
  "id": "box:factory-gateway-001",
  "type": "FabricBox",
  "cluster": "cluster:customer-a:edge",
  "osProfile": "ubuntu-core-26-realtime",
  "managedBy": "landscape:computer:factory-gateway-001",
  "participants": ["participant:fabric-kernel:factory-gateway-001"],
  "status": "active"
}
```

```json
{
  "id": "participant:fabric-kernel:factory-gateway-001",
  "type": "FabricParticipant",
  "box": "box:factory-gateway-001",
  "snap": "fabric-kernel",
  "capabilities": ["validate", "reconcile", "project", "replay"],
  "status": "active"
}
```

---

## Topology relationships

Canonical predicates:

```text
contains
belongsTo
managedBy
governedBy
ownedBy
operatedBy
runsOn
participatesIn
trusts
federatesWith
reconciles
```

Examples:

```text
federation:agennext contains domain:customer-a
domain:customer-a contains cluster:customer-a:edge
cluster:customer-a:edge contains box:factory-gateway-001
box:factory-gateway-001 contains participant:fabric-kernel
participant:fabric-kernel runsOn box:factory-gateway-001
box:factory-gateway-001 managedBy landscape:computer:factory-gateway-001
```

---

## Landscape mapping

```text
Landscape Account        -> Fabric Federation or Domain
Landscape Computer Group -> Fabric Domain or Cluster
Landscape Computer       -> Fabric Box
Landscape Activity       -> Fabric Event
Landscape Alert          -> Drift Signal
Landscape Compliance     -> Validation Evidence
```

Rule:

```text
Landscape observes and operates the estate. Fabric projects governed state from those observations.
```

---

## Horizon mapping

```text
Horizon Federation View -> Fabric Federation
Horizon Domain View     -> Fabric Domain
Horizon Cluster View    -> Fabric Cluster
Horizon Box View        -> Fabric Box
Horizon Participant View -> Fabric Participant
```

Rule:

```text
Horizon commands through Fabric messages. It must not bypass authority or reconciliation.
```

---

## Ubuntu Core mapping

```text
Ubuntu Core model assertion  -> Box model identity
Ubuntu Core serial assertion -> Box instance identity
Gadget snap                  -> Box hardware contract
Kernel snap                  -> Box kernel boundary
Base snap                    -> Box base runtime
Application snaps            -> Fabric participants
Validation set               -> Approved participant set
Recovery system              -> Box recovery boundary
```

---

## Snapcraft mapping

```text
snapcraft.yaml -> participant package contract
snap            -> participant artifact
channel         -> participant release ring
revision        -> participant version
assertion       -> participant trust statement
```

Rule:

```text
If it participates in Fabric, it must be packageable as a snap or explicitly marked external.
```

---

## Authority boundaries

| Topology level | Authority scope |
|---|---|
| Federation | protocol admission, cross-domain trust, root vocabulary governance |
| Domain | tenant/org policy, compliance, ownership, local governance |
| Cluster | update domain, failure domain, placement, operational grouping |
| Box | execution, snap lifecycle, local health, recovery |
| Participant | capability, message behavior, local commitments |

Rule:

```text
Authority narrows as topology descends.
```

---

## Trust boundaries

```text
Federation trust = can exchange protocol messages
Domain trust     = can share governance and policy context
Cluster trust    = can coordinate operations
Box trust        = can execute sealed participants
Participant trust = can perform declared capabilities
```

Trust is not inherited blindly.
It must be scoped and evidenced.

---

## Failure boundaries

| Failure | Containment |
|---|---|
| Participant failure | Box-level recovery or restart |
| Box failure | Cluster-level reconciliation |
| Cluster failure | Domain-level incident and routing |
| Domain failure | Federation-level isolation |
| Federation conflict | protocol-level suspension or partition |

Rule:

```text
Failure should reconcile at the smallest safe boundary.
```

---

## Update boundaries

| Update target | Boundary |
|---|---|
| participant snap | Box or Cluster |
| validation set | Cluster or Domain |
| policy | Domain |
| vocabulary | Federation or Domain |
| kernel snap | Box, Cluster, or Domain |
| gadget/kernel/base | Box model boundary |

Rule:

```text
Updates must respect authority, validation set, health check, rollback, and reconciliation.
```

---

## Reconciliation boundaries

```text
Participant reconciliation -> local capability or health state
Box reconciliation         -> snap, health, interface, recovery state
Cluster reconciliation     -> box set, update state, drift backlog
Domain reconciliation      -> policy, authority, commitments, compliance
Federation reconciliation  -> cross-domain protocol and trust state
```

Rule:

```text
Reconcile locally unless the failure crosses a boundary.
```

---

## Identity boundaries

Each topology level must have identity.

```text
federation identity
domain identity
cluster identity
box identity
participant identity
```

Rule:

```text
No topology object without identity.
```

---

## Minimal Fabric topology model

```text
Federation
  id
  domains
  authority
  trustPolicy
  status

Domain
  id
  federation
  clusters
  policies
  authority
  status

Cluster
  id
  domain
  boxes
  profile
  updatePolicy
  status

Box
  id
  cluster
  osProfile
  managedBy
  participants
  health
  status

Participant
  id
  box
  snap
  identity
  capabilities
  authorityBoundary
  health
  status
```

## One-line definition

Fabric Federation Model is the canonical topology that binds federation, domain, cluster, box, and participant into governed identity, authority, trust, update, failure, and reconciliation boundaries.
