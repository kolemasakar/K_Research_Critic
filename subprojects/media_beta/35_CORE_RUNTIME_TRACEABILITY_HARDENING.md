# Core Runtime Traceability Hardening

Version: 1.1
Date: 2026-08-23
Status: RUNTIME_ACCEPTED_MAIN_CORE

## Trigger

The main `K-Research & Critic` was manually synchronized with the clean Core Builder candidate and tested in a new chat using the CRITICAL medical query about cold showers and immunity.

The first valid runtime behavior correctly enforced:
- `risk_level=CRITICAL`;
- `required_cross_checks=3`;
- claim-level `PASS` and `SHORTFALL` states;
- explicit `1/3 - SHORTFALL` with limitation;
- revision before finalization.

Two remaining auditability defects were then observed:
1. the Review Protocol did not include the required per-claim `required / achieved_independent / exception` summary;
2. some claims reported `3/3` or `4/3` PASS while fewer independent evidence origins were visibly traceable in the user-facing report.

## Hardening

The clean Core Builder instructions were hardened to require:
- every evidence origin counted in `achieved_independent` must be visible and traceable by title/citation to that claim;
- the reported achieved count cannot exceed the number of visibly traceable independent evidence origins;
- duplicates, derivative reporting, repeated pages, and multiple URLs to one origin do not increase the count;
- a systematic review/meta-analysis counts as one evidence origin unless specific underlying studies were independently inspected and cited;
- Critic verifies that `achieved_independent` equals the number of valid traceable origins;
- an untraceable PASS count blocks unconditional PASS.

The Review Protocol has a mandatory compact table with columns exactly:

```text
Claim | Required | Achieved independent | Exception
```

The table must include every material factual claim, use `NONE` or `SHORTFALL`, and match the visible claim blocks/evidence origins.

## Regression protection

`tests/test_core_builder_instructions.py` asserts:
- Builder remains <=8000 characters;
- traceability invariant exists;
- PASS count cannot exceed visible independent origins;
- systematic-review counting rule exists;
- Critic checks traceability;
- mandatory claim-level protocol table exists with exact columns;
- Core remains clean of Media Beta operational logic.

CI run #687 on commit `d838787f3b3040143842e7674a42477e757d26cd` passed Python 3.13/3.14 tests and all quality/package/coverage gates. Later documentation-only commits do not change this code acceptance.

## Final runtime acceptance

After the owner manually resynchronized the hardened Builder, a final NEW-chat regression was run on 2026-08-23.

Observed PASS evidence:
- claim 1 exposed `3/3 - PASS` with three named/cited independent origins: Buijze 2016, Collier 2015, El-Ansary 2024;
- claim 2 exposed `3/3 - PASS` with three named/cited independent origins: El-Ansary 2024, Janský 1996, Brenner 1999;
- claim 3 exposed `1/3 - SHORTFALL` for the 29% sick-leave result;
- a later systematic review repeating Buijze 2016 was explicitly NOT counted as a second independent origin;
- the claim-level protocol summary table was present and consistent with the claim blocks;
- Critic ran `REVISE -> PASS`;
- reliability score: `0.88`;
- final status: `COMPLETED`, with remaining evidence scarcity stated explicitly.

The rendered Markdown header visually collapsed in the pasted output, but all four logical table columns and values were present. This is a non-blocking presentation issue.

Canonical runtime record: `36_CORE_TRACEABILITY_RUNTIME_ACCEPTANCE.md`.

## Runtime state

`CORE_CLAIM_LEVEL_ENFORCEMENT_RUNTIME = ACCEPTED`

`CORE_TRACEABILITY_HARDENING_CODE = PASS`

`CORE_TRACEABILITY_HARDENING_RUNTIME = ACCEPTED`

No repository merge to `main` is authorized by this record.
