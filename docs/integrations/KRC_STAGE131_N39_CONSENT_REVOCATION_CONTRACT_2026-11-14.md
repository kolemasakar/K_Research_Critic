# KRC Stage131 / N39 — scientific consent revocation and artifact retrieval contract (2026-11-14)

**Scope:** isolated source-only validation; signed GET disabled in installed services. Production NO-GO. 200 MiB owner-waived load test remains NOT_TESTED.

## Authority and policy

1. A scientific execution MUST be authorized by a current, independently protected, single-use original grant through `ConsentCustody128` **before dispatch**. Missing/invalid/revoked-before-use consent fails closed: no new `dispatch`, no new scientific result, no signed receipt. The installed service must not mint grants. A prior `RequestLedger.COMPLETE` record is historical evidence of a completed request, NOT a fresh consent or automatic retrieval right.
2. Upon completion, the origin consent may be expired, consumed or revoked. Its original provenance MUST remain durably recorded, distinct from an independently issued **current artifact retrieval grant**, scoped to exact `principal + request_id + artifact_id`, with expiry and revocation. Reading never re-consumes original execution consent and never runs a scientific operation.
3. An artifact read is allowed only if BOTH a completed owner-matched RequestLedger and intact owner-matched ArtifactExchange exist, and the independent current retrieval grant and historic origin provenance are present. A valid original consent alone is insufficient. Following revocation of original execution consent, a separately authorized unexpired retrieval grant can still allow a read within the artifact retention period. Without such grant, deny. This distinction is deliberate; original consent revocation does not retroactively invalidate properly issued separate retrieval authorization.
4. For all absence/invalidity/revocation of origin provenance or independent retrieval permission, emit **HTTP 403 / `{"error":"FORBIDDEN"}`**, no body or metadata disclosure, and no client auto-retry. Do not reveal whether a consent reference, artifact, or provenance entry existed. For a request lacking a completed owner-matched ledger, existing behavior is **404 / NOT_FOUND**; this is checked before N39 authorization. After successful authorization, an expired artifact remains **410 / GONE**. Invalid HMAC/peer/replay remains **403 / FORBIDDEN**.
5. **Revocation/read race:** the atomic SQLite `is_authorized` decision is the linearization point. A committed retrieval-grant revocation *before* this check denies the read; a read already authorized before revocation may finish. This policy does not promise cancellation or retraction of bytes already authorized/streaming. For stronger post-authorization cancellation, a new streaming protocol and independent review are required.
6. **Fail closed by default:** `SignedArtifactReadBoundary` with no configured trusted retrieval authorizer denies artifact reads, including when its other HMAC/ledger/storage controls pass. Trusting a caller-provided boolean is not permitted as evidence of original consent.
7. **Provisioning gate:** `N39ConsentPolicy.record_original` only accepts the real `ConsentCustody128` type. The isolated `record_read_grant` method is test/operator-only; it MUST NOT be exposed on HTTP/UDS or called by the running service without a separately authenticated, out-of-band retrieval authorization issuer and audit. Owner provenance, grant issuance and installed ACL/key parity must be reviewed before deployment.

## Test evidence and boundaries

- New source: `src/krc_research/stage131_n39_consent_policy.py`; fail-closed integration: `src/krc_research/stage131_signed_artifact_boundary.py`.
- N39 tests: `tests/test_stage131_n39_consent_policy.py`.
- Scenarios: missing origin despite COMPLETE ledger and intact stored artifact -> 403; no authorizer -> 403; original provenance without retrieval grant -> 403; independently authorized read -> 200; original revoked with still-valid independent retrieval grant -> 200; retrieval grant revoked -> 403; expired retrieval grant -> 403; grant issue without provenance refused; science consent missing -> zero dispatch; committed revoke before check -> denied.
- Nonprivileged source tests include **synthetically seeded origin provenance**, not evidence of a root-issued human consent. A separate root-only test is provided to validate actual root-owned synthetic `ConsentCustody128` grants and durable consumption; it is **SKIPPED** in the unprivileged runner and **NOT accepted as an actual root-owned test**. Do not conflate a fake provenance seed with genuine consent.
- Source-only/host tests are not K_Sentinel N39 independent E2E or K_Science provenance ACK. The installed Stage127 and Stage131 GET and signer remain OFF, no real grant issued, no real science executed.

## Independent acceptance requests

**K_Sentinel:** independently test N39 with fresh synthetic but actually root-controlled Consent Custody + RequestLedger + ArtifactExchange + nonce on an authorized isolated STAGING machine. Confirm 403/200/403 post-revocation matrix, non-reexecution, no automatic retry, race linearization and no-leak; return per-case ACK/MISMATCH. Do not mark N39 full external PASS from source-only tests.

**K_Science:** independently verify consent origin/issue/revoke auditing, descriptor provenance, distinct independent retrieval grant, and receiver behavior for 403/410/200. Report ACK/MISMATCH.

**Release state:** SOURCE IMPLEMENTATION / INDEPENDENT ROOT-OWNED CUSTODY AND EXTERNAL ACCEPTANCE PENDING. Production NO-GO.
