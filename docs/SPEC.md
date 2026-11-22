# KeyVault – Specification

Status: **v0.3** – all questions decided; *Why (draft)* rationales still to be rewritten by the maintainer · Leading document for all tickets (see `AGENTS.md`).

How to read this document:

- **Decision** – what we build.
- **Why** – the rationale. Marked *(draft)* until the maintainer has rewritten it in his own words.
- **Decision (Qn)** – a decision taken from a question in §8, where the options, pros, cons and trade-offs are kept as a record.

---

## 1. Purpose

KeyVault is a mini credential wallet for iOS and Android. Users join an
organisation by scanning an invitation QR code. The app creates a private key
in secure hardware, receives an X.509 certificate from the organisation's
backend, and approves login requests by signing them after a biometric check.

**Why** *(draft)*: Hardware-bound keys plus certificates are the basis of
modern passwordless login and smart-card replacements. The project shows the
full chain end to end: native key handling in Swift and Kotlin, a Flutter UI,
a small PKI and a multi-tenant backend.

## 2. Glossary

| Term | Meaning |
|---|---|
| Organisation | A tenant. Users, keys, certificates and login requests always belong to exactly one organisation. |
| Member | A user of an organisation, identified by e-mail and display name. |
| Enrollment | The result of onboarding: one key + one certificate for one member in one organisation on one device. |
| Invitation | A single-use token, shown as QR code, that allows one member to enroll. |
| Login request | A challenge the backend asks the member to approve by signing it. |
| Mini CA | The backend component that turns a CSR into an X.509 certificate. |

## 3. Core flow

```
Admin page          Backend (FastAPI + PostgreSQL)           App (Flutter + Swift/Kotlin)
    |  create invitation  |                                       |
    |-------------------->|  QR: {backend URL, invitation token}  |
    |                     |<------------- scan QR ----------------|
    |                     |                                       | 1. create P-256 key in hardware
    |                     |                                       | 2. build CSR, sign it (biometrics)
    |                     |<------ POST /enroll (token, CSR) -----|
    |                     | verify CSR, issue X.509 cert          |
    |                     |------- certificate + device token --->| 3. store cert, show organisation
    |  trigger login      |                                       |
    |-------------------->| create login request (challenge)      |
    |                     |<---------- poll pending requests -----|
    |                     |                                       | 4. show request, biometrics, sign
    |                     |<------ POST signature ----------------|
    |  shows result       | verify signature with cert public key |
```

## 4. Functional requirements

### F1 – Onboarding via QR code

- **Decision:** The admin creates an invitation for a member in an
  organisation. The backend renders a QR code that contains the backend URL and
  a random, single-use invitation token. The app scans it and enrolls.
- **Why** *(draft)*: Scanning is fast, avoids typing URLs or codes, and binds the
  invitation to one organisation and one member. It mirrors how enterprise
  wallets are rolled out.

- **Decision (Q1):** Invitations are valid for 24 hours, single use (config value). Options and trade-offs: §8.

### F2 – Hardware key per organisation

- **Decision:** For each enrollment the app creates a new ECDSA P-256 key in the
  Secure Enclave (iOS) or Android Keystore. The key is not exportable. The app
  only ever handles the public key and a key alias.
- **Why** *(draft)*: P-256 is the only curve the Secure Enclave supports and is
  available on all Android Keystores, so one algorithm works on both platforms.
  One key per organisation keeps tenants cryptographically separate: a
  compromised or revoked enrollment in one organisation cannot affect another.

- **Decision (Q2):** Android uses the best available Keystore level (StrongBox > TEE > software) and the app shows it. On the emulator keys are software-backed; a production build would require TEE or better. Options and trade-offs: §8.

- **Decision (Q3):** Android is developed and tested on the **emulator only**. iOS is tested on a physical iPhone.
- **Why** *(draft)*: No Android device is available. The emulator supports fingerprint simulation, so the biometric flow can be shown. Consequence: on Android the key is not protected by real secure hardware in this project (see Q2). This is documented in the README.

### F3 – Biometrics on every signature

- **Decision:** Each key requires biometric authentication for every use.
  No device passcode / PIN fallback. iOS: access control `.biometryCurrentSet`.
  Android: `setUserAuthenticationRequired(true)` with authentication per use and
  `BIOMETRIC_STRONG` only.
- **Why** *(draft)*: A signature should prove that the enrolled person was
  present, not just that someone knew the phone's PIN. Binding the check to the
  key in hardware means the app cannot bypass it, even if the Dart code had a bug.

- **Decision (Q4):** Keys are invalidated when biometrics change; the app detects this and offers re-enrollment. Options and trade-offs: §8.

### F4 – CSR and certificate (mini CA)

- **Decision:** The app builds a PKCS#10 CSR. The CSR is signed by the hardware
  key (this is the first biometric prompt). The backend verifies the CSR
  signature, checks the invitation, and issues an X.509 certificate with the
  member and organisation in the subject.
- **Why** *(draft)*: The CSR proves the device holds the private key for the
  public key it submits (proof of possession). A certificate gives the backend
  a signed, standard binding of "this public key belongs to this member of this
  organisation".

- **Decision (Q5):** Dart builds the PKCS#10 CSR; native code only offers `createKey`, `publicKey`, `sign`. Options and trade-offs: §8.

- **Decision (Q6):** One root CA plus one intermediate CA per organisation (fallback to a single CA if the timeline is at risk). Options and trade-offs: §8.

- **Decision (Q7):** Certificates are valid for 1 year; revocation = disabling the enrollment in the database. Options and trade-offs: §8.

### F5 – Login approval (2FA)

- **Decision:** The admin page triggers a login request for a member. The
  backend creates a random challenge. The app polls for pending requests, shows
  who/what is asking, asks for biometrics, signs the challenge and sends the
  signature. The backend verifies it with the public key from the member's
  certificate and marks the request approved or denied.
- **Why** *(draft)*: This is the passwordless / push-2FA pattern. Signing a
  server challenge with a hardware key is phishing resistant and needs no
  shared secret.
- **Why polling** *(draft)*: Real push (APNs/FCM) needs Apple/Google accounts,
  certificates and setup that do not show anything about the core skill. Polling
  shows the same flow; push can replace the transport later.

- **Decision (Q8):** The app signs the exact payload bytes sent by the backend (request id, organisation id, challenge, timestamp, display text). Options and trade-offs: §8.

- **Decision (Q9):** The app polls every 5 s in the foreground; login requests expire after 60 s (config values). Options and trade-offs: §8.

- **Decision (Q10):** Enrollment returns a device token for reading pending requests; approving always requires the biometric signature. Options and trade-offs: §8.

### F6 – Multiple organisations

- **Decision:** A user can be enrolled in several organisations. The app shows a
  list and lets the user switch the active organisation. Each has its own key,
  certificate and login requests.
- **Why** *(draft)*: Mirrors workspaces in enterprise wallets and makes tenant
  separation visible in the UI.

- **Decision (Q11):** Users can leave an organisation in the app (delete key + disable enrollment); late, low-priority ticket. Options and trade-offs: §8.

### F7 – Admin page

- **Decision:** FastAPI serves a simple server-rendered web page: create
  organisations, create invitations (show QR), list enrollments, trigger a login
  request and see its result.
- **Why** *(draft)*: Needed to demo the flow in a video or screenshots without
  building a second app. Plain HTML keeps the focus on the mobile side.

- **Decision (Q12):** Admin page uses HTTP Basic auth with a password from an environment variable; real admin login (C) is an optional later ticket. Options and trade-offs: §8.

## 5. Non-functional requirements

| Area | Requirement |
|---|---|
| Security | Private keys never leave the secure key store. No key material or tokens in logs. Android emulator keys are software-backed (Q2). |
| Tenant isolation | Every backend query is filtered by organisation. Tests prove a member of org A cannot see or approve requests of org B. |
| Replay protection | Challenges are ≥ 128 bit random, single use, expire. |
| Platforms | iOS and Android from the start. Minimum iOS 16, Android 11 (API 30) – see Q13 in §8. |
| Transport | HTTPS in a real deployment. Local demo over HTTP on the LAN is acceptable and documented. |
| Testing | pytest for CA and signature checks; Dart unit tests; widget tests; integration tests. GitHub Actions on every push. |
| Code quality | `flutter analyze` and `ruff` clean. |

## 6. Out of scope

Listed in the README as well.

- NFC / HCE (door access) and BLE
- Real push notifications (APNs / FCM)
- App Store / Play Store release
- Certificate renewal, CRL / OCSP
- Key backup or migration to a new device
- Production hardening of the admin page

## 7. Architecture overview

- **app/** – Flutter. Riverpod for state, GoRouter for navigation.
  A `KeyStore` platform channel (`createKey`, `publicKey`, `sign`) with
  implementations in Swift and Kotlin. Everything else in Dart.
- **backend/** – FastAPI. Modules: organisations, invitations, enrollment
  (mini CA), login requests, admin page. PostgreSQL via docker-compose.
  Crypto with the `cryptography` library.

### Data model (first sketch)

| Table | Key columns |
|---|---|
| organisation | id, name, ca_cert, ca_key_ref |
| member | id, organisation_id, email, display_name |
| invitation | id, organisation_id, member_id, token_hash, expires_at, used_at |
| enrollment | id, organisation_id, member_id, certificate_pem, device_token_hash, created_at, disabled_at |
| login_request | id, organisation_id, member_id, challenge, status, created_at, expires_at, signature |

## 8. Decision records

Each question lists the options with pros, cons and the main trade-off, the
recommendation and the accepted answer. The decision itself is summarised in §4/§5;
this section keeps the reasoning.

### Q1 – Invitation lifetime

How long can an invitation QR code be used?

- **A – 15 minutes, single use**
  - Pro: A leaked photo of the QR code is useless almost immediately.
  - Con: Only works if the admin shows the code live; sending it by e-mail is impractical.
- **B – 24 hours, single use**
  - Pro: Can be sent by e-mail or chat and used the same day.
  - Con: A leaked code works for a day (but only once, and only for one member).
- **C – 7 days, single use**
  - Pro: Most convenient for real rollouts.
  - Con: Longest attack window; invitations pile up and need cleanup.

Trade-off: security window vs. convenience. Because tokens are single use and
bound to one member, the risk of a longer lifetime is limited.
Recommendation: **B**. Lifetime is a config value, so it is cheap to change.
Answer: **B** – accepted 2026-11-23.

### Q2 – Android hardware security level

Which Keystore security level is accepted on Android?

- **A – StrongBox only**
  - Pro: Separate secure chip, closest to the iOS Secure Enclave.
  - Con: Many devices and **every emulator** lack it – the app would not run on Android at all in this project (see Q3). Signing is slower.
- **B – Best available level, shown in the app**
  - Pro: Runs everywhere, including the emulator. Honest: the UI and the CSR/backend record show `StrongBox`, `TEE` or `Software`.
  - Con: On the emulator the key is effectively software-backed, so "keys never leave the hardware" is only true on real devices. One extra code path to detect the level.
- **C – TEE or better, reject software keys**
  - Pro: Clear minimum guarantee on real devices.
  - Con: The emulator would be rejected, so Android could not be tested.

Trade-off: strict guarantee vs. being able to run Android at all with only an emulator.
Recommendation: **B**, plus a documented rule: "a production build would enforce C".
Optional later ticket: verify Android key attestation on the backend.
Answer: **B** – accepted 2026-11-23.

### Q4 – What happens when biometrics change?

If a new fingerprint or face is enrolled on the phone, should existing keys stay valid?

- **A – Invalidate the key** (iOS `.biometryCurrentSet`, Android `setInvalidatedByBiometricEnrollment(true)`)
  - Pro: Someone who knows the phone passcode cannot add their own finger and then sign.
  - Con: The user must re-enroll each organisation after changing biometrics; the app needs a "key invalid → re-enroll" flow.
- **B – Keep the key valid** (iOS `.biometryAny`, Android `setInvalidatedByBiometricEnrollment(false)`)
  - Pro: No re-enrollment, simpler.
  - Con: The biometric check then only proves "some enrolled biometric", which the passcode holder controls.

Trade-off: strong binding to the enrolled person vs. user friction.
Recommendation: **A** – it is what high-security customers (police, defence) expect.
Answer: **A** – accepted 2026-11-23.

### Q5 – Where is the CSR built?

- **A – Dart builds the CSR, native code only signs**
  - Pro: One implementation for both platforms, unit-testable with `flutter test`. Native API stays tiny: `createKey`, `publicKey`, `sign`.
  - Con: ASN.1/DER encoding in Dart (library or hand-written); encoding bugs are possible and must be covered by tests (the backend parsing the CSR is the real check).
- **B – Native code builds the CSR**
  - Pro: Everything crypto-related stays native.
  - Con: Two implementations (Swift and Kotlin), neither platform has a built-in CSR builder, so it is manual ASN.1 twice or BouncyCastle on Android.
- **C – No CSR: send public key + signed nonce, backend builds the certificate**
  - Pro: Least code.
  - Con: Not the PKCS#10 standard; loses the "real PKI" part that matters for the job.

Trade-off: amount of native code vs. control over encoding.
Note: both platforms produce DER-encoded ECDSA signatures over SHA-256 of the input
(iOS `ecdsaSignatureMessageX962SHA256`, Android `SHA256withECDSA`), so the same
Dart code works for both.
Recommendation: **A**.
Answer: **A** – accepted 2026-11-23.

### Q6 – CA hierarchy

- **A – One CA for all organisations, organisation in the certificate subject**
  - Pro: Simplest; one CA key.
  - Con: Tenant separation depends only on checking the subject/database. A bug that skips that check would accept an org-A certificate in org B.
- **B – One root CA + one intermediate CA per organisation**
  - Pro: Separation is cryptographic: a certificate only validates against its own organisation's intermediate. Realistic, like real enterprise PKIs.
  - Con: Chain building and path validation, more keys to store, more tests (about 1–2 hours extra).
- **C – Independent root CA per organisation**
  - Pro: Strong separation, simple verification per organisation.
  - Con: No common trust anchor; less realistic.

Trade-off: realism and defence in depth vs. time.
Recommendation: **B**; fall back to **A** if the timeline is at risk.
CA private keys are stored in a git-ignored file in development (no HSM – out of scope).
Answer: **B** – accepted 2026-11-23.

### Q7 – Certificate validity and revocation

- **A – 1 year validity, revocation = disable the enrollment in the database**
  - Pro: Simple. The backend is the only relying party, so a database check is enough.
  - Con: Not standard revocation; no other system could check it.
- **B – Short-lived certificates (e.g. 30 days) with renewal**
  - Pro: Limits damage of a lost device without a revocation infrastructure.
  - Con: Needs a renewal flow (new CSR, biometric prompt) and handling of expired certificates.
- **C – CRL or OCSP**
  - Pro: The standard way; shows PKI depth.
  - Con: Much work, and there is no external relying party to use it.

Trade-off: PKI completeness vs. scope.
Recommendation: **A**, with B and C listed as out of scope.
Answer: **A** – accepted 2026-11-23.

### Q8 – What exactly is signed for a login approval?

- **A – Only the random challenge**
  - Pro: Simplest. Already replay-safe, because challenges are single use and keys are per organisation.
  - Con: The signature says nothing about *what* was approved; the app could display one thing while the signature covers another.
- **B – A structured payload: request id, organisation id, challenge, timestamp and the text shown to the user** (e.g. "Login to Demo Portal")
  - Pro: "What you see is what you sign" – the signature binds to the displayed request. Defence in depth against mix-ups.
  - Con: Needs a canonical byte format. Rule: the backend sends the exact bytes (base64); the app parses them for display and signs those bytes unchanged, so no re-encoding mismatch is possible.

Trade-off: simplicity vs. a signature that proves what the user approved.
Recommendation: **B**.
Answer: **B** – accepted 2026-11-23.

### Q9 – Polling and expiry timing

- **Polling interval**
  - 2 s: near-instant, but more requests and battery.
  - 5 s: feels quick enough for a demo, modest load.
  - 15 s: cheap, but feels slow in a demo.
  - Alternative – long polling / Server-Sent Events: near-instant with few requests, but more backend complexity and fragile on mobile networks.
- **Request expiry**
  - 60 s: small attack window; the user must react quickly.
  - 120 s: more relaxed, still short.
  - 5 min: comfortable but a long window for a request someone else triggered.

Note: iOS does not allow reliable background polling, so the app only polls in
the foreground. The user opens the app to approve (fine for the demo; real push is out of scope).
Trade-off: responsiveness vs. load; user time vs. attack window.
Recommendation: **5 s polling, 60 s expiry**, both config values.
Answer: **5 s / 60 s** – accepted 2026-11-23.

### Q10 – How does the app authenticate when polling?

Signing every poll with the biometric key would show a prompt every 5 s.

- **A – Device token issued at enrollment**
  - Pro: Simple and standard. Stored in Keychain / EncryptedSharedPreferences, only a hash in the database. Can only *read* pending requests; approving still requires the biometric signature.
  - Con: A stored secret: if stolen, an attacker can see pending requests (but not approve them).
- **B – A second hardware key without biometrics, used only to sign poll requests**
  - Pro: No stored secret; nothing to steal.
  - Con: Two keys per organisation, more native code, plus a request-signing scheme (nonce/timestamp) on the backend.
- **C – No authentication, poll by member id**
  - Pro: No work.
  - Con: Anyone can read anyone's pending requests. Not acceptable.

Trade-off: simplicity vs. not storing any secret.
Recommendation: **A**; B as an optional later ticket.
Answer: **A** – accepted 2026-11-23.

### Q11 – Leaving an organisation in the app

- **A – In the app: delete the key and tell the backend to disable the enrollment**
  - Pro: Clean lifecycle; shows key deletion on both platforms.
  - Con: Extra ticket; offline case (delete locally, retry backend call).
- **B – Delete locally only**
  - Pro: Little work.
  - Con: The backend still considers the enrollment active.
- **C – Not in the app; only the admin can disable enrollments**
  - Pro: No app work.
  - Con: Users cannot clean up; re-enrolling into the same organisation needs admin help.

Trade-off: completeness vs. time.
Recommendation: **A**, as a late, low-priority ticket.
Answer: **A** – accepted 2026-11-23.

### Q12 – Admin page authentication

- **A – HTTP Basic auth, password from an environment variable**
  - Pro: About ten lines of code, enough for a demo.
  - Con: One shared admin for all organisations (no per-organisation admin roles); over plain HTTP on the LAN the password is visible on the network.
- **B – No authentication, admin routes only reachable from localhost**
  - Pro: No secret to manage.
  - Con: The phone must reach the API over the LAN, so the localhost restriction must be done carefully per route; easy to get wrong.
- **C – Real login with admin users per organisation (sessions, password hashing)**
  - Pro: Matches the job's "SaaS backend with login and tenants" requirement and makes tenant isolation visible on the admin side too.
  - Con: Several hours of work that is not mobile-related.

Trade-off: time vs. showing SaaS backend skills.
Recommendation: **A** now; **C** as an optional ticket after the application is sent.
Answer: **A** – accepted 2026-11-23.

### Q13 – Minimum OS versions

- **iOS**
  - iOS 15: more devices; nothing in this project needs newer APIs.
  - iOS 16: covers nearly all active iPhones; the test iPhone runs a current version anyway.
  - iOS 17: newest SwiftUI/API niceties not needed here (UI is Flutter).
- **Android**
  - API 28 (Android 9): BiometricPrompt and StrongBox exist, but per-use biometric keys need the older `setUserAuthenticationValidityDurationSeconds(-1)` path – two code paths.
  - API 30 (Android 11): `setUserAuthenticationParameters(0, AUTH_BIOMETRIC_STRONG)` – one clean code path; still covers the large majority of active devices.

Trade-off: device reach vs. simpler, more testable native code. With only an
emulator (Q3), an untested legacy code path would be risky.
Recommendation: **iOS 16, Android 11 (API 30)** – this changes the earlier proposal (Android 9).
Answer: **iOS 16 / API 30** – accepted 2026-11-23.

## 9. Change log

| Version | Date | Change |
|---|---|---|
| 0.1 | 2026-11-23 | First draft from the decisions of 2026-11-22. |
| 0.2 | 2026-11-23 | Open questions moved to §8 with options, pros, cons and trade-offs. Q3 decided: Android emulator only. |
| 0.3 | 2026-11-23 | All recommendations in §8 accepted; §4 updated with decisions. |
