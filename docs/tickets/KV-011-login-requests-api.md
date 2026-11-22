# KV-011 – Login requests API (challenge, verification)

Status: Ready
Evening: 3 · SPEC: F5, Q8, Q9, Q10

## Goal

The backend can create a login request for a member, the app can fetch and
approve/deny it, and the backend verifies the signature with the member's
certificate.

## Scope

In:
- Table `login_request` (migration).
- `POST /admin/organisations/{org_id}/members/{member_id}/login-requests` `{display_text}` → request id.
- `GET /admin/login-requests/{id}` → status.
- `GET /device/login-requests` (device token) → pending requests incl. `payload` (base64 of the exact bytes to sign).
- `POST /device/login-requests/{id}/approve` `{signature}` and `POST …/deny`.
- Payload: compact JSON, sorted keys: `request_id`, `organisation_id`, `challenge` (32 random bytes, base64url), `created_at`, `display_text`.
- Verification: certificate chain valid for the org (KV-008), enrollment not disabled, request pending and not expired (60 s), signature over the stored payload bytes.

Out:
- App UI (KV-012).

## Acceptance criteria

- [ ] Valid signature → `approved`; any other outcome → `failed` with reason in the server log only.
- [ ] Replay: approving an already decided request fails.
- [ ] Expired request (time injected in tests) cannot be approved.
- [ ] Tenant isolation: a device token of org A neither sees nor approves requests of org B.
- [ ] Signature from a different key of the same member (other org) is rejected.

## Check

```bash
cd backend
pytest
ruff check .
```
