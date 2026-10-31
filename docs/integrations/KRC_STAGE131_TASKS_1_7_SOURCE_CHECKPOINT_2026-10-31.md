# KRC Stage131 — 1–7 source implementation and safety checkpoint (2026-10-31)

**Source-only. STAGING ONLY / FREE_ONLY / Production NO-GO.**

## 1–3. Inner science and artifact storage
- Existing `stage131_consumer_boundary_checks.py` validates task_id/operation correlation and result shape, and artifact descriptor expiry.
- New `stage131_correlated_dispatch.py` provides fail-closed post-dispatch result check, but remains opt-in and **is not wired to installed Stage131**.
- New `stage131_safe_composition.py` provides consent-required correlation and internal scoped artifact read. `artifact_read_gate` requires authenticated principal equality, bound request_id, nonexpired descriptor; underlying exchange rechecks scope, actual TTL and digest.
- **Concrete defect fixed:** `HardenedExchange.store_stream()` previously stored expiry in SQLite but returned descriptor without `expires_at_epoch`, contradicting stricter schema. Now returns committed stored expiry. Source commit `790f6164c2980a943f2339da3aaeb387594af101`.
- Hardening tests with isolated real disk-backed HardenedExchange confirmed expired, cross-principal, cross-request, corrupted artifact are denied.
- Caveat: cannot call a supplied `consent_verified=True` Boolean an owner grant. Safe composition is a staging **testing seam** only; production trusted consent must be verified by `ConsentCustody128` inside reviewed dispatch.

## 4–6. External GET, consent and signer
- **NO external GET route enabled.** Design requires Sentinel OIDC/auth/replay, signed trusted identity, internal principal+request_id+artifact_id, server-clock TTL and SHA/size checks. Selector header alone is not authorization. External error mapping remains for joint ACK.
- `ConsentCustody128` verifies root-owned grants and context SHA, expiry and replay ledger. `KRCInternalScienceSigner` requires independent authorizer; existing Stage131 entrypoint continues to reject enabled science signing. Existing consent+signer tests re-run successfully with temporary synthetic grants/keys.
- No real grant issued, no signer enabled, no permissions/routes changed. Real owner-authorized grant issuance/revoke path and separately reviewed signer-enabled runtime are NOT COMPLETE.

## 7. Bibliography
- `stage131_bibliography_http.py` bounded and domain-allowlisted HTTPS metadata client with 429/503 retry limits, timeout and byte limit.
- `stage131_bibliography_adapter.py` matches DOI across Crossref and Europe PMC conservatively; `stage131_bibliography_reconcile.py` evaluates title/year. New `bibliography_metadata_gate` requires explicit provider_approved and allow_network. **Default disabled**, not integrated into deployed research handler.
- Prior read-only live Crossref DOI for K_Science paper succeeded, Europe PMC returned zero hits (coverage gap, not evidence of nonexistent publication); title mismatches remain review-required. Licensing, provider release review, real operational budgets still pending.

## Tests / release gate
Focused combined suite from `tests/test_stage131_safe_composition.py`, correlated dispatch, artifact get denials, Stage117 storage, bibliography HTTP/adapter, consent custody and science signer: **48/48 PASS** after committed-expiry fix. Initial suite **1 failure / 41 pass** exposed missing expiry in Stage117 return value; corrective source patch and retest **48/48 PASS**. Full KRC regression, installed source parity, deployment and independent consumer ACK **not performed**.

Installed Stage131 remains `49f8b857b46ebdf45636deffe90f8a4ee578bddf`; signer false, Stage127 sole external transport. 48 real scientific E2E scenarios NOT_RUN.

## Next blocking decisions
1. Independent review and partner ACK of changed Stage117 manifest and opt-in boundary API.
2. Reviewed signer entrypoint + authentic scoped owner grant mechanism, explicitly authorized staging rollout with source/install parity.
3. Scoped authenticated external Artifact GET implementation across Sentinel transport (if approved); otherwise scenarios remain NOT_RUN.
4. Bibliography backend integration into authorized science handler and provider security/license checks; no unapproved network.
