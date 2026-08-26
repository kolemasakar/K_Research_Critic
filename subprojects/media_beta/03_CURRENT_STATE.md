# MEDIA BETA Current State

Canonical implementation checkpoint for continuation without reconstruction.

Version: 6.2
Status: ACTIVE_CHECKPOINT
Checkpoint date: 2026-08-26

## Executive state

Current phase state:

`A4_COMPLETE / A5_COMPLETE / A6_COMPLETE / A7_EXTERNAL_ROLLOUT_PAUSED / A8_BROWSER_ASSISTED_OWNER_BASELINE_COMPLETE / A9_OWNER_ZERO_CLIENT_MEDIA_INPUT_ACCEPTED / YOUTUBE_ACCEPTED / INSTAGRAM_ACCEPTED / FACEBOOK_COBALT_ACCEPTED / FACEBOOK_FAILURE_POLICY_E2E_ACCEPTED / TELEGRAM_ACCEPTED / LOCAL_ATTACHMENT_PRIVATE_GPT_E2E_ACCEPTED / A10_COPY_SAFE_RUNTIME_RETEST_PENDING`

A9.10 remains accepted. A10 does not reopen media transport/transcription. It is presentation stabilization for the claim-summary table plus canonical instruction alignment.

Accepted owner-only zero-client ingress:
- prerecorded YouTube;
- Instagram Reel;
- Facebook Video/Reel through free Cobalt retrieval -> AssemblyAI -> durable KRCM;
- supported public Telegram video posts through public Telegram web/embed retrieval -> trusted Telegram CDN -> AssemblyAI -> durable KRCM;
- one local audio/video attachment from the current ChatGPT conversation through `openaiFileIdRefs` -> trusted OpenAI attachment delivery -> AssemblyAI -> durable KRCM.

Historical/not-active boundaries:
- Facebook Supadata route is historical/not accepted;
- ScrapeCreators paid Facebook fallback is reserve-only, unconfigured, inactive and not offerable;
- private/authenticated Telegram retrieval is unsupported;
- paid Telegram fallback is unsupported;
- A8 Helper is fallback evidence only and is not normal owner UX.

Repository `main`, production VoiceBridge, external tester rollout and public sharing remain outside the current release gate.

## Repositories and isolation boundary

KRC:
- repo `kolemasakar/K_Research_Critic`;
- branch `agent/video-url-research`;
- draft PR #8;
- `main` unchanged.

VoiceBridge:
- repo `kolemasakar/VoiceBridge`;
- branch `agent/krc-media-transcript`;
- draft PR #28;
- `main` unchanged.

Isolated beta runtime:
- Render service `voicebridge-krc-media-beta-kolemasakar`;
- production VoiceBridge not targeted.

## Accepted Research/Critic workflow

Two-stage CriticProfile gate is runtime accepted:
- profile created before independent research;
- first gate offers direct run / review-edit / cancel;
- explicit `1` approves before research;
- material profile changes require re-approval.

Claim-level cross-check enforcement is runtime accepted:
- floors `LOW>=0`, `MEDIUM>=1`, `HIGH>=2`, `CRITICAL>=3`;
- every material factual claim maintains `required / achieved_independent / exception`;
- independence is based on underlying evidence, not URL count;
- real shortfalls remain visible and qualified;
- achieved cannot exceed visible independent evidence origins;
- Critic audits material claims before PASS.

Report language defaults to Ukrainian unless explicitly changed by the user.

## A9 runtime markers retained

`CRITICPROFILE_TWO_STAGE_GATE_RUNTIME = ACCEPTED`

`CLAIM_LEVEL_CROSS_CHECK_RUNTIME = ACCEPTED`

`CORE_TRACEABILITY_HARDENING_RUNTIME = ACCEPTED`

`CORE_REPORT_LABEL_LOCALIZATION_RUNTIME = ACCEPTED`

`MEDIA_BETA_TRACEABILITY_HARDENING_RUNTIME = ACCEPTED`

`MEDIA_BETA_REPORT_LABEL_LOCALIZATION_RUNTIME = ACCEPTED`

`a9_7_i_private_gpt_e2e_complete = true`

`managed_telegram_private_gpt_e2e_complete = true`

`managed_attachment_transport_live_accepted = true`

`managed_attachment_ingestion_live_accepted = true`

`managed_attachment_private_gpt_e2e_complete = true`

`rollout_state = A9_10_ATTACHMENT_PRIVATE_GPT_E2E_ACCEPTED`

## A10 stabilization state

Repository package:
- Builder package identity remains `0.9.1-beta-a10`;
- Action schema `0.6.0-a9.10` unchanged;
- canonical managed reference `0.5.0-a10-stabilization`;
- strict four-column Markdown table contract present;
- copy-safe fenced-table fallback added;
- backend/VoiceBridge unchanged.

### Runtime attempt 1

Owner applied the initial A10 Builder package and reran Telegram fact-check on `https://t.me/techcrimes/12107`.

Observed:
- CriticProfile gate: PASS;
- visible `ПІДСУМОК ЗА ТВЕРДЖЕННЯМИ`: PASS as four distinct columns;
- whole-response Copy: FAIL because the rendered table header serialized as `ТвердженняПотрібноОтримано незалежнихВиняток` while row values stayed intact.

This is treated as a ChatGPT UI copy/serialization defect rather than a malformed rendered-table source because the owner screenshot shows four correct visual columns.

### Copy-safe refinement

The Builder now requires both:

```text
| Твердження | Потрібно | Отримано незалежних | Виняток |
| --- | ---: | ---: | --- |
```

and immediately afterward:
- heading `КОПІЯ ДЛЯ НАДІЙНОГО КОПІЮВАННЯ`;
- one fenced `text` code block;
- the same complete table with literal `|` delimiters;
- identical values in rendered and copy-safe representations.

Regression coverage: `tests/test_a10_copy_safe_claim_table.py`.

Final refined package head:
`dc8120d43219cc39c02fa10f6ec0136664af067b`

Final refined-package Tests run:
`33005278994` -> SUCCESS, including Python 3.13, Python 3.14, Ruff, mypy, repository policy, GPT Store package validation and coverage.

Authoritative A10 markers intentionally remain pending until the refined package is applied to the actual private GPT and retested:
- `builder_runtime_applied = false`;
- `gpt_builder_private_update_required = true`;
- `claim_summary_table_hardening_package_ready = true`;
- `claim_summary_table_hardening_runtime_applied = false`;
- `a10_claim_summary_table_runtime_accepted = false`.

Canonical A10 record:
`51_A10_STABILIZATION_AND_RELEASE_BOUNDARY.md`.

## Accepted owner media UX

```text
supported public media URL OR one local audio/video attachment
 -> no Helper / beta code / manual Job ID / platform login
 -> route by source type
 -> transcript acquisition
 -> CriticProfile gate only after transcript availability
 -> explicit owner approval
 -> Research -> Critic
 -> localized final report in same conversation
```

Routes:

```text
YouTube/Instagram
 -> managed native first where applicable
 -> billable Supadata operations retain explicit consent gates

Facebook
 -> startManagedFacebookFallback
 -> Cobalt success -> AssemblyAI -> durable KRCM
 -> Cobalt failure -> media unavailable -> STOP
 -> no active paid Facebook continuation

Telegram
 -> startManagedTelegramPublicTranscription
 -> public Telegram web/embed -> trusted Telegram CDN
 -> AssemblyAI -> durable KRCM
 -> retrieval credits 0
 -> unavailable/no-speech -> STOP
 -> no login/cookies/session/bot token or paid fallback

Local attachment
 -> startManagedAttachmentTranscription
 -> openaiFileIdRefs
 -> trusted *.oaiusercontent.com temporary delivery
 -> bounded ingestion / media normalization
 -> AssemblyAI -> durable KRCM
 -> retrieval credits 0
 -> no Helper or user-facing attachment token
```

## A9.10 local attachment accepted state

Actual owner test:
- local `videoplayback (1).mp4`, approximately 5 MB;
- canonical CriticProfile gate reached;
- owner selected `1`;
- AssemblyAI language confidence `0.9984`;
- source duration `70.668 s`;
- STT accounting `71 s`;
- two durable transcript segments;
- retrieval/provider credits `0`;
- seven material claims evaluated;
- real `0/1 - SHORTFALL` preserved;
- reliability `88/100`;
- final status `COMPLETED_WITH_LIMITATIONS`;
- no KRCM Job ID, OpenAI file ID, signed URL or provider credential exposed.

Canonical records:
- `49_A9_10_ATTACHMENT_TRANSPORT_RUNTIME_ACCEPTANCE.md`;
- `50_A9_10_PRIVATE_GPT_LOCAL_ATTACHMENT_E2E_ACCEPTANCE.md`.

## Credit and replay invariants

- local attachment retrieval credits `0`; AssemblyAI STT accounted separately;
- Telegram public retrieval credits `0`, no paid fallback;
- Facebook active retrieval free Cobalt-only;
- Supadata native hard cap one explicitly approved credit;
- Instagram AI fallback requires separate quote and explicit consent;
- automatic managed AI fallback prohibited;
- `credit_charge_uncertain=true` operations never automatically retried;
- durable duplicate starts reuse existing jobs where defined.

## Current next boundary

1. Re-apply the refined `prompts/GPT_STORE_MEDIA_BETA_BUILDER_INSTRUCTIONS.md` to the actual private MEDIA BETA GPT.
2. Do not change/reimport Action schema `0.6.0-a9.10`.
3. Run a fresh Telegram final-report regression.
4. Confirm the visual table is four columns.
5. Confirm the following copy-safe fenced `text` table preserves literal `|` separators when the whole response is copied and matches the visual values exactly.
6. Only after that mark A10 runtime accepted and clear runtime-pending markers.

External tester/public sharing, repository `main` merge and production VoiceBridge promotion remain paused until a separate explicit owner decision.
