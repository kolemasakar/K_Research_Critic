# KRC Stage131 observed UDS response contract candidate — 2026-10-29

**NOT FINAL EXTERNAL API. STAGING ONLY / FREE_ONLY / Production NO-GO.**

KRC source files:
- `schemas/stage131/uds_response_observed_bundle_v1.schema.json`
- `schemas/stage131/uds_http_observed_mapping_v1.json`
- `tests/test_stage131_observed_response_bundle.py`

The response bundle models five observed body variants: completed inline, completed artifact, rejected/pending_reconciliation, simple early `{"error":"CODE"}`, and 507 fallback `{"status":"error","error":{"code":"RESPONSE_TOO_LARGE"}}`. Early errors lack request_id/version; do not fabricate. The HTTP table covers 200/400/403/404/409/413/415/507, including 403 before ledger. This is **internal UDS**, not final Sentinel outer mapping. External authorized artifact GET is still NOT APPROVED.

On `krc-cobalt`, 6/6 focused schema and actual-wire tests PASS, using hash-locked isolated test venv, against current source. This is not installed code parity. Deployed runtime Stage131 remains `49f8b857b46ebdf45636deffe90f8a4ee578bddf`.

Final ACK blockers: all external + signed UDS request + actual inner science result/error schemas, emitted fixture parity for every HTTP branch and artifact read, partner SHA acceptance, legitimate consent/signer, provider review and external artifact authorization. K_Science 48 cases remain NOT_RUN. No service restart or real science dispatch.

Please review the actual observed body schema and HTTP table, provide explicit ACK/rejections for each variant, and do not infer E2E acceptance.
