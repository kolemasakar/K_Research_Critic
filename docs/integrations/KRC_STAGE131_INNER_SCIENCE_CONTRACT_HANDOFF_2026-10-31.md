# Stage131 KRC inner science contract acceptance handoff — 2026-10-31

Status: SOURCE_SCHEMA_CANDIDATE / INDEPENDENT_ACK_PENDING / NO DEPLOYMENT.

## Source and contracts
- Added `schemas/stage131/inner_science_success_v1.schema.json` for the four currently supported science operations, mapped to observed `science_dispatch.handle_science_request`: `research.profile.validate`, `research.evidence.preflight`, `research.bibliography.audit`, `research.inspection.review`.
- Requires exact `task_id`, `operation`, `status`, `engine_result`, `scientific_approval=false`; only evidence preflight may return REVISE, other operations PENDING. Tests require no invented scientific APPROVED status.
- **This is an observed success-envelope schema, not final engine_result operation-specific semantics or a final error wire schema**. The existing dispatcher returns exception on error, and ResearchBoundary may return pending_reconciliation; unsupported ERROR wire is NOT asserted as observed.
- Correct task/operation equality to the admitted request requires `stage131_correlated_dispatch.py` and independent trusted context; standalone JSON Schema cannot prove it.
- Tests `tests/test_stage131_inner_science_success_contract.py` plus focused correlation and previous contract cases: **20/20 PASS**.
- Existing observed UDS HTTP response bundle remains a separate transport schema; transport status `completed` is not scientific approval.

## Required independent K_Science review
- Pin exact schema Git blob and source revision; compare positive and negative shape decisions for four operations.
- Return per-case ACK/MISMATCH for status, fields, no science approval, response/request correlation, and proposed operation-specific engine_result content; identify exact available result fields for each handler, not imaginary fields.
- Review exact error path (handler exception→reconciliation) and propose only source-supported error contract; **do not accept fabricated science ERROR variant**.

## Required independent K_Sentinel review
- Verify identity/transport binding via signed UDS and no caller-controlled consent flags; no new external GET route.
- Review early errors, 409 reconciliation, 507 fallback and whether observed output schema is distinct from proposed external HTTP mapping.

## Operational bounds
No deployed Stage131 update, no real owner consent, no signer enabling, no provider/network calls. 48 real scientific E2E NOT_RUN. STAGING ONLY / FREE_ONLY / Production NO-GO.
