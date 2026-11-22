# KV-005 – Organisations and members (backend)

Status: Ready
Evening: 1 · SPEC: §2, §5 (tenant isolation), §7 data model, Q12

## Goal

The backend stores organisations and their members, and every query is scoped
to one organisation.

## Scope

In:
- Tables `organisation`, `member` (Alembic migration).
- Admin JSON API, protected by HTTP Basic auth (`ADMIN_PASSWORD`):
  - `POST /admin/organisations`, `GET /admin/organisations`
  - `POST /admin/organisations/{org_id}/members`, `GET /admin/organisations/{org_id}/members`
- A repository/service layer where every member query requires `organisation_id`.
- E-mail unique per organisation (not globally).

Out:
- CA columns on `organisation` (KV-008).
- HTML admin page (KV-013).

## Acceptance criteria

- [ ] Admin endpoints return 401 without or with a wrong password.
- [ ] Creating and listing organisations and members works.
- [ ] Tenant isolation test: listing members of org A never returns members of org B; requesting org B's member via org A's URL returns 404.
- [ ] Same e-mail can exist in two organisations; duplicate in one organisation returns 409.

## Check

```bash
cd backend
pytest
ruff check .
```

## Notes

- IDs: UUIDs (no guessable sequential IDs).
- Password compared with `secrets.compare_digest`.
