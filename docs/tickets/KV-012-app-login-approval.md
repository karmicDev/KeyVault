# KV-012 – App login approval (polling, biometric signature)

Status: Ready
Evening: 3 · SPEC: F3, F5, Q8, Q9 · **Milestone: core flow works → send application**

## Goal

While the app is open, a login request triggered on the backend appears within
seconds, and the user approves it with biometrics or denies it.

## Scope

In:
- Polling provider (Riverpod): every 5 s, only while the app is in the foreground (`AppLifecycleState`).
- Request screen: organisation, display text, time left; buttons Approve / Deny.
- Approve: `KeyStore.sign(alias, payloadBytes)` on the exact bytes from the backend, then POST signature.
- Results: approved, denied, expired, key invalidated (→ hint to re-enroll).

Out:
- Background polling / push (out of scope), multi-org switching UI (KV-014).

## Acceptance criteria

- [ ] Demo on the iPhone: trigger via admin API → request visible within ~5 s → Face ID → backend shows `approved`.
- [ ] Same on the emulator.
- [ ] Polling stops in the background and resumes in the foreground (unit test with a fake clock/lifecycle).
- [ ] Widget tests: request screen states (pending, expired, approved, error).
- [ ] The payload is signed byte-for-byte as received (unit test).

## Check

```bash
cd app && flutter analyze && flutter test
```

## Notes

- After this ticket: record a short screen video for the application.
