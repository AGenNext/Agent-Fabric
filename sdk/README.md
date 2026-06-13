# Agent-Fabric SDKs

The product ships with its **vocabulary** — the node kinds and relation
predicates it speaks — generated for every language from the single source of
truth, `schema/registry/registry.json`. No language hand-maintains the list, so
none can drift.

## Generated bindings

| Language | File | Exposes |
|---|---|---|
| Python | [`python/agent_fabric/vocabulary.py`](python/agent_fabric/vocabulary.py) | `NODE_KINDS`, `RELATION_PREDICATES`, `LIFECYCLE_STATES`, `REGISTRY_VERSION` |
| TypeScript / NestJS | [`typescript/`](typescript/) | full SDK — vocabulary, types, `GraphKernel`, query/ego, and a NestJS module/service (see [its README](typescript/README.md)) |
| Go | [`go/vocabulary.go`](go/vocabulary.go) | `NodeKinds`, `RelationPredicates`, `LifecycleStates`, `RegistryVersion` |
| JSON | [`vocabulary.json`](vocabulary.json) | language-neutral list for any other toolchain |

## Regenerate

```bash
python tools/fab.py vocab --lang python -o sdk/python/agent_fabric/vocabulary.py
python tools/fab.py vocab --lang ts     -o sdk/typescript/vocabulary.ts
python tools/fab.py vocab --lang go     -o sdk/go/vocabulary.go
python tools/fab.py vocab --lang json   -o sdk/vocabulary.json
```

The e2e suite (`fab test`) asserts the committed `vocabulary.json` matches the
registry, so a vocabulary change that isn't regenerated fails CI.

## What an SDK builds on

Every language SDK starts from this generated vocabulary plus the machine-readable
contracts already in the repo, all language-neutral:

- `schema/` — JSON Schema (draft 2020-12) for every element (validate anywhere).
- `schema/context.jsonld` — JSON-LD context for semantic interop.
- `schema/registry/registry.json` — kinds & predicates with domain/range.

A graph is plain JSON, an event is plain JSON — so an SDK is a thin typed wrapper
over data, in keeping with the model: storage + calculation, no runtime to embed.
