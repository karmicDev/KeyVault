# KV-006 – Key store platform channel: Dart API + iOS (Secure Enclave)

Status: Ready
Evening: 2 · SPEC: F2, F3, Q4, Q5 · AGENTS.md rules 1–3

## Goal

Dart can create a biometric-bound P-256 key in the Secure Enclave, read its
public key and sign bytes – without the private key ever leaving the enclave.

## Scope

In:
- Dart interface `KeyStore` with `createKey(alias)`, `publicKey(alias)` (X9.63 / uncompressed point), `sign(alias, bytes, reason)` (DER ECDSA SHA-256), `deleteKey(alias)`.
- Typed errors: `KeyNotFound`, `KeyInvalidated` (biometrics changed, Q4), `UserCancelled`, `BiometryNotAvailable`.
- `MethodChannelKeyStore` + `FakeKeyStore` for tests (fake uses a software key **only in tests**).
- Swift implementation: `SecKeyCreateRandomKey` with `kSecAttrTokenIDSecureEnclave`, access control `.privateKeyUsage + .biometryCurrentSet`; signing with `ecdsaSignatureMessageX962SHA256`; `NSFaceIDUsageDescription`.
- Debug screen (debug builds only): create key, show public key, sign "hello", show signature.

Out:
- Android (KV-007), CSR (KV-010).

## Acceptance criteria

- [ ] On the iPhone: create → sign triggers Face ID / Touch ID every time; cancelling returns `UserCancelled`.
- [ ] The signature verifies against the public key (verification in a Dart unit/integration test with `pointycastle`, public key only).
- [ ] Two aliases produce two different keys.
- [ ] After adding a new face/finger, `sign` returns `KeyInvalidated` (manual test, documented in the ticket).
- [ ] Dart unit tests for the channel mapping (method names, error codes) pass.

## Check

```bash
cd app
flutter analyze
flutter test
flutter run -d <iphone>   # manual: debug screen
```

## Notes

- Simulator has no Secure Enclave: the Swift code returns `BiometryNotAvailable` there.
