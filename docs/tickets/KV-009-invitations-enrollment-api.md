# KV-009 – Invitations and enrollment API

Status: Ready
Evening: 3 · SPEC: F1, F4, Q1, Q10

## Goal

An admin can create an invitation (with QR code), and the app can exchange the
invitation token and a CSR for a certificate and a device token.

## Scope

In:
- Tables `invitation`, `enrollment` (migration).
- `POST /admin/organisations/{org_id}/members/{member_id}/invitations` → invitation id + expiry.
- `GET /admin/invitations/{id}/qr.png` → QR with JSON `{"v":1,"url":"<backend base URL>","token":"<token>"}`.
- `POST /enroll` `{token, csr}` → `{organisation, member, certificate_chain_pem, device_token}`.
- Token and device token: 32 random bytes, only SHA-256 hashes stored.
- Invitation: 24 h, single use (config value).

Out:
- App side (KV-010), HTML admin page (KV-013).

## Acceptance criteria

- [ ] Valid token + valid CSR → certificate + device token; invitation marked used.
- [ ] Reused, expired or unknown token → 400/410 with no details about which (no oracle).
- [ ] Invalid CSR → 400, invitation stays unused.
- [ ] Plain tokens never stored or logged.

## Check

```bash
cd backend
pytest
ruff check .
```
