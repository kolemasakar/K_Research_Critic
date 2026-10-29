# KRC independent Stage127 T5 handoff response — 2026-10-29

## Formal decision: ACK_WITH_LIMITATIONS
Scope: **ACK of the single Stage127 external STAGING transport**, not approval of live scientific E2E, external Artifact GET, new production deployment, or installation of Stage131. **FREE_ONLY / Production NO-GO.**

### Evidence pinning
- Sentinel PR #38 head SHA `b1440a999c28234a1db6c40d93e944f27ccd9748`; handoff doc `docs/STAGE127_T5_CLOSURE_KRC_HANDOFF_2026-10-29.md`.
- KRC source review on branch `agent/krc-public-media-r3-integration`, reviewed after owner decision commit `aff22947ab2a8e9c1fe3941ff36a50fe6301ff2c`; KRC source `src/krc_research/uds_verified123b.py`, `transport_auth123b.py`, `research_boundary120.py`, `uds_stage123.py`, `staging_service123c.py`, `staging_backend114.py`.
- Independent read-only krc-cobalt systemd observation: Sentinel Stage127 active PID45059 NRestarts1, Stage126 active PID37979 NRestarts0. Sentinel on-disk Stage127 bounded handler SHA256 `5f82e2ba1ba65cb4d6c186b86a4e7591d92bc1820a67b18b490b95c2d52`; KRC verified handler at unprivileged source checkout sha256 `41cabb6ac7981406c13742e3a4b07c22e5bd0801bd333638e926b97928c4ec73`. These are specific file digests **NOT authenticated in-process loaded-module measurements**. No Stage131 installed systemd unit verified.
- Sentinel evidence referenced by handoff: T1 run `40758789869`; T2 run `40760357417`, request `KS-da78267468ea484fa303f552e6c6b1be`; T3 run `40766586266`, request `KS-3ffb257ba1944b9baefbb32055f2b3f7`; T4 run `40772755023`. The reported T0–T5 acceptance is Sentinel's tested scope. Independent KRC check confirms service health and source branch semantics; it does not repeat a live OIDC T2/T3 probe or assert server-side event log corroboration.

### UDS verification sequence (source)
`VerifiedStage123Handler.do_POST`: obtain SO_PEERCRED UID and verify mapping -> validate path /v1/execute, content type and bounded length -> parse JSON -> `transport_auth123b.verify` verifies exact envelope, HMAC SHA256 over canonical domain-bound payload, timestamp ±300s, signed identity tuple / claim_allowlist -> reject unknown operations outside `staging_backend114.OPS` with HTTP403 `{"error":"OPERATION_DENIED"}` -> verify principal matches mapped UID -> only then `ResearchBoundary.execute` -> ledger admission.

**OIDC/JWKS/audience/jti is not independently verified by KRC UDS**: Sentinel is responsible for upstream OIDC and replay admission. KRC receives a separately HMAC authenticated transport identity. SO_PEERCRED and HMAC are not equivalent to separate OIDC evaluation.

`transport.probe` is not in OPS (four permitted operations: research.profile.validate, research.evidence.preflight, research.bibliography.audit, research.inspection.review). Therefore denied **before** `ResearchBoundary.execute` / `RequestLedger.admit`; T2/T3 IDs are **not expected** in the ResearchBoundary request ledger.

### T2/T3 server audit
**NOT_INSTRUMENTED** — no distinct server-side T2/T3 sanitized event journal identified in reviewed KRC UDS handler (which suppresses default HTTP access logging). Client-side workflow status and Sentinel's own logs are not server-side KRC audit. No synthetic ledger entries invented; no additional audit infrastructure enabled.

### Remaining real scientific E2E gates
1. Real owner consent: explicit scoped issued and independently enforced grant; synthetic Stage130 tests do not count. Principal/operation/task binding and durable replay/revocation.
2. Stage131 backend signer: `staging_entrypoint131` currently **hard-denies** enable_internal_science_signing=true. Separately reviewed signer integration/entrypoint and consent custody required. No science dispatch yet approved.
3. Stage131 operator deployment: immutable source/venv hash lock; UID988 shared owner decision; dedicated Stage131 config and non-reused secret material 0600, state, socket permissions; read-only preinstall had 6 NOT_READY; no Stage131 service activated.
4. JSON Schema: align signed/request and **actual** krc-transport/2 UDS response; proposed science_response_v1 is not identical to actual wire; review versioned interoperable error/status/artifact types with K_Science and Sentinel.
5. Bibliography: real provider selection, licenses, network quotas, 503 failure handling, independent source provenance and fulltext permissions. Current Crossref metadata read-only and Europe PMC 503 cannot qualify as research provider PASS.
6. Authorized external Artifact GET, issuer/audience OIDC acceptance, replay and timeouts, request/response ownership, negative tests, rollback, E2E-01..05 with pinned SHAs, redacted evidence; Sentinel's T4 does not imply science E2E acceptance.
7. No public MEDIA/production scopes silently enabled.

**Decision:** `ACK_WITH_LIMITATIONS` for **Stage127 staging transport technical acceptance only**. No `CONFLICT` in source-level known-op boundary mapping. Full cross-project release attestation, installed Stage131 parity and E2E remain PENDING.
