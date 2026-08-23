# MEDIA BETA Current State

Canonical implementation checkpoint for continuation without reconstruction.

Version: 5.1
Status: ACTIVE_CHECKPOINT
Checkpoint date: 2026-08-23

## Executive state

Current phase state:

`A4_COMPLETE / A5_COMPLETE / A6_COMPLETE / A7_EXTERNAL_ROLLOUT_PAUSED / A8_BROWSER_ASSISTED_OWNER_BASELINE_COMPLETE / A9_1_COMPLETE / A9_2_DIRECT_YOUTUBE_BLOCKED / A9_2R_MANAGED_NATIVE_COMPLETE / A9_3_DURABLE_MANAGED_COMPLETE / A9_5_PRIVATE_GPT_ZERO_CLIENT_E2E_COMPLETE / A9_8_OWNER_ZERO_CLIENT_YOUTUBE_COMPLETE / A9_6_INSTAGRAM_MANAGED_COMPLETE / A9_6_FACEBOOK_IN_PROGRESS`

Current accepted owner-only zero-client adapters:
- public prerecorded YouTube;
- public Instagram Reel through managed native first, with separately authorized AI fallback only when native transcript is unavailable.

Not accepted yet:
- Facebook public Video/Reels;
- Telegram public video posts;
- local audio/video attachment.

Repository `main`, external tester rollout, and production VoiceBridge remain outside the current merge gate.

The main `K-Research & Critic` has passed final Core traceability runtime acceptance. The same traceability contract is now implemented in the MEDIA BETA branch instructions/tests but still requires manual private-Builder resynchronization and a NEW-chat runtime regression.

## Repositories and isolation boundary

KRC:
- repo `kolemasakar/K_Research_Critic`;
- branch `agent/video-url-research`;
- draft PR #8;
- repository `main` unchanged.

VoiceBridge:
- repo `kolemasakar/VoiceBridge`;
- branch `agent/krc-media-transcript`;
- draft PR #28;
- production service and `main` unchanged.

Isolated beta runtime:
- service `voicebridge-krc-media-beta-kolemasakar`;
- service ID `srv-da1kic5bedkc73d6fk60`;
- endpoint `https://voicebridge-krc-media-beta-kolemasakar.onrender.com`;
- auto-deploy false.

Do not merge PR #8 or PR #28 and do not target production without a separate explicit owner decision.

## Accepted owner UX

```text
supported public media URL in ChatGPT
 -> analysis mode if missing
 -> no separate media opening
 -> no Helper
 -> no beta-code prompt
 -> no manual Job ID
 -> native managed credit preflight
 -> explicit user consent
 -> ChatGPT consequential-Action confirmation when shown
 -> native transcript when available
 -> for supported Instagram Reel only: if native unavailable, separate AI preflight + separate explicit consent
 -> CriticProfile created internally
 -> direct analysis OR profile review/edit
 -> requested K-Research & Critic workflow
 -> result in same conversation
```

Remote adapters remain public-only. Do not request platform login/password/cookies/session state/account tokens. Auth/private content must return `UNSUPPORTED_PRIVATE_OR_AUTH_REQUIRED`.

## Language invariant

Default user-facing report language is Ukrainian unless the user explicitly requests another language.

The selected report language controls all user-visible workflow text: prompts, CriticProfile, headings, verdict labels, final report, claim verification, and review protocol. The media/transcript/source language must never switch the report language.

For Ukrainian reports use:
- VERIFIED -> `ПІДТВЕРДЖЕНО`;
- PARTLY_SUPPORTED -> `ЧАСТКОВО ПІДТВЕРДЖЕНО`;
- UNSUPPORTED -> `НЕ ПІДТВЕРДЖЕНО`;
- CONTRADICTED -> `СУПЕРЕЧИТЬ ДЖЕРЕЛАМ`;
- MISLEADING -> `ВВОДИТЬ В ОМАНУ`;
- UNVERIFIABLE -> `НЕМОЖЛИВО ПЕРЕВІРИТИ`;
- OPINION -> `ДУМКА`.

## CriticProfile gate runtime acceptance

Status: PASS / RUNTIME_ACCEPTED_PRIVATE_OWNER_BETA.

On 2026-08-23 the actual private `K-Research & Critic - MEDIA BETA` Custom GPT was synchronized with the two-stage CriticProfile gate and tested using a medicine/health research request.

Observed PASS sequence:
- profile created internally without automatic display;
- first direct-run/review/cancel gate displayed correctly;
- option `2` displayed the complete unapproved profile;
- profile edit preserved `REVIEW_REQUIRED` and produced version 2;
- second gate repeated after edit;
- option `1` approved version 2 and immediately started Research -> Critic;
- final Ukrainian report recorded profile version 2, 2 critic iterations, `PASS`, reliability `0.89`, `COMPLETED_WITH_LIMITATIONS`, and 0 media credits.

Canonical record: `32_CRITICPROFILE_GATE_RUNTIME_ACCEPTANCE.md`.

## MEDIA BETA claim-level cross-check enforcement

Status: PASS / RUNTIME_ACCEPTED_PRIVATE_OWNER_BETA for the prior claim-level contract.

The Builder contract requires a ledger for EACH material factual claim before verdict:

```text
required: approved required_cross_checks
achieved_independent: independent underlying evidence sources actually obtained
exception: NONE | SHORTFALL
```

Accepted rules:
- default floors: `LOW>=0`, `MEDIUM>=1`, `HIGH>=2`, `CRITICAL>=3`;
- count underlying evidence independence, not URL count;
- duplicates, syndication, repeated reporting of one study/source, and source media/transcript do not count separately;
- if `achieved_independent < required`, mark `SHORTFALL`, state the reason, lower confidence as appropriate, and qualify the conclusion;
- never claim the requirement was met for that claim;
- Critic verifies the ledger claim-by-claim;
- unconditional `PASS` is forbidden while a material shortfall is hidden or unqualified;
- fact-check output shows `Cross-check: achieved/required - PASS|SHORTFALL` for each material claim.

Observed acceptance evidence included a real `Cross-check: 1/3 - SHORTFALL` and final `COMPLETED_WITH_LIMITATIONS` rather than unconditional `PASS`.

Canonical contract: `33_CLAIM_LEVEL_CROSS_CHECK_ENFORCEMENT.md`.
Canonical runtime record: `34_CLAIM_LEVEL_CROSS_CHECK_RUNTIME_ACCEPTANCE.md`.

`cross_check_claim_level_runtime_accepted=true` remains historical acceptance for this prior contract.

## MEDIA BETA traceability alignment

Status: IMPLEMENTED_IN_BRANCH / RUNTIME_PENDING.

The MEDIA BETA Research/Critic instructions are now aligned with the traceability contract already accepted in the main Core:
- every evidence origin counted in `achieved_independent` must be visible and traceable by source title/citation to that claim;
- achieved count cannot exceed visibly traceable independent evidence origins;
- duplicates/derivative reporting do not increase the count;
- a systematic review/meta-analysis counts as one evidence origin unless specific underlying studies were independently inspected and cited;
- Critic verifies evidence-origin traceability before PASS;
- an untraceable PASS count blocks unconditional PASS;
- Review Protocol MUST contain `Claim | Required | Achieved independent | Exception` for every material factual claim.

Updated branch artifacts:
- `prompts/GPT_STORE_MEDIA_BETA_BUILDER_INSTRUCTIONS.md`;
- `prompts/GPT_STORE_MEDIA_MANAGED_BETA_INSTRUCTIONS.md` version `0.3.5-a9.6`;
- `gpt_store/media_beta_manifest.yaml`;
- claim-level/package regression tests.

Manifest compatibility versions remain `schema_version: 0.6-beta` and instruction version `0.6-beta-a9.6`.

Canonical alignment record: `37_MEDIA_BETA_TRACEABILITY_ALIGNMENT.md`.

Current runtime markers:

`MEDIA_BETA_TRACEABILITY_HARDENING_CODE = IMPLEMENTED`

`MEDIA_BETA_TRACEABILITY_HARDENING_RUNTIME = PENDING`

`gpt_builder_private_update_required = true`

## Main Core GPT runtime acceptance

Status: PASS / RUNTIME_ACCEPTED_MAIN_CORE.

The main `K-Research & Critic` was manually synchronized with the hardened clean Core Builder and retested in a NEW chat using the cold-shower CRITICAL medical query.

Accepted behavior:
- two-stage CriticProfile gate worked on the current GPT version;
- `risk_level=CRITICAL`;
- `required_cross_checks=3`;
- material claims exposed `PASS` or `SHORTFALL` claim-by-claim;
- `3/3 PASS` values were backed by three named/cited independent evidence origins visible to the user;
- the 2016 sick-leave result remained `1/3 - SHORTFALL`;
- a later systematic review repeating the 2016 result was explicitly not counted as a second independent origin;
- the mandatory claim-level protocol summary table was present and consistent with visible claim blocks;
- Critic ran `REVISE -> PASS`;
- final reliability score was `0.88`;
- remaining evidence scarcity was stated explicitly.

Canonical hardening record: `35_CORE_RUNTIME_TRACEABILITY_HARDENING.md`.
Canonical runtime acceptance: `36_CORE_TRACEABILITY_RUNTIME_ACCEPTANCE.md`.

`CORE_TRACEABILITY_HARDENING_RUNTIME = ACCEPTED`

## A8 browser-assisted baseline

Status: PASS / COMPLETE_BASELINE. A8 Helper 0.2.2 / `KRCC_` remains emergency/dev fallback evidence only.

## A9.1 - Server-side STT privacy parity

Status: PASS / COMPLETE. AssemblyAI EU routing remains available for the accepted browser-assisted fallback path.

## A9.2 - Direct Render-to-YouTube

Status: BLOCKED / CLOSED AS PRIMARY STRATEGY.
Disposition: `DIRECT_RENDER_YOUTUBE = BLOCKED_BY_DATACENTER_ANTIBOT`.

## A9.2R - Managed provider native route

Status: PASS / COMPLETE_FOR_NATIVE_OWNER_BETA.
Provider: `Supadata`. Mode: `native`.
Initial acceptance source: `https://www.youtube.com/watch?v=IzYyKRx7Qwg`.
Accepted transcript facts: detected language `ru`; 277 timestamped segments; one approved native credit; no Helper, cookies, login/session state or residential proxy; no automatic AI fallback.

## Credit consent invariant

A billable managed transcript request must never start merely because a URL was pasted. Native hard cap: `credit_consent.max_credits = 1`. If native transcript is unavailable, previous consent does not authorize managed AI generation. Automatic AI fallback is prohibited.

## A9.3 - Durable managed jobs and credit-safe idempotency

Status: PASS / COMPLETE.
Accepted live code: `7736f2e7acc5abbb3415e3753d0ca022c1b8d7b2`.
Durable jobs remain restart-safe; duplicate start reuses the completed job; uncertain interrupted provider operations are not auto-replayed.

## A9.5 - Private GPT Action integration

Status: PASS / COMPLETE.
Accepted VoiceBridge owner-auth implementation: `970d7cc5819a623ec1d3cc7a70aceb44bfe311b9`.
Actual private GPT zero-client YouTube E2E remains accepted with Supadata native, source language `ru`, 277 segments, 1 credit, reliability `0.91`, `PASS / COMPLETED`.

## A9.6 - Instagram managed adapter

Status: PASS / COMPLETE_FOR_MANAGED_OWNER_BETA.
Accepted live flow: native 1 credit -> `AWAITING_AI_CONSENT` -> separate AI quote/approval -> generated transcript; final detected language `en`, 11 segments, cumulative 3 credits. Automatic AI fallback remains disabled.

## A9.6 - Facebook adapter

Status: IN_PROGRESS / NOT_ACCEPTED.
A separately authorized Facebook AI generate request failed with `MANAGED_PROVIDER_TRANSCRIPT_INVALID`, `segments=0`, `credit_charge_uncertain=true`; automatic retry is prohibited. Nested async-result parser remediation is committed as `f6b32c2a03425deaecadd10fc902671d62eaab5d`, but latest recorded isolated deploy attempt failed.

## Completion markers

`OWNER_ONLY_ZERO_CLIENT_YOUTUBE = COMPLETE`

`OWNER_ONLY_MANAGED_INSTAGRAM_REEL = COMPLETE`

`CRITICPROFILE_TWO_STAGE_GATE_RUNTIME = ACCEPTED`

`CLAIM_LEVEL_CROSS_CHECK_RUNTIME = ACCEPTED`

`CORE_TRACEABILITY_HARDENING_RUNTIME = ACCEPTED`

`MEDIA_BETA_TRACEABILITY_HARDENING_CODE = IMPLEMENTED`

`MEDIA_BETA_TRACEABILITY_HARDENING_RUNTIME = PENDING`

These markers do not authorize repository merge, external testers, production VoiceBridge changes, private/authenticated media, automatic AI fallback, Facebook, Telegram, or local upload.

## Next task

`Manually resynchronize the private K-Research & Critic - MEDIA BETA Builder with the updated Builder instructions and run one NEW-chat traceability regression. After PASS, resume A9.6 Facebook remediation without replaying any uncertain-charge operation.`
