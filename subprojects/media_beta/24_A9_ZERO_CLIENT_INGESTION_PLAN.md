# A9 Zero-Client Public Media URL and Local Upload Ingestion Plan

Version: 1.2
Status: IN_PROGRESS
Started: 2026-08-20
Updated: 2026-08-20

## Product goal

The final private owner-only UX must support two source classes:

```text
A. Public media URL in ChatGPT
 -> choose/check request type
 -> no separate media opening
 -> no Helper
 -> no manual Job ID handling
 -> transcript acquisition runs server-side
 -> Research/Critic workflow
 -> result in the same ChatGPT conversation

B. Local video/audio attachment in ChatGPT
 -> choose/check request type
 -> upload from local storage/device
 -> media normalization/transcript acquisition
 -> Research/Critic workflow
 -> result in the same ChatGPT conversation
```

This must work equivalently from desktop and smartphone where the ChatGPT client supports the required attachment flow.

YouTube is the first public-URL implementation adapter, not the final product boundary. Local upload is a separate approved ingress adapter, not a workaround for private platform access.

## Public-only access boundary for URL sources

APPROVED owner decision, 2026-08-20:

- support only publicly accessible media URLs/posts/channels;
- do not use user logins, passwords, cookies, browser sessions, account tokens, or imported authenticated sessions;
- do not attempt to bypass private, friends-only, group-only, age/account-gated, or otherwise authenticated content;
- if media requires authentication, return an explicit unsupported/auth-required result rather than requesting credentials;
- private-platform support is out of scope unless a future explicit owner decision changes this boundary.

Target error semantic:

`UNSUPPORTED_PRIVATE_OR_AUTH_REQUIRED`

This public-only rule applies to platform URL adapters. It does not prohibit the owner from explicitly uploading a local video/audio file that is already present on the owner's device or local storage.

## Approved source adapters

### Public URL adapters

Planned first group:
- YouTube public videos;
- Instagram public Reels/posts containing video;
- Facebook public Video/Reels;
- Telegram public posts containing video.

Later adapters may include other public media URLs supported reliably by the ingestion layer, for example TikTok, X/Twitter, Vimeo, or other sites.

Support is defined per public URL/content type, not as blanket support for an entire platform.

### Local upload adapter

APPROVED owner decision, 2026-08-20.

Target source types:
- local video files;
- local audio files.

Initial processing target:

```text
local file
 -> validate type/size/duration
 -> inspect embedded subtitle/text tracks when available
 -> if usable transcript/subtitles exist: normalize without STT
 -> otherwise extract/normalize audio
 -> AssemblyAI EU fallback during current beta architecture
 -> normalized timestamped transcript
 -> requested analysis workflow
```

The local-upload path must not require platform login/cookies/session state.

Before implementation is marked supported, validate the actual Custom GPT/ChatGPT attachment-to-Action transport contract and practical file-size/type limits. Approval of the architecture does not imply that this transport has already been accepted live.

Original media files should be temporary processing artifacts, not durable project records. Durable state should retain only the job metadata/transcript segments required by the accepted media contract unless a later explicit decision changes the retention policy.

Visual-frame analysis of what is shown in a video is a possible later extension. The initial local-upload target is transcript/audio-content analysis; visual evidence extraction requires a separate acceptance scope.

## Target architecture

```text
Media input
 -> MediaSourceRouter
      -> Public URL
           -> detect platform/content type
           -> platform adapter
           -> captions/transcript when reliable
           -> otherwise public audio/media acquisition
      -> Local Upload
           -> validate media
           -> embedded subtitle/text extraction when usable
           -> otherwise audio extraction/normalization
 -> normalized MediaAsset
 -> Transcript Router
 -> requested analysis workflow
```

Normalized internal media contract should converge on:
- source_kind (`public_url` or `local_upload`);
- platform where applicable;
- source_url where applicable;
- original filename where applicable;
- title;
- author/channel where available;
- duration;
- transcript_source;
- detected_language;
- timestamped segments.

Research/Critic should consume the normalized transcript/evidence contract and should not need platform-specific or upload-specific logic.

## Required user-facing modes

At minimum:
- verify facts/claims;
- analyze argumentation;
- produce a concise summary;
- analyze a specific fragment.

## A9.0 Architecture audit

Status: COMPLETE

Existing VoiceBridge branch already contains a server-side media path:

- endpoint family: `/api/v1/media/transcriptions`;
- job prefix: `KRCB_`;
- server-side YouTube inspection through `yt-dlp`;
- server-side captions attempt through `youtube_captions.ts`;
- server-side audio download through `yt-dlp` when captions are unavailable;
- ffmpeg normalization;
- AssemblyAI Universal-2 fallback;
- status and paginated segment readback.

The VoiceBridge beta Docker runtime already includes:
- `yt-dlp[default]`;
- Node runtime support for YouTube extraction;
- `bgutil-ytdlp-pot-provider`;
- local bgutil provider process;
- `mweb` YouTube client selection in the server-side media path.

This is directionally aligned with the current yt-dlp PO-token guidance for YouTube extraction.

The same ffmpeg/ffprobe processing layer is directionally reusable for a future local-upload adapter, but the ChatGPT attachment transport and local-upload API contract are not yet implemented or live-accepted.

## Identified A9 blockers

### B1. Server-side AssemblyAI region mismatch

The accepted browser-assisted Audio fallback uses the configurable EU endpoint:

`https://api.eu.assemblyai.com`

The legacy server-side `MediaBetaTranscriptService` still hardcodes:

`https://api.assemblyai.com`

No live server-side audio fallback may be accepted until this is changed to the same configurable EU routing contract and covered by an automated test.

### B2. Server-side job durability

`KRCB_` jobs are currently held in process memory.

The accepted `KRCC_` browser-assisted path uses durable Postgres job state and a durable STT quota ledger.

Final zero-client acceptance requires durable job/status/segments and restart-safe quota behavior. An in-memory-only zero-client path is not sufficient for final acceptance.

### B3. GPT Action still exposes the client-assisted path

The current Builder Action exposes `/api/v1/media/client-transcriptions` and therefore normally returns `AWAITING_CLIENT`.

A9 requires a GPT-facing server-side start/status/segments contract that does not require Helper during the normal public-URL path.

The future local-upload path additionally requires a validated attachment/file transport contract between ChatGPT and the isolated backend.

### B4. Server-side public-source reachability is not yet fully live-accepted

A first isolated Render probe on 2026-08-20 confirmed that the server-side YouTube extractor can reach YouTube and receive a source-specific response without an anti-bot/403/429 failure. The tested unavailable live-stream recording returned `MEDIA_FETCH_FAILED` with the upstream message `This live stream recording is not available.`

This is evidence of basic server-side YouTube extractor reachability, not yet acceptance of normal prerecorded metadata/captions/audio ingestion.

Each additional platform adapter must receive its own public-source reachability and negative-auth-path acceptance before being marked supported.

### B5. Local-upload transport not yet validated

The source architecture is approved, but the actual ChatGPT/Custom GPT mechanism for passing a user-attached audio/video file to the Action/backend must be tested before implementation is selected.

Do not mark local upload supported solely because ffmpeg/STT processing is available server-side.

## Implementation sequence

### A9.1 Privacy parity before live fallback

- make server-side AssemblyAI base URL configurable;
- use `KRC_MEDIA_ASSEMBLYAI_BASE_URL` with the accepted EU value in the isolated beta runtime;
- add an automated endpoint-contract test analogous to the accepted client-ingest EU test;
- keep production VoiceBridge unchanged.

Acceptance: code + CI PASS before any server-side Audio fallback live test.

### A9.2 Safe server-side YouTube probe

Test the existing isolated server-side `KRCB_` path directly, outside GPT Builder first.

Probe order:
1. metadata/reachability;
2. captions-first on a known captioned prerecorded video;
3. only after EU routing is confirmed, audio fallback on a captions-unavailable case.

Capture exact extraction failure class if blocked: bot/login, token, 403, 429, format/JS, or other.

### A9.3 Durable zero-client job state

Preferred approach: reuse/adapt the existing Postgres media-client persistence layer instead of introducing a second persistence model.

Required durable fields include:
- created/updated timestamps;
- source kind;
- normalized source URL or upload identity;
- ownership/access-code digest where still used;
- status;
- transcript source;
- provider/model;
- provider cleanup result;
- STT charge;
- media metadata;
- segments;
- terminal error.

Process replacement must not silently lose a zero-client job or duplicate quota charge.

### A9.4 Unified media ingestion router

Target public-URL behavior:

```text
start media job
 -> detect public platform/content type
 -> platform adapter
 -> server captions/transcript attempt
      -> success: COMPLETED / captions-or-transcript / STT=0
      -> unavailable:
           server audio/media acquisition
            -> AssemblyAI EU
            -> COMPLETED
 -> if public acquisition is specifically blocked:
      return explicit SERVER_MEDIA_BLOCKED
 -> if authentication/private access is required:
      return UNSUPPORTED_PRIVATE_OR_AUTH_REQUIRED
```

Target local-upload behavior:

```text
start media job from attachment
 -> validate file
 -> embedded transcript/subtitle attempt
      -> success: COMPLETED / embedded_text / STT=0
      -> unavailable:
           extract/normalize audio
            -> AssemblyAI EU
            -> COMPLETED
```

During development, Helper remains an emergency/dev fallback for the already accepted YouTube browser-assisted baseline. It is not part of the final normal owner UX.

### A9.5 GPT Action integration

Expose zero-client operations to the private GPT and update Builder instructions so the normal public-URL flow is:

```text
public URL + request type
 -> start server job
 -> bounded status checks
 -> retrieve all transcript pages
 -> continue workflow automatically
```

For local upload, first validate the supported ChatGPT attachment transport, then expose a file-ingest operation that converges on the same normalized job/status/segments contract.

The GPT must not ask for platform credentials or instruct the owner to authenticate to a source. It must not instruct the owner to open media or use Helper in the final normal path.

### A9.6 Multi-platform adapter expansion

After the YouTube zero-client path is accepted, add adapters one at a time:
1. Instagram public video/Reels;
2. Facebook public Video/Reels;
3. Telegram public video posts;
4. other public platforms only after explicit compatibility validation.

Each adapter requires:
- supported URL-pattern contract;
- public-only positive live case;
- auth/private negative case returning the explicit unsupported/auth-required result;
- metadata/transcript normalization;
- resource/privacy regression checks.

### A9.7 Local media upload adapter

After the common durable ingestion contract is ready:
- validate ChatGPT attachment/file handoff to the Action/backend;
- define accepted audio/video formats and practical size/duration limits;
- validate ffprobe/ffmpeg normalization;
- prefer embedded subtitle/text tracks when usable;
- use the accepted AssemblyAI EU fallback only when STT is required;
- delete temporary original/normalized media after processing;
- verify durable transcript/job state without retaining the original media file;
- run owner smoke tests from desktop and smartphone where supported.

Local upload receives a separate acceptance marker and must not be described as supported before these checks pass.

### A9.8 Owner-only final acceptance

Required final live test from the actual private GPT for the first accepted source adapter:

```text
media source
 -> select/request analysis type
 -> zero extra browser/media actions by owner
 -> transcript obtained
 -> requested analysis completed
```

For fact-check mode, the CriticProfile approval gate remains mandatory before independent research.

YouTube zero-client acceptance may precede acceptance of additional public platform adapters and local upload; support must be reported explicitly rather than implied globally.

## Final acceptance state

Only after the core zero-client router and first accepted source adapter pass may the private product be called:

`OWNER_ONLY_ZERO_CLIENT_COMPLETE`

Additional public platform adapters and `local_upload` receive separate support/acceptance markers.

## Non-goals for A9

A9 does not require:
- private or login-required platform media;
- user cookies or authenticated platform sessions;
- visual-frame evidence analysis in the first local-upload implementation;
- public GPT sharing;
- external testers;
- GPT Store publication;
- merge to production `main`;
- a permanent free public STT architecture.

Those remain separate future gates.
