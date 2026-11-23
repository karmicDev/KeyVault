# KeyVault

KeyVault is a mini credential wallet for iOS and Android. Users join an
organisation by scanning an invitation QR code. The app creates a private key
in secure hardware (Secure Enclave / Android Keystore), receives an X.509
certificate from the organisation's backend, which acts as a small CA, and
approves login requests by signing them after a biometric check. The app is
built with Flutter (native key handling in Swift and Kotlin), the backend with
FastAPI and PostgreSQL.

**Status: work in progress.**

The full specification is in [`docs/SPEC.md`](docs/SPEC.md).

## Out of scope

This is a showcase project. The following are deliberately not part of it:

- NFC / HCE (door access) and BLE
- Real push notifications (APNs / FCM)
- App Store / Play Store release
- Certificate renewal, CRL / OCSP
- Key backup or migration to a new device
- Production hardening of the admin page
