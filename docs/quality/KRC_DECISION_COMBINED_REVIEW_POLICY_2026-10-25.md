# KRC owner decision №75 — combined Critic and external reviewer

**Date:** 2026-10-25  
**Owner approval:** Option 3 — automated Critic now, genuine independent external scientific reviewer only for final scientific acceptance.

## Binding decision
1. DEVELOPMENT and INTERNAL_VALIDATION: permit automatic deterministic Critic without an external reviewer, preserve evidence provenance rules, PASS/SHORTFALL, uncertainty and revision logs.
2. FINAL_SCIENTIFIC_ACCEPTANCE: do not claim complete review unless separately authenticated external reviewer attestation exists and author approval is recorded. No synthetic test reviewer may count.
3. No automatic system may guarantee truth, research novelty, journal acceptance, or AI-detector evasion.
4. Owner manual intervention is **not required now**. Final reviewer selection and author approval are **deferred**.
5. FREE_ONLY, research only; public publication, MEDIA, production deployment, public security/load tests stay on hold.
6. Continue P1/P3/P4 first, prepare P2 technical boundary in parallel, P5 then P7. P6 K_Science live connectivity depends on the separate K_Sentinel readiness.

## Implementation
- `src/krc_research/review_policy.py`: explicit state of owner-approved combined review, allowed phases, status and terminal gates.
- `src/krc_research/scientific_cycle_v3.py`: emits `review_policy` for INTERNAL_VALIDATION using **actually executed** deterministic Critic, never a self-reported PASS.
- `tests/test_p0_review_policy.py`: seven new positive/negative cases, including absent reviewer, missing author approval, invalid invented PASS and final nonpublication guarantee.

## Acceptance
Isolated `krc-cobalt` checkout `/tmp/krc-p0-offline-20261025`: `pytest -q tests/` → **146 PASSED / 0 failed in 0.98s**, exit 0. Previous baseline 139 PASS. Production unchanged. This is engineering validation only.

## Manual actions
**Now: NONE.** At final scientific stage the owner must nominate/authorize an independent scientific reviewer, arrange assessment of actual original source material, and explicitly approve the finalized scholarly output. If the reviewer is unavailable the final gate stays `AWAIT_EXTERNAL_REVIEWER` and scientific publication acceptance stays NO_GO.
