# KRC field-level response to K_Sentinel signed Artifact GET candidate — 2026-10-31

Source evidence reviewed:
- Sentinel candidate pin `faa8b9f9a9f1419f932197d8bbd4a93b61070d7e`; `schemas/stage127/artifact_get_signed_request_v1.schema.json`, `artifact_get_error_v1.schema.json`, `docs/STAGE127_GET_SIGNED_WIRE_SOURCE_CANDIDATE_2026-10-31.md`.
- KRC source pin `72e114e5e169bb32f557db672922d0e4fbf149a3`: `src/krc_research/uds_verified123b.py`, `uds_stage123.py`, `artifact_stage117.py`.

## Field-level ACK / MISMATCH / BLOCKED
| Field or behavior | Verdict | KRC evidence / condition |
|---|---|---|
| Sentinel `version=krc-transport/2` | MISMATCH | Existing signed POST envelope; not a GET authorization |
| Sentinel `operation=artifact.get` | MISMATCH | VerifiedStage123Handler accepts only science OPS on POST; no approved artifact.get dispatch |
| `identity.client/principal/repository/workflow_ref` | ACK_DESIGN_ONLY | Requires server-derived identity, MAC binding, peer UID, exact workflow and request/ledger verification |
| `payload.artifact_id/request_id` | ACK_DESIGN_ONLY | Both must bind to principal + RequestLedger and stored object |
| `transport_auth.alg/key_id/issued_at/mac` | BLOCKED | Only shape candidate; no GET-specific canonicalization, key scope, freshness window and replay proof |
| Internal UDS GET /v1/artifacts/{artifact_id} | ACK_SOURCE_EXISTENCE | Inherited Stage123Handler.do_GET uses peer principal and X-KRC-Request-ID selector; distinct from signed envelope proposal |
| GET response 200/404/410 + byte preflight | BLOCKED | No server-observed signed GET; existing handler maps ExchangeError to 404, and may stream after only generator preflight, not adopted as external 410 |
| Error schema `{error: CODE}` | ACK_EXTERNAL_DESIGN_ONLY | Cannot assert KRC internal UDS server outputs exact external codes |
| Sentinel 22 shape checks | ACK_REPORTED_ONLY | Not live GET HMAC/endpoint/negative tests |

## Required wire freeze
1. Choose one VERSIONED mechanism, preferably a separately scoped signed internal retrieval operation/endpoint, with explicit request/response protocol (do not rebrand science POST). Endpoint, method, auth canonical JSON bytes, MAC verification rules, binding to OIDC-derived identity and trusted SO_PEERCRED, key rotation and nonce/jti replay must be specified AND implemented before ACK.
2. On KRC: durable scope binding artifact_id+request_id+principal+RequestLedger and owner proof; server trusted-clock TTL with expiry <= now denial; full file digest and size before first byte; no unauthorized data leakage. Server responses for 401/403/404/410, corruption/quota and timeouts must be measured in isolated server integration.
3. K_Sentinel should keep GET DISABLED (404) until independent KRC and K_Science ACK and separate user staging rollout. Do not call new `artifact.get` through existing signed science POST, and do not infer permission from pre-existing unsigned-selector GET.

Result: **SOURCE-ONLY MISMATCH/BLOCKED**. No GET implementation/deployment, signer enablement or production changes. 40 GET negative tests and 48 scientific E2E still NOT_RUN. STAGING ONLY / FREE_ONLY / Production NO-GO.
