# MEDIA BETA Current State
Канонічний знімок фактичного стану реалізації для відновлення роботи без припущень.

Version: 1.8
Status: ACTIVE_CHECKPOINT
Checkpoint date: 2026-08-17

## Executive state

Current phase: `A4 - Live transcript validation`

Current state:

`A3_COMPLETE / A4_1_SERVER_INGRESS_BLOCKED / A4_2_CLIENT_ASSISTED_IMPLEMENTED / FIRST_BROWSER_CAPTURE_REACHED_BACKEND / WEBM_DURATION_FIX_LIVE / OWNER_RETEST_NEXT`

The direct Render/datacenter YouTube acquisition path is confirmed blocked by YouTube anti-bot enforcement. A4.2 therefore uses client/browser-assisted ingestion. The first real owner browser capture reached the beta backend but exposed a MediaRecorder WebM duration-metadata issue before STT. The backend duration handling has been corrected, validated in CI, and explicitly redeployed to the isolated Render MEDIA BETA service. Production VoiceBridge and the published K-Research & Critic GPT remain unchanged.

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

## Dedicated Render beta

Service:
`voicebridge-krc-media-beta-kolemasakar`

Service ID:
`srv-da1kic5bedkc73d6fk60`

Endpoint:
`https://voicebridge-krc-media-beta-kolemasakar.onrender.com`

Verified beta baseline:
- plan `free`;
- max duration 3600 sec;
- max concurrent jobs 1;
- daily STT budget 7200 sec;
- language hints auto/uk/ru/en.

## A4.1 server-side conclusion

Acceptance URL:
`https://www.youtube.com/watch?v=DZLzmQ2kwaA`

Three server-side attempts failed before transcript acquisition:
- `KRCB_1c137194-3b23-4ed9-ab1e-fa5a49255cc9`;
- `KRCB_03d37ccd-4059-4b0c-9675-6f2568d4c207`;
- `KRCB_981465dc-e400-470f-a236-c5414c26bd63`.

All returned YouTube `Sign in to confirm you're not a bot` and charged `0` STT seconds.

Diagnostic run `32060462596`, job `95480351954`, confirmed the PO-provider/runtime wiring worked. Server-side cloud/datacenter YouTube ingress is therefore not the approved beta acceptance path.

## Approved A4.2 client-assisted flow

```text
YouTube URL
 -> KRC MEDIA BETA Action creates KRCC_ job
 -> status AWAITING_CLIENT
 -> separate KRC MEDIA BETA browser helper
 -> same active YouTube tab captured through tester browser/network path
 -> compressed audio uploaded to isolated beta backend
 -> normalize browser audio with bounded ffmpeg processing
 -> duration/source/quota validation
 -> AssemblyAI async multilingual STT
 -> timestamped transcript segments
 -> provider delete request
 -> KRC claim inventory
 -> CriticProfile gate
 -> user approval
 -> independent Research / Critic
```

Direct reliable transcript/caption intake remains preferred when available through current built-in/web capabilities. Helper-side caption extraction is not implemented in 0.1.0 and remains a planned optimization.

## VoiceBridge A4.2 implementation

Initial A4.2 implementation commit:
`923389b3fdd89eef4a57b308b8fe2a98d41ce8e5`

Current deployed duration-fix commit:
`772901a167611f0197d1bc05cea8091da211dc47`

Core backend components:
- `src/cloud/src/media_client_ingest.ts`;
- `src/cloud/src/media_client_http.ts`;
- additive integration in `src/cloud/src/server.ts`.

Action-facing routes:
```text
POST /api/v1/media/client-transcriptions
GET  /api/v1/media/client-transcriptions/{KRCC_job_id}
GET  /api/v1/media/client-transcriptions/{KRCC_job_id}/segments
```

Browser-only routes:
```text
POST /api/v1/media/client-transcriptions/{KRCC_job_id}/audio
GET  /api/v1/media/client-transcriptions/{KRCC_job_id}/client-status
```

Controls:
- `KRCC_` client job IDs;
- `AWAITING_CLIENT`;
- same-YouTube-video matching;
- temporary SHA-256 access-code ownership digest;
- max client upload 32 MiB;
- browser WebM/Opus is normalized before duration probing;
- ffmpeg normalization has a hard approximately 60-minute processing cap;
- duration is probed on normalized MP3 where metadata is reliable;
- STT quota is reserved only after duration validation succeeds;
- 60-minute limit;
- 16 kHz mono approximately 32 kbps STT normalization;
- UK/RU/EN/auto AssemblyAI transcription;
- timestamped segments;
- provider transcript delete request;
- temporary media cleanup;
- in-memory job TTL.

## Separate browser helper

Directory:
`src/media_beta_helper/`

Helper 0.1.0:
- Chrome/Edge Manifest V3;
- active-tab YouTube validation;
- tabCapture + offscreen recording;
- Opus approximately 32 kbps;
- normal tab-audio playback while capturing;
- Start/Stop UI;
- upload with tester code and active source URL;
- backend status polling;
- detected-language/segment/STT/provider-cleanup display.

It does not receive the Action bearer token or AssemblyAI API key.

The duration fix is backend-only; helper 0.1.0 does not require reinstall for the next retest.

## Automated validation

Initial VoiceBridge A4.2 CI:
- run `32062552003`;
- commit `923389b3fdd89eef4a57b308b8fe2a98d41ce8e5`;
- result SUCCESS.

Duration-fix VoiceBridge CI:
- run `32067365619`;
- commit `772901a167611f0197d1bc05cea8091da211dc47`;
- browser-extension SUCCESS;
- cloud build/tests SUCCESS;
- repository-docs SUCCESS;
- overall SUCCESS.

KRC package CI after A4.2 contract/privacy updates:
- run `32063557028`;
- result SUCCESS.

## Live Render A4.2 deployment history

Initial A4.2 deploy:
- workflow run `32063396120`: SUCCESS;
- deploy ID `dep-da1mgebutv3s73fd2grg`;
- exact commit `923389b3fdd89eef4a57b308b8fe2a98d41ce8e5` reached `live`;
- health HTTP 200;
- `media_client_ingest.mode=client_assisted`;
- `media_client_ingest.configured=true`;
- `requires_browser_helper=true`;
- `upload_max_bytes=33554432`.

Duration-fix redeploy:
- workflow run `32067505039`: SUCCESS;
- deploy ID `dep-da1n5rou01pc73b5v73g`;
- exact commit `772901a167611f0197d1bc05cea8091da211dc47` reached `live`;
- health HTTP 200;
- service status `ok`;
- `media_client_ingest.mode=client_assisted`;
- `configured=true`;
- `requires_browser_helper=true`.

Temporary deployment workflow files were removed after verification. Production VoiceBridge was not targeted.

## First real owner browser acceptance evidence

Created job:
`KRCC_aa3b2cbc-4d4e-4f89-b6e6-4549766f34f5`

Initial state:
- `AWAITING_CLIENT`;
- `client_upload_required=true`;
- `stt_seconds_charged=0`;
- daily quota remaining 7200 sec.

Owner Edge helper 0.1.0:
- installed successfully;
- same YouTube URL open;
- helper reached `CAPTURING`;
- active tab audio was captured and upload reached backend processing.

First Stop result:
`MEDIA_DURATION_UNKNOWN: The browser-captured audio duration could not be determined.`

Root cause:
MediaRecorder streaming WebM/Opus may omit container-level duration metadata. The backend had probed the raw capture before ffmpeg normalization.

Resolution:
- normalize browser capture to bounded MP3 first;
- probe normalized MP3 duration;
- enforce duration limit after reliable probe;
- reserve STT quota only after successful duration validation.

The failed job is terminal and must not be reused for the retest. No AssemblyAI charge was recorded for this failed duration check.

## KRC beta contract

Closed-beta GPT Action uses:
- `startMediaBetaClientTranscription`;
- `getMediaBetaClientTranscriptionStatus`;
- `getMediaBetaClientTranscriptSegments`.

Expected initial Action state:
```text
HTTP 202
job_id=KRCC_...
status=AWAITING_CLIENT
client_upload_required=true
stt_seconds_charged=0
```

Browser audio/status endpoints are intentionally absent from the GPT Action schema and are used only by the helper.

## Known beta limitations

- first browser capture exposed and resolved the raw WebM duration issue; successful end-to-end STT acceptance is still pending retest;
- helper requires normal-speed playback for timestamp alignment;
- helper buffers compressed audio until Stop;
- client-side captions are not implemented yet;
- the client-ingest STT quota gate is separate from the legacy server-side media route; beta GPT must use the client route only until quota accounting is unified or legacy route disabled;
- process-memory jobs/quota can reset on service restart;
- AssemblyAI model-training opt-out remains a public-release gate.

## Exact next action

Create a NEW fresh `KRCC_...` job for the same acceptance URL because the previous browser job is terminal FAILED.

Reuse the already installed helper 0.1.0; no reinstall is required. Capture approximately 60-90 seconds at normal speed and require:
- upload accepted;
- `TRANSCRIBING` then `COMPLETED`;
- non-empty timestamped segments;
- detected language;
- sensible `stt_seconds_charged`;
- provider cleanup result.

Do not merge PR #8 or PR #28, modify the public GPT, introduce personal YouTube cookies, or add paid residential proxy ingress merely to continue A4 beta testing.
