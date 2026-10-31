# KRC Stage131 — owner-side 1–4 implementation checkpoint (2026-10-31)

**Scope:** source-only, opt-in staging. FREE_ONLY. Production NO-GO. No live Stage131 mutation, user grant, key export, or scientific dispatch.

## 1. Artifact TTL and ownership
Re-executed existing concrete `HardenedExchange.read_stream` tests: `tests/test_stage131_artifact_get_denials.py`. Covers expiration by injected clock (EXPIRED), mutated payload integrity failure, wrong principal or request_id (NOT_FOUND), bad artifact ID and oversized chunks. This tests real exchange implementation with temporary isolated storage; **not installed service or external HTTP**. Note physical expiration enforcement in read_stream precedes delivery. Source also includes cleanup_expired and ownership-scoped retrieval.

## 2. Correlated science result
Added `src/krc_research/stage131_correlated_dispatch.py` and `tests/test_stage131_correlated_dispatch.py`. The fail-closed adapter accepts injected, already authorized dispatch, requires task_id from the request, validates returned task_id+operation+status+scientific_approval=false+engine_result, rejects malformed/cross-task output before return. **Not wired to deployed service; not permission to dispatch.** Final enabled signer-entrypoint still must integrate after review and owner consent.

## 3. External artifact GET: PROPOSED CONTRACT, ROUTE DISABLED
- Sole allowed public ingress remains Sentinel Stage127 Tailnet `:19017`; no direct KRC backend exposure.
- A future GET requires Sentinel authentication and scoped OIDC/identity verification for the same principal/repository/workflow, not just URL or `X-KRC-Request-ID`. That header is a selector, **not a credential**.
- Server-side identity must be projected through signed authenticated UDS context, scoped to immutable `artifact_id + request_id + principal`; unknown or cross-principal lookup must deny without leaking object metadata.
- At retrieval time verify expiry against the trusted server clock (`expires<=now` deny), integrity SHA-256 and size, ownership, request ledger binding and replay policy. Return streaming octets only after preflight; do not expose internal file paths or Science HMAC. HTTP 403/404/410/429/5xx mapping, audit logging, no credential echo, size limits and idempotency require formal Sentinel ACK.
- **No external GET route was implemented or activated** pending cross-project API approval.

## 4. Consent and signer verification, no activation
- `ConsentCustody128` uses root-owned grant files with context SHA256 matching, approver, issue/expiry, one-time consumed replay ledger and checks reject untrusted directory/file permissions. No grant was issued in this task.
- `KRCInternalScienceSigner` validates operation+payload and delegates authorization to independent custody; only then signs internal science envelope. The existing staging entrypoint **hard-denies enabling signing**; an enabled reviewed entrypoint with grant issue/revoke/expiry and deployment equivalence is still REQUIRED before any legitimate science E2E. This task did not enable signing.
- For actual operator grant issuance, explicit user-scoped authorization and reviewed request context are prerequisites. No client Boolean substitutes for owner consent.

## Validation
Hash-locked development venv on krc-cobalt: combined tests `tests/test_stage131_correlated_dispatch.py`, `tests/test_stage131_consumer_boundary_checks.py`, `tests/test_stage131_artifact_get_denials.py`, `tests/test_consent_custody128.py`, `tests/test_science_signer127.py`, `tests/test_stage131_consent_path.py`, `tests/test_stage128_internal_signer_live_uds.py`: **32/32 PASS**. No general KRC full regression claimed.

Installed runtime Stage131 pinned `49f8b857b46ebdf45636deffe90f8a4ee578bddf`, unchanged. 48 real scientific E2E NOT_RUN. Source-only handoff requires K_Science/Sentinel independent ACK.
