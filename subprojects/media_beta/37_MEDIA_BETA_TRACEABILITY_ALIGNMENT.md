# MEDIA BETA Traceability Alignment

Version: 1.0
Date: 2026-08-23
Status: IMPLEMENTED_IN_BRANCH_PENDING_BUILDER_RESYNC_RUNTIME

## Purpose

Align the Research/Critic evidence-audit contract in `K-Research & Critic - MEDIA BETA` with the traceability behavior already runtime-accepted in the main `K-Research & Critic` Core.

This change does NOT alter managed-media ingestion, provider pricing, credit consent, Actions, platform support, or Facebook state.

## Added contract

For every material factual claim:
- keep `required / achieved_independent / exception` claim-level ledger;
- every evidence origin counted in `achieved_independent` must be visible and traceable by source title/citation to that claim;
- `achieved_independent` cannot exceed the number of visibly traceable independent evidence origins;
- duplicates, syndication and derivative reporting do not increase the count;
- a systematic review/meta-analysis counts as one evidence origin unless specific underlying studies were independently inspected and cited;
- Critic verifies evidence-origin traceability before PASS;
- an untraceable PASS count blocks unconditional PASS;
- `SHORTFALL` remains explicit when achieved < required.

The Review Protocol MUST include, for every material factual claim, the table columns exactly:

```text
Claim | Required | Achieved independent | Exception
```

Values must match the visible claim blocks and traceable evidence origins. Exception is `NONE` or `SHORTFALL`.

## Files changed

- `prompts/GPT_STORE_MEDIA_BETA_BUILDER_INSTRUCTIONS.md`
- `prompts/GPT_STORE_MEDIA_MANAGED_BETA_INSTRUCTIONS.md`
- `gpt_store/media_beta_manifest.yaml`
- `tests/test_claim_level_cross_check_enforcement.py`
- `tests/test_media_beta_managed_package.py`

Managed canonical instructions version: `0.3.5-a9.6`.
Manifest compatibility versions remain unchanged (`schema_version: 0.6-beta`, instruction version `0.6-beta-a9.6`).

## Runtime boundary

Existing MEDIA BETA claim-level runtime acceptance remains historical evidence for the prior claim-level contract, but it does not prove the newly added traceability invariant.

Therefore:

`MEDIA_BETA_CLAIM_LEVEL_RUNTIME = ACCEPTED`

`MEDIA_BETA_TRACEABILITY_HARDENING_CODE = IMPLEMENTED`

`MEDIA_BETA_TRACEABILITY_HARDENING_RUNTIME = PENDING`

The actual private MEDIA BETA Custom GPT must be manually resynchronized with `prompts/GPT_STORE_MEDIA_BETA_BUILDER_INSTRUCTIONS.md` and tested in a NEW chat before runtime acceptance.

## Unchanged media invariants

- public YouTube and Instagram remain the accepted adapters;
- Facebook remains in progress / not accepted;
- native Supadata credit cap remains 1;
- Instagram AI fallback remains separately quoted/approved, max 40 credits;
- `credit_charge_uncertain=true` operations are never auto-retried;
- no Helper, cookies, login/session, beta-code prompt, provider API key, or exposed KRCM Job ID in normal owner flow;
- no repository merge to `main` is authorized by this alignment.
