# api/

The Agent-Fabric API — the first sellable slice of the service catalog
described in [`docs/platform-as-service-delivery-model.md`](../docs/platform-as-service-delivery-model.md).

That doc lays out a broad, long-horizon catalog (Fabric Box Management,
Kubernetes Operator Management, Edge Agent Management, ...) built on the
platform-as-agent thesis. None of that infrastructure exists in this repo yet.
What already exists, and already computes deterministic answers, is the
[`fab`](../tools/README.md) toolchain — compile, validate, grade, migrate,
query. This service exposes exactly that over HTTP, metered per call, so the
two catalog lines that don't require any managed fleet — **Compliance
Evidence Management** and **Drift Detection and Reconciliation** — are
sellable today, without waiting on the Kubernetes/Ubuntu Core edge story.

It is intentionally narrow. It is not the Platform Agent, it does not manage
Fabric Boxes, and it makes no claims about outcome contracts, SLAs, or
authority chains — it wraps the four things `fab` already does correctly and
meters who called what.

**License:** this directory is proprietary (see [`LICENSE`](LICENSE)) — it
is the sellable layer, not part of the Apache-2.0 open core described in the
root [`NOTICE`](../NOTICE). It imports the Apache-2.0 `tools/` and `schema/`
code as a dependency; that doesn't change either side's license.

## Run it

```bash
# local, stdlib only
python api/server.py --port 8080

# issue a key (raw key is shown once, only its hash is stored)
python api/manage_keys.py create --customer domain:acme --tier provider

# docker
docker build -f api/Dockerfile -t agent-fabric-api .
docker run --rm -p 8080:8080 -v fabric-api-data:/data agent-fabric-api
```

Environment variables:

| Variable | Default | Meaning |
|---|---|---|
| `FABRIC_API_HOST` | `0.0.0.0` | listen address |
| `FABRIC_API_PORT` | `8080` | listen port |
| `FABRIC_API_DB` | `api/fabric_api.db` | SQLite path for keys + usage ledger |
| `FABRIC_API_MAX_BODY` | `2097152` (2MB) | request body cap, bytes |
| `FABRIC_API_RATE_LIMIT` | `120` | requests/min per API key |

## Endpoints

All routes except `/v1/health` and `/v1/vocabulary` require
`Authorization: Bearer <api_key>`.

| Route | Method | Body | Does |
|---|---|---|---|
| `/v1/health` | GET | — | liveness, public |
| `/v1/vocabulary` | GET | — | registered node kinds / predicates / lifecycle states, public |
| `/v1/compile` | POST | `{source}` | FAL text → compiled + validated graph |
| `/v1/graphs/validate` | POST | `{graph}` | correctness check (schema or built-in fallback) |
| `/v1/graphs/grade` | POST | `{graph}` | quality score 0-100 + verdict + per-criterion findings |
| `/v1/graphs/migrate` | POST | `{graph, minQuality?}` | gated promotion of proposals → active |
| `/v1/graphs/query` | POST | `{graph, query\|ego, events?, at?, radius?}` | BQL traversal, optionally over emulated (event-overlaid) state |
| `/v1/usage` | GET | — | this key's metered usage: summary by unit type + last 50 events |

Example:

```bash
curl -s https://api.example/v1/graphs/grade \
  -H "Authorization: Bearer $FABRIC_API_KEY" \
  -d @graph.json | jq
```

Errors are a consistent envelope: `{"error": {"code": "...", "message": "..."}}`
with the matching HTTP status (`400` bad request, `401` unauthorized, `413`
payload too large, `422` a domain gate failed — invalid FAL, invalid graph,
or a migrate quality gate — `429` rate limited, `500` internal error).

## Metering and pricing units

Every authenticated call is recorded in `api/keystore.py` as a usage event
tagged with a unit type, using the same vocabulary
[`docs/platform-as-service-delivery-model.md`](../docs/platform-as-service-delivery-model.md#pricing-and-packaging-units)
already names as candidate pricing units:

| Route | `unitType` |
|---|---|
| `/v1/compile` | `compile` |
| `/v1/graphs/validate` | `evidence_trail` |
| `/v1/graphs/grade` | `evidence_trail` |
| `/v1/graphs/migrate` | `reconciliation` |
| `/v1/graphs/query` | `query` |

`GET /v1/usage` lets a caller self-serve their own usage; a billing system
reads the same `usage_events` table (via `keystore.usage_summary` /
`keystore.list_usage`) to produce invoices. This module produces the ledger —
it does not itself charge anyone.

## Keys and tiers

```bash
python api/manage_keys.py create --customer domain:acme --tier deliveryPartner --label "acme prod"
python api/manage_keys.py list
python api/manage_keys.py revoke <raw-key>
```

`--tier` reuses the tiers from
[`docs/partnership-model.md`](../docs/partnership-model.md#partnership-tiers)
(`vendor`, `provider`, `certifiedProvider`, `deliveryPartner`,
`strategicPartner`, `ecosystemPartner`) so a key's tier means the same thing
here as it does in a partnership contract, instead of inventing a parallel
scheme. The API does not yet enforce different behavior per tier — today
every valid key gets the same rate limit and the same routes — but the field
is there so tier-based limits (e.g. higher rate limits for certified
providers) can be added without a schema change.

Raw keys are shown exactly once, at creation. Only a SHA-256 hash is
persisted; there is no recovery path for a lost key, only reissue.

## What's deliberately not here

- **Multi-tenant isolation of graph data.** Callers send their own graph in
  every request body; nothing is stored server-side except usage metadata
  (service, unit type, status, small detail blob — never the graph itself).
  There is no "save my graph on the server" endpoint yet.
- **Per-tier rate limits or pricing enforcement.** The tier is recorded; it
  isn't yet used to change behavior.
- **TLS termination.** Run this behind a reverse proxy / load balancer that
  terminates TLS; the server itself speaks plain HTTP.
- **Horizontal scaling of rate limiting.** The limiter is an in-memory
  per-process counter — correct for a single instance, not for multiple
  replicas behind a load balancer without a shared store. Fine for the wedge
  stage; would need moving to the SQLite table (or Redis) before running more
  than one instance.

## Tests

```bash
python api/test_api.py -v
```

Spins up the real server (the actual `Handler`, not a mock) on an ephemeral
localhost port and drives it over HTTP with `urllib` — auth, the full
compile→validate→grade→migrate pipeline, query, per-key usage isolation, rate
limiting, and the oversized-body rejection path.
