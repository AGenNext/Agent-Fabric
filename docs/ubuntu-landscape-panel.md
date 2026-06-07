# Ubuntu Landscape Panel for Agent-Fabric

Ubuntu Landscape is the fleet operations panel for Fabric Boxes.

It manages Ubuntu machines, packages, security updates, compliance, inventory, scripts, roles, and fleet health. In Agent-Fabric, Landscape should be treated as an operator tool used by the Fabric Orchestrator and human operators, not as the Fabric authority model itself.

## Definition

Ubuntu Landscape Panel is the Ubuntu fleet-management surface for observing, maintaining, patching, auditing, grouping, and operating Fabric Boxes.

```text
Ubuntu Landscape
  -> fleet inventory
  -> update and patch visibility
  -> compliance visibility
  -> machine grouping
  -> scripts and operations
  -> health/status panel
  -> Fabric events
  -> Fabric reconciliation
```

## Core rule

```text
Landscape operates the Ubuntu fleet.
Fabric governs the operational state.
```

Landscape can observe and operate Fabric Boxes.
Fabric records, validates, authorizes, reconciles, and projects state.

## Role in the stack

```text
Human Operator
  -> Ubuntu Landscape Panel
  -> Ubuntu Core / Ubuntu Server Fabric Boxes
  -> Snapcraft-built Fabric participants
  -> Fabric Orchestrator
  -> Fabric Kernel
  -> Fabric State
```

## Landscape responsibilities

Landscape should be used for:

```text
fleet inventory
machine grouping
package and snap visibility
security update visibility
patch operations
compliance reporting
script execution
machine health checks
access-aware operations
estate monitoring
lifecycle operations
```

Landscape should not be used as:

```text
Fabric Protocol source of truth
Fabric AuthorityChain replacement
Fabric Reconciliation engine
Fabric StateProjection engine
Agent runtime
Policy engine
Identity provider
```

## Fabric mapping

| Landscape concept | Fabric concept |
|---|---|
| Computer / machine | Fabric Box |
| Computer group | Fabric Cluster or Domain |
| Package status | Component state |
| Snap status | Participant snap state |
| Update profile | Desired maintenance state |
| Script execution | Operator action event |
| Alert | Fabric event or drift signal |
| Compliance report | Evidence for validation/reconciliation |
| Access role | Operator authority input |
| Activity log | Trace/evidence source |

## Fabric Box inventory

Each Landscape-managed machine should map to a Fabric node.

```json
{
  "id": "box:factory-gateway-001",
  "type": "FabricBox",
  "managedBy": "landscape:account:agennext",
  "os": "Ubuntu Core 26",
  "profile": "realtime",
  "status": "active"
}
```

## Landscape as observation source

Landscape observations should enter Fabric as events.

Examples:

```text
MachineRegistered
MachineOffline
SecurityUpdateAvailable
PackageOutOfDate
SnapRevisionChanged
ComplianceFailed
ScriptExecuted
RebootRequired
HealthDegraded
```

These events feed:

```text
Trace Store
Event Store
Drift Detector
Reconciliation Engine
Projection Engine
```

## Landscape as operator panel

Landscape gives humans a trusted panel to act on machines.

Fabric must still record:

```text
who acted
what action was requested
which machine was affected
why it was done
which authority allowed it
what evidence was produced
what state changed
```

## Operator action flow

```text
Operator action in Landscape
  -> Landscape activity/event
  -> Fabric Observe message
  -> Trace attached
  -> AuthorityChain linked
  -> Reconciliation required if state changed
  -> Project Fabric Box state
```

## Patch and update flow

```text
Landscape detects update
  -> Fabric records UpdateAvailable
  -> Policy checks maintenance window
  -> AuthorityChain approves update
  -> Landscape applies update
  -> Fabric records result
  -> Health check runs
  -> Reconciliation projects updated box state
```

## Snap refresh flow

```text
Snap revision available
  -> Landscape/Fabric observes snap state
  -> Validation set checked
  -> AuthorityChain approves refresh
  -> snap refresh executes
  -> health check passes or fails
  -> rollback if needed
  -> Fabric reconciles state
```

## Compliance flow

```text
Landscape compliance signal
  -> Fabric ComplianceEvent
  -> Validator checks policy impact
  -> DriftDetector classifies drift
  -> Reconciler decides repair, quarantine, or escalation
  -> Projected state updates
```

## Relationship to Ubuntu Core

Ubuntu Core provides sealed device behavior.
Snapcraft packages Fabric participants.
Landscape monitors and operates the fleet.
Fabric governs the state model above those operations.

```text
Snapcraft builds.
Ubuntu Core runs.
Landscape operates.
Fabric governs.
```

## Relationship to PREEMPT_RT

For real-time Fabric Boxes, Landscape can observe and operate the node, but real-time scheduling policy remains part of the Fabric real-time profile and host configuration.

Timing violations should still become Fabric drift events:

```text
DeadlineMissed
PriorityViolation
RealtimeHealthDegraded
```

## Panel boundaries

Landscape Panel must not create hidden control paths.

Rule:

```text
Every Landscape-triggered action that changes Fabric state must emit a Fabric event and reconciliation record.
```

## Minimal integration

First integration should be simple:

```text
Landscape machine inventory
Landscape health/status
Landscape update/compliance signals
Fabric events from Landscape observations
Fabric projected state for boxes
```

Later integration:

```text
Landscape API adapter
Fabric Orchestrator plugin
Landscape-backed operator action records
Landscape compliance evidence ingestion
Landscape grouping -> Fabric cluster/domain mapping
```

## One-line definition

Ubuntu Landscape is the fleet operations panel for Fabric Boxes; Agent-Fabric turns Landscape observations and actions into governed, traceable, reconciled operational state.
