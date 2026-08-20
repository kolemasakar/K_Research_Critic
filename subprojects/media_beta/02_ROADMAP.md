# MEDIA BETA Roadmap

Roadmap for the private MEDIA BETA and later optional public/sustainable media work.

Version: 3.0
Status: ACTIVE
Updated: 2026-08-20

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
- AssemblyAI fallback budget 7200 sec per UTC day;
- captions path STT charge 0;
- helper audio upload guard 32 MiB;
- mono 16 kHz speech normalization at about 32 kbps;
- provider delete request on normal AssemblyAI completion;
- access-code guard;
- durable Postgres job state and STT quota ledger for the accepted KRCC path;
- negative-path guards for invalid code, wrong source, duration, concurrency, and quota exhaustion.

### A3. Dedicated Render beta deployment

Status: COMPLETE

Dedicated service:
- `voicebridge-krc-media-beta-kolemasakar`;
- ID `srv-da1kic5bedkc73d6fk60`;
- isolated from production VoiceBridge.

### A4. Live transcript validation

Status: COMPLETE

Accepted browser-assisted intake:
- captions-first UK/RU/EN/AUTO cases;
- captions STT charge 0;
- AssemblyAI Universal-2 Audio fallback;
- AssemblyAI EU endpoint acceptance;
- exact duration/quota accounting;
- provider cleanup on normal completion;
- status/segment readback;
- durable restart/resume and quota-ledger restoration;
- forced active-audio process loss -> retry-safe deterministic failure;
- no duplicate STT charge after process replacement;
- U+FFFD anomaly dispositioned as non-reproducible/non-blocking.

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
- three GPT-facing operations manually tested;
- transcript pagination confirmed;
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

Canonical acceptance:
`23_A8_OWNER_ONLY_BROWSER_ASSISTED_ACCEPTANCE.md`.

A8 proves the current product works end-to-end, but Helper is not part of the final desired normal UX.

### A9. Zero-client MediaSourceRouter

Status: PLANNED / IMPLEMENTATION_NOT_STARTED

Canonical plan:
`24_A9_ZERO_CLIENT_INGESTION_PLAN.md`.

Final target:

```text
media input in ChatGPT
 -> MediaSourceRouter
 -> zero-client transcript acquisition
 -> requested analysis workflow
 -> result in the same conversation
```

Approved ingress directions:
- public media URL adapters;
- `local_upload` for local video/audio.

Initial public URL adapters:
1. YouTube public videos;
2. Instagram public Reels/posts containing video;
3. Facebook public Video/Reels;
4. Telegram public posts containing video.

Access boundary:
- public sources only;
- no user logins, passwords, cookies, authenticated browser sessions, account tokens, or imported session state;
- auth/private content returns `UNSUPPORTED_PRIVATE_OR_AUTH_REQUIRED`.

Approved local-upload direction:
- local video/audio attachment;
- inspect embedded subtitles/text first where available;
- otherwise extract/normalize audio and use the accepted EU STT path;
- temporary source media deleted after processing;
- attachment-to-Action/backend transport still requires technical feasibility validation.

#### A9.0 Architecture audit

Status: COMPLETE

VoiceBridge already contains a legacy server-side `KRCB_` path using yt-dlp, captions-first logic, audio fallback, ffmpeg, and paginated transcript readback.

Known blockers before final zero-client acceptance:
- server-side legacy AssemblyAI path must use the accepted configurable EU endpoint;
- `KRCB_` job/quota state is in-memory and must converge on durable persistence;
- current GPT Action exposes the client-assisted KRCC path;
- each public platform adapter requires its own live positive and auth/private negative acceptance.

#### A9.2a Server-side YouTube reachability probe

Status: PARTIAL_PASS / REACHABILITY_CONFIRMED

Probe job:
`KRCB_252bb38a-aba7-4e2e-8148-b31d55974161`

The isolated Render service reached the YouTube extractor and returned a source-specific yt-dlp error:
`This live stream recording is not available.`

No bot/login, HTTP 403, HTTP 429, or PO-token failure was returned. STT charge remained zero.

This confirms server-side YouTube extractor reachability for that probe, but does not yet accept prerecorded metadata, captions-first extraction, audio fallback, durability, or GPT integration.

## Phase B - Sustainable Free Media

Status: DEFERRED

Potential future work:
- caption-path hardening;
- Cloudflare Whisper proof of concept;
- provider-neutral transcript router;
- owner-controlled local media processing where practical;
- remove permanent dependence on exhaustible paid STT credits from any future public free path.

## Phase C - Public media release

Status: PAUSED / FUTURE

Would require a new explicit owner decision plus sharing/publication resolution, sustainable resource architecture, privacy re-validation, runtime-plan compatibility, stable public privacy-policy delivery, production smoke tests, and explicit promotion approval.

## Current transition marker

`A4_COMPLETE / A5_COMPLETE / A6_COMPLETE / A7_EXTERNAL_ROLLOUT_PAUSED / A8_BROWSER_ASSISTED_OWNER_BASELINE_COMPLETE / A9_ZERO_CLIENT_MEDIA_ROUTER_PLANNED / A9_IMPLEMENTATION_NOT_STARTED`

## Roadmap rule

A roadmap item marked COMPLETE means implementation/acceptance evidence exists. READY/IN_PROGRESS/PAUSED/BLOCKED/PLANNED must never be described as already validated.
