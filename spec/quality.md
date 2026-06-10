# Model quality — from correctness to quality

*Validation proves a model is **correct**. Grading asks whether it is **good**.*

Status: Draft · Version 1.0.0 · Tool: [`tools/grade.py`](../tools/grade.py)
(`fab grade`)

---

## 1. Why

Schema validation is table stakes: it proves a graph is well-formed,
registry-bound, and referentially intact. But a model can be perfectly correct
and still be a poor model — agents with no identity, tools with no governing
policy, orphan nodes, no provenance. The question worth asking is not "is it
valid?" but **"would you actually ship this model?"**

This mirrors the shift FrontierCode made for code — from *correctness* to
*mergeability/quality*, graded by an ensemble of verifiers and rubrics rather
than a single pass/fail. Agent-Fabric applies the same idea to the model itself.

## 2. The rubric

`grade(graph)` runs a weighted ensemble of verifiers and returns a score in
0–100 plus a verdict (`ship-ready` ≥ 85, `needs review` ≥ 70, else `not ready`):

| Criterion | Weight | Asks |
|---|---|---|
| **correctness** | 30 | registered kinds/predicates + referential integrity (edge reification allowed) |
| **identity-coverage** | 15 | does every Agent have an identity (`HAS_IDENTITY`/`ASSUMES_IDENTITY`)? |
| **runtime-placement** | 10 | does every Agent `RUNS_ON` a runtime? |
| **workspace-scoping** | 10 | is every non-workspace node scoped (field or `SCOPED_TO`/`DEPLOYED_IN`/`RUNS_ON`)? |
| **governance** | 15 | are tools & resources `GOVERNED_BY` a policy? |
| **connectivity** | 10 | are there orphan nodes (degree 0)? |
| **provenance** | 10 | do elements carry provenance? |

Each verifier reports a fraction (`hits/total`) and sample offenders, so a low
score points at exactly what to fix.

## 3. Correct ≠ good

The FAL-authored `examples/research.graph.json` is **100% correct** yet grades
**~64/100 — "not ready"**: the orchestrator has no identity and no runtime, a
resource is ungoverned, and nothing carries provenance. The model validates; it
is not yet good. That gap is the whole point.

## 4. Usage

```bash
fab grade GRAPH.json            # human-readable rubric report + verdict
fab grade GRAPH.json --json     # machine-readable {score, verdict, criteria}
```

Compose with emulation to grade a *projected* model before committing it:
`fab sim base.json events.json -o projected.json && fab grade projected.json`.

## 5. Scope

The rubric is intentionally registry/graph-driven and heuristic; weights and
criteria are a starting baseline. Future work: per-domain rubrics, LLM-judge
verifiers for semantic quality, and grading deltas (did this change improve or
regress the model?).
