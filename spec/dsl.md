# Fabric Agent Language (FAL)

**An indentation-style authoring language for the Agent-Fabric meta-model.**

FAL is the human-writable front-end to the graph schema. You declare agents,
teams, tools and their relationships in a concise `.af` file; the compiler
(`tools/afc.py`) lowers it to a [`Graph`](../schema/meta/graph.schema.json) JSON
document that validates against the meta-model. The language carries no
semantics of its own — every construct maps directly onto a node or edge.

Status: Draft · Version 1.0.0 · File extension `.af`

---

## 1. Example

```af
@id research-snapshot
@tenant agennext
@asOf 2026-06-07T12:00:00Z

workspace research
  environment: prod
  purpose: Autonomous research squad

agent researcher-3
  scope: research
  role: executor
  uses: web-search
  invokes: web-search (weight=17, callCount=17)
  runs_on: k8s-prod-eu
  member_of: research-squad
```

Compile:

```bash
python tools/afc.py examples/research.af --validate -o out.json
```

---

## 2. Lexical structure

- **Encoding** is UTF-8 text; significant unit is the line.
- **Comments** start with `#` (whole line) and blank lines are ignored.
- **Indentation** defines nesting. A line with no leading whitespace is a
  *declaration* or *directive*; an indented line is a *property* of the most
  recent declaration. Indent width is not significant (any amount > 0).
- **Directives** are column-0 lines beginning with `@`.

## 3. Header directives

| Directive | Effect |
|---|---|
| `@id <slug>` | Sets the graph id to `af:graph/<slug>` (default `compiled`). |
| `@tenant <name>` | Sets `Graph.tenant`. |
| `@asOf <iso-8601>` | Sets the snapshot watermark `asOf` (default epoch). |
| `@scope <workspace>` | Sets the graph-level `scope` to a declared workspace. |

## 4. Declarations (nodes)

```
<kind> <name>
  <key>: <value>
  ...
```

- `<kind>` is one of the 11 registered kinds (case-insensitive): `agent`,
  `human`, `team`, `tool`, `skill`, `runtime`, `resource`, `policy`, `trace`,
  `identity`, `workspace`.
- `<name>` is a unique identifier matching `[A-Za-z][A-Za-z0-9._-]*`. It becomes
  the node id `af:<kind>/<name>` and is how other declarations refer to it.

### Property resolution

Each `key: value` line is classified, in order:

1. **Relation predicate** — if `KEY.upper()` is a registered predicate (e.g.
   `member_of` → `MEMBER_OF`), the line emits one or more edges (see §5).
2. **Reserved entity field** — `label`, `description`, `scope`, `tenant`,
   `state`, `version`, `tags`. Set directly on the node. `scope` resolves a
   workspace name to its id; `tags` is a comma-separated list.
3. **Attribute** — anything else goes into the node's `attributes` object, with
   light coercion: `true`/`false` → boolean, integers and decimals → numbers,
   otherwise string.

## 5. Relations (edges)

A relation property's value is a comma-separated list of target node names, each
with an optional modifier group:

```
delegates_to: researcher-3 (weight=0.8)
uses: web-search, file-read
invokes: web-search (weight=17, callCount=17)
```

For each target the compiler emits an edge `from` the declaring node `to` the
target, with `relation` set to the predicate. Modifiers: `weight=` sets the
edge `weight`; any other `k=v` goes into the edge's `attributes`. Predicates
marked `symmetric` in the registry (e.g. `communicates_with`) emit
`directed: false`.

The compiler enforces the registry's **domain/range** constraints: a predicate
whose domain or range excludes the endpoint kind is a compile error.

## 6. Compilation guarantees

1. **Schema-valid output.** Compiled graphs validate against
   `graph.schema.json` (run `--validate`).
2. **Registry-bound.** Only registered kinds and predicates compile; unknown
   ones are errors. Domain/range is checked.
3. **Referential integrity.** Every relation target must be a declared node;
   dangling references are errors.
4. **Deterministic.** Node order follows declaration order; edge ids are
   assigned sequentially (`af:rel/N`).

## 7. Scope & limitations

FAL targets node-centric authoring. Out of scope for v1 (author directly in
JSON when needed): edge reification (an edge as the endpoint of another edge),
nested attribute objects, and bitemporal `validFrom`/`validTo` literals on
individual elements. The emitted document is a normal `Graph`, so these can be
layered on afterward.
