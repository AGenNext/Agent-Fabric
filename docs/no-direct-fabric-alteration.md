# No Direct Fabric Alteration

No one alters the Fabric directly.

The Fabric is not edited by force, shortcuts, hidden side paths, tunnels, direct database writes, unmanaged agents, or privileged bypasses.

## Core rule

```text
No direct alteration.
Only proposed, validated, authorized, reconciled, projected change.
```

## Canonical change path

```text
Observe
  -> Propose
  -> Validate
  -> Authorize
  -> Reconcile
  -> Project
  -> Publish current state
```

## What is forbidden

```text
direct state mutation
hidden side-channel updates
unreviewed graph edits
unmanaged agent writes
operator bypass
manual database edits
runtime patching outside authority
mesh side paths for state change
release promotion without gate
artifact publication without provenance
```

## What is allowed

```text
observation
proposal
challenge
reconciliation request
recovery request
evidence submission
human approval
validated operator action
projected state publication
```

## Responsibility split

```text
Human
  = accountable approval

Fabric Kernel
  = truth boundary

Runtime
  = executes governed state transitions

Graph
  = plans dependency order

Kubernetes
  = heals infrastructure

Mesh
  = transports traffic

Cortex
  = observes critical path

Agents
  = observe and propose at the edge
```

## Freeze rule

If trust is uncertain:

```text
Freeze transitions.
Preserve evidence.
Destroy nothing.
Reconcile before resuming.
```

## One-line definition

No direct Fabric alteration means every Fabric change must move through observation, proposal, validation, authority, reconciliation, and projection before it becomes trusted state.
