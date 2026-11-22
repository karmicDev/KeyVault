# KV-008 – Mini CA (root + intermediate per organisation)

Status: Ready
Evening: 3 · SPEC: F4, Q6, Q7

## Goal

The backend can verify a CSR and issue an X.509 certificate signed by the
organisation's intermediate CA, chaining up to one root CA.

## Scope

In:
- Root CA (P-256) created once on first start; private key in a git-ignored file under `backend/secrets/`.
- Intermediate CA per organisation, created when the organisation is created; stored in the `organisation` table (cert) + key file.
- `issue_certificate(org, member, csr_der)`:
  - verify the CSR signature (proof of possession), require P-256 public key;
  - subject: `CN=<member e-mail>, O=<organisation name>, OU=<organisation id>`;
  - validity 1 year; key usage `digitalSignature`; extended key usage `clientAuth`.
- `verify_chain(cert, org)` used later for login verification.

Out:
- HTTP endpoints (KV-009), revocation lists (out of scope).

## Acceptance criteria

- [ ] A CSR with a valid signature yields a certificate that chains to the org's intermediate and the root.
- [ ] A CSR with a broken signature, a non-P-256 key or a malformed DER is rejected.
- [ ] A certificate of org A fails `verify_chain` for org B (tenant isolation in the PKI).
- [ ] CA private keys are never written to the database or logs.

## Check

```bash
cd backend
pytest -k ca
ruff check .
```

## Notes

- Library: `cryptography`.
- Fallback if time is short (Q6): single CA, org in subject – then the chain test becomes a subject check.
