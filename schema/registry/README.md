# Registries

Everything the system speaks is declared in a registry — the single source of
truth. The tools and SDKs read their vocabulary from here, so nothing drifts.

| Registry | File | Declares | Mirrors / referenced by |
|---|---|---|---|
| **Types** | [`registry.json`](registry.json) | node kinds + relation predicates (domain/range, cardinality, flags) | `nodes/*.schema.json`, `meta/relation.schema.json`, `afc`, `bql` |
| **States** | [`states.json`](states.json) | the lifecycle state vocabulary | `meta/state.schema.json` (the validating schema) |

Surface any registry with `fab vocab` (human listing) or `fab vocab --lang …`
(generated bindings → [`../../sdk/`](../../sdk/)). The e2e suite asserts the
registries stay in sync with their schemas and with the generated SDKs.

To extend: add the entry here, add/adjust the referenced schema, bump the
registry `version`, regenerate the SDKs, and run `fab test`.
