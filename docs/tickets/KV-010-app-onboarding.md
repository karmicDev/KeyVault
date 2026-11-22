# KV-010 – App onboarding: QR scan, CSR, enrollment

Status: Ready
Evening: 3 · SPEC: F1, F2, F4, Q5, Q10

## Goal

The user scans an invitation QR code and ends up with an enrolled organisation
in the app: hardware key, certificate and device token stored.

## Scope

In:
- QR scanning screen (`mobile_scanner`), parse and validate the QR JSON.
- CSR builder in Dart: builds the PKCS#10 `CertificationRequestInfo` (ASN.1/DER), gets it signed by `KeyStore.sign`, assembles the final CSR.
- API client (`http` or `dio`, decide in plan) for `POST /enroll`.
- Persist enrollment: certificate chain + metadata in local storage, device token in `flutter_secure_storage`.
- Key alias per organisation: `keyvault.<organisation id>`.
- Error states: invalid QR, network error, enrollment rejected, biometrics cancelled (delete the half-created key).

Out:
- Multi-organisation switching UI (KV-014), login requests (KV-012).

## Acceptance criteria

- [ ] End to end on the iPhone and the emulator: scan QR from the admin API → organisation appears in the list.
- [ ] CSR unit tests: DER structure matches a known-good fixture; a CSR built with `FakeKeyStore` is accepted by the backend (cross-check test: fixture file used by pytest too).
- [ ] Widget tests for the error states.
- [ ] No private key material in Dart (code review against AGENTS.md rule 1).

## Check

```bash
cd app && flutter analyze && flutter test
cd backend && pytest -k enroll
```

## Notes

- The phone must reach the backend over the LAN: run uvicorn with `--host 0.0.0.0`; the backend base URL in the QR is the Mac's LAN IP (config value).
- iOS: `NSCameraUsageDescription`; local network permission prompt on first request.
