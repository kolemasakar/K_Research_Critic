# A9 Zero-Client YouTube Ingestion Plan

Version: 1.0
Status: IN_PROGRESS
Started: 2026-08-20

## Product goal

The final private owner-only UX must be:

```text
YouTube URL in ChatGPT
 -> choose/check request type
 -> no separate video opening
 -> no Helper
 -> no manual Job ID handling
 -> transcript acquisition runs server-side
 -> Research/Critic workflow
 -> result in the same ChatGPT conversation
```

This must work equivalently from desktop and smartphone.

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

### B4. Server-side YouTube reachability is not yet live-accepted

The existing server-side code must be re-tested on the actual isolated Render runtime. Datacenter YouTube access is known to be unstable and may fail because of bot/IP enforcement even when yt-dlp and PO-token support are correctly configured.

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

Capture exact yt-dlp failure class if blocked: bot/login, PO token, 403, 429, format/JS, or other.

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

### A9.4 Unified ingestion router

Target behavior:

```text
start media job
 -> server captions attempt
      -> success: COMPLETED / youtube_captions / STT=0
      -> unavailable:
           server audio acquisition
            -> AssemblyAI EU
            -> COMPLETED
 -> if server YouTube acquisition is specifically blocked:
      return explicit SERVER_MEDIA_BLOCKED / CLIENT_ASSISTED_AVAILABLE
```

During development, Helper remains an emergency/dev fallback. It is not part of the final normal owner UX.

### A9.5 GPT Action integration

Expose zero-client operations to the private GPT and update Builder instructions so the normal flow is:

```text
URL + request type
 -> start server job
 -> bounded status checks
 -> retrieve all transcript pages
 -> continue workflow automatically
```

The GPT must not instruct the owner to open the YouTube video or use Helper unless the backend explicitly returns a temporary development fallback condition.

### A9.6 Owner-only final acceptance

Required final live test from the actual private GPT:

```text
YouTube URL
 -> select/request analysis type
 -> zero extra browser/media actions by owner
 -> transcript obtained
 -> requested analysis completed
```

For fact-check mode, the CriticProfile approval gate remains mandatory before independent research.

## Final acceptance state

Only after A9.1-A9.6 pass may the private product be called:

`OWNER_ONLY_ZERO_CLIENT_COMPLETE`

## Non-goals for A9

A9 does not require:
- public GPT sharing;
- external testers;
- GPT Store publication;
- merge to production `main`;
- a permanent free public STT architecture.

Those remain separate future gates.
