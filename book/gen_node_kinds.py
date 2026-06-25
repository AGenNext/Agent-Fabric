import json, pathlib
root = pathlib.Path(".")
reg = json.load(open("schema/registry/registry.json"))
kinds = reg["nodeKinds"]
rels = reg["relationTypes"]

def schema_props(name):
    p = root / "schema" / "nodes" / f"{name.lower()}.schema.json"
    if not p.exists():
        return [], []
    d = json.load(open(p))
    props, req = {}, []
    # own properties may sit at top level and/or inside allOf branches
    def collect(obj):
        if not isinstance(obj, dict):
            return
        props.update(obj.get("properties", {}) or {})
        for r in obj.get("required", []) or []:
            if r not in req:
                req.append(r)
        for branch in obj.get("allOf", []) or []:
            collect(branch)
    collect(d)
    return props, req

out = []
out.append("# Node Kinds\n")
out.append("Agent Fabric models the ecosystem as one heterogeneous graph over "
           f"**{len(kinds)} node kinds** and **{len(rels)} relation predicates**, "
           "defined in the versioned [registry](https://github.com/AGenNextHub/Agent-Fabric/blob/main/schema/registry/registry.json) "
           f"(v{reg.get('version')}) — the single source of truth from which the tools and SDKs read their vocabulary.\n")
out.append("| Kind | Description |")
out.append("|---|---|")
for k in kinds:
    out.append(f"| [`{k['name']}`](#{k['name'].lower()}) | {k['description']} |")
out.append("")
for k in kinds:
    name = k["name"]
    out.append(f"## {name}\n")
    out.append(k["description"] + "\n")
    props, req = schema_props(name)
    # drop inherited base fields that every node shares for a tighter, kind-specific view
    base = {"id","kind","label","description","state","tags","attributes","scope",
            "tenant","version","revision","validFrom","validTo","observedAt",
            "createdAt","updatedAt","provenance"}
    own = {p:v for p,v in props.items() if p not in base}
    if own:
        out.append("Kind-specific properties:\n")
        out.append("| Property | Type | Required | Description |")
        out.append("|---|---|---|---|")
        for pn, pv in sorted(own.items()):
            t = pv.get("type", pv.get("$ref","").split("/")[-1] or "—")
            if isinstance(t, list): t = " \\| ".join(t)
            rq = "yes" if pn in req else ""
            desc = (pv.get("description","") or "").replace("\n"," ")
            out.append(f"| `{pn}` | {t} | {rq} | {desc} |")
        out.append("")
    out.append(f"_Schema: [`nodes/{name.lower()}.schema.json`](https://github.com/AGenNextHub/Agent-Fabric/blob/main/schema/nodes/{name.lower()}.schema.json)_\n")

# relation predicates appendix
out.append("## Relation Predicates\n")
out.append(f"The {len(rels)} directed predicates that connect node kinds:\n")
out.append("| Predicate | Description |")
out.append("|---|---|")
for r in rels:
    if isinstance(r, dict):
        out.append(f"| `{r.get('name')}` | {r.get('description','')} |")
    else:
        out.append(f"| `{r}` | |")
out.append("")

pathlib.Path("book/src/node-kinds.md").write_text("\n".join(out))
print("wrote book/src/node-kinds.md  (%d kinds, %d predicates)" % (len(kinds), len(rels)))
