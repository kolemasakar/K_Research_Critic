# KRC Stage123-B — independent peer-bound HMAC verifier (2026-10-28)

**Scope:** KRC isolated test checkout only; no production service/UDS deployment, Stage114 v1 and public services unchanged, FREE_ONLY.

## Implemented
- `src/krc_research/transport_auth123b.py`: independent KRC-side canonical JSON/HMAC-SHA256 verifier compatible with Sentinel `identity_assertion.py`. Signed five-field `krc-transport/2` envelope, domain `KRC-TRANSPORT-IDENTITY/2`, key ID and issued_at, ±300s skew, full envelope/body binding. Trusted local peer UID selects key set; allowlisted `(client,principal,repository,workflow_ref)` values, 256 KiB cap. Reject missing/changed MAC, unknown key, disallowed identity, expired assertion and unauthorized peer.
- `src/krc_research/uds_verified123b.py`: separate staging verified UDS handler, checks Linux `SO_PEERCRED`, verifies HMAC assertion and claim allowlist **before** ResearchBoundary admission or scientific dispatch. Binds allowed signed principal to configured UID principal; protects artifact GET against cross-principal aliasing in the inherited Stage123 handler. No production listener.
- `tests/test_transport_auth123b.py`: positive, tampered identity/operation/request_id/payload, expired, wrong UID, forbidden claim, and UDS verified-before-dispatch tests.

**Observed focused isolated krc-cobalt test suite: 66 passed, 7.12 seconds** (9 new + previous 57). The UDS integration test uses an injected synthetic research handler; previous Stage123-A test exercised real signed profile science through earlier UID-only handler. These have not yet been combined into a single verified-identity -> real-science E2E fixture.

## Restrictions / blockers
- The upstream OIDC/Tailscale attestation source is NOT connected or independently tested; Sentinel owns those checks before signing. A matching HMAC only proves key possession and integrity, not GitHub issuer/audience provenance.
- Staging keys are supplied to test fixture only. No live credentials provisioned, no key rotation, revocation ledger or secure production key store configured.
- Current UID-to-principal mapping deliberately supports only a single configured principal per UID: multi-workflow principals need separate approved secure mapping and ACL before deployment.
- Full four-operation signed science E2E, post-reboot request/science task replay, immutable file guarantee, state reconciliation, 200MiB stress, timeout/disconnect E2E and final HTTP error schema not complete.
- The proposed `/run/krc-research-v2/backend.sock` has NOT been deployed as a service; no live KRC↔Sentinel authenticated E2E. Full repo regression not rerun (prior baseline 884 PASS, 8 legacy FAIL, 17 SKIP).

**Decision:** isolated verification candidate PASS, staging integration remains PARTIAL, production NO-GO.
