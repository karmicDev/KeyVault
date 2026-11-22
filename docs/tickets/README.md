# Tickets

One file per ticket: `KV-XXX-short-name.md`, based on `_TEMPLATE.md`.
Commits reference the ticket: `KV-XXX: <summary>`.
Workflow: see `AGENTS.md` → *Ticket workflow*.

## Ready

| ID | Title | Evening |
|---|---|---|
| [KV-001](KV-001-repo-scaffolding.md) | Repository scaffolding | 1 |
| [KV-002](KV-002-backend-skeleton.md) | Backend skeleton (FastAPI, DB, tests, lint) | 1 |
| [KV-003](KV-003-app-skeleton.md) | Flutter app skeleton (Riverpod, GoRouter) | 1 |
| [KV-004](KV-004-ci.md) | GitHub Actions CI | 1 |
| [KV-005](KV-005-organisations-members.md) | Organisations and members (backend) | 1 |
| [KV-006](KV-006-keystore-ios.md) | Key store channel: Dart API + iOS Secure Enclave | 2 |
| [KV-007](KV-007-keystore-android.md) | Key store channel: Android Keystore | 2 |
| [KV-008](KV-008-mini-ca.md) | Mini CA (root + intermediate per org) | 3 |
| [KV-009](KV-009-invitations-enrollment-api.md) | Invitations and enrollment API | 3 |
| [KV-010](KV-010-app-onboarding.md) | App onboarding: QR, CSR, enrollment | 3 |
| [KV-011](KV-011-login-requests-api.md) | Login requests API | 3 |
| [KV-012](KV-012-app-login-approval.md) | App login approval → **send application** | 3 |

## Backlog (to be written as tickets later)

| ID | Title | Evening |
|---|---|---|
| KV-013 | Admin web page (server-rendered, Basic auth) | 4 |
| KV-014 | Multiple organisations: list, switch, re-enroll after key invalidation | 4 |
| KV-015 | Leave an organisation (Q11) | 4 |
| KV-016 | Integration tests (`integration_test`, app ↔ local backend) | 5 |
| KV-017 | README, screenshots, demo video | 6 |

Optional (after the application is sent):
- Admin login per organisation (Q12 option C)
- Verify Android key attestation on the backend (Q2)
- Second non-biometric key for polling instead of a device token (Q10 option B)
