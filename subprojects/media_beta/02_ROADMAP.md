# MEDIA BETA Roadmap

Roadmap for the private MEDIA BETA and later optional public/sustainable media work.

Version: 3.1
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
- AssemblyAI fallback budget 7200 sec per UTC day for the accepted legacy path;
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

Canonical records: `10_...` through `17_...` plus `20_A7_EU_AUDIO_PRIVACY_GATE_ACCEPTANCE.md`.

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

Accepted private owner path:

```text
private GPT
 -> public YouTube URL
 -> owner-designated credential
 -> KRCC job
 -> Helper 0.2.2
 -> captions-first transcript
 -> DRAFT CriticProfile
 -> owner APPROVE
 -> Research/Critic
 -> localized final report
```

Canonical acceptance: `23_A8_OWNER_ONLY_BROWSER_ASSISTED_ACCEPTANCE.md`.

A8 remains fallback evidence only. Helper is not part of the normal zero-client UX.

### A9. Zero-client MediaSourceRouter

Status: IN_PROGRESS / THREE_PUBLIC_ADAPTERS_ACCEPTED

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
- auth/private content returns an unsupported/unavailable boundary rather than requesting credentials.

#### A9.0 Architecture audit

Status: COMPLETE

VoiceBridge legacy server-side media extraction was audited and used as input to the managed zero-client design.

#### A9.1 Server-side STT EU alignment

Status: COMPLETE

Managed server-side STT uses the accepted AssemblyAI EU boundary where applicable.

#### A9.2R Managed native YouTube

Status: COMPLETE / OWNER E2E ACCEPTED

Accepted:
- zero-client YouTube managed route;
- one-credit native Supadata preflight/consent boundary;
- durable KRCM transcript jobs;
- owner private-GPT E2E.

#### A9.3 Durable managed jobs

Status: COMPLETE

Accepted:
- Postgres durable managed jobs;
- restart-safe readback;
- duplicate-start reuse;
- uncertain-charge no-replay invariant.

#### A9.5 Private GPT managed Action integration

Status: COMPLETE

Accepted Action auth, Builder integration, managed operations, and owner admission without a user-facing beta code.

#### A9.6 Instagram Reel

Status: COMPLETE / OWNER BETA ACCEPTED

Accepted route:
- native managed attempt first;
- when native transcript is unavailable, separate AI preflight and NEW explicit consent;
- AI generation cap 40 credits;
- no automatic AI fallback.

#### A9.6 Facebook Supadata route

Status: HISTORICAL / NOT_ACCEPTED

The Supadata Facebook route remains historical and must not be replayed automatically.

#### A9.7 Facebook Cobalt free path

Status: LIVE_ACCEPTED

Accepted backend positive path:

`Facebook public Video/Reel -> Cobalt -> AssemblyAI -> durable KRCM`

Canonical positive-path record: `41_A9_7_FACEBOOK_COBALT_LIVE_ACCEPTANCE.md`.

#### A9.7-I Facebook failure-policy hardening

Status: COMPLETE / PRIVATE_GPT E2E ACCEPTED

Active policy:

`Cobalt failure -> media retrieval unavailable -> STOP`

Accepted boundaries:
- no automatic paid fallback;
- no paid Facebook offer after Cobalt failure;
- ScrapeCreators reserve-only and inactive;
- backend terminal failure enforcement;
- private Builder policy re-applied;
- fresh owner NEW-chat Facebook failure-path E2E accepted with reported credits `0`.

Canonical records:
- `43_A9_7_I_FACEBOOK_POLICY_FIX_BACKEND_HARDENING.md`;
- `44_A9_7_I_PRIVATE_GPT_FACEBOOK_POLICY_E2E_ACCEPTANCE.md`.

#### A9.8 Owner zero-client acceptance

Status: COMPLETE for accepted YouTube/Instagram/Facebook boundaries

The private GPT now has accepted owner zero-client behavior for the three currently live public platform adapters.

#### A9.9 Telegram public video adapter

Status: NOT_STARTED / NEXT_ENGINEERING_TASK

Required before implementation:
- audit current KRC and VoiceBridge support for Telegram public post URLs;
- define public-only URL patterns and private/auth-required rejection behavior;
- identify free/direct extraction options before any paid-provider path;
- preserve zero-client, no-cookie, no-session boundary;
- define transcript/STT and durable-job integration;
- add adapter-specific unit/regression tests;
- run isolated live positive and negative acceptance before marking complete.

#### A9.10 Local upload

Status: FEASIBILITY_PENDING / NOT_ACCEPTED

Target direction:
- local video/audio attachment;
- inspect embedded subtitles/text first where available;
- otherwise extract/normalize audio and use the accepted EU STT path;
- temporary source media deleted after processing;
- attachment-to-Action/backend transport still requires technical feasibility validation.

Local upload must not be represented as implemented until the ChatGPT-to-backend transport boundary is proven.

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

`A4_COMPLETE / A5_COMPLETE / A6_COMPLETE / A7_EXTERNAL_ROLLOUT_PAUSED / A8_BROWSER_ASSISTED_OWNER_BASELINE_COMPLETE / A9_IN_PROGRESS / YOUTUBE_ZERO_CLIENT_ACCEPTED / INSTAGRAM_ZERO_CLIENT_ACCEPTED / FACEBOOK_COBALT_ACCEPTED / FACEBOOK_FAILURE_POLICY_E2E_ACCEPTED / TELEGRAM_NOT_STARTED / LOCAL_UPLOAD_FEASIBILITY_PENDING`

## Roadmap rule

A roadmap item marked COMPLETE means implementation/acceptance evidence exists. READY/IN_PROGRESS/PAUSED/BLOCKED/PLANNED/NOT_STARTED must never be described as already validated.
