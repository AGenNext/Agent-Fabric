"""SQLite-backed API key store and usage ledger for the Agent-Fabric API.

Every authenticated call is recorded as a usage event — the same unit types
already named as pricing candidates in docs/platform-as-service-delivery-model.md
(per evidence trail, per reconciliation, per compliance report). This module is
the metering substrate those units get billed against; it does not itself
charge anyone — it produces the ledger a billing system reads.

Raw API keys are never stored — only their SHA-256 hash — so a database leak
does not leak usable credentials. Pure standard library (sqlite3).
"""
import hashlib
import os
import secrets
import sqlite3
import time
import uuid

DB_PATH = os.environ.get(
    "FABRIC_API_DB", os.path.join(os.path.dirname(os.path.abspath(__file__)), "fabric_api.db")
)

SCHEMA = """
CREATE TABLE IF NOT EXISTS api_keys (
    id TEXT PRIMARY KEY,
    key_hash TEXT UNIQUE NOT NULL,
    customer TEXT NOT NULL,
    tier TEXT NOT NULL DEFAULT 'provider',
    label TEXT,
    created_at REAL NOT NULL,
    revoked_at REAL
);

CREATE TABLE IF NOT EXISTS usage_events (
    id TEXT PRIMARY KEY,
    api_key_id TEXT NOT NULL,
    customer TEXT NOT NULL,
    service TEXT NOT NULL,
    unit_type TEXT NOT NULL,
    status TEXT NOT NULL,
    detail TEXT,
    created_at REAL NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_usage_key ON usage_events (api_key_id, created_at);
"""


def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.executescript(SCHEMA)
    return conn


def hash_key(raw_key):
    return hashlib.sha256(raw_key.encode("utf-8")).hexdigest()


def create_key(customer, tier="provider", label=None):
    """Issue a new key. The raw key is returned once and never persisted."""
    raw = "fab_" + secrets.token_urlsafe(32)
    key_id = str(uuid.uuid4())
    conn = _connect()
    try:
        with conn:
            conn.execute(
                "INSERT INTO api_keys (id, key_hash, customer, tier, label, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (key_id, hash_key(raw), customer, tier, label, time.time()),
            )
    finally:
        conn.close()
    return {"id": key_id, "key": raw, "customer": customer, "tier": tier}


def revoke_key(raw_key):
    conn = _connect()
    try:
        with conn:
            cur = conn.execute(
                "UPDATE api_keys SET revoked_at = ? WHERE key_hash = ? AND revoked_at IS NULL",
                (time.time(), hash_key(raw_key)),
            )
        return cur.rowcount > 0
    finally:
        conn.close()


def authenticate(raw_key):
    """Return {'id', 'customer', 'tier'} for a valid, non-revoked key, else None."""
    if not raw_key:
        return None
    conn = _connect()
    try:
        row = conn.execute(
            "SELECT id, customer, tier FROM api_keys WHERE key_hash = ? AND revoked_at IS NULL",
            (hash_key(raw_key),),
        ).fetchone()
    finally:
        conn.close()
    if not row:
        return None
    return {"id": row[0], "customer": row[1], "tier": row[2]}


def list_keys():
    conn = _connect()
    try:
        rows = conn.execute(
            "SELECT id, customer, tier, label, created_at, revoked_at FROM api_keys "
            "ORDER BY created_at DESC"
        ).fetchall()
    finally:
        conn.close()
    return [
        {"id": i, "customer": c, "tier": t, "label": l, "createdAt": ca, "revokedAt": ra}
        for i, c, t, l, ca, ra in rows
    ]


def record_usage(api_key_id, customer, service, unit_type, status, detail=None):
    conn = _connect()
    try:
        with conn:
            conn.execute(
                "INSERT INTO usage_events "
                "(id, api_key_id, customer, service, unit_type, status, detail, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (str(uuid.uuid4()), api_key_id, customer, service, unit_type, status, detail,
                 time.time()),
            )
    finally:
        conn.close()


def usage_summary(api_key_id, since=None):
    """Return {unit_type: count} for billable units recorded against this key."""
    conn = _connect()
    try:
        q = "SELECT unit_type, COUNT(*) FROM usage_events WHERE api_key_id = ?"
        params = [api_key_id]
        if since is not None:
            q += " AND created_at >= ?"
            params.append(since)
        q += " GROUP BY unit_type"
        rows = conn.execute(q, params).fetchall()
    finally:
        conn.close()
    return {unit: count for unit, count in rows}


def list_usage(api_key_id, limit=50):
    conn = _connect()
    try:
        rows = conn.execute(
            "SELECT service, unit_type, status, detail, created_at FROM usage_events "
            "WHERE api_key_id = ? ORDER BY created_at DESC LIMIT ?",
            (api_key_id, limit),
        ).fetchall()
    finally:
        conn.close()
    return [
        {"service": s, "unitType": u, "status": st, "detail": d, "createdAt": c}
        for s, u, st, d, c in rows
    ]
