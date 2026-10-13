#!/usr/bin/env python3
"""fab serve — the Fabric Core kernel-boundary services over HTTP.

A zero-dependency (standard library only) service that turns the toolchain into
a running metabase. Storage is an append-only event log on disk; every read is
a calculated projection (the kernel fold) — no materialized subgraph, no
database. This is the same "storage + calculation" the CLI uses, exposed over
HTTP and durable across restarts.

Store layout (a directory):
    <store>/base.json      optional base graph ({"nodes": [], "edges": []})
    <store>/events.jsonl   append-only GraphEvent chain, one JSON per line

Endpoints (the Fabric Core kernel-boundary services):
    GET  /healthz                      liveness + event count
    POST /assert                       ASSERT/OBSERVE: append GraphEvent(s)
    GET  /project[?at=SEQ]             PROJECT: the emulated graph (optionally as-of)
    GET  /query?q=QUERY                query the projection (BQL)
    GET  /query?ego=ID&radius=N        ego-view of the projection
    GET  /verify                       VERIFY: validation result of the projection
    GET  /drift                        COMPARE: quality score + findings
    POST /reconcile                    RECONCILE: promote proposals -> active

Usage:
    fab serve <store> [--host H] [--port P]
"""
import argparse
import datetime
import json
import os
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

import afc
import bql
import grade as grade_mod
import migrate as migrate_mod
from kernel import GraphKernel, KernelError, _enforce, _seq


def _now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class Store:
    """Durable append-only event log + optional base graph. The source of truth
    is the log; the graph is always recomputed from base + events on read."""

    def __init__(self, path):
        self.path = path
        self.base_path = os.path.join(path, "base.json")
        self.log_path = os.path.join(path, "events.jsonl")
        self._lock = threading.Lock()
        os.makedirs(path, exist_ok=True)

    def base(self):
        if os.path.exists(self.base_path):
            with open(self.base_path) as fh:
                return json.load(fh)
        return {"nodes": [], "edges": []}

    def events(self):
        evs = []
        if os.path.exists(self.log_path):
            with open(self.log_path) as fh:
                for line in fh:
                    line = line.strip()
                    if line:
                        evs.append(json.loads(line))
        return evs

    def project(self, until=None):
        return GraphKernel(self.base(), self.events(), until=until).view()[0]

    def append(self, incoming):
        """Validate and append events; idempotent by event id. Returns a report."""
        with self._lock:
            existing = self.events()
            seen = {e.get("id") for e in existing}
            next_seq = (max((_seq(e) for e in existing), default=0)) + 1
            appended, skipped, errors = [], [], []
            lines = []
            for ev in incoming:
                eid = ev.get("id")
                if eid and eid in seen:
                    skipped.append(eid)
                    continue
                ev.setdefault("kind", "GraphEvent")
                if "sequence" not in ev:
                    ev["sequence"] = next_seq
                ev.setdefault("id", f"af:event/{_seq(ev)}")
                ev.setdefault("occurredAt", _now())
                eid = ev["id"]
                if eid in seen:  # id assigned from sequence may already exist
                    skipped.append(eid)
                    continue
                next_seq = max(next_seq, _seq(ev)) + 1
                try:
                    _enforce(ev)  # kernel enforcement at ingestion
                except KernelError as exc:
                    errors.append({"id": eid, "error": str(exc)})
                    continue
                lines.append(json.dumps(ev))
                appended.append(ev.get("id"))
                if eid:
                    seen.add(eid)
            if errors:
                # Reject the whole batch on any invalid event; nothing is written.
                return {"appended": [], "skipped": skipped, "errors": errors, "ok": False}
            if lines:
                with open(self.log_path, "a") as fh:
                    fh.write("\n".join(lines) + "\n")
            return {"appended": appended, "skipped": skipped, "errors": [], "ok": True}

    def reconcile(self, min_quality=0):
        """Promote proposals -> active by emitting upsert events (log stays the
        source of truth). Gated on correctness and, optionally, quality."""
        proj = self.project()
        migrated, report = migrate_mod.migrate(proj, min_quality)  # raises on gate failure
        promote = []
        for target, key in (("node", "nodes"), ("edge", "edges")):
            before = {el["id"]: el.get("state", "proposed") for el in proj.get(key, [])}
            for el in migrated.get(key, []):
                if el.get("state") == "active" and before.get(el["id"]) != "active":
                    promote.append({
                        "kind": "GraphEvent", "op": "upsert", "target": target,
                        "stream": "reconcile", "payload": el,
                    })
        append_report = self.append(promote) if promote else {"appended": [], "skipped": []}
        report["events_emitted"] = len(append_report.get("appended", []))
        return report


class Handler(BaseHTTPRequestHandler):
    store = None  # set on the server instance's handler class

    def _send(self, code, payload):
        body = json.dumps(payload, indent=2).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _body(self):
        length = int(self.headers.get("Content-Length", 0) or 0)
        raw = self.rfile.read(length) if length else b""
        return json.loads(raw) if raw else {}

    def log_message(self, *args):
        pass  # quiet; the caller owns logging

    def do_GET(self):
        u = urlparse(self.path)
        q = parse_qs(u.query)
        try:
            if u.path == "/healthz":
                return self._send(200, {"status": "ok", "events": len(self.store.events()),
                                        "store": self.store.path})
            if u.path == "/project":
                until = int(q["at"][0]) if "at" in q else None
                return self._send(200, self.store.project(until))
            if u.path == "/query":
                graph = self.store.project()
                if "ego" in q:
                    radius = int(q.get("radius", ["1"])[0])
                    return self._send(200, {"nodes": bql.ego(graph, q["ego"][0], radius)})
                if "q" in q:
                    query = q["q"][0]
                    if len(query) > 4096:
                        return self._send(413, {"error": "query too long (max 4096 chars)"})
                    return self._send(200, {"results": bql.evaluate(graph, query)})
                return self._send(400, {"error": "query requires ?q= or ?ego="})
            if u.path == "/verify":
                errs, mode = afc.validate_graph(self.store.project())
                return self._send(200, {"ok": not errs, "mode": mode, "errors": errs})
            if u.path == "/drift":
                score, criteria = grade_mod.grade(self.store.project())
                return self._send(200, {"score": score, "verdict": grade_mod.verdict(score),
                                        "criteria": criteria})
            return self._send(404, {"error": f"no such endpoint: {u.path}"})
        except Exception as exc:  # noqa: BLE001 - surface any failure as 500 JSON
            return self._send(500, {"error": f"{type(exc).__name__}: {exc}"})

    def do_POST(self):
        u = urlparse(self.path)
        try:
            if u.path == "/assert":
                payload = self._body()
                if isinstance(payload, dict) and "events" in payload:
                    events = payload["events"]
                elif isinstance(payload, list):
                    events = payload
                else:
                    events = [payload]
                report = self.store.append(events)
                return self._send(200 if report["ok"] else 422, report)
            if u.path == "/reconcile":
                body = self._body()
                try:
                    report = self.store.reconcile(int(body.get("min_quality", 0)))
                except ValueError as exc:  # a gate failed
                    return self._send(409, {"ok": False, "error": str(exc)})
                return self._send(200, {"ok": True, **report})
            return self._send(404, {"error": f"no such endpoint: {u.path}"})
        except Exception as exc:  # noqa: BLE001
            return self._send(500, {"error": f"{type(exc).__name__}: {exc}"})


def make_server(store_path, host, port):
    store = Store(store_path)
    handler = type("BoundHandler", (Handler,), {"store": store})
    return ThreadingHTTPServer((host, port), handler)


def main(argv=None):
    ap = argparse.ArgumentParser(prog="fab serve", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("store", help="store directory (base.json + events.jsonl)")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8777)
    args = ap.parse_args(argv)
    srv = make_server(args.store, args.host, args.port)
    print(f"fab serve: {args.host}:{args.port}  store={args.store}", file=sys.stderr)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        srv.shutdown()
    return 0


if __name__ == "__main__":
    sys.exit(main())
