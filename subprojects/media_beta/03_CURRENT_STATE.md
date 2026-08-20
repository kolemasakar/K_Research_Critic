# MEDIA BETA Current State

Canonical implementation checkpoint for continuation without reconstruction.

Version: 4.0
Status: ACTIVE_CHECKPOINT
Checkpoint date: 2026-08-20

## Executive state

Current phase state:

`A4_COMPLETE / A5_COMPLETE / A6_COMPLETE / A7_EXTERNAL_ROLLOUT_PAUSED / A8_BROWSER_ASSISTED_OWNER_BASELINE_COMPLETE / A9_ZERO_CLIENT_MEDIA_ROUTER_PLANNED / A9_IMPLEMENTATION_NOT_STARTED`

Current product target:

`PRIVATE OWNER-ONLY ZERO-CLIENT MEDIA ANALYSIS`

The owner paused GPT public/link sharing investigation and external Tester 1/2/3 rollout. The current focus is the private product only.

A8 browser-assisted operation is accepted as a working baseline. It is not the final target because Helper 0.2.2 still requires a separate browser/media action.

Canonical A8 acceptance:
`subprojects/media_beta/23_A8_OWNER_ONLY_BROWSER_ASSISTED_ACCEPTANCE.md`

Canonical A9 plan:
`subprojects/media_beta/24_A9_ZERO_CLIENT_INGESTION_PLAN.md`

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

Status: PLANNED / IMPLEMENTATION_NOT_STARTED.

Final desired UX:

```text
media input in ChatGPT
 -> no separate media opening
 -> no Helper
 -> no manual Job ID handling
 -> server/backend acquires or receives media
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

### A9 architecture audit

Status: COMPLETE.

Existing VoiceBridge code already contains a legacy server-side path:
- endpoint family `/api/v1/media/transcriptions`;
- job prefix `KRCB_`;
- yt-dlp metadata/media acquisition;
- server-side captions attempt;
- audio fallback;
- ffmpeg normalization;
- AssemblyAI Universal-2;
- paginated transcript readback.

Known blockers before final zero-client acceptance:
- legacy server-side AssemblyAI endpoint is not yet aligned with the accepted configurable EU endpoint;
- KRCB job/quota state is in-memory and must converge on durable persistence;
- current GPT Action exposes the accepted client-assisted KRCC path, not the zero-client path;
- each public-platform adapter needs its own positive live acceptance and auth/private negative case.

### A9 server-side YouTube reachability probe

Status: PARTIAL_PASS / REACHABILITY_CONFIRMED.

Probe job:
`KRCB_252bb38a-aba7-4e2e-8148-b31d55974161`

The isolated Render service reached the YouTube extractor and returned:
`This live stream recording is not available.`

The result was wrapped as `MEDIA_FETCH_FAILED`, but importantly there was no bot/login, HTTP 403, HTTP 429, or PO-token failure. STT charge remained zero.

This is evidence of extractor/source reachability only. It does not yet accept prerecorded metadata, server-side captions, server-side Audio fallback, durability, or GPT zero-client integration.

## CI state

Latest checked KRC documentation/contract commit before this checkpoint:
`0e283509aafd52de06a7f23a398ad8758a75d875`

GitHub Actions `Tests #503`: SUCCESS.

Checkpoint-document commits created after that success must still be allowed to run and must not be described as green until checked.

## Deferred / paused items

- GPT public/link sharing and appeal;
- external Tester 1/2/3 rollout;
- Free-plan compatibility;
- public Store promotion;
- production merge;
- sustainable public-free Phase B/C work.

## Exact next project boundary

Do not continue A9 implementation automatically at chat recovery.

The next chat should first recover this checkpoint and verify repository/CI state. Implementation begins only after an explicit owner command to continue A9.
