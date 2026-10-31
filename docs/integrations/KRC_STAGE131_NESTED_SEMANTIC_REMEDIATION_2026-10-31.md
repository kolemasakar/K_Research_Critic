# KRC Stage131 nested semantic remediation handoff — 2026-10-31

**SOURCE_ONLY_REVIEW_REQUIRED. STAGING ONLY / FREE_ONLY / Production NO-GO.**

## Exact code tested
Source pin before this report: `2b074037eb971096d30973ad3b59e3fa7979e062`.

Added `src/krc_research/stage131_science_semantic_contract.py`: strict fail-closed check of all four operations against admitted task_id/operation. In particular:
- Evidence preflight: rejects `result={}`, missing claims ledger/search_logs/manuscript_gate, inconsistent ledger count/pass/shortfall, incomplete search logs, invalid manuscript gate, fake submission readiness, and inconsistent `REVISE` vs `NO_GO` status. Empty claim ledger/search arrays are permitted ONLY when their documented counts and SHORTFALL/REVISE/NO_GO semantics are consistent; never infer reproducible search from missing logs.
- Bibliography: enforces 1–24 records, record count equality, metadata match count, recorded update count, retraction clearance NOT_ESTABLISHED, full texts inspected=0, methods/results verified=false, experimental origins verified=0. Metadata must never be promoted to verified scientific evidence.
- Inspection: requires SHA-256 shape, false scientific_truth_verified and shortfalls consistency with independent-claim-review eligibility. It does NOT independently authenticate inspection events, evidence provenance, signature, or genuine trace.
- Profile: requires exact fields and `approval_independently_verified=false`, `scientific_approval=false`. Source-only trust of upstream validator; no consent issued.
- Errors: actual handler exception maps in `ResearchBoundary` to `pending_reconciliation/error.code=HANDLER_ERROR` (409 UDS), not a fabricated inner `ERROR` science result.

## Source-derived schemas / transport proposal
- `schemas/stage131/inner_science_operation_results_v1.schema.json` defines four operation-specific structural branches. Semantic consistency is enforced in Python function, NOT yet deployed as the runtime authorized dispatch path.
- `schemas/stage131/uds_source_error_mapping_candidate_v1.json` documents actual internal error branches; external statuses are not asserted as observed.
- `docs/integrations/KRC_STAGE131_ARTIFACT_GET_V1_DISABLED_CONTRACT_2026-10-31.md` proposes signed UDS auth scope, OIDC jti replay protection, KRC ownership ledger, trusted-clock TTL, full SHA/size before first byte, disabled route 404 and provisional GET 400/401/403/404/410/405/413/429/500/502/503/504 semantics. This is a DESIGN, not a cryptographically signed active handler. Sentinel must finalize exact versioned signed-envelope/error schemas and independent negative tests.
- Static schemas do not establish actual synthetic handler output for all four cases. Source-derived minimal fixtures exist in tests; no installed Stage131 handler invocation was performed. Actual server-emitted synthetic response capture remains mandatory before final ACK.

## Test evidence / checksums
- New semantic negative test module `tests/test_stage131_science_semantic_contract.py`: 13/13 PASS.
- Full repository regression: **1083 passed, 17 skipped, 0 failed**, on krc-cobalt source checkout with stage131 Python venv (40.34 seconds).
- Source SHA256:
  - `src/krc_research/stage131_science_semantic_contract.py`: `45ee3f579a85017c9c981ff370932e01c9a67ba8670b01c99dfc1135d7306244`
  - `schemas/stage131/inner_science_operation_results_v1.schema.json`: `3e8ab11ab7458ce01681fa66ce75e3d2e2f921b153a4b4a02abf887d3235d782`
  - `schemas/stage131/uds_source_error_mapping_candidate_v1.json`: `0131a8c47d8609e8adc38e0fac5689ef89485c6934ee39b92689e51176d5985f`
  - `docs/integrations/KRC_STAGE131_ARTIFACT_GET_V1_DISABLED_CONTRACT_2026-10-31.md`: `4f8d95aa5a1d365978aa38aa4ea58a67f5e0ca72e73a25e881da07f2865ffeb9`

## Requested independent ACK
- K_Science: rerun nested negative fixtures, especially PRELIGHT result empty, metadata promoted as experiment, receipt eligibility, nonempty/empty evidence and search statuses; check source-emitted synthetic actual results; return per-case ACK/MISMATCH.
- K_Sentinel: field-level ACK/MISMATCH of disabled GET identity/OIDC-jti/HMAC-UDS, owner/ledger/TTL/SHA before first byte and distinct 401/403/404/410 mappings; publish versioned signed envelopes/error schema and 40 isolated negative test outcomes. No GET activation.
- KRC next release gate: integrate semantic function inside reviewed authorized runtime before deliver_result; ensure trusted custody before dispatch; capture genuine synthetic handler responses, retest full suite, immutable pin, source/install parity and rollback. Existing installed Stage131 still active PID 46327 and unchanged. Signer OFF; 48 real E2E NOT_RUN.

**No synthetic owner grants, external providers, or production operations were launched.**
