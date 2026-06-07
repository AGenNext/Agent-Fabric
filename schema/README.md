# Agent-Fabric Schema

Machine-readable definition of the Agent-Fabric meta-model — the multi-model,
real-time graph meta-model for autonomous agents. See the full specification in
[`../spec/meta-model.md`](../spec/meta-model.md).

## Layout

```
schema/
├── context.jsonld              JSON-LD context (semantic vocabulary + aliases)
├── meta/                       M1 model layer + M2 meta layer
│   ├── entity.schema.json        base node (vertex)
│   ├── relation.schema.json      base edge
│   ├── graph.schema.json         materialized snapshot + watermark
│   ├── event.schema.json         GraphEvent — real-time change unit
│   └── type-registry.schema.json the meta-model (schema of schemas)
├── nodes/                      M1 concrete node kinds (11)
│   ├── agent.schema.json   human.schema.json   team.schema.json
│   ├── tool.schema.json    skill.schema.json   runtime.schema.json
│   ├── resource.schema.json policy.schema.json trace.schema.json
│   ├── identity.schema.json workspace.schema.json
├── registry/
│   └── registry.json           populated node-kind & relation-type registry
└── examples/
    ├── graph.example.json        sample snapshot
    └── event-stream.example.json sample event stream
```

## Conventions

- **JSON Schema draft 2020-12.** `$id`s are absolute IRIs under
  `https://schema.agennext.dev/agent-fabric/`; `$ref`s use those IRIs, so a
  validator needs all files registered in one resource set.
- **JSON-LD.** Documents may set `"@context"` to `context.jsonld` to gain stable
  semantic meaning (`id → @id`, `kind → @type`, predicate IRIs, etc.).
- **IRIs.** Element ids use the `af:` prefix (e.g. `af:agent/orchestrator-7`) or
  any resolvable URN.

## Validating (example with `ajv`)

```bash
npm i -g ajv-cli ajv-formats
ajv validate -c ajv-formats \
  -r "schema/meta/*.json" -r "schema/nodes/*.json" \
  -s schema/meta/graph.schema.json \
  -d schema/examples/graph.example.json
```

## Extending

Add a node kind or predicate in `registry/registry.json` (M2). For a new node
kind, also add a `nodes/<kind>.schema.json` that `$ref`s `meta/entity.schema.json`
and pins `kind` to a `const`. Bump the registry `version`. Never hard-code kinds
or predicates outside the registry — that is what makes this a meta-model.
```
