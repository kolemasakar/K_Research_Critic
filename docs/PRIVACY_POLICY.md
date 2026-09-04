# PRIVACY_POLICY

Політика конфіденційності для майбутньої публічної MEDIA-функції K-Research & Critic; до окремого R3 оновлення GPT ця редакція є підготовленим кандидатом і не активує публічний MEDIA-доступ.

Version: 2.1-candidate
Status: PUBLIC_MEDIA_CANDIDATE / NOT_YET_ACTIVATED / FREE_TIER_ONLY
Updated: 2026-09-04

## 1. Scope

This policy describes the external MEDIA Action planned for the existing public `K-Research & Critic` GPT.

The initial public MEDIA scope is limited to supported public video/media URLs from:

- YouTube;
- Telegram;
- Instagram;
- Facebook.

Private, login-gated, friends-only, cookie/session-dependent, or otherwise non-public platform content is not supported. Public local-file upload is not part of the initial public rollout unless separately reviewed and activated later.

The normal text-research Core remains separate from MEDIA. A MEDIA failure must not prevent the user from continuing to use Core K-Research & Critic functions.

## 2. Data Processed

Depending on the selected route, the MEDIA backend may process:

- the public source URL supplied by the user;
- temporary retrieved media bytes or normalized audio derived from the public media;
- transcript text and timestamped segments where available;
- source/detected language information;
- media duration and technical validation metadata;
- provider, retrieval mode, quota, rate-limit, and failure-state metadata;
- internal request/job identifiers needed for idempotency and diagnostics.

Unrelated ChatGPT conversation content must not be sent to the MEDIA backend.

The service is designed for anonymous/shared public GPT access and does not require a KRC user account.

## 3. Authentication and Credentials

The GPT Action authenticates to the backend with a server-to-server bearer credential configured by the GPT owner.

Public users are not asked to provide or reveal:

```text
Action bearer token
provider API keys
owner beta codes
platform usernames/passwords
cookies or session tokens
Telegram bot tokens
payment credentials
internal KRCM job identifiers
```

Reusable secrets must not be written to reports, checkpoints, public logs, or normal user-facing responses.

## 4. Platform Routing

### YouTube and Instagram

The public MEDIA candidate uses the project's self-hosted Cobalt retrieval service for supported public YouTube and Instagram video URLs. The backend requests an audio-oriented media representation and may then send the retrieved audio to the active free-only speech-to-text provider.

The initial Instagram public scope is limited to supported public single-video Reel/video-post forms. Multi-asset picker/carousel responses fail closed rather than selecting an item implicitly.

If Cobalt cannot retrieve the public media, processing stops as unavailable. There is no automatic Supadata fallback and no automatic paid retrieval fallback in the public free-only configuration.

### Facebook

The service uses the same self-hosted Cobalt retrieval path for supported public Facebook video/reel media. Retrieved audio may then be sent to the active free-only speech-to-text provider.

If Cobalt cannot retrieve the public media, processing stops as unavailable. ScrapeCreators and automatic paid Facebook retrieval are not permitted in the public free-only configuration.

### Telegram

The service uses the public Telegram web surface and only accepted trusted Telegram media delivery for supported public posts. Retrieved audio may then be sent to the active free-only speech-to-text provider.

The service does not require Telegram login credentials, cookies, sessions, or a bot token, and it does not use a paid Telegram retrieval fallback.

## 5. Speech-to-Text Providers

### AssemblyAI

AssemblyAI `universal-2` remains the currently accepted prerecorded KRC MEDIA STT provider while the project operates within its available Free-plan credit balance.

The public free-only policy does not authorize automatic paid AssemblyAI continuation. If the free allowance is exhausted or the provider becomes unavailable, MEDIA must stop or use a separately validated free Gemini route as described below.

Where implemented, the backend attempts provider-side transcript deletion after processing and records whether deletion was confirmed. Deletion must not be claimed when it cannot be confirmed.

### Google Gemini - post-AssemblyAI free-credit route

The project owner has selected Google Gemini as the intended free-only replacement after AssemblyAI Free credits are exhausted.

The current candidate contains a prerecorded Gemini transcription adapter, but normal KRC MEDIA traffic is not yet routed to Gemini. Gemini activation requires a separately validated release step.

If the Gemini Free route is activated, the MEDIA backend may send normalized public-media audio to the Google Gemini API for transcription. Google currently states that content submitted under the Gemini API Free Tier may be used to improve Google products. Because this is materially different from a paid data-use boundary, public Gemini activation must include a clear user-facing disclosure and explicit consent before the first Gemini Free processing request. If that consent is not obtained, the operation must fail closed.

No paid Gemini fallback is authorized by this policy.

## 6. Free-Tier-Only Resource Policy

The public MEDIA feature is designed to operate only within free provider/service allowances configured for this project.

Current safety rules include:

```text
self-hosted Cobalt retrieval for public YouTube/Instagram/Facebook
Cobalt retrieval credits charged by KRC: 0
AssemblyAI Free-plan use only
no automatic paid AssemblyAI continuation
no ScrapeCreators credential in public free-only mode
no automatic paid retrieval fallback
no automatic Supadata fallback from public Cobalt routes
Gemini Free route only after separate validation/activation
provider/resource exhaustion -> MEDIA unavailable / fail closed
```

`0 retrieval credits` describes the KRC provider-credit accounting for the self-hosted retrieval route; it does not mean that hosting, bandwidth, or other infrastructure has no resource cost.

Users are not charged by K-Research & Critic for MEDIA processing.

## 7. Project-Side Retention

The isolated durable MEDIA store preserves accepted job state and transcript segments only for the bounded operational window needed for continuation/idempotency.

The current implementation defaults managed job/transcript expiry to approximately one hour (`MEDIA_JOB_TTL_SECONDS=3600`). Expired managed-job rows are purged by the backend cleanup path. Daily STT quota-accounting rows older than two days are also removed by the current implementation.

These values are implementation defaults and may be reduced or otherwise changed only with corresponding documentation and privacy review before public activation.

The project does not intentionally retain raw downloaded source-media files after processing. Temporary local media artifacts are cleaned up by the accepted provider pipelines.

## 8. Provider-Side Data Handling

Third-party providers process only the data required for the selected MEDIA operation. Their own privacy, retention, regional-routing, and model-improvement rules also apply and may change independently of this project.

Before any public provider activation, the project must re-check the then-current provider terms. In particular:

- AssemblyAI provider-side deletion is attempted where supported and must be reported accurately;
- Google Gemini Free Tier data-use terms must be disclosed before the Gemini route is enabled for public users;
- Cobalt is operated by the project as the free retrieval component for supported public YouTube, Instagram, and Facebook media and is not a paid fallback service;
- Telegram retrieval uses only the supported public web/media route and does not require account/session credentials.

Historical/private compatibility code may contain provider adapters that are not part of the public route. Their presence in the repository does not by itself authorize public transmission to those providers.

## 9. Data Minimization and Security

Controls include:

- public-only remote source adapters;
- bounded media duration and request size;
- rate and concurrency limits;
- durable quota checks before provider work where determinable;
- HTTPS provider and retrieval endpoints;
- no platform-session import;
- no credential echoing;
- no automatic uncertain-charge retry that could create hidden paid usage;
- log redaction for credentials and private transport URLs;
- explicit fail-closed behavior when retrieval, provider, quota, or durable-state requirements cannot be satisfied.

Transcript text is evidence of what the media said, not independent proof that factual claims are true. K-Research & Critic may separately verify claims using independent sources.

## 10. Public GPT Action Requirement

OpenAI currently requires a valid Privacy Policy URL for a public GPT that uses Actions. This document is the repository-side candidate policy intended for that Action configuration.

Updating this file does not itself publish or activate the MEDIA Action. The existing public GPT must be updated separately through the ChatGPT Builder only after the R2 release gates pass.

## 11. Changes and Contact

This policy may be revised when providers, retention behavior, supported platforms, or the public release state changes. The current repository version and update date should be used when reviewing changes.

Project/privacy questions may be raised with the repository owner through `kolemasakar/K_Research_Critic`.
