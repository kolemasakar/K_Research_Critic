# MEDIA BETA Current State

Canonical implementation checkpoint for continuation without reconstruction.

Version: 6.1
Status: ACTIVE_CHECKPOINT
Checkpoint date: 2026-08-26

## Executive state

Current phase state:

`A4_COMPLETE / A5_COMPLETE / A6_COMPLETE / A7_EXTERNAL_ROLLOUT_PAUSED / A8_BROWSER_ASSISTED_OWNER_BASELINE_COMPLETE / A9_OWNER_ZERO_CLIENT_MEDIA_INPUT_ACCEPTED / YOUTUBE_ACCEPTED / INSTAGRAM_ACCEPTED / FACEBOOK_COBALT_ACCEPTED / FACEBOOK_FAILURE_POLICY_E2E_ACCEPTED / TELEGRAM_ACCEPTED / LOCAL_ATTACHMENT_PRIVATE_GPT_E2E_ACCEPTED / A10_STABILIZATION_PACKAGE_READY_RUNTIME_PENDING`

A9.10 remains accepted. A10 does not reopen the accepted transport/transcription workflow; it hardens final-report Markdown presentation and aligns the canonical managed instruction reference.

Accepted owner-only zero-client ingress:
- prerecorded YouTube;
- Instagram Reel;
- Facebook Video/Reel through free Cobalt retrieval -> AssemblyAI -> durable KRCM;
- supported public Telegram video posts through public Telegram web/embed retrieval -> trusted Telegram CDN -> AssemblyAI -> durable KRCM;
- one local audio/video attachment from the current ChatGPT conversation through `openaiFileIdRefs` -> trusted OpenAI attachment delivery -> AssemblyAI -> durable KRCM.

Historical/not-active boundaries:
- Facebook Supadata route is historical/not accepted;
- ScrapeCreators paid Facebook fallback is reserve-only, unconfigured, inactive and not offerable in active MEDIA BETA;
- private/authenticated Telegram retrieval is unsupported;
- paid Telegram fallback is unsupported;
- A8 Helper remains fallback evidence only and is not normal owner UX.

Repository `main`, production VoiceBridge, external tester rollout and public sharing remain outside the current merge/release gate.

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

Report language defaults to Ukrainian unless explicitly changed by the user. User-visible workflow text, CriticProfile labels, verdicts and final report labels follow the selected report language.

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
- Builder instructions: `0.9.1-beta-a10`;
- Action schema target: `0.6.0-a9.10` unchanged;
- canonical managed reference: `0.5.0-a10-stabilization`;
- claim-summary strict Markdown hardening: package-ready;
- actual private-GPT Builder application of `0.9.1-beta-a10`: pending;
- runtime acceptance of the table fix: pending.

Authoritative A10 markers:
- `builder_runtime_applied = false` for the new A10 package;
- `gpt_builder_private_update_required = true`;
- `claim_summary_table_hardening_package_ready = true`;
- `claim_summary_table_hardening_runtime_applied = false`;
- `a10_claim_summary_table_runtime_accepted = false`;
- `stabilization_state = A10_CLAIM_TABLE_HARDENING_PACKAGE_READY_RUNTIME_PENDING`.

The previous A9.10 Builder/runtime acceptance remains historical evidence for the accepted media flow; the `false` A10 Builder marker means only that the new formatting package has not yet been applied to the actual private GPT.

### A10 table contract

For Ukrainian `ПІДСУМОК ЗА ТВЕРДЖЕННЯМИ`, the staged Builder package requires exactly:

```text
| Твердження | Потрібно | Отримано незалежних | Виняток |
| --- | ---: | ---: | --- |
```

Every material claim follows as one four-cell row. Header labels must not be merged/concatenated. The values must remain consistent with the visible claim blocks and traceable evidence origins.

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
- request: `Перевірити факти/твердження у прикріпленому відео.`;
- canonical CriticProfile gate reached;
- owner selected `1`;
- AssemblyAI detected Russian with language confidence `0.9984`;
- source duration `70.668 s`;
- STT accounting `71 s`;
- two durable transcript segments;
- retrieval/provider credits reported `0`;
- seven material claims evaluated;
- unsupported numeric timing claim preserved as `0/1 - SHORTFALL`;
- reliability `88/100`;
- final status `COMPLETED_WITH_LIMITATIONS`;
- no KRCM Job ID, OpenAI file ID, signed URL or provider credential exposed.

Canonical records:
- `49_A9_10_ATTACHMENT_TRANSPORT_RUNTIME_ACCEPTANCE.md`;
- `50_A9_10_PRIVATE_GPT_LOCAL_ATTACHMENT_E2E_ACCEPTANCE.md`.

## Credit and replay invariants

- local attachment retrieval credits are `0`; AssemblyAI STT is accounted separately by processed seconds/quota;
- Telegram public retrieval credits are `0` and has no paid fallback;
- Facebook active retrieval remains free Cobalt-only;
- Supadata native hard cap remains 1 explicitly approved credit;
- Instagram AI fallback requires a separate quote and explicit consent;
- automatic managed AI fallback is prohibited;
- `credit_charge_uncertain=true` operations are never automatically retried;
- durable duplicate starts reuse existing jobs where defined.

## Current next boundary

Repository-level A10 package validation must be green, then:
1. apply `prompts/GPT_STORE_MEDIA_BETA_BUILDER_INSTRUCTIONS.md` version `0.9.1-beta-a10` to the actual private MEDIA BETA GPT;
2. keep the existing Action schema `0.6.0-a9.10`;
3. run a fresh final-report regression;
4. confirm that `ПІДСУМОК ЗА ТВЕРДЖЕННЯМИ` renders/copies as four distinct Markdown columns and keeps the same cross-check accounting;
5. only after that mark A10 runtime accepted and clean the runtime-pending markers.

External tester/public sharing, repository `main` merge and production VoiceBridge promotion remain paused until a separate explicit owner decision.
