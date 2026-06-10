#!/usr/bin/env python3
"""End-to-end conformance test for the Agent-Fabric toolchain.

Pure standard library — no test framework, no extra software required. Exercises
the whole chain on the committed examples and asserts conformance:

    author (afc)  ->  query (bql)  ->  emulate (kernel/sim)  ->  validate

Run:  python tests/e2e.py        (exit 0 = all pass, 1 = failures)
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import afc                       # noqa: E402
import bql                       # noqa: E402
from kernel import GraphKernel, explode   # noqa: E402

checks = []


def check(name, cond):
    checks.append((name, bool(cond)))
    print(f"  {'PASS' if cond else 'FAIL'}  {name}")


def read(rel):
    with open(os.path.join(ROOT, rel)) as fh:
        return json.load(fh)


def src(rel):
    with open(os.path.join(ROOT, rel)) as fh:
        return fh.read()


def q(graph, query):
    return [n["id"] for n in bql.evaluate(graph, query)]


print("== authoring (afc) ==")
graph = afc.compile_source(src("examples/research.af"))
check("research.af compiles to the committed graph", graph == read("examples/research.graph.json"))
errs, mode = afc.validate_graph(graph)
check(f"compiled graph validates [{mode}]", not errs)
check("expected size (10 nodes / 12 edges)", len(graph["nodes"]) == 10 and len(graph["edges"]) == 12)
nsids = {n["id"] for n in afc.compile_source(src("examples/namespaced.af"))["nodes"]}
check("domain namespacing produces af:<domain>/<kind>/<name>",
      "af:acme/agent/invoice-agent" in nsids)

print("== querying (bql) ==")
check("forward hop", q(graph, "agent:orchestrator-7 > delegates_to > agent")
      == ["af:agent/researcher-3"])
check("multi-hop with attribute filters",
      q(graph, "agent:orchestrator-7 > delegates_to > agent[status=busy] "
               "> runs_on > runtime[platform=kubernetes]") == ["af:runtime/k8s-prod-eu"])
check("reverse hop", q(graph, "tool:web-search < uses < agent") == ["af:agent/researcher-3"])
check("wildcard predicate", q(graph, "policy:web-readonly > * > tool") == ["af:tool/web-search"])

print("== emulation (kernel) ==")
base = read("schema/examples/graph.example.json")
events = read("schema/examples/event-stream.example.json")
proj, _ = GraphKernel(base, events).view()
pnodes = {n["id"] for n in proj["nodes"]}
pedges = {e["id"] for e in proj["edges"]}
check("delete removes a node", "af:agent/researcher-3" not in pnodes)
check("upsert adds an edge", "af:rel/12" in pedges)
check("invalidate sets validTo",
      any(e["id"] == "af:rel/3" and e.get("validTo") for e in proj["edges"]))
check("watermark records last sequence", proj["watermark"].get("sequence") == 46)
proj44, _ = GraphKernel(base, events, until=44).view()
check("time-travel @44 keeps the node",
      "af:agent/researcher-3" in {n["id"] for n in proj44["nodes"]})
check("bql over emulated state (no subgraph materialized)",
      q(proj, "agent") == ["af:agent/orchestrator-7"])

print("== rebuild / sustainability ==")
genesis = explode(graph)
rebuilt, _ = GraphKernel({"nodes": [], "edges": []}, genesis).view()
check("graph rebuilds exactly from its genesis event log (from empty)",
      rebuilt["nodes"] == graph["nodes"] and rebuilt["edges"] == graph["edges"])
errs, _ = afc.validate_graph(rebuilt)
check("rebuilt graph validates", not errs)

print("== conformance (validate every example graph) ==")
for ex in ("schema/examples/graph.example.json", "examples/research.graph.json",
           "examples/namespaced.graph.json"):
    errs, _ = afc.validate_graph(read(ex))
    check(f"valid: {ex}", not errs)

passed = sum(1 for _, ok in checks if ok)
print(f"\n{passed}/{len(checks)} checks passed")
sys.exit(0 if passed == len(checks) else 1)
