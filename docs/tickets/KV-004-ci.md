# KV-004 – GitHub Actions CI

Status: Ready
Evening: 1 · SPEC: §5 (testing)

## Goal

Every push runs backend and app checks on GitHub, so every later ticket is
verified automatically.

## Scope

In:
- `.github/workflows/ci.yml` with two jobs:
  - `backend`: Python 3.12, PostgreSQL service container, `ruff`, `pytest`.
  - `app`: Flutter stable, `flutter analyze`, `flutter test`.
- Status badge in README.

Out:
- No integration tests on devices/emulators in CI (KV-016).
- No iOS/Android builds or signing in CI.

## Acceptance criteria

- [ ] A push triggers both jobs; both are green on the current main.
- [ ] A deliberately failing test makes the job red (checked once locally or in a throwaway branch, then reverted).

## Check

```bash
# after the maintainer pushes:
gh run list --limit 1      # status: completed / success
```

## Notes

- Moved earlier than in the original timeline (evening 5 → 1): CI is cheap now
  and protects every following ticket.
- Pin the Flutter version in the workflow to the local `flutter --version`.
