# MEDIA BETA Current State
Канонічний знімок фактичного стану реалізації для відновлення роботи без припущень.

Version: 1.9
Status: ACTIVE_CHECKPOINT
Checkpoint date: 2026-08-17

## Executive state

Current phase: `A4 - Live transcript validation`

Current state:

`A3_COMPLETE / A4_1_SERVER_INGRESS_BLOCKED / A4_2_CAPTIONS_FIRST_IMPLEMENTED / VOICEBRIDGE_CI_GREEN / RENDER_CAPTIONS_FIRST_LIVE / HELPER_0_2_OWNER_ACCEPTANCE_NEXT`

Direct Render/datacenter YouTube acquisition remains unsuitable because YouTube anti-bot enforcement blocks the cloud path. The approved A4.2 architecture is now captions-first browser-assisted ingestion: the helper reads the caption track through the tester browser and uses browser audio plus AssemblyAI only as fallback. The captions-first backend and Helper 0.2.0 are implemented, automated validation is green, and the exact implementation commit is live on the isolated Render MEDIA BETA service. Production VoiceBridge and the published K-Research & Critic GPT remain unchanged.

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
- daily AssemblyAI fallback budget 7200 sec;
- language hints auto/uk/ru/en;
- browser helper required for the current beta ingestion path.

## A4.1 server-side conclusion

Acceptance URL:
`https://www.youtube.com/watch?v=DZLzmQ2kwaA`

Three server-side attempts failed before transcript acquisition:
- `KRCB_1c137194-3b23-4ed9-ab1e-fa5a49255cc9`;
- `KRCB_03d37ccd-4059-4b0c-9675-6f2568d4c207`;
- `KRCB_981465dc-e400-470f-a236-c5414c26bd63`.

All returned YouTube `Sign in to confirm you're not a bot` and charged `0` STT seconds. Diagnostic run `32060462596`, job `95480351954`, confirmed the PO-provider/runtime wiring worked. Repeated server-side cloud-ingress retries are not an approved beta path.

## Approved A4.2 captions-first flow

```text
YouTube URL
 -> KRC MEDIA BETA Action creates KRCC_ job
 -> status AWAITING_CLIENT
 -> KRC MEDIA BETA Helper 0.2.0 in tester Chrome/Edge
 -> try active/source YouTube caption track through tester browser
    -> timestamped captions found
       -> browser-only /captions upload
       -> source/timestamp/access validation
       -> COMPLETED
       -> transcript_source=youtube_captions
       -> stt_seconds_charged=0
    -> captions unavailable/unusable
       -> Audio fallback
       -> tabCapture through tester browser/network path
       -> compressed audio upload
       -> bounded ffmpeg normalization
       -> duration/source/quota validation
       -> AssemblyAI async multilingual STT
       -> timestamped transcript
       -> provider delete request
 -> KRC claim inventory
 -> CriticProfile gate
 -> user approval
 -> independent Research / Critic
```

Caption text remains source content only. It proves what is represented as being said in the video; it is not independent evidence that the claims are true.

## VoiceBridge captions-first implementation

Current VoiceBridge feature/deployed commit:
`92f809440098fd42eb562a36c6feddeaa9c17155`

Core backend components:
- `src/cloud/src/media_client_ingest.ts`;
- `src/cloud/src/media_client_http.ts`;
- additive integration in `src/cloud/src/server.ts`.

Action-facing routes remain:
```text
POST /api/v1/media/client-transcriptions
GET  /api/v1/media/client-transcriptions/{KRCC_job_id}
GET  /api/v1/media/client-transcriptions/{KRCC_job_id}/segments
```

Browser-only routes:
```text
POST /api/v1/media/client-transcriptions/{KRCC_job_id}/captions
POST /api/v1/media/client-transcriptions/{KRCC_job_id}/audio
GET  /api/v1/media/client-transcriptions/{KRCC_job_id}/client-status
```

The browser-only routes are intentionally absent from the GPT Action schema.

Caption path controls:
- same-YouTube-video validation;
- per-tester job ownership digest;
- caption language/type validation;
- 1..20000 caption segments;
- monotonic timestamps;
- 60-minute timestamp boundary;
- bounded text sizes;
- `caption_type=manual|auto_generated`;
- `transcript_source=youtube_captions`;
- `provider=youtube`;
- `stt_seconds_charged=0`;
- no AssemblyAI provider transcript is created.

Audio fallback controls retained:
- max client audio upload 32 MiB;
- browser WebM/Opus normalized before duration probing;
- bounded ffmpeg processing;
- duration probed on normalized MP3;
- STT quota reserved only after duration validation;
- mono 16 kHz approximately 32 kbps normalization;
- AssemblyAI auto/uk/ru/en;
- timestamped segments;
- provider transcript delete request;
- temporary media cleanup.

## Browser helper

Directory:
`src/media_beta_helper/`

Current helper: `0.2.0`.

Implemented:
- Chrome/Edge Manifest V3;
- `activeTab` plus `scripting` for user-initiated YouTube caption extraction;
- best-effort access to the current YouTube player caption-track metadata;
- browser fetch of selected caption timed-text as `json3`;
- preference for active caption language and manual/source captions when suitable;
- timestamped caption upload to `/captions`;
- UI: `Use subtitles`, `Audio fallback`, `Stop`;
- fallback tabCapture/offscreen Opus recording remains available;
- status displays transcript source, caption type, language, segments, STT seconds and provider cleanup.

The helper never receives the Action bearer token or AssemblyAI API key. The tester beta code remains the only user-side beta credential.

YouTube player internals used for caption discovery are not a stable public YouTube API. Therefore caption extraction is best-effort and failure must fall back to audio rather than being treated as a terminal architecture failure.

## Validation evidence

VoiceBridge captions-first CI:
- run `32069122559`;
- commit `92f809440098fd42eb562a36c6feddeaa9c17155`;
- cloud build/tests SUCCESS;
- browser/helper JS + manifest validation SUCCESS;
- Helper 0.2.0 package SUCCESS;
- repository-docs SUCCESS.

Backend unit coverage includes caption completion with:
- `status=COMPLETED`;
- `transcript_source=youtube_captions`;
- `caption_type=auto_generated`;
- `provider=youtube`;
- `stt_seconds_charged=0`;
- timestamped segments;
- no STT quota consumption.

KRC media beta contract advanced to `0.3.0-beta` with `youtube_captions` and `assemblyai_stt` result semantics. KRC branch CI must remain green after the associated documentation/contract updates.

## Live Render captions-first deployment

Workflow run:
`32069270467` - SUCCESS.

Deploy:
- deploy ID `dep-da1nf76gekts738dst5g`;
- exact commit `92f809440098fd42eb562a36c6feddeaa9c17155` reached `live`;
- health HTTP 200;
- service status `ok`;
- `media_client_ingest.mode=client_assisted`;
- `configured=true`;
- `requires_browser_helper=true`.

Production VoiceBridge was not targeted.

## Previous owner browser evidence

Previous helper 0.1.0 proved:
- extension installation works;
- same YouTube URL can be used;
- tab capture reaches `CAPTURING`;
- browser audio reaches backend.

The first audio job `KRCC_aa3b2cbc-4d4e-4f89-b6e6-4549766f34f5` ended with `MEDIA_DURATION_UNKNOWN`; the backend duration bug was fixed in commit `772901a167611f0197d1bc05cea8091da211dc47` and remains included in the current captions-first commit.

## Exact next acceptance action

Install/reload Helper 0.2.0 and create a NEW fresh `KRCC_...` job for the acceptance URL.

First press `Use subtitles` rather than starting audio capture.

Required captions-first PASS evidence:
- helper/backend `COMPLETED`;
- `transcript_source=youtube_captions`;
- `caption_type=manual` or `auto_generated`;
- non-empty timestamped segments;
- sensible detected/source language;
- `stt_seconds_charged=0`;
- beta STT quota unchanged.

Only if Helper 0.2.0 reports captions unavailable/unusable should the owner run `Audio fallback` and validate AssemblyAI STT.

## Known beta limitations

- real owner Helper 0.2.0 caption extraction has not yet been accepted on the target video;
- YouTube player caption metadata is an internal browser-page interface and may change;
- audio fallback still requires normal-speed playback for timestamp alignment;
- process-memory jobs/quota can reset on service restart;
- client-ingest quota remains separate from the legacy server-side route;
- AssemblyAI model-training opt-out remains a public-release gate for fallback use.

Do not merge PR #8 or PR #28, modify the public GPT, introduce personal YouTube cookies, or add paid residential proxy ingress merely to continue A4 beta testing.
