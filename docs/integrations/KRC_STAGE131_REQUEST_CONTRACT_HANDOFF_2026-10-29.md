# Stage131 request/response candidate contract handoff — 2026-10-29

**Candidate, not final external or scientific E2E contract. STAGING ONLY / FREE_ONLY / Production NO-GO.**

Added schemas:
- `schemas/stage131/sentinel_external_request_candidate_v1.schema.json`: exact minimal external consumer request `request_id,operation,payload`. No transport MAC or Science HMAC on client boundary. Sentinel OIDC/replay is separate, not represented by these body fields. External shape requires partner ACK.
- `schemas/stage131/uds_signed_request_observed_v1.schema.json`: observed signed internal UDS `krc-transport/2` request envelope `version,request_id,operation,identity,payload,transport_auth`. KRC requires UID-key, allowed claims, canonical HMAC and ±300-second freshness; JSON Schema is only shape, **does not verify MAC**.
- Existing `uds_response_observed_bundle_v1.schema.json` and `uds_http_observed_mapping_v1.json`: internal response cases and status mapping; *not* external Sentinel mapping.
Focused new and actual wire request/response tests: **7/7 PASS** in isolated hash-locked test environment on krc-cobalt; no real UDS requests, no science operations, no deployed Stage131 modifications.

Outstanding: real handler-emitted fixture comparison, final partner-reviewed schema blob SHA bundle, nested science request/inner result contract, full error mapping including early errors without request_id, authorized external artifact GET or explicit NOT_RUN, owner consent/revocation and reviewed signer. K_Science scientific E2E 48 NOT_RUN. Installed Stage131 remains pinned `49f8b857b46ebdf45636deffe90f8a4ee578bddf` signer disabled.
