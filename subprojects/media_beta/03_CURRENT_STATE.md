# MEDIA BETA Current State
Канонічний знімок фактичного стану реалізації для відновлення роботи без припущень.

Version: 1.6
Status: ACTIVE_CHECKPOINT
Checkpoint date: 2026-08-17

## Executive state

Current phase: `A4 - Live transcript validation`

Current state:

`A3_COMPLETE / SERVER_SIDE_YOUTUBE_INGRESS_BLOCKED / A4_2_CLIENT_ASSISTED_IMPLEMENTED / VOICEBRIDGE_CI_PASS / KRC_CONTRACT_UPDATED / LIVE_CLIENT_TEST_NEXT`

The direct Render/datacenter YouTube acquisition path is confirmed blocked by YouTube anti-bot enforcement. The approved A4.2 response is a separate client/browser-assisted ingestion path. Production VoiceBridge and the published K-Research & Critic GPT remain isolated and unchanged.

## Repositories

KRC:
- repo `kolemasakar/K_Research_Critic`;
- branch `agent/video-url-research`;
- draft PR #8;
- public GPT and `main` unchanged.

VoiceBridge:
- repo `kolemasakar/VoiceBridge`;
- branch `agent/krc-media-transcript`;
- draft PR #28;
- production service and `main` unchanged.

## Render beta

Service: `voicebridge-krc-media-beta-kolemasakar`.

Service ID: `srv-da1kic5bedkc73d6fk60`.

Endpoint: `https://voicebridge-krc-media-beta-kolemasakar.onrender.com`.

Verified base configuration before A4.2 deployment verification:
- plan `free`;
- media mode `closed_beta`;
- action/provider configuration present;
- max duration 3600 sec;
- max concurrent jobs 1;
- daily STT budget 7200 sec;
- language hints auto/uk/ru/en.

## A4.1 server-side evidence

Acceptance URL:
`https://www.youtube.com/watch?v=DZLzmQ2kwaA`

Three server-side attempts failed before transcript acquisition:
- original yt-dlp path: `KRCB_1c137194-3b23-4ed9-ab1e-fa5a49255cc9`;
- `web_embedded,android_vr`: `KRCB_03d37ccd-4059-4b0c-9675-6f2568d4c207`;
- `mweb` + PO Token Provider: `KRCB_981465dc-e400-470f-a236-c5414c26bd63`.

All three returned YouTube `Sign in to confirm you're not a bot` and charged `0` STT seconds.

One-shot diagnostic run `32060462596`, job `95480351954`, proved the PO-token integration itself was functioning:
- bgutil provider `/ping`: PASS;
- yt-dlp `2026.07.04`: PASS;
- Node EJS runtime: PASS;
- `PO Token Providers: bgutil:http-1.3.1 (external)`: present;
- YouTube anti-bot response still occurred.

Conclusion: server-side cloud/datacenter YouTube ingress is not the beta acceptance path. Do not continue blind retries from the same cloud-IP architecture.

## Approved A4.2 architecture

User approved client/browser-assisted ingestion.

Current target flow:
```text
YouTube URL
 -> KRC MEDIA BETA Action creates KRCC_ job
 -> status AWAITING_CLIENT
 -> separate KRC MEDIA BETA browser helper
 -> active same YouTube tab captured through tester browser/network path
 -> compressed audio uploaded to isolated beta backend
 -> backend validates source, duration and quota
 -> AssemblyAI async multilingual STT
 -> timestamped transcript segments
 -> provider delete request
 -> KRC claim inventory
 -> CriticProfile gate
 -> user approval
 -> independent Research -> Critic -> final report
```

Direct reliable transcript/caption acquisition remains preferred when already available through current built-in/web capabilities. The A4.2 helper itself currently captures audio; client-side caption extraction is a planned optimization and must not be described as implemented.

## VoiceBridge A4.2 implementation

New isolated backend components:
- `src/cloud/src/media_client_ingest.ts`;
- `src/cloud/src/media_client_http.ts`;
- additive integration in `src/cloud/src/server.ts`.

Action-facing routes:
```text
POST /api/v1/media/client-transcriptions
GET  /api/v1/media/client-transcriptions/{KRCC_job_id}
GET  /api/v1/media/client-transcriptions/{KRCC_job_id}/segments
```

Browser-only routes, intentionally absent from the GPT Action contract:
```text
POST /api/v1/media/client-transcriptions/{KRCC_job_id}/audio
GET  /api/v1/media/client-transcriptions/{KRCC_job_id}/client-status
```

Implemented controls:
- `KRCC_` client job IDs;
- `AWAITING_CLIENT` state;
- same-YouTube-video matching;
- per-tester ownership using temporary access-code digest, not plaintext job persistence;
- max client upload 32 MiB;
- real captured duration checked with ffprobe;
- 60-minute limit;
- 16 kHz mono approximately 32 kbps STT normalization;
- UK/RU/EN/auto AssemblyAI async transcription;
- timestamped segments;
- provider transcript delete request;
- temporary media cleanup;
- in-memory job TTL.

## Separate browser helper

New directory:
`src/media_beta_helper/`

This is intentionally separate from the validated VoiceBridge translation extension.

Helper 0.1.0 implements:
- Chrome/Edge Manifest V3;
- active-tab YouTube validation;
- tabCapture + offscreen recording;
- Opus approximately 32 kbps;
- normal tab audio playback while capturing;
- Start/Stop UI;
- upload with tester code and active source URL;
- backend status polling;
- detected-language/segment/quota/provider-cleanup status display.

The helper does not receive the server-side Action bearer token or AssemblyAI key.

## Automated validation

VoiceBridge validation run `32062552003` for commit `923389b3fdd89eef4a57b308b8fe2a98d41ce8e5`: SUCCESS.

Validated:
- TypeScript cloud build/tests;
- new client-ingest unit tests;
- existing VoiceBridge browser-extension regression;
- new MEDIA BETA helper JavaScript/manifest checks;
- separate helper package artifact;
- repository documentation checks.

KRC beta contract has been switched to:
- `startMediaBetaClientTranscription`;
- `getMediaBetaClientTranscriptionStatus`;
- `getMediaBetaClientTranscriptSegments`;
- `KRCC_` job IDs;
- `AWAITING_CLIENT` semantics.

KRC CI for the final A4.2 contract/documentation branch state must pass before live Builder use.

## Known beta limitations

- helper runtime behavior in real Chrome/Edge is not yet live-validated;
- current helper requires video playback at normal speed for timestamp alignment;
- current helper buffers the recorded compressed audio until Stop;
- client-side captions are not implemented yet;
- current client-ingest STT quota gate is isolated from the legacy server-side media route; the beta GPT must use the client-assisted route only to avoid split quota semantics;
- process-memory jobs/quota are beta-only and may reset on service restart.

## Exact next actions

1. Require KRC CI green for the updated client-assisted Action package.
2. Verify the dedicated Render beta has deployed the new VoiceBridge head and health exposes `media_client_ingest` with `configured=true`.
3. Create a new client job for the acceptance URL and require `status=AWAITING_CLIENT`, `job_id=KRCC_...`, `stt_seconds_charged=0` before browser upload.
4. Install/load the separate helper in Chrome/Edge and run a short owner acceptance capture.
5. Require `COMPLETED`, non-empty timestamped segments, sensible STT charge, detected language, and provider cleanup evidence.

Do not merge PR #8 or PR #28, alter the public GPT, introduce personal YouTube cookies, or add paid residential proxy ingress merely to continue A4 beta testing.
