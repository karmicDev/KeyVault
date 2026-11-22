# KV-007 – Key store platform channel: Android (Keystore)

Status: Ready
Evening: 2 · SPEC: F2, F3, Q2, Q3, Q4, Q13

## Goal

The same Dart `KeyStore` API works on Android, using the best available
Keystore level and reporting it.

## Scope

In:
- Kotlin implementation of `createKey`, `publicKey`, `sign`, `deleteKey`:
  - `KeyGenParameterSpec` EC P-256, `PURPOSE_SIGN`, `DIGEST_SHA256`,
    `setUserAuthenticationRequired(true)`, `setUserAuthenticationParameters(0, AUTH_BIOMETRIC_STRONG)`,
    `setInvalidatedByBiometricEnrollment(true)`, try `setIsStrongBoxBacked(true)` first and fall back.
  - Signing via `BiometricPrompt` with a `CryptoObject` (`SHA256withECDSA`).
- New Dart method `securityLevel(alias)` → `strongBox | tee | software` (from `KeyInfo.securityLevel`); iOS returns `secureEnclave`.
- Same error mapping as KV-006.
- Debug screen shows the security level.

Out:
- Key attestation verification (backlog).

## Acceptance criteria

- [ ] On the emulator (with a simulated fingerprint): create → sign asks for the fingerprint every time.
- [ ] The emulator reports `software`; the level is visible on the debug screen.
- [ ] The signature verifies against the public key (same test as KV-006).
- [ ] Enrolling a new fingerprint makes `sign` return `KeyInvalidated`.

## Check

```bash
cd app
flutter analyze
flutter test
flutter run -d emulator-5554   # manual: debug screen
```

## Notes

- Emulator fingerprint: Extended controls → Fingerprint → "Touch sensor".
