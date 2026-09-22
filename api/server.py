#!/usr/bin/env python3
"""The Agent-Fabric API — the first sellable slice of the service catalog.

docs/platform-as-service-delivery-model.md defines a broad, long-horizon
service catalog (Fabric Box Management, Kubernetes Operator Management, Edge
Agent Management, ...) built on the platform-as-agent thesis. None of that
infrastructure exists yet. What already exists, and already computes
deterministic answers, is the `fab` toolchain: compile, validate, grade,
migrate, query. This service exposes exactly that over HTTP, metered per call,
so the two catalog lines that need no fleet at all — "Compliance Evidence
Management" and "Drift Detection and Reconciliation" — are sellable today.

    POST /v1/compile           {source}                    -> compiled graph
    POST /v1/graphs/validate   {graph}                      -> correctness check
    POST /v1/graphs/grade      {graph}                      -> quality score + verdict
    POST /v1/graphs/migrate    {graph, minQuality?}         -> gated promotion to active
    POST /v1/graphs/query      {graph, query|ego, events?}  -> BQL traversal
    GET  /v1/usage                                          -> this key's metered usage
    GET  /v1/vocabulary                                     -> public: kinds/predicates/states
    GET  /v1/health                                         -> public: liveness

Auth: `Authorization: Bearer <api_key>` on every route except /v1/health and
/v1/vocabulary. Issue keys with `python api/manage_keys.py create --customer ...`.

Every authenticated call is metered into api/keystore.py as a usage event
tagged with the pricing unit it represents (evidence_trail, reconciliation,
query, compile) — the "evidence trail" / "per reconciliation" units the
service-delivery doc already names, so a billing system can read the ledger
directly instead of re-deriving it from logs.

    python api/server.py [--host 0.0.0.0] [--port 8080]

Pure Python standard library (http.server + sqlite3) — no third-party
dependencies, consistent with the rest of the toolchain.
"""
import argparse
import json
import os
import sys
import time
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import afc  # noqa: E402
import bql  # noqa: E402
import fabriclib  # noqa: E402
import grade as grade_mod  # noqa: E402
import keystore  # noqa: E402
import migrate as migrate_mod  # noqa: E402

MAX_BODY_BYTES = int(os.environ.get("FABRIC_API_MAX_BODY", 2 * 1024 * 1024))  # 2MB
RATE_LIMIT_PER_MIN = int(os.environ.get("FABRIC_API_RATE_LIMIT", 120))

# api_key_id -> (window_start_minute, count_in_window). In-memory, per process;
# good enough for a single-instance wedge deployment, not a distributed one.
_rate_state = {}


class ApiError(Exception):
    def __init__(self, status, code, message):
        super().__init__(message)
        self.status = status
        self.code = code
        self.message = message


def _check_rate_limit(key_id):
    now_minute = int(time.time() // 60)
    start, count = _rate_state.get(key_id, (now_minute, 0))
    if start != now_minute:
        start, count = now_minute, 0
    count += 1
    _rate_state[key_id] = (start, count)
    if count > RATE_LIMIT_PER_MIN:
        raise ApiError(429, "rate_limited", f"more than {RATE_LIMIT_PER_MIN} requests/min")


def _vocab_payload():
    reg = fabriclib.read_json(os.path.join(ROOT, "schema", "registry", "registry.json"))
    state_reg = fabriclib.read_json(os.path.join(ROOT, "schema", "registry", "states.json"))
    return {
        "registryVersion": reg.get("version", "?"),
        "nodeKinds": [k["name"] for k in reg["nodeKinds"]],
        "relationPredicates": [p["name"] for p in reg["relationTypes"]],
        "lifecycleStates": [s["name"] for s in state_reg["states"]],
    }


class Handler(BaseHTTPRequestHandler):
    server_version = "AgentFabricAPI/1"

    def log_message(self, fmt, *args):
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))

    # -- wire helpers ------------------------------------------------------
    def _send_json(self, status, payload):
        body = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _error(self, status, code, message):
        self._send_json(status, {"error": {"code": code, "message": message}})

    def _drain(self, length, chunk_size=65536):
        """Read and discard up to `length` bytes without buffering the whole
        thing — used when we're about to reject a body as too large, so the
        client doesn't see a broken pipe from writing into a socket the
        server closed mid-upload."""
        remaining = length
        while remaining > 0:
            data = self.rfile.read(min(chunk_size, remaining))
            if not data:
                break
            remaining -= len(data)

    def _read_json_body(self):
        length = int(self.headers.get("Content-Length", 0) or 0)
        if length <= 0:
            raise ApiError(400, "bad_request", "missing request body")
        if length > MAX_BODY_BYTES:
            self._drain(length)
            raise ApiError(413, "payload_too_large", f"body exceeds {MAX_BODY_BYTES} bytes")
        raw = self.rfile.read(length)
        try:
            return json.loads(raw.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            raise ApiError(400, "bad_request", f"invalid JSON body: {e}")

    def _authenticate(self):
        auth = self.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            raise ApiError(401, "unauthorized", "missing 'Authorization: Bearer <api_key>'")
        principal = keystore.authenticate(auth[len("Bearer "):].strip())
        if not principal:
            raise ApiError(401, "unauthorized", "invalid or revoked API key")
        _check_rate_limit(principal["id"])
        return principal

    def _meter(self, principal, service, unit_type, status, detail=None):
        try:
            keystore.record_usage(
                principal["id"], principal["customer"], service, unit_type, status,
                json.dumps(detail) if detail is not None else None,
            )
        except Exception:
            # Metering must never break the response the caller is waiting on.
            traceback.print_exc()

    # -- routing -------------------------------------------------------------
    def do_GET(self):
        self._dispatch("GET")

    def do_POST(self):
        self._dispatch("POST")

    def _dispatch(self, method):
        path = self.path.split("?", 1)[0].rstrip("/") or "/"
        try:
            if method == "GET" and path == "/v1/health":
                return self._send_json(200, {"status": "ok", "time": time.time()})
            if method == "GET" and path == "/v1/vocabulary":
                return self._send_json(200, _vocab_payload())
            if method == "GET" and path == "/v1/usage":
                return self._handle_usage()
            if method == "POST" and path == "/v1/compile":
                return self._handle_compile()
            if method == "POST" and path == "/v1/graphs/validate":
                return self._handle_validate()
            if method == "POST" and path == "/v1/graphs/grade":
                return self._handle_grade()
            if method == "POST" and path == "/v1/graphs/migrate":
                return self._handle_migrate()
            if method == "POST" and path == "/v1/graphs/query":
                return self._handle_query()
            return self._error(404, "not_found", f"no route for {method} {path}")
        except ApiError as e:
            return self._error(e.status, e.code, e.message)
        except Exception as e:
            traceback.print_exc()
            return self._error(500, "internal_error", str(e))

    # -- handlers --------------------------------------------------------------
    def _handle_compile(self):
        principal = self._authenticate()
        body = self._read_json_body()
        source = body.get("source")
        if not isinstance(source, str) or not source.strip():
            raise ApiError(400, "bad_request", "'source' (FAL text) is required")
        try:
            graph = afc.compile_source(source)
        except afc.FALError as e:
            self._meter(principal, "compile", "compile", "error", {"error": str(e)})
            raise ApiError(422, "compile_error", str(e))
        errs, mode = afc.validate_graph(graph)
        self._meter(
            principal, "compile", "compile", "success" if not errs else "invalid",
            {"nodes": len(graph["nodes"]), "edges": len(graph["edges"]), "mode": mode},
        )
        self._send_json(200, {"graph": graph, "valid": not errs, "errors": errs, "mode": mode})

    def _handle_validate(self):
        principal = self._authenticate()
        body = self._read_json_body()
        graph = body.get("graph")
        if not isinstance(graph, dict):
            raise ApiError(400, "bad_request", "'graph' (object) is required")
        errs, mode = afc.validate_graph(graph)
        self._meter(
            principal, "validate", "evidence_trail", "success" if not errs else "invalid",
            {"errorCount": len(errs), "mode": mode},
        )
        self._send_json(200, {"valid": not errs, "errors": errs, "mode": mode})

    def _handle_grade(self):
        principal = self._authenticate()
        body = self._read_json_body()
        graph = body.get("graph")
        if not isinstance(graph, dict):
            raise ApiError(400, "bad_request", "'graph' (object) is required")
        score, criteria = grade_mod.grade(graph)
        verdict = grade_mod.verdict(score)
        self._meter(principal, "grade", "evidence_trail", "success",
                    {"score": score, "verdict": verdict})
        self._send_json(200, {"score": score, "verdict": verdict, "criteria": criteria})

    def _handle_migrate(self):
        principal = self._authenticate()
        body = self._read_json_body()
        graph = body.get("graph")
        min_quality = body.get("minQuality", 0)
        if not isinstance(graph, dict):
            raise ApiError(400, "bad_request", "'graph' (object) is required")
        try:
            migrated, report = migrate_mod.migrate(graph, float(min_quality))
        except ValueError as e:
            self._meter(principal, "migrate", "reconciliation", "gate_failed", {"error": str(e)})
            raise ApiError(422, "gate_failed", str(e))
        self._meter(principal, "migrate", "reconciliation", "success", report)
        self._send_json(200, {"graph": migrated, "report": report})

    def _handle_query(self):
        principal = self._authenticate()
        body = self._read_json_body()
        graph = body.get("graph")
        if not isinstance(graph, dict):
            raise ApiError(400, "bad_request", "'graph' (object) is required")
        events = body.get("events")
        if events:
            from kernel import GraphKernel
            evs = events if isinstance(events, list) else events.get("events", [events])
            graph, _ = GraphKernel(graph, evs, until=body.get("at")).view()
        try:
            if body.get("ego"):
                results = bql.ego(graph, body["ego"], int(body.get("radius", 1)))
            else:
                query = body.get("query")
                if not query:
                    raise ApiError(400, "bad_request", "'query' or 'ego' is required")
                results = bql.evaluate(graph, query)
        except ValueError as e:
            self._meter(principal, "query", "query", "error", {"error": str(e)})
            raise ApiError(422, "query_error", str(e))
        self._meter(principal, "query", "query", "success", {"resultCount": len(results)})
        self._send_json(200, {"results": results, "count": len(results)})

    def _handle_usage(self):
        principal = self._authenticate()
        summary = keystore.usage_summary(principal["id"])
        recent = keystore.list_usage(principal["id"], limit=50)
        self._send_json(
            200, {"customer": principal["customer"], "summary": summary, "recent": recent}
        )


def main(argv=None):
    ap = argparse.ArgumentParser(description="Run the Agent-Fabric API server.")
    ap.add_argument("--host", default=os.environ.get("FABRIC_API_HOST", "0.0.0.0"))
    ap.add_argument("--port", type=int, default=int(os.environ.get("FABRIC_API_PORT", 8080)))
    args = ap.parse_args(argv)
    httpd = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"fabric-api: listening on {args.host}:{args.port} (db={keystore.DB_PATH})",
          file=sys.stderr)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
