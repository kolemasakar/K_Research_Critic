# KRC Stage131 consumer ACK and schema gap closure — 2026-10-31

K_Science issued **ACK_TWO_SCHEMA_CORRECTIONS** after independent unchanged 13-case replay: 12 accepted valid-body cases + one correctly rejected malformed science approval. Source pin `0add1ad2cec8671d3dde627b447c685ecae738d5`, schema blob `d9300661de198a15e7671f4225e470bf0ed33626`. Their focused tests 11/11 PASS. Evidence: K_Science `docs/integrations/stage127-science-e2e/observed-review/REMEDIATION_ACK.md`, commit `63770c257b576d7e995f952087e03704de1121fd`.

Follow-up source-only contract tightening in `schemas/stage131/uds_response_observed_bundle_v1.schema.json`:
- Actual science-shaped INLINE results (identified by explicit `scientific_approval`) must include task_id, operation, status (PENDING/REVISE), and engine_result; scientific_approval remains false. Generic transport results without scientific_approval remain possible. This is NOT full semantic consent/provenance verification.
- ARTIFACT descriptor now requires filename, media_type and expires_at_epoch alongside id, SHA-256 and size. The source store emits these fields; external authorized GET is still NOT APPROVED.
- Updated historical test fixtures; added negative cases for absent task identity and artifact expiry.

Focused source unit tests **10/10 PASS** on krc-cobalt (after initial 2 fixture failures corrected). This is NOT an independent K_Science rerun of the new stricter schema, NOT runtime Stage131 deployment parity.

No service installation/restart, no signing enablement, no science dispatch. Deployed Stage131 remains pinned `49f8b857b46ebdf45636deffe90f8a4ee578bddf`. 48 scientific E2E cases remain NOT_RUN. External Sentinel HTTP mapping NOT_ACKED. **STAGING ONLY / FREE_ONLY / Production NO-GO.**
