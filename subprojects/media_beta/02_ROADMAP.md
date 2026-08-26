# MEDIA BETA Roadmap

Roadmap for the private MEDIA BETA and later optional public/sustainable media work.

Version: 3.2
Status: ACTIVE
Updated: 2026-08-26

## Phase A - Private MEDIA BETA

### A1. Architecture and isolation

Status: COMPLETE

Delivered:
- separate MEDIA BETA GPT identity;
- separate GPT Action contract;
- separate VoiceBridge media backend path;
- dedicated Render beta target;
- production VoiceBridge unchanged;
- published K-Research & Critic unchanged.

### A2. Resource protection

Status: COMPLETE_IN_CODE_AND_PRIMARY_LIVE_GUARDS

Accepted controls include:
- max source/capture duration 60 min;
- concurrency 1;
- AssemblyAI fallback budget 7200 sec per UTC day for accepted legacy/managed STT paths;
- captions path STT charge 0;
- helper audio upload guard 32 MiB;
- mono 16 kHz speech normalization at about 32 kbps;
- provider delete request on normal AssemblyAI completion;
- durable managed job state;
- negative-path guards for invalid access, wrong source, duration, concurrency, quota exhaustion, and uncertain-charge replay.

### A3. Dedicated Render beta deployment

Status: COMPLETE

Dedicated service:
- `voicebridge-krc-media-beta-kolemasakar`;
- isolated from production VoiceBridge.

### A4. Live transcript validation

Status: COMPLETE

Accepted browser-assisted intake includes captions-first UK/RU/EN/AUTO cases, AssemblyAI EU audio fallback, duration/quota accounting, provider cleanup, status/segment readback, restart/resume, and retry-safe failure handling.

### A5. Separate GPT Builder beta

Status: COMPLETE

Accepted:
- separate `K-Research & Critic - MEDIA BETA` GPT;
- Builder-safe instructions below the 8000-character limit;
- web search enabled;
- API Key/Bearer Action auth;
- isolated beta Action server;
- privacy policy configured;
- CriticProfile approval gate enforced;
- Ukrainian default response language;
- localized report headings and verdict labels;
- exactly one verdict per material claim.

### A6. Owner/operator end-to-end acceptance

Status: COMPLETE

The owner completed the full Research/Critic flow after transcript intake and explicit CriticProfile approval.

### A7. Controlled external tester rollout

Status: PAUSED_BY_OWNER

Previously accepted readiness evidence remains valid, but external Tester 1/2/3 onboarding, GPT sharing/publication investigation, and appeal work are paused by owner decision.

### A8. Owner-only browser-assisted baseline

Status: COMPLETE / BASELINE ACCEPTED

Accepted private owner path remains fallback evidence only. Helper is not part of normal zero-client UX.

### A9. Zero-client MediaSourceRouter

Status: IN_PROGRESS / FOUR PUBLIC ADAPTERS ACCEPTED

Canonical plan: `24_A9_ZERO_CLIENT_INGESTION_PLAN.md`.

Target:

```text
media input in ChatGPT
 -> MediaSourceRouter
 -> zero-client transcript acquisition
 -> requested analysis workflow
 -> result in the same conversation
```

Access boundary:
- public sources only;
- no user logins, passwords, cookies, authenticated browser sessions, account tokens, or imported session state;
- auth/private content returns unsupported/unavailable rather than requesting credentials.

#### A9.0 Architecture audit

Status: COMPLETE

#### A9.1 Server-side STT EU alignment

Status: COMPLETE

#### A9.2R Managed native YouTube

Status: COMPLETE / OWNER E2E ACCEPTED

Accepted zero-client YouTube managed route, explicit native credit consent, durable KRCM transcript jobs and owner private-GPT E2E.

#### A9.3 Durable managed jobs

Status: COMPLETE

Accepted Postgres persistence, restart-safe readback, duplicate reuse and uncertain-charge no-replay invariant.

#### A9.5 Private GPT managed Action integration

Status: COMPLETE

Accepted Action auth, Builder integration, managed operations, and owner admission without a user-facing beta code.

#### A9.6 Instagram Reel

Status: COMPLETE / OWNER BETA ACCEPTED

Accepted native-first route with separately authorized AI fallback only when native transcript is unavailable.

#### A9.6 Facebook Supadata route

Status: HISTORICAL / NOT_ACCEPTED

The Supadata Facebook route remains historical and must not be replayed automatically.

#### A9.7 Facebook Cobalt free path

Status: LIVE_ACCEPTED

Accepted positive path:

`Facebook public Video/Reel -> Cobalt -> AssemblyAI -> durable KRCM`

#### A9.7-I Facebook failure-policy hardening

Status: COMPLETE / PRIVATE_GPT E2E ACCEPTED

Active policy:

`Cobalt failure -> media retrieval unavailable -> STOP`

No automatic or offered paid Facebook fallback belongs to active MEDIA BETA.

Canonical records:
- `43_A9_7_I_FACEBOOK_POLICY_FIX_BACKEND_HARDENING.md`;
- `44_A9_7_I_PRIVATE_GPT_FACEBOOK_POLICY_E2E_ACCEPTANCE.md`.

#### A9.8 Owner zero-client acceptance

Status: COMPLETE for accepted YouTube/Instagram/Facebook/Telegram public boundaries

The private GPT now has accepted owner zero-client behavior for four public platform adapters.

#### A9.9 Telegram public video adapter

Status: COMPLETE / BACKEND LIVE + PRIVATE GPT E2E ACCEPTED

Accepted route:

```text
public t.me post
 -> Telegram public web/embed retrieval
 -> trusted Telegram CDN media
 -> AssemblyAI EU
 -> durable KRCM transcript
 -> CriticProfile gate
 -> owner approval
 -> Research/Critic
 -> localized final report
```

Positive backend/private-GPT target:

`https://t.me/techcrimes/12107`

Accepted facts:
- `retrieval_provider=telegram_public_web`;
- retrieval credits `0`;
- STT provider AssemblyAI;
- `53` STT seconds;
- one durable segment;
- duplicate request reuse accepted;
- no Telegram login/cookies/session/bot token;
- no paid Telegram fallback;
- actual private GPT reached CriticProfile, accepted owner `1`, ran Research/Critic and produced the final Ukrainian fact-check.

Companion negative/no-speech target `https://t.me/techcrimes/12101` stopped safely with `0` credits.

Canonical records:
- `45_A9_9_TELEGRAM_PUBLIC_ADAPTER_AUDIT.md`;
- `46_A9_9_PRIVATE_GPT_TELEGRAM_E2E_ACCEPTANCE.md`.

#### A9.10 Local upload

Status: FEASIBILITY_PENDING / NOT_ACCEPTED / NEXT ENGINEERING BOUNDARY

Target direction:
- local video/audio attachment;
- inspect embedded subtitles/text first where available;
- otherwise extract/normalize audio and use the accepted EU STT path;
- temporary source media deleted after processing;
- attachment-to-Action/backend transport must be proven before implementation is represented as available.

## Phase B - Sustainable Free Media

Status: DEFERRED

Potential future work:
- caption-path hardening;
- provider-neutral transcript router;
- owner-controlled local media processing where practical;
- reduce dependence on exhaustible paid STT credits from any future public free path.

## Phase C - Public media release

Status: PAUSED / FUTURE

Would require a new explicit owner decision plus sharing/publication resolution, sustainable resource architecture, privacy re-validation, runtime-plan compatibility, stable public privacy-policy delivery, production smoke tests, and explicit promotion approval.

## Current transition marker

`A4_COMPLETE / A5_COMPLETE / A6_COMPLETE / A7_EXTERNAL_ROLLOUT_PAUSED / A8_BROWSER_ASSISTED_OWNER_BASELINE_COMPLETE / A9_IN_PROGRESS / YOUTUBE_ZERO_CLIENT_ACCEPTED / INSTAGRAM_ZERO_CLIENT_ACCEPTED / FACEBOOK_COBALT_ACCEPTED / FACEBOOK_FAILURE_POLICY_E2E_ACCEPTED / TELEGRAM_ZERO_CLIENT_ACCEPTED / LOCAL_UPLOAD_FEASIBILITY_PENDING`

## Roadmap rule

A roadmap item marked COMPLETE means implementation/acceptance evidence exists. READY/IN_PROGRESS/PAUSED/BLOCKED/PLANNED/NOT_STARTED must never be described as already validated.
