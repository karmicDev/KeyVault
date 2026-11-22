# AGENTS.md

Rules for AI coding agents (Claude Code, Codex, …) working in this repository.
Humans: see `README.md`. The leading document for *what* to build is `docs/SPEC.md`.

## Project in one sentence

KeyVault is a mini credential wallet: a Flutter app keeps one hardware-bound
ECDSA P-256 key per organisation, gets an X.509 certificate from a small
FastAPI CA, and approves login requests by signing them after biometric checks.

## Non-negotiable rules

1. **Private keys never leave the secure key store.** Keys are created and used
   only in the Secure Enclave (iOS) or Android Keystore. No export, no logging of
   key material, no "temporary" in-memory keys, no Dart-side crypto libraries
   holding private keys. On Android the best available level is used
   (StrongBox > TEE > software, emulator = software) and must be shown in the
   app (SPEC Q2).
2. **Biometrics on every signature.** The key's access control requires
   biometrics (iOS: `.biometryCurrentSet`; Android: `setUserAuthenticationRequired(true)`
   + `setUserAuthenticationParameters(0, AUTH_BIOMETRIC_STRONG)`). No PIN/passcode
   fallback. Changing biometrics invalidates the key (SPEC Q4).
3. **One key per organisation.** Never reuse a key across organisations.
4. **Stay inside the ticket.** Only change what the current ticket in
   `docs/tickets/` asks for. No refactorings, renames or "drive-by" fixes outside
   its scope — write them down as a suggestion for a new ticket instead.
5. **Spec first.** If a ticket conflicts with `docs/SPEC.md`, stop and ask.
   Do not silently change the spec.
6. **Plan before code.** For every ticket, post a short plan (files, approach,
   tests) and wait for approval before implementing.
7. **No git operations.** Do not run `git commit`, `git push`, create branches
   or PRs. The maintainer reviews, commits (with ticket ID) and pushes.
8. **Explain commands.** When asking the maintainer to run a command, explain
   briefly what it does.
9. **Tests are part of the ticket.** A ticket is done only when its check
   command passes (see the ticket's *Check* section).
10. **Language:** code, comments, docs, tickets and commit messages in English.

## Stack

| Area | Choice |
|---|---|
| App | Flutter (Dart), Riverpod, GoRouter |
| Native | Swift (iOS Platform Channel), Kotlin (Android Platform Channel); native API only `createKey`, `publicKey`, `sign` |
| Min. OS | iOS 16, Android 11 (API 30) |
| Test devices | Physical iPhone; Android emulator only |
| Crypto (device) | Secure Enclave / Android Keystore, ECDSA P-256, SHA-256 |
| Backend | Python, FastAPI, PostgreSQL (docker-compose) |
| PKI | Backend acts as a mini CA: CSR → X.509 certificate |
| Tests | pytest · `flutter test` (unit + widget) · `integration_test` |
| CI | GitHub Actions on every push |

## Repository layout

```
AGENTS.md            # this file
CLAUDE.md            # imports AGENTS.md
README.md
LICENSE              # MIT
docs/SPEC.md         # what the app does and why (leading document)
docs/tickets/        # KV-001, KV-002, … each with acceptance criteria + check
app/                 # Flutter app (ios/ and android/ hold the platform channels)
backend/             # FastAPI service, mini CA, admin page
docker-compose.yml   # PostgreSQL (+ backend)
.github/workflows/   # CI
```

## Commands

> Fill in / correct as the tickets create the projects.

```bash
# Backend
docker compose up -d db            # start PostgreSQL
cd backend && pytest               # backend tests
cd backend && ruff check .         # backend lint

# App
cd app && flutter pub get
cd app && flutter analyze          # Dart lint
cd app && flutter test             # unit + widget tests
cd app && flutter test integration_test   # integration tests (device/emulator)
```

## Ticket workflow

1. Read the ticket in `docs/tickets/KV-XXX-*.md` and the relevant part of `docs/SPEC.md`.
2. Post a plan; wait for approval.
3. Implement in small steps, explaining each step.
4. Run the ticket's check command; all acceptance criteria must be met.
5. Hand over. The maintainer commits as `KV-XXX: <summary>`.

## Security notes for code review

- Verify signatures on the backend with the public key from the issued
  certificate, never with a key sent alongside the request.
- Login challenges are random (≥ 128 bit), single use and expire.
- Every backend query is scoped to an organisation (tenant isolation).
- Do not commit secrets. The CA's private key for development lives in a
  git-ignored file or environment variable.
