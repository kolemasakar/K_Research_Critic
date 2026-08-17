# MEDIA BETA Architecture
Архітектура ізольованого медіарежиму та межі відповідальності між K-Research & Critic, VoiceBridge і STT-провайдером.

Version: 1.0
Status: APPROVED_BASELINE
Updated: 2026-08-17

## 1. Architecture goals

- preserve the existing K-Research & Critic text workflow;
- isolate beta failures from published production services;
- minimize exhaustible free-tier resource use;
- keep transcript acquisition separate from claim verification;
- avoid user API keys;
- support Ukrainian, Russian, and English source media;
- keep the design replaceable so AssemblyAI can later be removed from the public free path.

## 2. Closed beta topology

```text
Tester
  |
  | YouTube URL + tester access code
  v
K-Research & Critic - MEDIA BETA
  |
  | GPT Action bearer authentication
  v
Dedicated VoiceBridge MEDIA BETA service
  |
  +--> access-code allowlist
  +--> URL validation / YouTube metadata
  +--> duration guard <= 60 min
  |
  +--> subtitle-first path
  |      |
  |      +--> usable captions found
  |             -> timestamped transcript
  |
  +--> STT fallback path
         |
         +--> daily budget reservation
         +--> concurrency guard = 1
         +--> download source audio
         +--> convert to mono 16 kHz ~32 kbps
         +--> AssemblyAI Universal-2
         +--> timestamped transcript
         +--> provider delete request

Transcript
  -> material claim inventory
  -> CriticProfile gate
  -> independent web research after approval
  -> Critic review
  -> final report and review protocol
```

## 3. Trust and evidence boundaries

### Transcript boundary

The transcript is source content, not independent corroboration.

The system may use the transcript before CriticProfile approval only to:

- determine subject/domain/risk;
- identify material claims;
- preserve timestamps;
- flag transcription uncertainty;
- propose the CriticProfile.

It must not perform independent truth verification before approval.

### Access-code boundary

Tester codes are beta admission credentials only. They are not provider API keys.

Rules:

- codes are configured server-side;
- codes are sent only when starting a beta media job;
- codes are not included in job state;
- codes are never returned in reports;
- codes are never checkpointed;
- codes must not be committed to GitHub.

### Provider-secret boundary

The following remain server-side secrets:

- `KRC_MEDIA_ACTION_TOKEN`;
- `KRC_MEDIA_BETA_CODES`;
- `ASSEMBLYAI_API_KEY`.

They must not appear in GPT instructions, checkpoints, repository files, transcripts, or user-visible reports.

## 4. Resource protection

Closed beta controls:

- intended testers: 4;
- max video duration: 3600 seconds;
- max active jobs: 1;
- global AssemblyAI fallback budget: 7200 seconds per UTC day;
- captions consume zero STT budget;
- duplicate normalized URL/language requests may reuse an existing non-failed job;
- transcript/job state expires from memory after TTL;
- temporary media files are deleted after processing.

Current daily STT budget state is process-memory based. A service restart can reset the budget counter. This is acceptable for closed beta but is not sufficient for a public multi-instance deployment.

## 5. Production isolation

The beta must use a dedicated Render service.

Production:

`voicebridge-cloud-us.onrender.com`

Beta target:

`voicebridge-krc-media-beta-kolemasakar.onrender.com`

Do not point the beta GPT Action at the production VoiceBridge endpoint.

Do not replace the published K-Research & Critic GPT with the beta package.

## 6. Repository boundaries

### K-Research & Critic

Feature branch: `agent/video-url-research`

Responsibilities:

- workflow rules;
- claim-verification semantics;
- CriticProfile gate;
- beta GPT package;
- OpenAPI Action contract;
- checkpoint safety;
- privacy documentation;
- Store/package validation.

### VoiceBridge

Feature branch: `agent/krc-media-transcript`

Responsibilities:

- media fetch;
- subtitle-first ingestion;
- audio fallback preparation;
- STT provider integration;
- beta quota controls;
- temporary data lifecycle;
- beta backend API;
- Render deployment definition.

## 7. Failure behavior

The media path must fail closed when:

- tester code is invalid;
- URL is unsupported;
- video exceeds duration limit;
- concurrency is exhausted;
- daily STT budget is exhausted and no usable captions exist;
- media retrieval fails;
- provider transcription fails;
- transcript cannot be acquired reliably.

A media failure must not degrade ordinary text research.

## 8. Future replaceability

The transcript acquisition interface must remain provider-neutral enough to allow this later routing:

```text
YouTube captions
  -> Cloudflare Workers AI Whisper
  -> local Whisper / faster-whisper fallback
```

K-Research & Critic should consume the same normalized timestamped transcript contract regardless of transcript provider.