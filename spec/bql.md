# BQL — Blockquote Query Language

**A path-traversal query language for the Agent-Fabric graph.**

BQL reads a compiled [`Graph`](../schema/meta/graph.schema.json) and returns the
nodes reached by following typed edges. It uses `>` — markdown's blockquote
marker — as the hop operator, so a query reads like a quoted path through the
graph. `<` traverses the same edge in reverse. The evaluator is
[`tools/bql.py`](../tools/bql.py).

Status: Draft · Version 1.0.0 · File extension `.bql`

---

## 1. Example

```bql
# agents an orchestrator delegates to, that run on a k8s runtime
agent:orchestrator-7
  > delegates_to > agent[status=busy]
  > runs_on > runtime[platform=kubernetes]
```

```bash
python tools/bql.py examples/research.graph.json \
  "agent:orchestrator-7 > delegates_to > agent > runs_on > runtime"
```

Whitespace and newlines are insignificant, so a query may span several indented
lines as above. `#` starts a comment to end of line.

## 2. Grammar

```
query    := selector hop*
hop      := ('>' | '<') predicate ('>' | '<') selector
selector := ('*' | kind | kind ':' name) filter*
filter   := '[' cond (',' cond)* ']'
cond     := key ('=' | '!=') value
```

- **`>`** is a forward hop (follow edges where the current node is `from`);
  **`<`** is a reverse hop (current node is `to`). The marker before and after
  the predicate share the hop's direction.
- **`predicate`** is a lowercased relation name (e.g. `delegates_to`,
  `runs_on`) or `*` to match any relation.

## 3. Selectors

A selector chooses nodes:

| Form | Selects |
|---|---|
| `*` | any node |
| `agent` | all nodes of kind Agent (kind is case-insensitive) |
| `agent:orchestrator-7` | the node with id `af:agent/orchestrator-7` |
| `runtime[platform=kubernetes]` | Runtimes whose `platform` attribute is `kubernetes` |
| `agent[status=busy][role!=critic]` | conjunction of filters |

Filter keys resolve against the node's top-level fields first (`kind`, `state`,
`scope`, `label`, …) then its `attributes`. Values are compared with light
coercion (numbers, booleans) and fall back to string equality. Operators are
`=` and `!=`.

## 4. Evaluation

1. The **start selector** seeds the working set with all matching nodes.
2. Each **hop** replaces the working set with the de-duplicated neighbors that
   (a) are reachable by an edge of the given predicate in the given direction
   and (b) satisfy the hop's target selector.
3. The result is the final working set (nodes). Order follows first discovery.

Because hops compose, a query expresses a path pattern; multi-hop queries are
the intersection of each stage's reachability.

## 5. Ego-view

Every party is the centre of its own view. `--ego NODE [--radius N]` returns the
**ego-network** — the centre node plus every node within `N` hops in any
direction (default radius 1). No QUERY is needed, and nothing is materialized;
it is a neighborhood walk over the same edge indexes.

```bash
bql.py GRAPH.json --ego af:agent/researcher-3 --radius 2
```

Combine with `--events` to see a party's world in the emulated state.

## 6. CLI

```bash
bql.py GRAPH.json "QUERY"                    # tab-separated id / kind / label
bql.py GRAPH.json -f query.bql               # read query from a file
bql.py GRAPH.json "QUERY" --json             # emit full node objects
bql.py GRAPH.json --ego NODE [--radius N]    # ego-network around a node
bql.py GRAPH.json "QUERY" --events EV [--at SEQ]  # query emulated state
```

Exit codes: `0` ok · `2` query syntax/center error.

## 6. Scope & limitations

v1 returns the set of end nodes. Out of scope for now: returning whole paths,
edge projection, aggregation, valid-time/`asOf` filtering, and variable-length
(`*N..M`) hops. The graph is plain JSON, so these can be added without changing
the data model.
