# A9 Zero-Client Public Media URL Ingestion Plan

Version: 1.1
Status: IN_PROGRESS
Started: 2026-08-20
Updated: 2026-08-20

## Product goal

The final private owner-only UX must be:

```text
Public media URL in ChatGPT
 -> choose/check request type
 -> no separate media opening
 -> no Helper
 -> no manual Job ID handling
 -> transcript acquisition runs server-side
 -> Research/Critic workflow
 -> result in the same ChatGPT conversation
```

This must work equivalently from desktop and smartphone.

YouTube is the first implementation adapter, not the final product boundary.

## Public-only access boundary

APPROVED owner decision, 2026-08-20:

- support only publicly accessible media URLs/posts/channels;
- do not use user logins, passwords, cookies, browser sessions, account tokens, or imported authenticated sessions;
- do not attempt to bypass private, friends-only, group-only, age/account-gated, or otherwise authenticated content;
- if media requires authentication, return an explicit unsupported/auth-required result rather than requesting credentials;
- private-platform support is out of scope unless a future explicit owner decision changes this boundary.

Target error semantic:

`UNSUPPORTED_PRIVATE_OR_AUTH_REQUIRED`

## Initial platform adapters

Planned first group:
- YouTube public videos;
- Instagram public Reels/posts containing video;
- Facebook public Video/Reels;
- Telegram public posts containing video.

Later adapters may include other public media URLs supported reliably by the ingestion layer, for example TikTok, X/Twitter, Vimeo, or other sites.

Support is defined per public URL/content type, not as blanket support for an entire platform.

## Target architecture

```text
Public media URL
 -> MediaSourceRouter
      -> detect platform/content type
      -> platform adapter
      -> captions/transcript when reliable
      -> otherwise public audio/media acquisition
 -> normalized MediaAsset
 -> Transcript Router
 -> requested analysis workflow
```

Normalized internal media contract should converge on:
- platform;
- source_url;
- title;
- author/channel where available;
- duration;
- transcript_source;
- detected_language;
- timestamped segments.

Research/Critic should consume the normalized transcript/evidence contract and should not need platform-specific logic.

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

A9 requires a GPT-facing server-side start/status/segments contract that does not require Helper during the normal path.

### B4. Server-side public-source reachability is not yet live-accepted

The existing server-side YouTube code must be re-tested on the actual isolated Render runtime. Datacenter source access may fail because of bot/IP enforcement even when extraction tooling is correctly configured.

Each additional platform adapter must receive its own public-source reachability and negative-auth-path acceptance before being marked supported.

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
2. captions-first on a known captioned video;
3. only after EU routing is confirmed, audio fallback on a captions-unavailable case.

Capture exact extraction failure class if blocked: bot/login, token, 403, 429, format/JS, or other.

### A9.3 Durable zero-client job state

Preferred approach: reuse/adapt the existing Postgres media-client persistence layer instead of introducing a second persistence model.

Required durable fields include:
- created/updated timestamps;
- normalized source URL;
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

### A9.4 Unified public-media ingestion router

Target behavior:

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

During development, Helper remains an emergency/dev fallback for the already accepted YouTube browser-assisted baseline. It is not part of the final normal owner UX.

### A9.5 GPT Action integration

Expose zero-client operations to the private GPT and update Builder instructions so the normal flow is:

```text
public URL + request type
 -> start server job
 -> bounded status checks
 -> retrieve all transcript pages
 -> continue workflow automatically
```

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

### A9.7 Owner-only final acceptance

Required final live test from the actual private GPT:

```text
public media URL
 -> select/request analysis type
 -> zero extra browser/media actions by owner
 -> transcript obtained
 -> requested analysis completed
```

For fact-check mode, the CriticProfile approval gate remains mandatory before independent research.

YouTube zero-client acceptance may precede acceptance of additional platform adapters; platform support must be reported explicitly rather than implied globally.

## Final acceptance state

Only after the core zero-client router and first accepted platform adapter pass may the private product be called:

`OWNER_ONLY_ZERO_CLIENT_COMPLETE`

Additional platform adapters receive separate support/acceptance markers.

## Non-goals for A9

A9 does not require:
- private or login-required media;
- user cookies or authenticated platform sessions;
- public GPT sharing;
- external testers;
- GPT Store publication;
- merge to production `main`;
- a permanent free public STT architecture.

Those remain separate future gates.
