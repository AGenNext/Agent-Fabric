# tools/

Pure standard library — no install, no packages, no services.

## fab — single entry point

`fab.py` is one command with a subcommand per stage; it dispatches to the same
module mains the individual scripts use.

```bash
python tools/fab.py compile EXAMPLE.af [--validate]   # == afc
python tools/fab.py query   GRAPH.json "QUERY"        # == bql
python tools/fab.py sim     BASE.json EVENTS.json     # == sim
python tools/fab.py vocab   [--lang python|ts|go|json]  # print/export the vocabulary
python tools/fab.py grade   GRAPH.json [--json]       # score model quality (not just correctness)
python tools/fab.py test                              # run tests/e2e.py
```

`fab vocab` prints the shipped vocabulary (kinds + predicates) from the registry,
or with `--lang` emits language bindings — the source for the generated
[`sdk/`](../sdk/) (Python, TypeScript, Go, JSON). The e2e suite guards against
drift between the SDKs and the registry.

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

**Footprint:** both tools run on a stock Python interpreter — no third-party
packages, no GPU, no server. `--validate` uses `jsonschema` for full JSON Schema
validation *if it is installed*, and otherwise falls back automatically to a
built-in zero-dependency structural check (registered kinds/predicates, required
fields, referential integrity). The mode is printed, e.g.
`afc: valid [builtin (zero-dependency)] — 10 nodes, 12 edges`.

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

# query EMULATED state: overlay an event delta through the kernel, no subgraph built
python tools/bql.py schema/examples/graph.example.json "agent" \
  --events schema/examples/event-stream.example.json
```

Exit codes: `0` ok · `2` query syntax error.

## kernel — emulation overlay (`kernel.py`)

`GraphKernel(base, events, until)` overlays an event delta on a base graph and
presents the emulated state on read — storage + calculation, no materialized
subgraph. Shared by `sim` and `bql --events`. Not a CLI; imported by the tools.
See [`../spec/simulation.md`](../spec/simulation.md).

## sim — event-fold simulator

`sim.py` folds a `GraphEvent` stream onto a base graph to project ("rehearse")
the resulting state without committing anything. See
[`../spec/simulation.md`](../spec/simulation.md).

```bash
# project the outcome of an event stream (nothing is mutated except -o output)
python tools/sim.py schema/examples/graph.example.json \
                    schema/examples/event-stream.example.json -o projected.json

# time-travel: fold only events up to sequence 44
python tools/sim.py base.json events.json --at 44 --summary

# rebuild/sustainability: emit the genesis log that reconstructs a graph from empty
python tools/sim.py examples/research.graph.json --explode -o genesis.json
echo '{"nodes":[],"edges":[]}' > empty.json
python tools/sim.py empty.json genesis.json -o rebuilt.json   # == research.graph.json
```
