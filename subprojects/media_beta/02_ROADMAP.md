# MEDIA BETA Roadmap

Roadmap for the private MEDIA BETA and later optional rollout/sustainable media work.

Version: 3.4
Status: ACTIVE
Updated: 2026-08-26

## Phase A - Private MEDIA BETA

### A1-A8 foundation

Status: COMPLETE for accepted owner baseline and private-beta infrastructure.

Delivered isolated MEDIA BETA GPT/Action/backend boundaries, resource protection, dedicated Render beta service, transcript validation, Builder integration, CriticProfile approval flow, owner E2E and preserved A8 browser-assisted fallback evidence. External tester rollout remains paused by owner decision.

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

Accepted owner ingress covers four public platform adapters plus one local audio/video attachment.

#### A9.2R Managed native YouTube

Status: COMPLETE / OWNER E2E ACCEPTED

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

## Phase B - A10 Stabilization / release-boundary review

Status: IN_PROGRESS / PACKAGE READY / PRIVATE GPT RUNTIME PENDING

Canonical record:
`51_A10_STABILIZATION_AND_RELEASE_BOUNDARY.md`.

### A10.1 Claim-summary Markdown hardening

Status: PACKAGE READY / RUNTIME PENDING

Observed owner-runtime defect:

```text
ТвердженняПотрібноОтримано незалежнихВиняток
```

could appear as a collapsed copied Markdown table header although data rows remained readable.

Builder package `0.9.1-beta-a10` now requires exact header rows:

```text
| Твердження | Потрібно | Отримано незалежних | Виняток |
| --- | ---: | ---: | --- |
```

and explicitly forbids merged/concatenated header labels.

Exit gate: actual private GPT Builder update plus a fresh final report showing four distinct Markdown columns with unchanged `required / achieved_independent / exception` semantics.

### A10.2 Canonical managed-instruction alignment

Status: COMPLETE IN PACKAGE

`GPT_STORE_MEDIA_MANAGED_BETA_INSTRUCTIONS.md` is aligned with accepted YouTube, Instagram, Facebook Cobalt, Telegram public and local-attachment ingress. This removes stale A9.7-I-only canonical framing without changing active backend behavior.

### A10.3 Action/backend stability boundary

Status: NO CHANGE REQUIRED

Action schema remains `0.6.0-a9.10`. No VoiceBridge code/deployment change is required for the A10 table-formatting regression gate.

### A10.4 Release boundary

Status: PAUSED / REQUIRES SEPARATE OWNER DECISION

A10 does not authorize:
- merge to KRC `main`;
- production VoiceBridge deployment;
- external tester onboarding;
- public sharing/store publication.

## Phase C - Public/external release

Status: PAUSED / FUTURE

Requires a new explicit owner decision plus sharing/publication resolution, privacy re-validation, sustainable resource architecture, production smoke tests and explicit promotion approval.

## Current transition marker

`A4_COMPLETE / A5_COMPLETE / A6_COMPLETE / A7_EXTERNAL_ROLLOUT_PAUSED / A8_BASELINE_ACCEPTED / A9_OWNER_ZERO_CLIENT_MEDIA_INPUT_ACCEPTED / YOUTUBE_ACCEPTED / INSTAGRAM_ACCEPTED / FACEBOOK_COBALT_ACCEPTED / FACEBOOK_FAILURE_POLICY_E2E_ACCEPTED / TELEGRAM_ACCEPTED / LOCAL_ATTACHMENT_PRIVATE_GPT_E2E_ACCEPTED / A10_CLAIM_TABLE_HARDENING_PACKAGE_READY_RUNTIME_PENDING`

## Roadmap rule

COMPLETE means implementation plus acceptance evidence exists. PACKAGE READY does not mean runtime accepted. PAUSED/DEFERRED/PLANNED items must not be represented as validated or released.
