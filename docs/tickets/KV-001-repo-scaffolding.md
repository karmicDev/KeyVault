# KV-001 – Repository scaffolding

Status: Ready
Evening: 1 · SPEC: §7

## Goal

The repository has its basic files and a running PostgreSQL via docker-compose.

## Scope

In:
- `README.md` stub: one-paragraph description, "Status: work in progress", out-of-scope list from SPEC §6, link to `docs/SPEC.md`.
- `LICENSE` (MIT, year 2026, copyright holder name confirmed by the maintainer).
- `.gitignore` for macOS, Python, Flutter/Dart, Xcode, Android/Gradle, `.env`, CA key files (`*.key`, `backend/secrets/`).
- `docker-compose.yml` with a `db` service: PostgreSQL 16, named volume, healthcheck, port 5432 on localhost only.
- `.env.example` with `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `ADMIN_PASSWORD`.

Out:
- No backend or app code.

## Acceptance criteria

- [ ] `docker compose up -d db` starts PostgreSQL and the container becomes `healthy`.
- [ ] `.env` is ignored by git; `.env.example` is committed.
- [ ] README states clearly what is out of scope.

## Check

```bash
cp .env.example .env
docker compose up -d db
docker compose ps          # db must show "healthy"
git status --ignored       # .env listed as ignored
```

## Notes

- Port bound to `127.0.0.1:5432` so the database is not reachable from the LAN.
