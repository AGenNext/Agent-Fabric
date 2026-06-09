# tools/

## afc — Fabric Agent Language compiler

`afc.py` compiles an indentation-style `.af` source (see
[`../spec/dsl.md`](../spec/dsl.md)) into an Agent-Fabric `Graph` JSON document
that validates against the meta-model.

```bash
# Compile to stdout
python tools/afc.py examples/research.af

# Compile to a file and validate against graph.schema.json
python tools/afc.py examples/research.af -o examples/research.graph.json --validate
```

Exit codes: `0` success · `2` FAL syntax/semantic error · `1` schema-invalid
output (only with `--validate`).

`--validate` requires `jsonschema` and `referencing` (`pip install jsonschema`).
The compiler reads the relation/kind vocabulary from
`schema/registry/registry.json`, so adding a kind or predicate there
immediately makes it usable in `.af` files.

## bql — Blockquote Query Language evaluator

`bql.py` queries a compiled `Graph` JSON by traversing typed edges, using `>`
(and `<` for reverse) as the hop operator. See [`../spec/bql.md`](../spec/bql.md).

```bash
# agents the orchestrator delegates to
python tools/bql.py examples/research.graph.json \
  "agent:orchestrator-7 > delegates_to > agent"

# multi-hop with attribute filters
python tools/bql.py examples/research.graph.json \
  "agent:orchestrator-7 > delegates_to > agent[status=busy] > runs_on > runtime[platform=kubernetes]"

# full node objects
python tools/bql.py examples/research.graph.json "agent" --json
```

Exit codes: `0` ok · `2` query syntax error.
