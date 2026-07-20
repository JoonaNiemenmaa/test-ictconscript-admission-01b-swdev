# AGENTS.md

## Repo overview

Admission test for Finnish Defence Forces ICT Conscript Program (II/26 intake).  
Challenge **01b-swdev-backend-api** — "Unit Logbook" REST API — is implemented under `/submission/`.

```
challenges/              challenge specs (one per role)
sample-data/data.json    seed data for the logbook API
submission/              the actual implementation (FastAPI + SQLModel)
```

## Working in this repo

- **Submission lives in `/submission/`** — all source, tests, and Docker config are there.
- **Challenge spec**: `challenges/01b-swdev-backend-api.MD` — the single source of truth for requirements.
- **Seed data**: `/sample-data/data.json` — 10 sample entries the API should serve.

## Dev commands

Run from `/submission/`:

| Action | Command |
|--------|---------|
| Install deps | `pip install -r requirements.txt` |
| Run tests | `pytest tests.py` |
| Dev server | `fastapi dev backend.py` |
| Prod server | `fastapi run` (Docker uses `fastapi run --entrypoint backend:app`) |
| Build & run | `docker build . && docker run -p 8000:8000 <image>` |

## Stack specifics

- **Framework**: FastAPI 0.139 with `fastapi[standard]` (provides `fastapi run/dev` CLI)
- **ORM/DB**: SQLModel 0.0.39, SQLite (`database.db` at repo root)
- **Tests**: `fastapi.testclient.TestClient`; no test runner config needed, just pytest
- **Python**: 3.13 (Docker base image)

## No CI / lint / typecheck configured

This repo has no CI workflows, no pre-commit, no formatter or typecheck config.  
Only the required stretch goal (unit tests via pytest) is present.

## Key constraints from the challenge

- `GET /entries` — newest first (not implemented in current code)
- `POST /entries` — `title` ≤ 120 chars; server assigns `id` and `isoTime`
- `GET /health` — returns body `"OK"`, status 200
- Dockerfile must work with `docker build . && docker run -p 8000:8000`
- Public deploy URL goes in the repo root README (per submission checklist)
