# Agent Fabric

Agent Fabric is the assertion-native operating model for AGenNext.

This repository defines the canonical primitives required to represent, verify, project, and reconcile governed reality across agents, services, devices, workspaces, organizations, and digital twins.

## Fabric Core

Fabric reduces governed systems to seven canonical records:

1. `Entity`
2. `Relationship`
3. `Assertion`
4. `Observation`
5. `Projection`
6. `Drift`
7. `Reconciliation`

Everything else is an extension of these records.

## Core Principle

```text
Identity establishes existence.
Relationships establish context.
Assertions establish truth.
Observations establish reality.
Projections establish visibility.
Drift establishes difference.
Reconciliation establishes order.
```

## Repository Layout

```text
specs/fabric-core-v1.md        Normative Fabric Core specification
schemas/v1/*.schema.json       JSON Schemas for canonical records
examples/v1/*.json             Valid example records
.github/workflows/validate.yml Schema validation workflow
```

## Fabric Core Conformance

A Fabric-compliant implementation MUST support:

- identity resolution
- assertion storage
- signature verification
- schema validation
- projection generation
- drift detection
- reconciliation recording

## Status

Draft v1.0.
