# KRC Stage131 — actual UDS v2 schema handoff (2026-10-28)

**STAGING ONLY / FREE_ONLY / Production NO-GO.**

Actual private response schema: `schemas/stage131/uds_response_transport_v2.schema.json`, commit `43631aff8543f90fdd645079b07b58306d121301`. Separate from proposed high-level `science_response_v1.schema.json` (currently not directly wire-compatible).

The schema captures Stage123 `completed/inline`, `completed/artifact` and `rejected|pending_reconciliation` body families and the bounded artifact id/SHA-256/size shape. This is a **provisional inventory schema**, not a frozen HTTP interoperability standard. The rejected family intentionally permits additional existing fields pending an exact golden-fixture inventory.

New contract regression `tests/test_stage131_actual_uds_response_schema.py`. On isolated SHA-pinned krc-cobalt source HEAD `75322f40bb873092ca132446583af80ad7853a52`, targeted actual wire, artifact store and four-op UDS tests **13/13 PASS**. No server activation or modifications.

## KRC-to-Sentinel handoff
- Canonical external staging transport candidate: Sentinel Stage127 existing :19017 only.
- KRC internal boundary: private UDS `/v1/execute` and `/v1/artifacts/{artifact_id}`. GET already exists in Stage123Handler; require validated SO_PEERCRED principal and request-scoped artifact ownership, expiry and SHA-256. `X-KRC-Request-ID` is a selector, NOT authentication.
- Do not expose GET through Stage127 until its separate authenticated method/path allowlist, OIDC identity projection, HMAC/UDS binding, max response bytes, timeouts, and replay/idempotency are documented and independently tested.
- T1 network and T2 OIDC belong to Sentinel. KRC owns artifact authenticity, provenance, scope and scientific approvals. Transport PASS never implies science PASS.

## Open KRC tasks
1. Add actual private GET negative regression including wrong peer/owner, request, expiry, corruption and oversize (current source tests cover storage but don't prove remote GET).
2. Freeze response HTTP status/error mapping with Sentinel and Science.
3. Continue owner consent/signing isolation and K5 Europe PMC 503 diagnostics.
4. Stage131 real isolated daemon installation remains NOT_RUN and Production NO-GO.
