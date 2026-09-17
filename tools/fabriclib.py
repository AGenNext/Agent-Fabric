"""Shared helpers for the Agent-Fabric tools (afc, bql).

Keeps the kind/predicate vocabulary and the set of reserved entity fields
derived from the schema/registry — the single source of truth — so the tools
never drift from the meta-model. Pure standard library.
"""
import functools
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read_json(path):
    with open(path) as fh:
        return json.load(fh)


def coerce(v):
    """Light scalar coercion for string values: bool, int, float, else str."""
    if isinstance(v, str):
        if v in ("true", "false"):
            return v == "true"
        if re.fullmatch(r"-?\d+", v):
            return int(v)
        if re.fullmatch(r"-?\d*\.\d+", v):
            return float(v)
    return v


@functools.lru_cache(maxsize=None)
def load_registry():
    """Return ({kind_lower: Kind}, {predicate_lower: relationType}) from the registry."""
    reg = read_json(os.path.join(ROOT, "schema", "registry", "registry.json"))
    kinds = {k["name"].lower(): k["name"] for k in reg["nodeKinds"]}
    predicates = {r["name"].lower(): r for r in reg["relationTypes"]}
    return kinds, predicates


@functools.lru_cache(maxsize=None)
def reserved_fields():
    """Entity-level field names, derived from the entity schema's properties.

    Excludes the structural keys handled elsewhere (`id`/`kind` come from the
    declaration, `attributes` is the catch-all bucket, `provenance` is a nested
    object). Everything else the schema defines on Entity is a reserved field.
    """
    schema = read_json(os.path.join(ROOT, "schema", "meta", "entity.schema.json"))
    structural = {"id", "kind", "attributes", "provenance"}
    return frozenset(k for k in schema.get("properties", {}) if k not in structural)
