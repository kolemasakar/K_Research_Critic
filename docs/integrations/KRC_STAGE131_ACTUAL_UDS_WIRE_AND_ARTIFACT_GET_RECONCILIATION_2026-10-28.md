# Stage131 actual UDS response and Artifact GET reconciliation — 2026-10-28

**STAGING ONLY / FREE_ONLY / Production NO-GO.**

## Code-grounded findings
- Existing `deliver_result` uses `version=krc-transport/2`, `status=completed`, `delivery=inline|artifact`, `request_id`, `result` or `artifact`. A rejected/pending response from ResearchBoundary has distinct `status=rejected|pending_reconciliation` and `error.code`.
- New `science_response_v1.schema.json` from Stage131 DRAFT uses `status=OK|ERROR` and additional fields. **Not wire-compatible as written.** It must NOT be marketed as tested deployed UDS contract. Options: introduce separately versioned explicit normalization at trusted boundary after contract approval, or publish faithful existing wire schema. Do not silently change Stage126 responses.
- Existing `Stage123Handler.do_GET` already implements **local Unix-socket** `/v1/artifacts/{artifact_id}`; it checks SO_PEERCRED-derived principal and scoped `X-KRC-Request-ID` selector, calls HardenedExchange.read_stream with principal/request scope, verifies bytes and SHA-256 and returns size/digest. `VerifiedStage123Handler` inherits this GET unchanged. This is **not** a public/remote Sentinel-accepted artifact endpoint, and no claim of OIDC authorization for GET is made. An untrusted supplied request-id header is only a scope selector; peer identity is mandatory. Need review against Sentinel Stage127 authenticated artifact retrieval policy and request ownership before making remote GET accessible.
- This is a reconciliation; avoid building duplicate GET or a new external port.
 
## Regression
Pinned Git checkout `5f67e4c22eb9320d28577d7bd45de5cb3fe51ba9`, targeted actual-wire/schema/private-UDS tests: **10/10 PASS**. These tests assert current behavior and explicitly exhibit draft mismatch, not full wire schema acceptance. No service changes, real owner grant or E2E.

## Next acceptance requirements
1. Publish canonical Stage123 existing wire schema alongside proposed higher-level Science response separately; define adapter only after bilateral contract.
2. Test UDS GET positive and wrong-principal/wrong-request/expired/corrupted data at same synthetic peer; require explicit Sentinel artifact authorization and byte limits.
3. Maintain Stage127 :19017 as sole external transport candidate and Stage131 local-only backend.
