# MEDIA BETA Current State

Canonical implementation checkpoint for continuation without reconstruction.

Version: 5.3
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

## Accepted Research/Critic workflow

Two-stage CriticProfile gate is runtime accepted:
- profile created internally;
- first gate offers direct run / review-edit / cancel;
- explicit `1` approves before research;
- displayed profile edits remain `REVIEW_REQUIRED` until re-approved;
- approval records ISO-8601 timestamp.

Claim-level cross-check enforcement is runtime accepted:
- floors: `LOW>=0`, `MEDIUM>=1`, `HIGH>=2`, `CRITICAL>=3`;
- every material factual claim maintains `required / achieved_independent / exception`;
- independence is based on underlying evidence, not URL count;
- derivative reporting and systematic-review repetition are not double-counted;
- real shortfalls remain visible and qualified;
- Critic audits each material claim before PASS.

Evidence-origin traceability is runtime accepted in BOTH main Core and MEDIA BETA:
- each origin counted in `achieved_independent` is visibly attributable to the claim;
- achieved count cannot exceed visible independent origins;
- traceable `3/3 PASS` values were demonstrated;
- a real `1/3 SHORTFALL` remained visible;
- MEDIA BETA latest text-only regression used 0 managed media credits.

Canonical records:
- `31_CRITICPROFILE_GATE_UX_UPDATE.md`;
- `32_CRITICPROFILE_GATE_RUNTIME_ACCEPTANCE.md`;
- `33_CLAIM_LEVEL_CROSS_CHECK_ENFORCEMENT.md`;
- `34_CLAIM_LEVEL_CROSS_CHECK_RUNTIME_ACCEPTANCE.md`;
- `35_CORE_RUNTIME_TRACEABILITY_HARDENING.md`;
- `36_CORE_TRACEABILITY_RUNTIME_ACCEPTANCE.md`;
- `37_MEDIA_BETA_TRACEABILITY_ALIGNMENT.md`;
- `39_REPORT_LANGUAGE_AND_MEDIA_TRACEABILITY_RUNTIME_ACCEPTANCE.md`.

## Report-language invariant

Default user-facing report language is Ukrainian unless the user explicitly requests another language.

The selected report language controls ALL user-visible workflow text including:
- prompts;
- CriticProfile presentation;
- section headings;
- table titles and columns;
- CriticProfile field labels;
- verdict labels;
- final report;
- claim verification;
- review protocol.

Canonical English/internal keys remain internal unless explicitly requested.

For Ukrainian reports use, as applicable:
- `ФІНАЛЬНИЙ ЗВІТ`;
- `ПЕРЕВІРКА ТВЕРДЖЕНЬ`;
- `ПРОТОКОЛ ПЕРЕВІРКИ`;
- `ПІДСУМОК ЗА ТВЕРДЖЕННЯМИ`;
- columns `Твердження | Потрібно | Отримано незалежних | Виняток`.

Latest NEW-chat regressions in BOTH actual Custom GPTs passed this localization contract. Main Core displayed the Ukrainian claim summary and localized profile summary. MEDIA BETA displayed localized CriticProfile field labels such as `Ідентифікатор профілю`, `Рівень ризику`, `Необхідних незалежних перевірок`, and `Час схвалення`.

Canonical hardening record: `38_REPORT_LANGUAGE_LABEL_LOCALIZATION_HARDENING.md`.
Canonical runtime record: `39_REPORT_LANGUAGE_AND_MEDIA_TRACEABILITY_RUNTIME_ACCEPTANCE.md`.

## Runtime markers

`CRITICPROFILE_TWO_STAGE_GATE_RUNTIME = ACCEPTED`

`CLAIM_LEVEL_CROSS_CHECK_RUNTIME = ACCEPTED`

`CORE_TRACEABILITY_HARDENING_RUNTIME = ACCEPTED`

`CORE_REPORT_LABEL_LOCALIZATION_RUNTIME = ACCEPTED`

`MEDIA_BETA_TRACEABILITY_LOGIC_RUNTIME = PASS`

`MEDIA_BETA_TRACEABILITY_HARDENING_RUNTIME = ACCEPTED`

`MEDIA_BETA_REPORT_LABEL_LOCALIZATION_RUNTIME = ACCEPTED`

`gpt_builder_private_update_required = false`

A compact Markdown copy may visually concatenate adjacent table-header text; this is non-blocking while the four required labels/columns remain structurally present in the actual ChatGPT output.

## Accepted owner media UX

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
 -> Instagram only: if native unavailable, separate AI preflight + separate explicit consent
 -> CriticProfile gate
 -> Research -> Critic
 -> result in same conversation
```

Remote adapters remain public-only. Do not request platform login/password/cookies/session state/account tokens.

## Credit consent invariant

A billable managed transcript request must never start merely because a URL was pasted.
- native Supadata hard cap: 1 approved credit;
- Instagram AI fallback: separate quote + separate explicit approval;
- AI rate: 2 credits/minute;
- conservative maximum: 40 credits / 20 minutes;
- automatic AI fallback prohibited;
- `credit_charge_uncertain=true` operation must never be automatically retried or replayed.

## Accepted A9 media milestones

### A9.2R - managed native YouTube

PASS. Supadata native zero-client path accepted. Initial owner E2E evidence: source language `ru`, 277 timestamped segments, 1 credit.

### A9.3 - durable managed jobs

PASS. Durable jobs restart-safe; duplicate start reuses completed job; uncertain interrupted provider operations are not replayed. Accepted VoiceBridge commit: `7736f2e7acc5abbb3415e3753d0ca022c1b8d7b2`.

### A9.5 / A9.8 - private GPT integration and owner YouTube E2E

PASS. Owner auth accepted; private GPT zero-client YouTube path complete. Accepted owner-auth commit: `970d7cc5819a623ec1d3cc7a70aceb44bfe311b9`.

### A9.6 - Instagram

PASS for isolated owner beta. Accepted flow: native 1 credit -> `AWAITING_AI_CONSENT` -> separate AI quote/approval -> generated transcript; source language `en`, 11 segments, cumulative 3 credits.

### A9.6 - Facebook

IN_PROGRESS / NOT_ACCEPTED.

A separately authorized Facebook AI generate request failed with:
- `MANAGED_PROVIDER_TRANSCRIPT_INVALID`;
- `segments=0`;
- `credit_charge_uncertain=true`.

Automatic retry/replay is prohibited. Nested async-result parser remediation exists in VoiceBridge commit `f6b32c2a03425deaecadd10fc902671d62eaab5d`, but the latest recorded isolated deploy attempt failed.

## Next task

Resume A9.6 Facebook remediation without replaying the uncertain-charge operation:
1. deploy parser remediation without a billable provider call;
2. verify isolated service health/capability;
3. obtain a fresh credit quote;
4. require fresh explicit authorization;
5. execute one fresh acceptance test;
6. only after backend PASS, run private GPT E2E.

These markers do NOT authorize repository merge, external tester rollout, production VoiceBridge changes, private/authenticated media, automatic AI fallback, Facebook acceptance, Telegram, or local upload.
