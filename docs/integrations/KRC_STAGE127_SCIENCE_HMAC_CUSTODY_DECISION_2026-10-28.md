# Stage127 — KRC Science HMAC custody decision (2026-10-28)

**Decision: APPROVE design only; implementation and production activation NOT APPROVED.**
**Mode: isolated staging, FREE_ONLY, PRODUCTION NO-GO.**

## Verified baseline
- Sentinel Stage126 checkpoint: live HMAC/UDS positive request HTTP 409 (deliberately incomplete science payload); bad transport HMAC HTTP 403; no science completion, actual v2 upstream GitHub OIDC/Tailscale provenance NOT RUN.
- Current KRC `ScienceAdapter122` requires `payload.science_envelope` and `payload.science_signature` and validates both against KRC-owned Science HMAC via `dispatch_coded`.
- Existing K_Science workflow targets legacy `:19015` gateway. Do not repoint it silently.

## Approved trust boundary
1. K_Science owns scientific intent, requested operation, immutable content digest, and explicit user consent/authorization. K_Science cannot directly access Science HMAC.
2. K_Sentinel v2 ingress (UID 987) verifies **real** GitHub OIDC RS256/JWKS issuer/audience/repository ID, selected workflow/ref and permitted actor, actual Tailnet peer identity and ACL, durable one-time `(issuer,jti)` replay registry, then signs a bounded `krc-transport/2` request using its *separate* Transport HMAC. A claimed identity alone never constitutes origin proof.
3. KRC UDS (UID 988) independently verifies `SO_PEERCRED`, transport MAC, key ID, allowlist and request ledger, before any internal science-signature construction.
4. A KRC-owned **internal**, narrowly scoped signer performs operation-specific envelope validation and explicit authorization check, binds canonical payload digest, principal, request_id, operation, timestamp/expiry and consent evidence to the science envelope according to the existing signed science contract, then signs with KRC Science HMAC. Pass the signed envelope to `ScienceAdapter122` / `dispatch_coded`; preserve replay and durable receipts.
5. The KRC signer must be non-exportable as a network API or generic signing oracle. Sentinel must not receive Science HMAC, signing signatures from other requests or independent signing capability. Never log secrets/MACs/JWTs.

## Implementation blockers (fail closed)
- The current `staging_service123c.make_staging_server` directly constructs `ScienceAdapter122` with no KRC signer. **Do not enable automatic signing on all transport-authenticated requests.** Add a bounded adapter between trusted boundary and ScienceAdapter only with explicit user-approved operation policy, signed/verified consent custody, request digest binding and negative tests.
- Current bibliography path has `bibliography_fn=None` by default, therefore bibliography operation must remain denied until an approved offline/test provider exists; never present all 4 operations as live PASS prematurely.
- Implement tests: valid request+consent per operation; no consent; forged consent; bad actor/repository/workflow; incorrect payload digest; replay across restart; oversized/expired/changed request; negative MAC; cross-principal; no signing oracle; no secret disclosure.
- Sentinel v2 ingress config/deploy is separate, UID 987, dedicated protected replay database; isolate v1 `:19015`; a dedicated v2-only workflow must be approved and run.
- Trace request_id across K_Science -> Sentinel v2 -> KRC UDS -> Science dispatch -> artifact receipt, with no key/JWT exposure.

## Acceptance
A) Real v2 OIDC/Tailnet/UDS origin proof, replay and negative tests PASS.
B) Live science execution through KRC-owned internal signer for approved operations, with separate scientific approval and artifacts.
C) Real restart/rollback + Stage114/v1/public MCP invariants.
Until then E2E-01 complete = NO-GO; E2E-02–05 live = NOT RUN; Sentinel PR #38 stays DRAFT.
