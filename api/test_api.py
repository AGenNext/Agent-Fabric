#!/usr/bin/env python3
"""End-to-end tests for the Agent-Fabric API.

Spins up the real server (ThreadingHTTPServer + the actual Handler) on an
ephemeral localhost port and drives it over HTTP using only the standard
library — no test framework beyond unittest, no mocking of the handler.

    python api/test_api.py
"""
import json
import os
import sys
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# Isolate this run's data — read at import time by keystore.py, so it must be
# set before that module is imported. The rate limit test patches
# api_server.RATE_LIMIT_PER_MIN directly rather than lowering it globally, so
# the shared default key other tests use isn't affected.
_TMP_DB = tempfile.NamedTemporaryFile(prefix="fabric_api_test_", suffix=".db", delete=False)
_TMP_DB.close()
os.environ["FABRIC_API_DB"] = _TMP_DB.name

sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
import keystore  # noqa: E402
import server as api_server  # noqa: E402


class ApiTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.httpd = ThreadingHTTPServer(("127.0.0.1", 0), api_server.Handler)
        cls.port = cls.httpd.server_address[1]
        cls.thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f"http://127.0.0.1:{cls.port}"
        key_info = keystore.create_key("domain:test-customer", tier="provider", label="ci")
        cls.api_key = key_info["key"]

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()
        os.unlink(_TMP_DB.name)

    def _call(self, method, path, body=None, api_key="__default__", expect=200):
        url = self.base + path
        data = json.dumps(body).encode("utf-8") if body is not None else None
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("Content-Type", "application/json")
        if api_key == "__default__":
            api_key = self.api_key
        if api_key:
            req.add_header("Authorization", f"Bearer {api_key}")
        try:
            with urllib.request.urlopen(req) as resp:
                status = resp.status
                payload = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            status = e.code
            payload = json.loads(e.read().decode("utf-8"))
        self.assertEqual(status, expect, payload)
        return payload

    # -- public routes -----------------------------------------------------
    def test_health_is_public(self):
        payload = self._call("GET", "/v1/health", api_key=None)
        self.assertEqual(payload["status"], "ok")

    def test_vocabulary_is_public(self):
        payload = self._call("GET", "/v1/vocabulary", api_key=None)
        self.assertIn("Agent", payload["nodeKinds"])
        self.assertIn("delegates_to", [p.lower() for p in payload["relationPredicates"]])

    # -- auth ----------------------------------------------------------------
    def test_unauthenticated_call_rejected(self):
        self._call("POST", "/v1/graphs/grade", {"graph": {"nodes": [], "edges": []}},
                    api_key=None, expect=401)

    def test_invalid_key_rejected(self):
        self._call("POST", "/v1/graphs/grade", {"graph": {"nodes": [], "edges": []}},
                    api_key="not-a-real-key", expect=401)

    def test_revoked_key_rejected(self):
        info = keystore.create_key("domain:revoke-test")
        self.assertTrue(keystore.revoke_key(info["key"]))
        self._call("GET", "/v1/usage", api_key=info["key"], expect=401)

    # -- the actual pipeline: compile -> validate -> grade -> migrate --------
    def test_compile_then_validate_then_grade_then_migrate(self):
        source = (
            "workspace demo\n"
            "  environment: prod\n"
            "\n"
            "agent researcher-1\n"
            "  scope: demo\n"
            "  role: executor\n"
        )
        compiled = self._call("POST", "/v1/compile", {"source": source})
        self.assertTrue(compiled["valid"], compiled["errors"])
        graph = compiled["graph"]

        validated = self._call("POST", "/v1/graphs/validate", {"graph": graph})
        self.assertTrue(validated["valid"])

        graded = self._call("POST", "/v1/graphs/grade", {"graph": graph})
        self.assertIn("score", graded)
        self.assertIn("verdict", graded)
        self.assertIsInstance(graded["criteria"], list)

        migrated = self._call("POST", "/v1/graphs/migrate", {"graph": graph, "minQuality": 0})
        self.assertIn("report", migrated)
        self.assertTrue(all(n.get("state") == "active" for n in migrated["graph"]["nodes"]))

    def test_compile_rejects_bad_source(self):
        self._call("POST", "/v1/compile", {"source": "not a valid fal line\n  bad: value"},
                    expect=422)

    def test_migrate_gate_failure_on_unreachable_min_quality(self):
        graph = {"kind": "Graph", "nodes": [], "edges": []}
        self._call("POST", "/v1/graphs/migrate", {"graph": graph, "minQuality": 999}, expect=422)

    def test_query_against_shipped_example(self):
        with open(os.path.join(ROOT, "examples", "research.graph.json")) as fh:
            graph = json.load(fh)
        result = self._call("POST", "/v1/graphs/query", {"graph": graph, "query": "agent"})
        self.assertGreaterEqual(result["count"], 1)

    def test_query_requires_query_or_ego(self):
        graph = {"kind": "Graph", "nodes": [], "edges": []}
        self._call("POST", "/v1/graphs/query", {"graph": graph}, expect=400)

    # -- metering -------------------------------------------------------------
    def test_usage_is_metered_per_key(self):
        info = keystore.create_key("domain:usage-test")
        before = self._call("GET", "/v1/usage", api_key=info["key"])
        self.assertEqual(sum(before["summary"].values()), 0)
        self._call("POST", "/v1/graphs/grade", {"graph": {"nodes": [], "edges": []}},
                    api_key=info["key"])
        after = self._call("GET", "/v1/usage", api_key=info["key"])
        self.assertEqual(sum(after["summary"].values()), 1)
        self.assertEqual(after["summary"].get("evidence_trail"), 1)

    def test_usage_is_isolated_between_keys(self):
        info_a = keystore.create_key("domain:isolation-a")
        info_b = keystore.create_key("domain:isolation-b")
        self._call("POST", "/v1/graphs/grade", {"graph": {"nodes": [], "edges": []}},
                    api_key=info_a["key"])
        usage_b = self._call("GET", "/v1/usage", api_key=info_b["key"])
        self.assertEqual(sum(usage_b["summary"].values()), 0)

    # -- abuse resistance -------------------------------------------------------
    def test_rate_limit_is_enforced(self):
        info = keystore.create_key("domain:rate-test")
        original_limit = api_server.RATE_LIMIT_PER_MIN
        api_server.RATE_LIMIT_PER_MIN = 3
        try:
            for _ in range(3):
                self._call("GET", "/v1/usage", api_key=info["key"])
            self._call("GET", "/v1/usage", api_key=info["key"], expect=429)
        finally:
            api_server.RATE_LIMIT_PER_MIN = original_limit

    def test_oversized_body_rejected(self):
        info = keystore.create_key("domain:size-test")
        huge_source = "x" * (api_server.MAX_BODY_BYTES + 1)
        self._call("POST", "/v1/compile", {"source": huge_source}, api_key=info["key"],
                    expect=413)


if __name__ == "__main__":
    unittest.main()
