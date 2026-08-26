# MEDIA BETA Current State

Canonical implementation checkpoint for continuation without reconstruction.

Version: 5.9
Status: ACTIVE_CHECKPOINT
Checkpoint date: 2026-08-26

## Executive state

Current phase state:

`A4_COMPLETE / A5_COMPLETE / A6_COMPLETE / A7_EXTERNAL_ROLLOUT_PAUSED / A8_BROWSER_ASSISTED_OWNER_BASELINE_COMPLETE / A9_1_COMPLETE / A9_2_DIRECT_YOUTUBE_BLOCKED / A9_2R_MANAGED_NATIVE_COMPLETE / A9_3_DURABLE_MANAGED_COMPLETE / A9_5_PRIVATE_GPT_ZERO_CLIENT_E2E_COMPLETE / A9_8_OWNER_ZERO_CLIENT_COMPLETE / A9_6_INSTAGRAM_MANAGED_COMPLETE / A9_6_FACEBOOK_SUPADATA_NOT_ACCEPTED / A9_7_FACEBOOK_COBALT_LIVE_ACCEPTED / A9_7_I_PRIVATE_GPT_E2E_ACCEPTED / A9_9_TELEGRAM_BACKEND_LIVE_ACCEPTED / A9_9_PRIVATE_GPT_E2E_ACCEPTED`

Accepted owner-only public zero-client adapters:
- prerecorded YouTube;
- Instagram Reel;
- Facebook Video/Reel through free Cobalt retrieval -> AssemblyAI -> durable KRCM;
- supported public Telegram video posts through public Telegram web/embed retrieval -> trusted Telegram CDN -> AssemblyAI -> durable KRCM.

Not accepted:
- historical Facebook Supadata route;
- ScrapeCreators paid Facebook fallback (reserve-only, unconfigured, inactive);
- private/authenticated Telegram retrieval;
- any paid Telegram fallback;
- local audio/video attachment transport and ingestion.

Repository `main`, external tester rollout, public sharing and production VoiceBridge remain outside the current merge gate.

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
- production VoiceBridge not targeted by A9.9 acceptance.

## Accepted Research/Critic workflow

Two-stage CriticProfile gate is runtime accepted:
- profile created before independent research;
- first gate offers direct run / review-edit / cancel;
- explicit `1` approves before research;
- displayed profile edits remain review-required until re-approved.

Claim-level cross-check enforcement is runtime accepted:
- floors `LOW>=0`, `MEDIUM>=1`, `HIGH>=2`, `CRITICAL>=3`;
- each material factual claim maintains `required / achieved_independent / exception`;
- independence is based on underlying evidence, not URL count;
- real shortfalls remain visible and qualified;
- Critic audits material claims before PASS.

Evidence-origin traceability is runtime accepted in Core and MEDIA BETA:
- each counted origin is visibly attributable to its claim;
- achieved count cannot exceed visible independent origins;
- derivative reporting is not double-counted.

## Report-language invariant

Default report language is Ukrainian unless explicitly changed by the user.

The selected report language controls user-visible workflow text, prompts, CriticProfile presentation, section/table labels, verdict labels, final report, claim verification and review protocol. Canonical/internal keys remain internal unless explicitly requested.

## Runtime markers

`CRITICPROFILE_TWO_STAGE_GATE_RUNTIME = ACCEPTED`

`CLAIM_LEVEL_CROSS_CHECK_RUNTIME = ACCEPTED`

`CORE_TRACEABILITY_HARDENING_RUNTIME = ACCEPTED`

`CORE_REPORT_LABEL_LOCALIZATION_RUNTIME = ACCEPTED`

`MEDIA_BETA_TRACEABILITY_HARDENING_RUNTIME = ACCEPTED`

`MEDIA_BETA_REPORT_LABEL_LOCALIZATION_RUNTIME = ACCEPTED`

`builder_policy_fix_runtime_applied = true`

`a9_7_i_private_gpt_e2e_complete = true`

`managed_telegram_backend_live_accepted = true`

`managed_telegram_builder_runtime_applied = true`

`managed_telegram_private_gpt_e2e_complete = true`

`a9_9_telegram_private_gpt_e2e_complete = true`

`gpt_builder_private_update_required = false`

`rollout_state = A9_9_TELEGRAM_PRIVATE_GPT_E2E_ACCEPTED`

## Accepted owner media UX

```text
supported public media URL in ChatGPT
 -> no Helper / beta code / manual Job ID / platform login
 -> route by platform
 -> transcript acquisition
 -> CriticProfile gate only after transcript availability
 -> explicit owner approval
 -> Research -> Critic
 -> localized final report in same conversation
```

Platform routes:

```text
YouTube/Instagram
 -> managed native first where applicable
 -> billable operations require explicit consent

Facebook
 -> startManagedFacebookFallback
 -> Cobalt success -> AssemblyAI -> durable KRCM
 -> Cobalt failure -> media unavailable -> STOP
 -> no active paid Facebook offer/preflight/continuation

Telegram
 -> startManagedTelegramPublicTranscription
 -> Telegram public web/embed retrieval
 -> trusted Telegram CDN
 -> AssemblyAI -> durable KRCM
 -> retrieval credits 0
 -> unavailable/no-speech -> STOP
 -> no login/cookies/session/bot token
 -> no paid fallback
```

## Credit and replay invariants

- Supadata native hard cap remains 1 approved credit;
- Instagram AI fallback requires a separate quote and explicit consent;
- automatic AI fallback prohibited;
- Facebook active retrieval remains free Cobalt-only;
- Telegram public retrieval credits are 0;
- Telegram has no paid fallback;
- `credit_charge_uncertain=true` operations are never automatically retried or replayed;
- durable duplicate starts reuse existing terminal/completed jobs where defined.

## Accepted A9 milestones

### A9.2R - managed native YouTube

PASS. Zero-client managed native route accepted with explicit credit boundary and durable transcript jobs.

### A9.3 - durable managed jobs

PASS. Postgres durable jobs, restart-safe readback, duplicate reuse and uncertain-charge no-replay accepted.

### A9.5 / A9.8 - private GPT integration and owner YouTube E2E

PASS. Private GPT Action auth and owner admission accepted without user-facing beta code.

### A9.6 - Instagram

PASS for isolated owner beta. Native-first route accepted with separately authorized AI fallback only when native transcript is unavailable.

### A9.6 - Facebook Supadata route

HISTORICAL / NOT_ACCEPTED. Must not be replayed automatically.

### A9.7 - Facebook Cobalt free path

LIVE ACCEPTED. Canonical positive path:

`Facebook Reel -> Cobalt -> AssemblyAI -> durable KRCM`

Positive backend evidence recorded 0 retrieval credits, 23 STT seconds and durable reread.

### A9.7-I - Facebook failure policy

PRIVATE GPT E2E ACCEPTED.

Active behavior:

`Cobalt failure -> FACEBOOK_RETRIEVAL_UNAVAILABLE -> terminal FAILED -> STOP`

No paid Facebook fallback offer belongs to active MEDIA BETA. ScrapeCreators remains reserve-only compatibility code.

Canonical records:
- `43_A9_7_I_FACEBOOK_POLICY_FIX_BACKEND_HARDENING.md`;
- `44_A9_7_I_PRIVATE_GPT_FACEBOOK_POLICY_E2E_ACCEPTANCE.md`.

### A9.9 - Telegram public video

BACKEND LIVE + PRIVATE GPT E2E ACCEPTED.

Architecture audit:
- dedicated free `TelegramPublicWebRetriever` boundary;
- public `t.me/<channel>/<post_id>` only;
- no Telegram account/session/cookies/bot token;
- public web/embed retrieval only;
- trusted Telegram CDN media only;
- no arbitrary message-link fetch;
- AssemblyAI EU STT;
- durable KRCM output;
- no paid fallback.

Canonical positive target:

`https://t.me/techcrimes/12107`

Isolated backend live acceptance:
- workflow run `32969713110` SUCCESS;
- `retrieval_provider=telegram_public_web`;
- `provider=assemblyai`;
- `provider_mode=telegram_public_retrieval_stt`;
- retrieval credits `0`;
- total credits `0`;
- STT seconds `53`;
- segment count `1`;
- transcript characters `769`;
- provider data deleted;
- durable status/segments readback PASS;
- duplicate reuse PASS;
- invalid/private input rejection PASS.

Actual private-GPT NEW-chat positive acceptance:
- target `techcrimes/12107` reached CriticProfile after Telegram intake/transcription;
- owner selected `1` to approve direct analysis;
- Research/Critic completed;
- final report was Ukrainian;
- report stated AssemblyAI, English language confidence `0.9927`, one segment, 53 s STT, average recognition confidence ~0.975, credits `0`;
- localized verdicts and claim-level cross-check accounting were visible;
- unresolved physical-fit claims remained `0/2 - SHORTFALL`;
- no KRCM Job ID, backend secret or provider credential was exposed;
- final status was `ЗАВЕРШЕНО З ОБМЕЖЕННЯМИ`.

Companion negative/no-speech target:

`https://t.me/techcrimes/12101`

Private GPT stopped safely after determining no recognizable speech; reported 0 credits and 0 STT seconds, with no paid/auth bypass.

Non-blocking presentation observation:
- copied Markdown of the claim-summary table showed a malformed header row;
- data rows and required/achieved/exception values remained understandable;
- does not block A9.9 transport/transcript/workflow acceptance.

Canonical records:
- `45_A9_9_TELEGRAM_PUBLIC_ADAPTER_AUDIT.md`;
- `46_A9_9_PRIVATE_GPT_TELEGRAM_E2E_ACCEPTANCE.md`.

## Action schema boundary

Current private MEDIA BETA Action schema:

`0.5.0-a9.9`

It includes:
- `startManagedTelegramPublicTranscription` -> `POST /api/v1/media/managed/telegram`;
- existing YouTube/Instagram managed operations;
- Facebook Cobalt operation;
- historical paid Facebook operation definitions retained only as compatibility surface.

Active Builder instructions forbid offering/calling historical paid Facebook continuation after Cobalt failure.

## Private GPT state

The A9.9 Builder instructions and Action schema are applied in the actual private `K-Research & Critic - MEDIA BETA` GPT.

Current authoritative markers:
- `builder_package_ready = true`;
- `builder_runtime_applied = true`;
- `managed_telegram_action_schema_ready = true`;
- `managed_telegram_builder_runtime_applied = true`;
- `managed_telegram_private_gpt_e2e_complete = true`;
- `a9_9_telegram_private_gpt_e2e_complete = true`;
- `rollout_state = A9_9_TELEGRAM_PRIVATE_GPT_E2E_ACCEPTED`.

## Next task

A9.9 Telegram is closed.

Remaining not-accepted ingress target:
- local audio/video attachment transport and ingestion.

Next engineering boundary:
1. determine whether the current Custom GPT/Action environment can transport a user attachment to the isolated backend without a separate Helper/client;
2. define the smallest privacy-safe transport contract;
3. only then implement subtitle/audio extraction and AssemblyAI fallback;
4. keep public/production promotion paused.
