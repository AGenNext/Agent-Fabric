# Ubuntu Horizon Panel for Agent-Fabric

Ubuntu Horizon is the visual command surface for Agent-Fabric operations.

Landscape manages the Ubuntu estate.
Horizon presents the operational horizon: domains, clusters, boxes, participants, drift, authority, reconciliation, and projected state.

## Definition

Ubuntu Horizon Panel is the Fabric command surface that gives operators a visual view of the operational landscape and the projected horizon of Fabric state.

```text
Landscape = fleet operations panel
Horizon   = Fabric command horizon
```

Horizon should not replace Landscape.
Horizon sits above Landscape and Fabric state projections.

## Core rule

```text
Landscape operates machines.
Horizon visualizes and commands Fabric state.
Fabric remains the source of governed truth.
```

## Role in the stack

```text
Human Operator
  -> Ubuntu Horizon Panel
  -> Fabric Query / Command API
  -> Fabric Orchestrator
  -> Rust Fabric Kernel
  -> Fabric State Projection
  -> Landscape / Ubuntu Core / Snapcraft / Participants
```

## Horizon responsibilities

Horizon should display and operate:

```text
Fabric Federation
Fabric Domains
Fabric Clusters
Fabric Boxes
Fabric Participants
Snap revisions
Validation sets
Authority chains
Open proposals
Active drift
Reconciliation records
Commitments
Timing violations
Health posture
Projected state
```

Horizon should not own:

```text
stable state
reconciliation truth
authority bypass
identity source of truth
policy source of truth
Landscape fleet operations
snap update mechanics
kernel correctness rules
```

## Landscape vs Horizon

| Layer | Responsibility |
|---|---|
| Landscape | Ubuntu fleet inventory, patching, package status, compliance, machine operations |
| Horizon | Fabric topology, drift, authority, reconciliation, commitments, projected state |
| Fabric Kernel | Validity, invariants, reconciliation correctness, projection correctness |
| Fabric Orchestrator | APIs, controllers, adapters, message routing |
| Ubuntu Core | sealed execution substrate |
| Snapcraft | packaging compiler |

## Horizon topology model

```text
Fabric Federation
└── Fabric Domain
    └── Fabric Cluster
        └── Fabric Box
            └── Fabric Participant
```

Landscape maps into this model:

```text
Landscape Account        -> Fabric Federation
Landscape Computer Group -> Fabric Domain or Cluster
Landscape Computer       -> Fabric Box
Snap                     -> Fabric Participant
```

## Horizon views

### 1. Federation view

Shows all domains, clusters, and box health.

```text
federation health
number of domains
active clusters
boxes online/offline
critical drift
pending approvals
failed reconciliations
```

### 2. Domain view

Shows a governed operational boundary.

```text
tenant/domain identity
policies
validation sets
Landscape groups
authority owners
active commitments
risk posture
```

### 3. Cluster view

Shows grouped Fabric Boxes.

```text
cluster health
box count
snap revision consistency
update compliance
active drift
reconciliation backlog
```

### 4. Box view

Shows one Fabric Box.

```text
Ubuntu profile
standard / edge / realtime
installed snaps
snap revisions
interfaces
health
trace status
Landscape status
PREEMPT_RT timing status
```

### 5. Participant view

Shows an agent, tool, runtime, adapter, or controller.

```text
identity
capabilities
accepted messages
emitted messages
authority boundary
health
last trace
current commitments
open challenges
```

### 6. Drift view

Shows active gaps and drift.

```text
missing identity
missing relationship
missing evidence
missing contract
runtime drift
authority drift
policy drift
trust drift
timing drift
orphan nodes
```

### 7. Reconciliation view

Shows reconciliation loops.

```text
proposal
validation result
authority chain
policy decision
reconciliation record
resulting state
rollback/supersession
```

### 8. Authority view

Shows who can decide what.

```text
observer
proposer
validator
reviewer
approver
reconciler
state projector
accountable authority
```

### 9. Commitment view

Shows promises and obligations.

```text
debtor
creditor
condition
obligation
due time
fulfillment
violation
release
expiry
```

### 10. Temporal horizon view

Shows past, current, and future state.

```text
observed state
recorded state
current projection
pending future effective changes
expiring commitments
upcoming validation set changes
scheduled snap refreshes
```

## Command model

Horizon sends Fabric commands, not direct hidden operations.

Allowed commands:

```text
Query
Challenge
Approve
Reject
RequestReconciliation
RequestEvidence
RequestAuthority
RequestRollback
RequestSupersession
```

Risky commands require authority.

```text
Horizon command
  -> Fabric message
  -> identity check
  -> validation
  -> authority chain
  -> reconciliation
  -> projected state
```

## Operator safety

Horizon must make unsafe state visible.

It should highlight:

```text
unapproved critical proposals
expired authority
missing evidence
failed validation
stale traces
Landscape compliance failure
snap validation set mismatch
PREEMPT_RT deadline misses
unreconciled drift
orphan boxes
```

## Integration with Landscape

Horizon consumes Landscape as an observation and operations source.

Minimal integration:

```text
machine inventory
machine groups
health status
update status
compliance signals
script/action history
```

Fabric transformation:

```text
Landscape observation
  -> Fabric Event
  -> Trace
  -> Drift classification
  -> Reconciliation
  -> Horizon projection
```

## Integration with Ubuntu Core and Snapcraft

Horizon should show:

```text
model assertion
serial assertion
installed snaps
snap revisions
channels
validation set status
interface connections
refresh history
rollback history
recovery state
```

## Integration with PREEMPT_RT

For real-time Fabric Boxes, Horizon should show:

```text
profile = realtime
deadline misses
priority violations
health loop latency
trace emission latency
reconciliation loop latency
real-time drift status
```

## Boundary rule

```text
Horizon sees and commands.
Fabric decides and records.
Landscape operates the machine.
Ubuntu Core enforces the box.
Snapcraft packages the participant.
```

## One-line definition

Ubuntu Horizon is the Fabric command surface that lets operators see the landscape, understand the horizon, and act through governed Fabric messages without bypassing state, authority, or reconciliation.
