# Stage131 KRC-owned consumer-boundary implementation — 2026-10-31

**Scope:** source-only, isolated, no runtime service changes. STAGING ONLY / FREE_ONLY / Production NO-GO.

Added `src/krc_research/stage131_consumer_boundary_checks.py`:
- `validate_science_result(result, expected_task_id, expected_operation)`: five exact fields, approved operation enumeration, strict task/operation equality to KRC-supplied context, PENDING/REVISE, `scientific_approval is False`, object engine_result. A valid outcome is `VALID_SHAPE_ONLY`, **not scientific approval**.
- `validate_artifact_descriptor(descriptor, now_epoch)`: ID/hash/size/filename/media_type/expiry shape; tests the current time against expiry, `expiry <= now` is EXPIRED; nonexpired produces `DESCRIPTOR_VALID_NOT_AUTHORIZED`, not access permission.
- `tests/test_stage131_consumer_boundary_checks.py`: positive, mismatch, negative approval and TTL boundary tests.

With existing strict schema regressions: **8/8 PASS**, hash-locked isolated local environment on krc-cobalt. No live UDS request, HTTP network activity, science dispatch, real signer/consent or secret access.

**Critical remaining gates:**
- These pure functions are **not integrated** in actual ResearchBoundary or artifact GET, therefore runtime TTL/correlation enforcement has NOT been proved.
- Existing `artifact_exchange.py` `get_bytes` checks `expires <= clock`, principal and request_id before returning bytes; this must be independently exercised for authorized retrieval and scoped identity before enabling any external route.
- Inner science semantics must be agreed with K_Science and Sentinel. Scientific evidence verification, artifact external GET ownership authentication, approved response schema and deployment parity remain pending.
- Deployed Stage131 still pinned `49f8b857b46ebdf45636deffe90f8a4ee578bddf`, signer disabled. K_Science 48 real scientific E2E NOT_RUN.
