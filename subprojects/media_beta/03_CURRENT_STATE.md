# MEDIA BETA Current State

Canonical implementation checkpoint for continuation without reconstruction.

Version: 5.2
Status: ACTIVE_CHECKPOINT
Checkpoint date: 2026-08-23

## Executive state

Current phase state:

`A4_COMPLETE / A5_COMPLETE / A6_COMPLETE / A7_EXTERNAL_ROLLOUT_PAUSED / A8_BROWSER_ASSISTED_OWNER_BASELINE_COMPLETE / A9_1_COMPLETE / A9_2_DIRECT_YOUTUBE_BLOCKED / A9_2R_MANAGED_NATIVE_COMPLETE / A9_3_DURABLE_MANAGED_COMPLETE / A9_5_PRIVATE_GPT_ZERO_CLIENT_E2E_COMPLETE / A9_8_OWNER_ZERO_CLIENT_YOUTUBE_COMPLETE / A9_6_INSTAGRAM_MANAGED_COMPLETE / A9_6_FACEBOOK_IN_PROGRESS`

Accepted owner-only zero-client adapters:
- public prerecorded YouTube;
- public Instagram Reel through managed native first, with separately authorized AI fallback only when native transcript is unavailable.

Not accepted yet:
- Facebook public Video/Reels;
- Telegram public video posts;
- local audio/video attachment.

Repository `main`, external tester rollout, and production VoiceBridge remain outside the current merge gate.

The main `K-Research & Critic` previously passed final evidence-origin traceability runtime acceptance. MEDIA BETA was then aligned to the same traceability contract and rerun in a NEW chat. That MEDIA BETA run passed the traceability logic but exposed a default-language regression: some user-visible table headings/columns and CriticProfile field labels remained English. The branch now contains a localization hardening for BOTH Core and MEDIA BETA Builder instructions. Both actual Custom GPTs require manual Builder resynchronization and fresh visual regression for the new localization contract.

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

The selected report language controls ALL user-visible workflow text, including prompts, CriticProfile text, section headings, table titles, table columns, CriticProfile field labels, verdict labels, final report, claim verification, and review protocol. Source/transcript language must never switch the report language. Canonical English/internal keys remain internal unless explicitly requested.

For Ukrainian reports use, as applicable:
- `ФІНАЛЬНИЙ ЗВІТ`;
- `ПЕРЕВІРКА ТВЕРДЖЕНЬ`;
- `ПРОТОКОЛ ПЕРЕВІРКИ`;
- `ПІДСУМОК ЗА ТВЕРДЖЕННЯМИ`;
- claim-level columns `Твердження | Потрібно | Отримано незалежних | Виняток`.

Do not expose `Claim-level summary`, `Claim`, `Required`, `Achieved independent`, `Exception` or raw CriticProfile keys such as `profile_id`, `risk_level`, `required_cross_checks`, `approved_at` as Ukrainian user-visible labels unless the user explicitly requests canonical/internal keys.

Ukrainian verdict labels remain:
- VERIFIED -> `ПІДТВЕРДЖЕНО`;
- PARTLY_SUPPORTED -> `ЧАСТКОВО ПІДТВЕРДЖЕНО`;
- UNSUPPORTED -> `НЕ ПІДТВЕРДЖЕНО`;
- CONTRADICTED -> `СУПЕРЕЧИТЬ ДЖЕРЕЛАМ`;
- MISLEADING -> `ВВОДИТЬ В ОМАНУ`;
- UNVERIFIABLE -> `НЕМОЖЛИВО ПЕРЕВІРИТИ`;
- OPINION -> `ДУМКА`.

Canonical localization record: `38_REPORT_LANGUAGE_LABEL_LOCALIZATION_HARDENING.md`.

## CriticProfile gate runtime acceptance

Status: PASS / RUNTIME_ACCEPTED_PRIVATE_OWNER_BETA for the established two-stage gate behavior.

Accepted behavior:
- profile created internally without automatic display;
- first direct-run/review/cancel gate;
- option `2` displays complete unapproved profile;
- edits preserve `REVIEW_REQUIRED` and increment version when appropriate;
- explicit `1` approves and starts Research -> Critic;
- `approved_at` recorded as ISO-8601.

Canonical runtime record: `32_CRITICPROFILE_GATE_RUNTIME_ACCEPTANCE.md`.

The newly required localization of visible CriticProfile field labels is a separate pending visual runtime gate.

## Claim-level cross-check enforcement

Status: PASS / RUNTIME_ACCEPTED_PRIVATE_OWNER_BETA for the earlier claim-level contract.

Each material factual claim maintains:

```text
required: approved required_cross_checks
achieved_independent: independent underlying evidence sources actually obtained
exception: NONE | SHORTFALL
```

Rules:
- floors: `LOW>=0`, `MEDIUM>=1`, `HIGH>=2`, `CRITICAL>=3`;
- count underlying evidence independence, not URL count;
- duplicates, syndication, repeated reporting of one study/source, and source media/transcript do not count separately;
- if achieved < required, mark `SHORTFALL`, state reason, adjust confidence and qualify conclusion;
- Critic verifies claim-by-claim;
- hidden/unqualified shortfall forbids unconditional PASS.

Canonical contract: `33_CLAIM_LEVEL_CROSS_CHECK_ENFORCEMENT.md`.
Canonical prior runtime acceptance: `34_CLAIM_LEVEL_CROSS_CHECK_RUNTIME_ACCEPTANCE.md`.

## MEDIA BETA traceability alignment and latest runtime

Traceability code: IMPLEMENTED.
Traceability logic runtime: PASS.
Final combined runtime acceptance: PENDING localization regression.

Accepted in the latest NEW-chat MEDIA BETA run:
- `risk_level=CRITICAL`;
- `required_cross_checks=3`;
- visible claim-level PASS/SHORTFALL;
- counted evidence origins visibly attributable to claims;
- achieved counts matched visible independent origins;
- derivative systematic-review evidence was not double-counted as an independent origin;
- mandatory four-column claim-level summary was present;
- managed media credits were 0 for the text-only test.

Observed language defect:
- heading `Claim-level summary` appeared in English;
- columns `Claim`, `Required`, `Achieved independent`, `Exception` appeared in English;
- raw CriticProfile keys were visible as field labels.

Therefore:

`MEDIA_BETA_TRACEABILITY_LOGIC_RUNTIME = PASS`

`MEDIA_BETA_REPORT_LABEL_LOCALIZATION_CODE = IMPLEMENTED`

`MEDIA_BETA_REPORT_LABEL_LOCALIZATION_RUNTIME = PENDING`

`MEDIA_BETA_TRACEABILITY_HARDENING_RUNTIME = PENDING_FINAL_LANGUAGE_REGRESSION`

Updated branch artifacts:
- `prompts/GPT_STORE_MEDIA_BETA_BUILDER_INSTRUCTIONS.md`;
- `prompts/GPT_STORE_MEDIA_MANAGED_BETA_INSTRUCTIONS.md` version `0.3.6-a9.6`;
- `gpt_store/media_beta_manifest.yaml`;
- claim-level/package regression tests.

Canonical traceability alignment: `37_MEDIA_BETA_TRACEABILITY_ALIGNMENT.md`.
Canonical localization hardening: `38_REPORT_LANGUAGE_LABEL_LOCALIZATION_HARDENING.md`.

## Main Core track

Evidence-origin traceability status remains accepted from the previous NEW-chat runtime:

`CORE_TRACEABILITY_HARDENING_RUNTIME = ACCEPTED`

The Core Builder now also contains the stricter user-visible label localization contract:
- Ukrainian headings/table titles/columns by default;
- localized CriticProfile field labels;
- canonical raw keys internal unless requested;
- Ukrainian claim-level protocol columns `Твердження | Потрібно | Отримано незалежних | Виняток`.

This NEW localization behavior is not yet runtime accepted because the actual main Custom GPT still requires manual resynchronization with the updated `prompts/GPT_STORE_CORE_BUILDER_INSTRUCTIONS.md`.

`CORE_REPORT_LABEL_LOCALIZATION_CODE = IMPLEMENTED`

`CORE_REPORT_LABEL_LOCALIZATION_RUNTIME = PENDING`

Canonical Core traceability records:
- `35_CORE_RUNTIME_TRACEABILITY_HARDENING.md`;
- `36_CORE_TRACEABILITY_RUNTIME_ACCEPTANCE.md`.

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
Accepted YouTube evidence: source language `ru`; 277 timestamped segments; one approved native credit; no Helper, cookies, login/session state or residential proxy; no automatic AI fallback.

## Credit consent invariant

A billable managed transcript request must never start merely because a URL was pasted. Native hard cap: `credit_consent.max_credits = 1`. If native transcript is unavailable, previous consent does not authorize managed AI generation. Automatic AI fallback is prohibited.

## A9.3 - Durable managed jobs

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

`CORE_REPORT_LABEL_LOCALIZATION_CODE = IMPLEMENTED`

`CORE_REPORT_LABEL_LOCALIZATION_RUNTIME = PENDING`

`MEDIA_BETA_TRACEABILITY_LOGIC_RUNTIME = PASS`

`MEDIA_BETA_REPORT_LABEL_LOCALIZATION_CODE = IMPLEMENTED`

`MEDIA_BETA_REPORT_LABEL_LOCALIZATION_RUNTIME = PENDING`

These markers do not authorize repository merge, external testers, production VoiceBridge changes, private/authenticated media, automatic AI fallback, Facebook, Telegram, or local upload.

## Next task

`Manually resynchronize BOTH actual Custom GPT Builder instruction sets (main Core and MEDIA BETA) with their latest branch Builder files, then run NEW-chat visual regressions to verify Ukrainian default headings/table columns/CriticProfile field labels. After PASS, resume A9.6 Facebook remediation without replaying any uncertain-charge operation.`
