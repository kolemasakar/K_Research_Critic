# MEDIA BETA Current State

Canonical implementation checkpoint for continuation without reconstruction.

Version: 4.2
Status: ACTIVE_CHECKPOINT
Checkpoint date: 2026-08-21

## Executive state

Current phase state:

`A4_COMPLETE / A5_COMPLETE / A6_COMPLETE / A7_EXTERNAL_ROLLOUT_PAUSED / A8_BROWSER_ASSISTED_OWNER_BASELINE_COMPLETE / A9_IMPLEMENTATION_ACTIVE / A9_1_COMPLETE / A9_2_DIRECT_YOUTUBE_BLOCKED / A9_2R_MANAGED_NATIVE_COMPLETE / A9_3_DURABLE_MANAGED_COMPLETE / A9_5_GPT_ACTION_NEXT`

Current product target:

`PRIVATE OWNER-ONLY ZERO-CLIENT MEDIA ANALYSIS`

The owner paused GPT public/link sharing investigation and external Tester 1/2/3 rollout. The current focus is the private product only.

A8 browser-assisted operation remains an accepted fallback baseline. It is not the final target because Helper 0.2.2 still requires a separate browser/media action.

Canonical A8 acceptance:
`subprojects/media_beta/23_A8_OWNER_ONLY_BROWSER_ASSISTED_ACCEPTANCE.md`

Canonical A9 plan:
`subprojects/media_beta/24_A9_ZERO_CLIENT_INGESTION_PLAN.md`

Canonical managed-provider acceptance:
`subprojects/media_beta/26_A9_MANAGED_PROVIDER_ACCEPTANCE.md`

Canonical A9.3 durability acceptance:
`subprojects/media_beta/27_A9_DURABLE_MANAGED_ACCEPTANCE.md`

## Accepted browser-assisted baseline

```text
public YouTube URL
 -> private MEDIA BETA GPT
 -> durable KRCC job
 -> Helper 0.2.2
 -> captions first
      -> COMPLETED / youtube_captions / STT=0
 -> if captions unavailable/unusable
      -> Audio fallback
      -> AssemblyAI EU Universal-2
 -> GPT retrieves complete transcript
 -> material claim inventory
 -> DRAFT CriticProfile
 -> explicit owner APPROVE/EDIT/REJECT
 -> independent Research
 -> Critic/revision
 -> localized final report
```

Accepted report contract includes:
- Ukrainian response by default unless the user explicitly requests another response language;
- transcript/source language must not switch report language;
- localized report headings;
- localized verdict labels;
- exactly one canonical verdict per material claim.

Transcript text is evidence of what the media says, not independent evidence that a factual claim is true.

## Repositories and production boundary

KRC:
- repo `kolemasakar/K_Research_Critic`;
- branch `agent/video-url-research`;
- draft PR #8;
- public GPT and `main` unchanged.

VoiceBridge:
- repo `kolemasakar/VoiceBridge`;
- branch `agent/krc-media-transcript`;
- draft PR #28;
- production service and `main` unchanged.

Do not merge PR #8 or PR #28 without a new explicit owner decision.

## Dedicated beta runtime

Service:
`voicebridge-krc-media-beta-kolemasakar`

Service ID:
`srv-da1kic5bedkc73d6fk60`

Endpoint:
`https://voicebridge-krc-media-beta-kolemasakar.onrender.com`

Accepted browser-assisted controls:
- max duration 3600 sec;
- concurrency 1;
- AssemblyAI fallback budget 7200 sec per UTC day;
- durable Postgres KRCC job state;
- durable STT quota ledger;
- restart-resilient waiting/completed jobs;
- active-audio hard process loss returns retry-safe terminal failure;
- AssemblyAI fallback routed through `https://api.eu.assemblyai.com`.

Managed-provider runtime addition:
- `SUPADATA_API_KEY` is configured only for the isolated MEDIA BETA runtime;
- Supadata starts in `native` mode;
- automatic managed AI fallback is disabled;
- managed transcript operations require explicit credit consent;
- `KRCM_` job and segment state is durable in Postgres;
- managed duplicate starts reuse durable state across runtime restart;
- A9.3 live acceptance consumed exactly one approved native credit and left the provider balance at 98.

## A4-A6

Status: PASS / COMPLETE.

A4 transcript intake, durability, quota, fallback and guard evidence is preserved in records `10_...` through `17_...`.

A5 separate GPT Builder beta is accepted.

A6 owner/operator Research/Critic end-to-end acceptance is complete.

Historical credential attribution correction remains documented in `21_CREDENTIAL_ATTRIBUTION_CORRECTION.md`.

## A7 - External tester rollout

Status: PAUSED_BY_OWNER.

GPT sharing/publication investigation, appeal work, and Tester 1/2/3 onboarding are intentionally paused. Existing EU Audio privacy/fallback acceptance remains valid.

## A8 - Owner-only browser-assisted baseline

Status: PASS / COMPLETE_BASELINE.

The actual private GPT, not only Builder Preview, completed a full owner-operated flow using the owner-designated beta credential.

Accepted:
- private GPT access mode `Only me`;
- owner credential accepted;
- KRCC job creation;
- Helper 0.2.2 captions-first completion;
- complete transcript retrieval;
- CriticProfile approval gate;
- independent Research only after approval;
- Critic/revision;
- final report;
- Ukrainian default-language regression fixed;
- localized verdict and heading regressions fixed;
- Builder instructions compacted below the Builder character limit;
- KRC CI green after these instruction/document updates.

Canonical record:
`23_A8_OWNER_ONLY_BROWSER_ASSISTED_ACCEPTANCE.md`.

## A9 - Zero-client MediaSourceRouter

Status: IMPLEMENTATION_ACTIVE.

Final desired UX:

```text
media input in ChatGPT
 -> no separate media opening
 -> no Helper
 -> no manual Job ID handling
 -> backend acquires/receives transcript source
 -> credit preflight when a managed provider may spend credits
 -> explicit user consent
 -> transcript
 -> requested analysis
 -> result in the same conversation
```

### Approved ingress modes

Public URL router:
- YouTube public videos;
- Instagram public Reels/posts containing video;
- Facebook public Video/Reels;
- Telegram public posts containing video;
- later public platforms only after separate compatibility validation.

Public-only boundary:
- no user logins;
- no passwords;
- no cookies;
- no authenticated browser sessions;
- no account tokens or imported authenticated state;
- auth/private sources return `UNSUPPORTED_PRIVATE_OR_AUTH_REQUIRED`.

Local upload:
- local video/audio is an approved future ingress mode `local_upload`;
- inspect embedded subtitles/text first when available;
- otherwise extract/normalize audio and use the accepted EU STT path;
- original source media should be temporary and deleted after processing;
- ChatGPT attachment-to-Action/backend transport still requires technical feasibility validation.

### A9.1 - Server-side STT privacy parity

Status: PASS / COMPLETE.

The VoiceBridge server-side AssemblyAI path now uses the configurable endpoint contract:

`KRC_MEDIA_ASSEMBLYAI_BASE_URL`

The isolated beta runtime remains configured for the accepted EU endpoint:

`https://api.eu.assemblyai.com`

### A9.2 - Direct Render-to-YouTube prerecorded probe

Status: BLOCKED.

A normal prerecorded public YouTube source was tested from the isolated Render runtime.

Result:

`Sign in to confirm you're not a bot`

The failure occurred before metadata/captions and before STT. Charge remained zero.

This supersedes the earlier partial reachability probe as the decision-relevant result for normal prerecorded YouTube ingestion from Render datacenter IPs.

Disposition:

`DIRECT_RENDER_YOUTUBE = BLOCKED_BY_DATACENTER_ANTIBOT`

The project will not continue blind yt-dlp player-client permutations as the primary A9 strategy.

### A9.2R - Managed provider native path

Status: PASS / COMPLETE_FOR_NATIVE_OWNER_BETA.

Primary provider:

`Supadata`

Initial mode:

`native`

Backend contract:

```text
POST /api/v1/media/managed/preflight
POST /api/v1/media/managed/transcriptions
GET  /api/v1/media/managed/transcriptions/{job_id}
GET  /api/v1/media/managed/transcriptions/{job_id}/segments
```

Credit consent invariant:
- preflight must show available credits;
- preflight must show estimated operation cost;
- preflight must show estimated balance after;
- no billable transcript request starts before explicit owner approval;
- native Supadata request hard cap is `credit_consent.max_credits=1`;
- native failure must stop at `AWAITING_AI_CONSENT`;
- managed AI fallback requires a separate future preflight and separate explicit consent.

Live acceptance source:

`https://www.youtube.com/watch?v=IzYyKRx7Qwg`

Initial managed-provider acceptance:

```text
job_id: KRCM_705fe6a2-5ff4-47de-b6e5-b6c9bf90caa4
status: COMPLETED
detected_language: ru
segment_count: 277
credits_charged: 1
balance_before: 100
balance_after: 99
ai_fallback_authorized: false
```

Timestamped segment validation passed.

Canonical record:
`26_A9_MANAGED_PROVIDER_ACCEPTANCE.md`.

### A9.3 - Durable managed jobs and credit-safe idempotency

Status: PASS / COMPLETE.

Accepted isolated live code:

`7736f2e7acc5abbb3415e3753d0ca022c1b8d7b2`

Final live acceptance:

```text
job_id: KRCM_6f359971-b061-4db8-b4a2-9f6422f351b6
status: COMPLETED
detected_language: ru
segment_count: 277
credits_charged: 1
provider_balance_before: 99
provider_balance_after: 98
```

Acceptance proved:
- durable `KRCM_` job read before restart;
- durable timestamped segments before restart;
- isolated runtime restart with an intentionally invalid provider key;
- same job and segments readable after restart;
- duplicate start succeeded by reusing the same durable completed job while the provider key was invalid;
- therefore the duplicate path did not require a second valid provider call;
- valid provider key was restored;
- final provider balance changed by exactly one approved credit.

The reservation parser was hardened to select the actual seven-field PostgreSQL returned row rather than assuming the final `psql` stdout line is data. Regression coverage was added before live acceptance.

Canonical record:
`27_A9_DURABLE_MANAGED_ACCEPTANCE.md`.

## Remaining A9 blockers

Before final owner-only zero-client acceptance:
- the private GPT Action must be switched from Helper/KRCC UX to managed preflight/consent/transcript UX;
- the GPT must hide internal Job ID mechanics from the user;
- full private-GPT end-to-end analysis must pass with only the media URL and chat choices;
- each additional public-platform adapter needs its own positive public case and auth/private negative case;
- local upload transport remains unvalidated.

The managed YouTube backend path is now durable and credit-safe enough for private GPT integration.

## Next task

`A9.5 - Private GPT Action zero-client integration.`

Normal target flow:

```text
public YouTube URL
 -> private GPT
 -> analysis-mode choice
 -> managed credit preflight
 -> explicit approval when one credit may be spent
 -> managed start/status/segments handled internally
 -> no Helper
 -> no manual Job ID
 -> requested Research/Critic workflow
 -> result in the same ChatGPT conversation
```
