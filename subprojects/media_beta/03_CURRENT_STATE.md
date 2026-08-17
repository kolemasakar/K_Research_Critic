# MEDIA BETA Current State
Канонічний знімок фактичного стану реалізації для відновлення роботи без припущень.

Version: 1.7
Status: ACTIVE_CHECKPOINT
Checkpoint date: 2026-08-17

## Executive state

Current phase: `A4 - Live transcript validation`

Current state:

`A3_COMPLETE / A4_1_SERVER_INGRESS_BLOCKED / A4_2_CLIENT_ASSISTED_IMPLEMENTED / CI_GREEN / RENDER_LIVE / OWNER_BROWSER_ACCEPTANCE_NEXT`

The direct Render/datacenter YouTube acquisition path is confirmed blocked by YouTube anti-bot enforcement. The approved A4.2 response is a separate client/browser-assisted ingestion path. A4.2 code is implemented, automated validation is green, and the exact VoiceBridge implementation commit is live on the isolated Render MEDIA BETA service. Production VoiceBridge and the published K-Research & Critic GPT remain unchanged.

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
 -> source/duration/quota validation
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

Implementation commit:
`923389b3fdd89eef4a57b308b8fe2a98d41ce8e5`

New backend components:
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
- ffprobe duration check;
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

Actual Chrome/Edge runtime acceptance is the next live gate.

## Automated validation

VoiceBridge CI:
- run `32062552003`;
- commit `923389b3fdd89eef4a57b308b8fe2a98d41ce8e5`;
- result SUCCESS.

KRC package CI after A4.2 contract/privacy updates:
- run `32063557028`;
- result SUCCESS.

## Live Render A4.2 deployment

An initial read-only check confirmed auto-deploy had not occurred and old R2 commit `d7864ad1625f815613deaea8043b4f1786768c61` was still live. This was expected because the beta service was originally created with auto-deploy disabled.

An explicit isolated deployment then targeted only MEDIA BETA service `srv-da1kic5bedkc73d6fk60`.

Deployment evidence:
- workflow run `32063396120`: SUCCESS;
- deploy ID `dep-da1mgebutv3s73fd2grg`;
- exact commit `923389b3fdd89eef4a57b308b8fe2a98d41ce8e5` reached `live`;
- health HTTP 200;
- service status `ok`;
- `media_client_ingest.mode=client_assisted`;
- `media_client_ingest.configured=true`;
- `requires_browser_helper=true`;
- `upload_max_bytes=33554432`.

The temporary deployment workflow file was removed after verification. Production VoiceBridge was not targeted.

## KRC beta contract

Closed-beta GPT Action now uses:
- `startMediaBetaClientTranscription`;
- `getMediaBetaClientTranscriptionStatus`;
- `getMediaBetaClientTranscriptSegments`.

Expected first Action state:
```text
HTTP 202
job_id=KRCC_...
status=AWAITING_CLIENT
client_upload_required=true
stt_seconds_charged=0
```

Browser audio/status endpoints are intentionally absent from the GPT Action schema and are used only by the helper.

## Known beta limitations

- real owner Chrome/Edge helper execution is not yet accepted;
- helper requires normal-speed playback for timestamp alignment;
- helper buffers compressed audio until Stop;
- client-side captions are not implemented yet;
- the client-ingest STT quota gate is separate from the legacy server-side media route; beta GPT must use the client route only until quota accounting is unified or legacy route disabled;
- process-memory jobs/quota can reset on service restart;
- AssemblyAI model-training opt-out remains a public-release gate.

## Exact next action

Create one fresh `KRCC_...` job for the acceptance URL without exposing credentials in chat.

Then run a short owner browser test with helper 0.1.0 and require:
- `COMPLETED`;
- non-empty timestamped segments;
- detected language;
- sensible `stt_seconds_charged`;
- provider cleanup result.

Do not merge PR #8 or PR #28, modify the public GPT, introduce personal YouTube cookies, or add paid residential proxy ingress merely to continue A4 beta testing.
