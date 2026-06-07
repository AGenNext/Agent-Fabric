# Fabric SDK Schema Catalog

This catalog defines the canonical schemas that SDKs and MCP clients must use to validate Fabric payloads before sending them to a Fabric MCP Server or Fabric Kernel.

## Rule

```text
SDKs validate locally first. Fabric Kernel validates authoritatively.
```

Local SDK validation improves developer experience, but it does not replace server-side validation, authority checks, reconciliation, or projection.

## Canonical schemas

```text
schemas/node.schema.json
schemas/relationship.schema.json
schemas/event.schema.json
schemas/trace.schema.json
schemas/intent.schema.json
schemas/commitment-record.schema.json
schemas/authority-chain.schema.json
schemas/gap-fill-proposal.schema.json
schemas/validation-result.schema.json
schemas/reconciliation-record.schema.json
schemas/state.schema.json
schemas/message-envelope.schema.json
```

## SDK validation chain

```text
Construct payload
  -> Validate schema locally
  -> Attach identity, intent, trace
  -> Send MCP tool call
  -> Kernel validates again
  -> Authority check
  -> Reconciliation if state-changing
  -> Projection if accepted
```

## Required SDK behavior

SDKs must:

```text
reject malformed envelopes before send
require identity, intent, trace, and subject
preserve lifecycle state
preserve risk level
preserve evidence references
not auto-activate proposals
not bypass authority or reconciliation
```

## Schema ownership

Schemas are part of the Fabric protocol specification.

SDK implementations may generate types from them, but must not redefine them independently.

## One-line definition

Fabric schemas are the executable structure layer that turns Fabric vocabulary and MCP contracts into locally and server-validatable payloads.
