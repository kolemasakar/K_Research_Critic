# PRIVACY_POLICY
Політика конфіденційності для майбутньої публічної MEDIA-функції K-Research & Critic; до окремого R3 оновлення GPT ця редакція є підготовленим кандидатом і не активує публічний MEDIA-доступ.

Version: 2.2-candidate
Status: PUBLIC_MEDIA_CANDIDATE / NOT_YET_ACTIVATED / FREE_TIER_ONLY
Updated: 2026-09-07

## 1. Scope

This policy describes the external MEDIA Action planned for the existing public `K-Research & Critic` GPT.

The initial public MEDIA scope is limited to supported public video/media URLs from:

- YouTube;
- Telegram;
- Instagram;
- Facebook.

Private, unlisted where a provider cannot lawfully/technically access them, login-gated, friends-only, cookie/session-dependent, or otherwise non-public platform content is not supported. Public local-file upload is not part of the initial public rollout unless separately reviewed and activated later.

The normal text-research Core remains separate from MEDIA. A MEDIA failure must not prevent the user from continuing to use Core K-Research & Critic functions.

## 2. Data Processed

Depending on the selected route, the MEDIA backend or selected provider may process:

- the public source URL supplied by the user;
- for YouTube, the public YouTube URL sent directly to Google Gemini after explicit consent;
- for Instagram, Facebook, or Telegram, temporary retrieved media bytes or normalized audio derived from public media where required by the route;
- transcript text and transcript segments where available;
- source/detected language information;
- media duration and technical validation metadata where available;
- provider, retrieval mode, quota, rate-limit, consent-state, and failure-state metadata;
- internal request/job identifiers needed for idempotency and diagnostics.

Unrelated ChatGPT conversation content must not be sent to the MEDIA backend or media providers.

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
YouTube login/session data
Telegram bot tokens
payment credentials
internal KRCM job identifiers
```

Reusable secrets must not be written to reports, checkpoints, public logs, or normal user-facing responses.

## 4. Platform Routing

### YouTube - Gemini Developer API Free Tier direct public URL

The public MEDIA candidate sends a supported public YouTube URL directly to Google Gemini for video understanding/transcript extraction. The YouTube public route does not use Cobalt, AssemblyAI, user cookies, YouTube login/session data, a paid proxy, Supadata, or a paid Gemini fallback.

Before any new YouTube URL/content is sent through the Gemini Developer API Free Tier, the user must receive a clear disclosure that content submitted through the Free Tier may be used by Google to improve Google products and must explicitly consent to that boundary. A preflight or durable-job lookup may occur before this consent, but it must not submit the YouTube media to Gemini.

If explicit consent is not obtained, the YouTube MEDIA operation stops without calling Gemini. If Gemini Free is unavailable, rejects the video, reaches its free quota, or otherwise fails, YouTube MEDIA fails closed. There is no automatic Cobalt, AssemblyAI, paid Gemini, login/cookie, paid proxy, or Supadata fallback.

### Instagram

The public MEDIA candidate uses the project's self-hosted Cobalt retrieval service for supported public Instagram Reel/video URLs. The backend requests an audio-oriented media representation and may then send the retrieved audio to AssemblyAI `universal-2` while the project's accepted free allowance remains available.

The initial Instagram public scope is limited to supported public single-video Reel/video-post forms. Multi-asset picker/carousel responses fail closed rather than selecting an item implicitly.

If Cobalt cannot retrieve the public media, processing stops as unavailable. There is no automatic Supadata fallback and no automatic paid retrieval fallback.

### Facebook

The service uses the self-hosted Cobalt retrieval path for supported public Facebook video/reel media. Retrieved audio may then be sent to AssemblyAI `universal-2` while the project's accepted free allowance remains available.

If Cobalt cannot retrieve the public media, processing stops as unavailable. ScrapeCreators and automatic paid Facebook retrieval are not permitted in the public free-only configuration.

### Telegram

The service uses the public Telegram web surface and only accepted trusted Telegram media delivery for supported public posts. Retrieved audio may then be sent to AssemblyAI `universal-2` while the project's accepted free allowance remains available.

The service does not require Telegram login credentials, cookies, sessions, or a bot token, and it does not use a paid Telegram retrieval fallback.

## 5. Processing Providers

### Google Gemini - YouTube direct Free Tier route

Google Gemini is the selected public YouTube provider for the candidate route because the previously tested self-hosted Cobalt path encountered YouTube datacenter anti-bot/login requirements.

The backend sends the supported public YouTube URL and a bounded instruction asking Gemini to extract spoken transcript content. It does not intentionally send unrelated ChatGPT conversation text.

Google states that content submitted through the Gemini Developer API Free Tier may be used to improve Google products. For that reason, this route requires a user-facing disclosure and explicit consent before each new provider submission for which consent has not already been validly established in the current flow. Consent is recorded only as bounded operation metadata; it is not a general waiver for unrelated data or providers.

No paid Gemini fallback is authorized. The project must not silently switch a failed Free Tier request to a paid Gemini path.

### AssemblyAI - Instagram/Facebook/Telegram prerecorded STT

AssemblyAI `universal-2` remains the accepted prerecorded STT provider for the non-YouTube public routes while the project operates within its available Free-plan credit balance.

The public free-only policy does not authorize automatic paid AssemblyAI continuation. If the free allowance is exhausted or AssemblyAI becomes unavailable, the affected MEDIA route must stop unless a separately reviewed and explicitly activated replacement is available.

Where implemented, the backend attempts provider-side transcript deletion after processing and records whether deletion was confirmed. Deletion must not be claimed when it cannot be confirmed.

Historical/private repository code may contain other Gemini prerecorded audio adapters. Their existence does not authorize an automatic public-provider switch.

## 6. Free-Tier-Only Resource Policy

The public MEDIA feature is designed to operate only within free provider/service allowances configured for this project.

Current candidate safety rules include:

```text
YouTube -> Gemini Developer API Free Tier direct public URL, explicit consent required
YouTube -> no Cobalt / AssemblyAI / cookies / login / paid proxy fallback
Instagram/Facebook -> self-hosted Cobalt retrieval -> AssemblyAI Free only
Telegram -> public Telegram web retrieval -> AssemblyAI Free only
Cobalt retrieval credits charged by KRC: 0
no automatic paid AssemblyAI continuation
no paid Gemini fallback
no ScrapeCreators credential in public free-only mode
no automatic paid retrieval fallback
no automatic Supadata fallback
provider/resource exhaustion -> MEDIA unavailable / fail closed
```

`0 retrieval credits` describes KRC provider-credit accounting for the self-hosted Cobalt and public-web retrieval routes; it does not mean that hosting, bandwidth, or other infrastructure has no resource cost.

Users are not charged by K-Research & Critic for MEDIA processing.

## 7. Project-Side Retention

The isolated durable MEDIA store preserves accepted job state and transcript segments only for the bounded operational window needed for continuation/idempotency.

The current implementation defaults managed job/transcript expiry to approximately one hour (`MEDIA_JOB_TTL_SECONDS=3600`). Expired managed-job rows are purged by the backend cleanup path. Daily STT quota-accounting rows older than two days are also removed by the current implementation for routes using that quota ledger.

These values are implementation defaults and may be reduced or otherwise changed only with corresponding documentation and privacy review before public activation.

The project does not intentionally retain raw downloaded source-media files after processing. The YouTube direct Gemini route does not require VoiceBridge to download the YouTube media first. Temporary local media artifacts used by non-YouTube retrieval/STT routes are cleaned up by the accepted provider pipelines.

## 8. Provider-Side Data Handling

Third-party providers process only the data required for the selected MEDIA operation. Their own privacy, retention, regional-routing, and model-improvement rules also apply and may change independently of this project.

Before any public provider activation, the project must re-check the then-current provider terms. In particular:

- Google Gemini Free Tier data-use terms must be disclosed before a new YouTube provider submission and explicit consent must be obtained;
- AssemblyAI provider-side deletion is attempted where supported and must be reported accurately;
- Cobalt is operated by the project as the free retrieval component for supported public Instagram and Facebook media and is not a paid fallback service;
- Telegram retrieval uses only the supported public web/media route and does not require account/session credentials.

Historical/private compatibility code may contain provider adapters that are not part of the public route. Their presence in the repository does not by itself authorize public transmission to those providers.

## 9. Data Minimization and Security

Controls include:

- public-only remote source adapters;
- explicit Gemini Free data-use consent before YouTube provider work;
- bounded request size and provider-route scope;
- rate and concurrency limits;
- durable idempotency to avoid duplicate provider work;
- HTTPS provider and retrieval endpoints;
- no platform-session import;
- no credential echoing;
- no automatic uncertain-result replay that could create duplicate provider work;
- no automatic paid fallback;
- log redaction for credentials and private transport URLs;
- explicit fail-closed behavior when retrieval, provider, quota, consent, or durable-state requirements cannot be satisfied.

Transcript text is evidence of what the media said, not independent proof that factual claims are true. K-Research & Critic may separately verify claims using independent sources after its research-control gate.

## 10. Public GPT Action Requirement

OpenAI requires a valid Privacy Policy URL for a public GPT that uses Actions. This document is the repository-side candidate policy intended for that Action configuration.

Updating this file does not itself publish or activate the MEDIA Action. The existing public GPT must be updated separately through the ChatGPT Builder only after the R2 release gates pass and the owner separately authorizes R3.

## 11. Changes and Contact

This policy may be revised when providers, retention behavior, supported platforms, or the public release state changes. The current repository version and update date should be used when reviewing changes.

Project/privacy questions may be raised with the repository owner through `kolemasakar/K_Research_Critic`.
