# KRC Stage131 inner-engine schemas and observed error mapping handoff — 2026-10-31

## Source-backed KRC work
- K_Science independent success-envelope review: 32/32 expectations, source pin d2671a4b4f77aa320cb2e8ec0177b7cd8f529e56. Its file receiver 10/10 local tests PASS; not an external GET integration.
- Created `schemas/stage131/inner_science_operation_results_v1.schema.json` from exact output fields in KRC `profile_validator.py`, `offline_acceptance.py`, `bibliography_audit.py`, `inspection_receipts.py`, cross-checked against K_Science engine_result_fields_candidate_v1 schema (commit 5e37b5d).
- Four exclusive branches require profile validation KRC-CRITICPROFILE-1, evidence KRC-P0D-1, bibliography KRC-BIB-1 and inspection receipt fields respectively. Status REVISE only evidence preflight, scientific_approval false in every branch. No scientific approval or source authenticity implied.
- Added `schemas/stage131/uds_source_error_mapping_candidate_v1.json` for actual KRC boundary-level 409 rejected/pending, early 403 and 507 fallback. These are source-derived candidates, NOT measured deployed fixtures. No inner science ERROR exists in the current source; therefore none is approved.
- `tests/test_stage131_operation_engine_contract.py` with existing success schema tests: **20/20 PASS** in isolated source checkout on krc-cobalt.

## Explicit limits and required follow-up
1. Engine result field validation covers top-level types, required fields and source constants, but nested evidence items, record details and count consistency still require operation-specific semantic validation and source-emitted fixtures.
2. Source-supported exception mapping must be independently exercised under injected dependencies, then compared to transport HTTP output by K_Sentinel. Some early error bodies omit request_id.
3. Correlation with immutable admitted request requires code validator, not only JSON schema; independent source acceptance does not establish deployed parity.
4. No actual provider calls, grant, signer-enabled runtime, external GET, or science E2E. Installed Stage131 unchanged; 48 science E2E NOT_RUN, 40 external GET negatives NOT_RUN. STAGING ONLY/FREE_ONLY/Production NO-GO.

## Requested partner responses
- K_Science: per-operation ACK/MISMATCH including nested engine fields and source emitted synthetic fixtures, result/error semantic validator; preserve historic 32/32 case evidence separately.
- K_Sentinel: source-bound UDS error-to-HTTP mapping, 403 early/409/507 and versioned signed envelope. External GET remains OFF.
