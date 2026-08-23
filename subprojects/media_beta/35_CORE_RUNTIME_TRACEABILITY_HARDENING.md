# Core Runtime Traceability Hardening

Version: 1.0
Date: 2026-08-23
Status: IMPLEMENTED_IN_BRANCH_PENDING_BUILDER_RESYNC

## Trigger

The main `K-Research & Critic` was manually synchronized with the clean Core Builder candidate and tested in a new chat using the CRITICAL medical query about cold showers and immunity.

The runtime behavior correctly enforced:
- `risk_level=CRITICAL`;
- `required_cross_checks=3`;
- claim-level `PASS` and `SHORTFALL` states;
- explicit `1/3 - SHORTFALL` with limitation;
- `REVISE -> REVISE -> REVISE` and final `COMPLETED_WITH_LIMITATIONS` rather than unconditional PASS.

Two remaining auditability defects were observed:
1. the Review Protocol did not include the required per-claim `required / achieved_independent / exception` summary;
2. some claims reported `3/3` or `4/3` PASS while fewer independent evidence origins were visibly traceable in the user-facing report.

## Hardening

The clean Core Builder instructions now require a strict traceability invariant:
- every evidence origin counted in `achieved_independent` must be visible and traceable by title/citation to that claim;
- the reported achieved count cannot exceed the number of visibly traceable independent evidence origins;
- duplicates, derivative reporting, repeated pages, and multiple URLs to one origin do not increase the count;
- a systematic review/meta-analysis counts as one evidence origin unless specific underlying studies were independently inspected and cited;
- Critic verifies that `achieved_independent` equals the number of valid traceable origins;
- an untraceable PASS count blocks unconditional PASS.

The Review Protocol now has a mandatory compact table with columns exactly:

```text
Claim | Required | Achieved independent | Exception
```

The table must include every material factual claim, use `NONE` or `SHORTFALL`, and match the visible claim blocks/evidence origins.

## Regression protection

`tests/test_core_builder_instructions.py` now asserts:
- Builder remains <=8000 characters;
- traceability invariant exists;
- PASS count cannot exceed visible independent origins;
- systematic review counting rule exists;
- Critic checks traceability;
- mandatory claim-level protocol table exists with exact columns;
- Core remains clean of Media Beta operational logic.

CI run #687 on commit `d838787f3b3040143842e7674a42477e757d26cd` passed:
- Python 3.13 tests: PASS;
- Python 3.14 tests: PASS;
- dependency integrity: PASS;
- Ruff: PASS;
- mypy: PASS;
- repository policy: PASS;
- GPT Store package validation: PASS;
- coverage gate: PASS.

## Runtime state

The currently configured main `K-Research & Critic` still contains the previous Core candidate until the owner manually resynchronizes the updated `prompts/GPT_STORE_CORE_BUILDER_INSTRUCTIONS.md`.

Therefore:

`CORE_CLAIM_LEVEL_ENFORCEMENT_RUNTIME = PASS_WITH_REQUIRED_FIX`

`CORE_TRACEABILITY_HARDENING_CODE = PASS`

`CORE_TRACEABILITY_HARDENING_RUNTIME = PENDING`

No repository merge to `main` is authorized by this record.
