# Stage131 ↔ Sentinel — authenticated Artifact GET V1 contract candidate (DISABLED)

Status: SOURCE_CONTRACT_ONLY / GET_OFF / SIGNER_OFF / STAGING ONLY / FREE_ONLY / Production NO-GO.

## Endpoint, disabled behavior, provenance
- Candidate external path: `GET /staging/v2/artifacts/{artifact_id}`. While route is disabled, ALWAYS respond 404 with no artifact access; no 405 alternate response.
- External bearer OIDC is verified by Sentinel: GitHub issuer/audience/JWKS, repository, workflow_ref, principal, fresh jti, durable replay and bounded validity. No user-supplied principal is trusted.
- Sentinel derives authenticated identity from claims and submits to KRC via signed UDS envelope with strict peer UID, HMAC/key ID, timestamp and request ID. `X-KRC-Request-ID` is only a selector, NOT an authentication secret. Require artifact_id + request_id + principal + repository + workflow binding against stored ledger.
- KRC obtains the record using its own authenticated ledger and fixed-time checks. Check scope, stored expiry using trusted server clock (deny at expiry <= now), expected SHA-256 and exact size over full bytes BEFORE first byte streaming. Non-verified bytes may never be partially released. Bounded buffers/temp store apply; no implicit redirects, resume or cross-principal fallback.
- Never treat transport status `completed` or verified artifact bytes as a science approval. ConsentCustody must be KRC-owned and enforced before science dispatch, independently of GET access.

## Proposed disabled / enabled error mapping (design, NOT runtime observations)
| Situation | Candidate HTTP |
|---|---|
| GET route disabled (regardless of provided selector) | 404 |
| Malformed request / invalid selector | 400 |
| Missing/invalid/expired bearer OIDC | 401 |
| Valid identity lacking permitted scope / replay | 403 |
| Cross-owner, unknown ID, wrong request, unproven owner | 404 (do not disclose existence) |
| Verified owner, expired artifact, trusted expiry <= clock | 410 |
| Method disallowed when enabled | 405 |
| Request/body size limit | 413 |
| Quota/rate ceiling | 429 |
| KRC unexpected fail-closed internal error | 500 |
| Sentinel ↔ KRC invalid upstream response | 502 |
| KRC service unavailable | 503 |
| Trusted upstream timeout | 504 |

No unauthenticated lookup of ownership, expiry or ledger permitted. Unauthorized conditions must not leak whether artifact exists.

## Replay & restart
Every GET attempt needs a fresh OIDC jti, even a retry. Reusing jti or stale signed UDS identity is denied; replay rejection must survive Sentinel process restart. GET never repeats science dispatch and is not a mutation of consent grant. Verify server audit log includes non-secret request ID, result class, principal identity binding, timestamp and denial reason; never log bearer tokens, signing material or retrieved bytes.

## Separate research boundary errors
Observed KRC inner handler exception → `pending_reconciliation`, `error.code=HANDLER_ERROR` at transport boundary, HTTP 409 in current isolated UDS mapping. Do NOT introduce fictitious `engine_result.status=ERROR`. Distinguish this from proposal above for a FUTURE GET HTTP handler.

## Acceptance still due
- K_Sentinel: finalize versioned signed UDS envelope and error JSON Schema, pinned fixtures and 40 isolated GET negative scenarios with GET OFF; field-level ACK/MISMATCH.
- K_Science: error consumer mapping, no automatic retry/redirect/resume, local temp receiver and audit receipt integration; field-level ACK/MISMATCH.
- KRC: trusted-source authentication/consent wiring, live schema parity and independent testing prior to separately approved staging release.
No route or signer activation performed.
