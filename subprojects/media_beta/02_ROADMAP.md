# MEDIA BETA Roadmap

Roadmap for the private MEDIA BETA and later optional rollout/sustainable media work.

Version: 3.3
Status: ACTIVE
Updated: 2026-08-26

## Phase A - Private MEDIA BETA

### A1. Architecture and isolation

Status: COMPLETE

Delivered separate MEDIA BETA GPT identity, Action contract, VoiceBridge feature branch/runtime path and dedicated Render beta service. Production VoiceBridge and published K-Research & Critic remain unchanged.

### A2. Resource protection

Status: COMPLETE_IN_CODE_AND_PRIMARY_LIVE_GUARDS

Accepted controls include duration/size limits, concurrency/quota accounting, provider cleanup, durable managed jobs, invalid-input guards and uncertain-charge no-replay behavior.

### A3. Dedicated Render beta deployment

Status: COMPLETE

Dedicated service: `voicebridge-krc-media-beta-kolemasakar`.

### A4. Live transcript validation

Status: COMPLETE

Browser-assisted baseline and server-side transcript/STT paths were validated with quota, cleanup, status/segment readback and failure protections.

### A5. Separate GPT Builder beta

Status: COMPLETE

Accepted separate private GPT, Builder instructions, Action auth/schema, isolated beta server, privacy policy, CriticProfile gate, Ukrainian default/report localization and exactly one verdict per material claim.

### A6. Owner/operator end-to-end acceptance

Status: COMPLETE

Owner completed full transcript -> CriticProfile -> Research/Critic workflows.

### A7. Controlled external tester rollout

Status: PAUSED_BY_OWNER

External tester onboarding, sharing/publication and production promotion remain paused and require a separate owner decision.

### A8. Owner-only browser-assisted baseline

Status: COMPLETE / BASELINE ACCEPTED

Preserved as fallback evidence only. Helper is not part of normal zero-client UX.

### A9. Zero-client MediaSourceRouter

Status: COMPLETE / OWNER TARGET INGRESS ACCEPTED

Canonical target:

```text
media input in ChatGPT
 -> MediaSourceRouter / managed Action
 -> zero-client transcript acquisition
 -> CriticProfile gate
 -> Research/Critic
 -> localized result in same conversation
```

Accepted owner ingress now covers four public platform adapters plus local audio/video attachments.

#### A9.1 Server-side STT EU alignment

Status: COMPLETE

#### A9.2R Managed native YouTube

Status: COMPLETE / OWNER E2E ACCEPTED

Zero-client YouTube managed route, explicit native credit boundary and durable KRCM jobs accepted.

#### A9.3 Durable managed jobs

Status: COMPLETE

Postgres persistence, restart-safe readback, duplicate reuse and uncertain-charge no-replay accepted.

#### A9.5 Private GPT managed Action integration

Status: COMPLETE

Action auth, Builder integration and server-side owner admission accepted without a user-facing beta code.

#### A9.6 Instagram Reel

Status: COMPLETE / OWNER BETA ACCEPTED

Native-first route accepted with separately authorized AI fallback only when required.

#### A9.6 Facebook Supadata route

Status: HISTORICAL / NOT_ACCEPTED

Historical only; must not be replayed automatically.

#### A9.7 Facebook Cobalt free path

Status: COMPLETE / LIVE_ACCEPTED

`Facebook public Video/Reel -> Cobalt -> AssemblyAI -> durable KRCM`

#### A9.7-I Facebook failure-policy hardening

Status: COMPLETE / PRIVATE_GPT E2E ACCEPTED

Active policy:

`Cobalt failure -> media retrieval unavailable -> STOP`

Paid Facebook continuation is not part of active MEDIA BETA. ScrapeCreators remains reserve-only and unconfigured.

#### A9.8 Owner zero-client acceptance

Status: COMPLETE

Owner zero-client behavior is accepted for YouTube, Instagram, Facebook, Telegram and local attachment ingress.

#### A9.9 Telegram public video adapter

Status: COMPLETE / BACKEND LIVE + PRIVATE GPT E2E ACCEPTED

Accepted route:

```text
public t.me post
 -> Telegram public web/embed
 -> trusted Telegram CDN
 -> AssemblyAI EU
 -> durable KRCM
 -> CriticProfile
 -> Research/Critic
```

Canonical positive target: `https://t.me/techcrimes/12107`.

Accepted facts include zero retrieval credits, 53 STT seconds, durable reread/duplicate reuse, no Telegram auth state and no paid fallback.

Canonical records:
- `45_A9_9_TELEGRAM_PUBLIC_ADAPTER_AUDIT.md`;
- `46_A9_9_PRIVATE_GPT_TELEGRAM_E2E_ACCEPTANCE.md`.

#### A9.10 Local audio/video attachment

Status: COMPLETE / TRANSPORT + BACKEND + PRIVATE GPT E2E ACCEPTED

Accepted route:

```text
one current-conversation local audio/video attachment
 -> openaiFileIdRefs
 -> trusted *.oaiusercontent.com temporary delivery
 -> bounded VoiceBridge ingestion
 -> ffmpeg/audio normalization as needed
 -> AssemblyAI
 -> durable KRCM segments
 -> CriticProfile gate
 -> explicit owner approval
 -> Research/Critic
 -> localized final report
```

Accepted security/resource boundary:
- exactly one attachment;
- no Helper/client extension;
- no user beta code;
- retrieval provider `openai_attachment`;
- retrieval credits `0`;
- maximum attachment size `32 MiB`;
- signed URL/file identifiers are not exposed;
- provider credentials remain server-side.

Runtime acceptance evidence from the real owner private GPT:
- actual MP4 approximately 5 MB;
- media duration `70.668 s`;
- AssemblyAI accounting `71 s`;
- two durable transcript segments;
- detected Russian language confidence `0.9984`;
- retrieval/provider credits reported `0`;
- canonical CriticProfile gate reached before research;
- owner selected `1`;
- Research/Critic completed in Ukrainian;
- seven material claims checked;
- real `0/1 - SHORTFALL` preserved for the unsupported numeric timing claim;
- reliability `88/100`;
- final status `COMPLETED_WITH_LIMITATIONS`.

Canonical records:
- `47_A9_10_LOCAL_UPLOAD_TRANSPORT_AUDIT.md`;
- `49_A9_10_ATTACHMENT_TRANSPORT_RUNTIME_ACCEPTANCE.md`;
- `50_A9_10_PRIVATE_GPT_LOCAL_ATTACHMENT_E2E_ACCEPTANCE.md`.

Non-blocking backlog:
- copied Markdown claim-summary table can render a malformed header row even though rows/counts remain readable; treat as UX formatting hardening, not an A9.10 reopening condition.

## Phase B - Stabilization / sustainable media

Status: NEXT / DEFERRED UNTIL OWNER PRIORITIZATION

Potential work:
- harden claim-summary table rendering without changing accepted semantics;
- reduce exhaustible-provider dependence where practical;
- provider-neutral transcript routing;
- additional operational cleanup/observability;
- decide whether old compatibility surfaces should be retired in a later controlled change.

## Phase C - Public/external release

Status: PAUSED / FUTURE

Requires a new explicit owner decision plus sharing/publication resolution, privacy re-validation, sustainable resource architecture, production smoke tests and explicit promotion approval.

## Current transition marker

`A4_COMPLETE / A5_COMPLETE / A6_COMPLETE / A7_EXTERNAL_ROLLOUT_PAUSED / A8_BASELINE_ACCEPTED / A9_OWNER_ZERO_CLIENT_MEDIA_INPUT_ACCEPTED / YOUTUBE_ACCEPTED / INSTAGRAM_ACCEPTED / FACEBOOK_COBALT_ACCEPTED / FACEBOOK_FAILURE_POLICY_E2E_ACCEPTED / TELEGRAM_ACCEPTED / LOCAL_ATTACHMENT_PRIVATE_GPT_E2E_ACCEPTED`

## Roadmap rule

COMPLETE means implementation plus acceptance evidence exists. PAUSED/DEFERRED/PLANNED items must not be represented as already validated.
