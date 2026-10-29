# KRC response to K_Science independent 13-case review — 2026-10-29

**Independent input**: K_Science `docs/integrations/stage127-science-e2e/observed-review/ACCEPTANCE_TABLE.md` at `d7f5b362fcf4401b9fa6c8a59e8bfc321f262ab0`, issue comment `6488673008`. 13 source-emitted local cases: **11 ACK / 2 MISMATCH**; consumer tests 14/14 PASS because negatives were expected. **Not live installed service responses, no science E2E.**

## Source-only corrective action

1. The observed response bundle `schemas/stage131/uds_response_observed_bundle_v1.schema.json` now includes trusted `GET /healthz` 200 body `{"status":"staging","production":false}`, previously defined only by a separate healthz schema.
2. The inline `result` schema now rejects *explicit* `scientific_approval:true` in `result` or directly nested `result.engine_result`. This is a **bounded negative shape guard**, not complete inner-science validation. Other nesting, task_id, operation, scientific provenance and consent require independently reviewed semantic contracts. A transport `completed` is never scientific approval.
3. Added `tests/test_stage131_consumer_mismatch_regression.py` with success/negative fixture assertions. Source regression with existing response and healthz tests: **6/6 PASS** on `krc-cobalt` in isolated hash-locked development venv.

## Partner gate

Ask K_Science to repeat its unchanged 13-case independent harness on the new source pin, report 13 ACK/0 MISMATCH or concrete new findings. Distinguish strict raw wire validation from consumer receipt validation, and do not approve external HTTP mapping. Artifact expiry metadata remains an additional consumer contract strictness question, not part of the original two MISMATCH tally.

## Deployment and limits

Changes are **repository source only**; deployed `krc-research-stage131.service` remains immutable commit `49f8b857b46ebdf45636deffe90f8a4ee578bddf` with signer disabled and `workflow_ref=staging-disabled`. No service changes, no real science dispatch. K_Science 48 scientific cases NOT_RUN. STAGING ONLY / FREE_ONLY / Production NO-GO.
