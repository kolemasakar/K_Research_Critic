# MEDIA BETA Current State

Canonical implementation checkpoint for continuation without reconstruction.

Version: 6.0
Status: ACTIVE_CHECKPOINT
Checkpoint date: 2026-08-26

## Executive state

Current phase state:

`A4_COMPLETE / A5_COMPLETE / A6_COMPLETE / A7_EXTERNAL_ROLLOUT_PAUSED / A8_BROWSER_ASSISTED_OWNER_BASELINE_COMPLETE / A9_OWNER_ZERO_CLIENT_MEDIA_INPUT_ACCEPTED / YOUTUBE_ACCEPTED / INSTAGRAM_ACCEPTED / FACEBOOK_COBALT_ACCEPTED / FACEBOOK_FAILURE_POLICY_E2E_ACCEPTED / TELEGRAM_ACCEPTED / LOCAL_ATTACHMENT_PRIVATE_GPT_E2E_ACCEPTED`

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

## Runtime markers

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

`builder_runtime_applied = true`

`gpt_builder_private_update_required = false`

`rollout_state = A9_10_ATTACHMENT_PRIVATE_GPT_E2E_ACCEPTED`

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

### Transport

PASS.

Actual private GPT runtime injected a usable `openaiFileIdRefs` object. The sanitized probe observed the current OpenAI CDN family, and the hardened backend accepted HTTPS `*.oaiusercontent.com` while retaining anti-lookalike, redirect, port, credential and bounded-read protections.

Real probe result:
- `transport_available=true`;
- file class video;
- MIME `video/mp4` consistent;
- 65,536 probe bytes;
- HTTP Range supported;
- retrieval credits `0`;
- STT seconds `0`.

Canonical record: `49_A9_10_ATTACHMENT_TRANSPORT_RUNTIME_ACCEPTANCE.md`.

### Full ingestion/backend

PASS.

Action operation:

`POST /api/v1/media/managed/attachment`

`operationId: startManagedAttachmentTranscription`

Boundary:
- exactly one current-conversation audio/video attachment;
- maximum bytes `33554432` (32 MiB);
- trusted OpenAI attachment delivery only;
- duration constrained by MEDIA BETA maximum;
- temporary media cleanup;
- AssemblyAI STT;
- durable KRCM transcript/segments;
- duplicate/replay protections preserved;
- file ID, signed URL and provider secrets not exposed.

### Actual private GPT E2E

PASS / ACCEPTED.

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

Canonical record: `50_A9_10_PRIVATE_GPT_LOCAL_ATTACHMENT_E2E_ACCEPTANCE.md`.

Non-blocking presentation backlog:
- copied Markdown of `ПІДСУМОК ЗА ТВЕРДЖЕННЯМИ` may collapse the header cells into the first column;
- data rows/counts remain readable and internally consistent;
- this does not invalidate A9.10 transport, transcription or workflow acceptance.

## Action / Builder state

Current private MEDIA BETA Action schema:

`0.6.0-a9.10`

Current Builder instructions:

`0.9-beta-a9.10`

Actual private GPT has both applied.

Key attachment operations:
- `startManagedAttachmentTranscription` -> `POST /api/v1/media/managed/attachment`;
- `probeManagedAttachmentTransport` -> `POST /api/v1/media/managed/attachment-probe`.

Current authoritative markers:
- `builder_package_ready = true`;
- `builder_runtime_applied = true`;
- `managed_attachment_action_schema_ready = true`;
- `managed_attachment_builder_runtime_applied = true`;
- `managed_attachment_ingestion_live_accepted = true`;
- `managed_attachment_private_gpt_e2e_complete = true`;
- `gpt_builder_private_update_required = false`;
- `rollout_state = A9_10_ATTACHMENT_PRIVATE_GPT_E2E_ACCEPTED`.

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

A9 owner zero-client ingress target is functionally complete/accepted.

Next work is stabilization and release-boundary review, not another required ingress adapter:
1. preserve accepted routes and security invariants;
2. optionally harden the non-blocking copied-table header defect;
3. clean temporary acceptance automation after CI evidence is preserved;
4. keep external tester/public sharing, repository `main` merge and production VoiceBridge promotion paused until a separate explicit owner decision.
