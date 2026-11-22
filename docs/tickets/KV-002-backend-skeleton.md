# KV-002 – Backend skeleton (FastAPI, DB, tests, lint)

Status: Ready
Evening: 1 · SPEC: §7

## Goal

A FastAPI service in `backend/` that connects to PostgreSQL, has a health
endpoint, database migrations, tests and linting.

## Scope

In:
- `backend/pyproject.toml` with dependencies and tool config (pytest, ruff).
- App factory, settings from environment (`pydantic-settings`).
- SQLAlchemy 2 + Alembic, first empty migration.
- `GET /health` returns `{"status": "ok", "db": "ok"}` (runs `SELECT 1`).
- pytest setup with a separate test database and a test client fixture.

Out:
- No domain models yet (KV-005).
- No Dockerfile for the backend yet (runs locally with uvicorn).

## Acceptance criteria

- [ ] `uvicorn` starts the app; `/health` returns 200 with DB ok.
- [ ] `/health` returns 503 with `"db": "error"` when the database is down (test).
- [ ] `alembic upgrade head` runs against the docker database.
- [ ] pytest and ruff pass.

## Check

```bash
docker compose up -d db
cd backend
pytest
ruff check . && ruff format --check .
```

## Notes

Proposals to confirm in the plan:
- Python 3.12, virtual environment in `backend/.venv`, install with `pip install -e ".[dev]"`.
- Synchronous SQLAlchemy (simpler than async; load is tiny).
