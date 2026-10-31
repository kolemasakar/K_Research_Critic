# KRC Stage131 signed Artifact GET reconciliation decision — 2026-10-31

Status: PARTIAL_ACK_SOURCE_ONLY / RUNTIME_NO_GO. Sentinel proposal: docs/STAGE127_SIGNED_GET_KRC_FIELD_MISMATCH_RECONCILIATION_2026-10-31.md.

## KRC source-level contract decision
- ACK proposed dedicated internal `POST /v1/artifacts/read`, `version=krc-artifact-get/1`, `operation=artifact.read`; never dispatch via `POST /v1/execute`.
- ACK canonical UTF-8 JSON with sort_keys=True, separators=(',',':'), ensure_ascii=False, allow_nan=False; remove only `auth.mac_sha256` before signing. HMAC-SHA256 includes version, operation, identity, selectors and key metadata. Example synthetic signing helper `sign_fixture` is test-only and not production signer.
- ACK bounded timestamp skew up to 300s, exact trusted identity match, nonce replay denial via an injected *trusted durable and atomic* nonce_claim. Current test callback is in-memory and only verifies the seam; it does NOT establish restart durability.
- New verifier source: `src/krc_research/stage131_signed_artifact_read.py`; tests: `tests/test_stage131_signed_artifact_read.py` **9/9 PASS**.
- Prior KRC `schemas/stage131/artifact_get_signed_uds_envelope_candidate_v1.schema.json` matches this shape. No new secret provisioned; separate retrieval-scoped key creation/rotation still requires approval.

## BLOCKED — endpoint implementation and real server wire
- No registered `POST /v1/artifacts/read` handler in installed Stage131 or Stage127; existing Stage123 GET with unsigned selector is NOT this protocol.
- No integration of authoritative SO_PEERCRED / OIDC-derived identity or durable nonce store to the new verifier.
- No verified artifact retrieval from RequestLedger + principal + request_id, no complete spool/size/SHA/TTL-before-first-byte server response implementation, no signed server 200/401/403/404/410 fixtures.
- Signature verification is not sufficient to grant artifact access or scientific consent. 40 Sentinel GET negative scenarios and 48 science E2E remain NOT_RUN. No service/transport/deployment or external provider changes.

## Follow-up to partners
K_Sentinel: align source-only adapter to the agreed envelope, no default activation, prepare independently generated canonical/MAC fixture comparison and 40 tests after KRC server endpoint exists. K_Science: independent review of client receiver and signed retrieval semantics. KRC: implement and test durable authenticated GET server boundary under separate release review before claiming endpoint parity.

STAGING ONLY / FREE_ONLY / Production NO-GO.
