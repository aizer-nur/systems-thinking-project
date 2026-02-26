# systems-thinking-project

Small FastAPI + SQLite API used to study system behavior under load, errors, and basic security constraints.

## Quickstart

```bash
py -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Run tests

```bash
py -m pytest -v
```

## Endpoints (current)

Public:
- `GET /health`
- (planned) `POST /auth/login`

Notes:
- `GET /notes`
- `POST /notes`
- `GET /notes/{id}`
- `PATCH /notes/{id}`
- `DELETE /notes/{id}`

## Targets + Measurement setup 

| Scenario  | Duration | What I measure                |
| --------- | -------: | ----------------------------- |
| Baseline  |  60–120s | p95 latency, error rate, RPS  |
| Peak      |     120s | p95 latency, error rate, RPS  |
| DB outage |  60–120s | 503 fail-fast + degraded=true |

**Measurement setup**

- Machine: TODO (CPU/RAM/OS)
- Server: uvicorn workers = TODO
- Load tool: `scripts/load_test.py`
- Traffic mix: TODO (e.g., 80% GET / 20% write)

## Evidence

- ✅ CRUD + SQLite + tests (7 passed)
  - Screenshot: `docs/pytest 7 passed.png`
- (TODO: JWT PR, metrics PR, load test report, outage evidence)

## Architecture

```mermaid
flowchart TB
  C[Client] -->|HTTP| API[FastAPI API]
  API --> H[GET /health]
  API --> N[Notes CRUD]
  API --> DB[(SQLite)]
  API --> M[Metrics (planned)]
```

## Repro steps

- Run API: `uvicorn app.main:app --reload`
- Run tests: `py -m pytest -v`
- (planned) Run load test: `py scripts/load_test.py`
- (planned) Export metrics: `GET /metrics/summary` + export script
- (planned) Simulate outage: `SIMULATE_DB_DOWN=1 uvicorn...`

## Known limitations

- SQLite single-writer limits concurrent writes.
- No refresh tokens (JWT expiry planned: 15 min).
- Metrics may be in-memory (lost on restart).
- No Prometheus/Grafana (intentionally kept simple).

## Docs

- docs/runbook.md
- docs/design.md (trade-offs, observability)
- docs/failure_scenario.md
- docs/security.md