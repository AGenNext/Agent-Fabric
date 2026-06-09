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
