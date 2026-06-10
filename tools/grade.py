#!/usr/bin/env python3
"""grade — score the *quality* of an Agent-Fabric model, not just its correctness.

Validation proves a graph is correct (schema-valid, registry-bound, referential
integrity). That is table stakes. This grader raises the bar to quality: a
rubric of verifiers — identity coverage, runtime placement, workspace scoping,
governance, connectivity, provenance — each scored and weighted into 0-100 with
a deploy-readiness verdict. The question is not "is it valid?" but "would you
actually ship this model?"

    grade.py GRAPH.json [--json]

Pure standard library.
"""
import argparse
import json
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fabriclib import load_registry, read_json


def _index(graph):
    nodes = {n["id"]: n for n in graph.get("nodes", [])}
    out_pred = defaultdict(set)   # (node_id) -> set of outgoing predicates
    degree = defaultdict(int)
    for e in graph.get("edges", []):
        out_pred[e["from"]].add(e["relation"])
        degree[e["from"]] += 1
        degree[e["to"]] += 1
    return nodes, out_pred, degree


def _ratio(hits, total):
    return 1.0 if total == 0 else hits / total


def grade(graph):
    """Return (score 0-100, [criteria]). Each criterion: name, weight, score,
    findings (sample offenders)."""
    nodes, out_pred, degree = _index(graph)
    kinds, predicates = load_registry()
    valid_kinds = set(kinds.values())
    by_kind = defaultdict(list)
    for n in nodes.values():
        by_kind[n.get("kind")].append(n)
    edges = graph.get("edges", [])
    criteria = []

    def add(name, weight, hits, total, offenders):
        criteria.append({
            "name": name, "weight": weight, "score": round(_ratio(hits, total), 3),
            "detail": f"{hits}/{total}", "findings": offenders[:5],
        })

    # 1. Correctness (table stakes): registered kinds/predicates + referential
    # integrity. Edge ids are valid endpoints too (edge reification).
    ids = set(nodes) | {e["id"] for e in edges}
    bad = 0
    for n in nodes.values():
        if n.get("kind") not in valid_kinds:
            bad += 1
    for e in edges:
        if e.get("relation", "").lower() not in predicates or \
                e.get("from") not in ids or e.get("to") not in ids:
            bad += 1
    total_elems = len(nodes) + len(edges)
    add("correctness", 30, total_elems - bad, total_elems,
        ["unregistered or dangling elements present"] if bad else [])

    # 2. Identity coverage: agents bound to an identity.
    agents = by_kind.get("Agent", [])
    no_id = [a["id"] for a in agents
             if not ({"HAS_IDENTITY", "ASSUMES_IDENTITY"} & out_pred[a["id"]])]
    add("identity-coverage", 15, len(agents) - len(no_id), len(agents),
        [f"{i} has no identity" for i in no_id])

    # 3. Runtime placement: agents that run on a runtime.
    no_rt = [a["id"] for a in agents if "RUNS_ON" not in out_pred[a["id"]]]
    add("runtime-placement", 10, len(agents) - len(no_rt), len(agents),
        [f"{i} runs on no runtime" for i in no_rt])

    # 4. Workspace scoping: non-workspace nodes scoped (field or edge).
    scoped_targets = {"SCOPED_TO", "DEPLOYED_IN", "RUNS_ON"}
    non_ws = [n for n in nodes.values() if n.get("kind") != "Workspace"]
    unscoped = [n["id"] for n in non_ws
                if not n.get("scope") and not (scoped_targets & out_pred[n["id"]])]
    add("workspace-scoping", 10, len(non_ws) - len(unscoped), len(non_ws),
        [f"{i} is unscoped" for i in unscoped])

    # 5. Governance: tools & resources governed by a policy.
    governed_kinds = by_kind.get("Tool", []) + by_kind.get("Resource", [])
    ungoverned = [n["id"] for n in governed_kinds if "GOVERNED_BY" not in out_pred[n["id"]]]
    add("governance", 15, len(governed_kinds) - len(ungoverned), len(governed_kinds),
        [f"{i} is ungoverned" for i in ungoverned])

    # 6. Connectivity / scope discipline: no orphan nodes.
    orphans = [nid for nid in nodes if degree[nid] == 0]
    add("connectivity", 10, len(nodes) - len(orphans), len(nodes),
        [f"{i} is orphaned" for i in orphans])

    # 7. Provenance: elements carrying provenance.
    elems = list(nodes.values()) + edges
    with_prov = sum(1 for x in elems if x.get("provenance"))
    add("provenance", 10, with_prov, len(elems),
        ["no provenance on most elements"] if with_prov < len(elems) else [])

    total_w = sum(c["weight"] for c in criteria)
    score = round(sum(c["weight"] * c["score"] for c in criteria) / total_w * 100, 1)
    return score, criteria


def verdict(score):
    if score >= 85:
        return "ship-ready"
    if score >= 70:
        return "needs review"
    return "not ready"


def main(argv=None):
    ap = argparse.ArgumentParser(description="Grade the quality of an Agent-Fabric model.")
    ap.add_argument("graph", help="graph JSON file")
    ap.add_argument("--json", action="store_true", help="emit the report as JSON")
    args = ap.parse_args(argv)

    graph = read_json(args.graph)
    score, criteria = grade(graph)

    if args.json:
        print(json.dumps({"score": score, "verdict": verdict(score),
                          "criteria": criteria}, indent=2))
        return 0

    print(f"Quality {score}/100  —  {verdict(score)}\n")
    for c in criteria:
        bar = "#" * int(c["score"] * 10) + "." * (10 - int(c["score"] * 10))
        print(f"  {c['name']:<18} [{bar}] {c['detail']:>7}  (w{c['weight']})")
        for f in c["findings"]:
            print(f"      - {f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
