# KRC → K_Sentinel Stage127/131 transport reconciliation — 2026-10-31

**SOURCE-ONLY. STAGING ONLY / FREE_ONLY / Production NO-GO.** No Stage127, installed Stage131, consent, signer, provider, port or external GET activation.

## 1. UDS POST /v1/execute — definitive source semantics

The verified Stage123 handler returns HTTP 200 when boundary output.status=completed; otherwise HTTP 409. Early transport/authorization errors may use HTTP 400/403/404/413/415, JSON shape `{"error":"CODE"}`, without request_id. Stage123Handler.send_json sends **HTTP 507** with `{"status":"error","error":{"code":"RESPONSE_TOO_LARGE"}}` when serialized body exceeds 1 MiB.

ResearchBoundary.execute (transport v2):
- INVALID_REQUEST before ledger: `409 {"status":"rejected","error":{"code":"INVALID_REQUEST"}}`, request_id **omitted**. A request_id may appear with rejected LedgerError; the schema allows optional string/null on rejected.
- Ledger refusal including IDEMPOTENCY_CONFLICT: `409 {"status":"rejected","request_id":"...","error":{"code":"IDEMPOTENCY_CONFLICT"}}`.
- Ambiguous ledger: `409 {"status":"pending_reconciliation","request_id":"...","error":{"code":"AMBIGUOUS_REQUEST"}}`.
- Handler exception: `409 {"status":"pending_reconciliation","request_id":"...","error":{"code":"HANDLER_ERROR"}}`; never pretend execution was safely rejected or retry it automatically.
- ExchangeError/LedgerError during dispatch/delivery: `pending_reconciliation` with original error.code and request_id, no implicit execution retry.
- 403 bare OPERATION_DENIED: `{"error":"OPERATION_DENIED"}`.

**Decision:** KRC ACKs the source HTTP codes and structured status/error values above. KRC **MISMATCH** with Sentinel's mapping of 409 INVALID_REQUEST/HANDLER_ERROR to AMBIGUOUS_REQUEST, and 507 RESPONSE_TOO_LARGE to 503 BACKEND_UNAVAILABLE. Correct mapping must retain original `status`, `error.code`, optional `request_id` or expose a versioned external abstraction explicitly preserving meaning. 507 cannot be advertised as ordinary backend downtime. No automatic retry/re-execution for any 409 until explicit reconciliation.

Contract schema: `schemas/stage131/uds_source_errors_v1.schema.json`. Source-emitted **actual in-process** isolated fixtures for INVALID_REQUEST/HANDLER_ERROR/AMBIGUOUS_REQUEST and literal handler shapes for early 403/overflow 507: `docs/integrations/stage131_uds_source_error_fixtures_v1.json`; generator `tools/stage131_source_error_fixtures.py`. NOT live UDS or external HTTP observation.

## 2. Artifact GET v1 — signed-envelope design candidate

Source-only **proposed** envelope `schemas/stage131/artifact_get_signed_uds_envelope_candidate_v1.schema.json` requires version, artifact.read operation, request_id, artifact_id (48 hex), identity(principal,repository,workflow_ref), auth(key_id,issued_at_epoch,nonce,mac_sha256). The JSON Schema validates SHAPE ONLY: **MAC algorithm, canonicalization, identity provenance, SO_PEERCRED, and replay ledger verification are NOT implemented by the schema**. The identity must be derived from independently checked OIDC claims by Sentinel, signed over full canonical envelope and verified by KRC; never accept caller-controlled identity/approval Boolean. Signature key management and nonce replay must be independently attested. GET only via existing Stage127 ingress; do not deploy new listener.

Ownership: KRC must match trusted principal, request_id, artifact_id, ledger and object row. Request ID header is a selector, not credential. GET access cannot issue or impersonate consent for science dispatch.

KRC source HardenedExchange.read_stream checks owner/request, expiry <= trusted clock, full SHA256 and size before releasing bytes from its generator; **but the inherited Stage123 GET is not a finalized authenticated signed artifact-get endpoint**. Final installed byte-stream parity and rollback testing remain pending. Buffered/verified-before-first-byte semantics must be checked in actual approved route.

Candidate external GET statuses: disabled 404; missing/expired token 401; valid but disallowed identity 403; cross-owner/request unknown 404; authenticated verified owner and expired object 410; invalid selector 400; bounded rate 429; quota 413; server failures 500/502/503/504. This is NEW external GET design, not a claim about existing internal Stage123 GET. 40 negatives remain NOT_RUN.

## 3. Science contract
Four operation-specific nested schemas and source-level semantic validation are present. The installed Stage131 runtime still does not run the new semantic gate in its authorized dispatch chain. Immutable admitted task_id and operation correlation, scientific_approval=false, strict evidence/status/metadata-only semantics remain mandatory. No invented inner science ERROR. K_Science independent full semantic ACK and integrated fixture parity remain open.

## 4. Test evidence / acceptance matrix
- `tests/test_stage131_transport_handoff_contract.py` **2/2 PASS**: source-generated 409 error fixture schema, early 403/507 literal branches, GET envelope missing/invalid fields rejection.
- Complete KRC repository: **1085 passed, 17 skipped, 0 failed** on krc-cobalt with PYTHONPATH=src:. and Python stage131 venv (41.40 seconds).
- HTTP/UDS server POST end-to-end and signed GET replay+ownership/expiry/stream not executed in this package; these require Sentinel and authorized isolated integration.

| Requested topic | KRC result | Evidence or blocker |
|---|---|---|
| 403 OPERATION_DENIED | ACK_SOURCE | VerifiedStage123Handler branch |
| 409 IDEMPOTENCY_CONFLICT | ACK_SOURCE_WITH_STATUS_LOSS | LedgerError and external loss requires correction |
| 409 AMBIGUOUS_REQUEST | ACK_SOURCE_WITH_STATUS_LOSS | Ledger ambiguous path |
| 409 INVALID_REQUEST external AMBIGUOUS | MISMATCH | Actual rejected/INVALID_REQUEST |
| 409 HANDLER_ERROR external AMBIGUOUS | MISMATCH | Actual pending_reconciliation/HANDLER_ERROR |
| 507 RESPONSE_TOO_LARGE external 503 | MISMATCH | Actual 507 fallback |
| Source-bound UDS error JSON schema/fixtures | ACK_SOURCE | Separate from live UDS |
| GET candidate signed envelope/error design | ACK_DESIGN_ONLY | MAC verification, signed envelope security, transport tests BLOCKED |
| GET 40 negative cases | BLOCKED_NOT_RUN | GET disabled; Sentinel controls test transport |
| Four science operation semantic schema | ACK_SOURCE_ONLY | independent K_Science final ACK and deployed parity pending |
| 48 scientific E2E | BLOCKED_NOT_RUN | explicit scoped consent, reviewed signer/runtime and partner approval |

## 5. Partner actions
K_Sentinel: correct the 3 mapped errors; preserve 409 status/error and non-retry, publish versioned *actually signed* UDS retrieval envelope/error schemas and field-level negative fixtures; run authorized isolated 40-case tests with live route still OFF; provide ACK/MISMATCH and exact SHA.
K_Science: independently review source-generated science results and error distinctions, ensure 409 never triggers automatic science dispatch, and test artifact consumer only after signed GET contract frozen.
KRC: review partner contracts, wire fail-closed semantic check into independently reviewed runtime, prove trusted ConsentCustody-before-dispatch and immutable request correlation, validate source/installed parity and rollback before any release.

**Activation gate:** separate explicit user approval, source SHA lock, rollback, independent partner acceptance, no production exposure.
