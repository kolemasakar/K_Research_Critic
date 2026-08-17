# MEDIA BETA Work Log
Хронологічний журнал суттєвих робіт і перевірок підпроєкту для аудиту та відновлення контексту.

Version: 1.8
Status: ACTIVE

## 2026-08-17 - Media URL upgrade initiated

Approved goal: public YouTube URL -> transcript -> material claims -> CriticProfile gate -> independent research -> Critic -> final claim verification/report. Existing text mode remains intact.

## 2026-08-17 - Feature branches and draft PRs

KRC: branch `agent/video-url-research`, draft PR #8.

VoiceBridge: branch `agent/krc-media-transcript`, draft PR #28.

Automated implementation CI reached green state.

## 2026-08-17 - Free-tier review and closed beta controls

Approved: owner + up to 3 testers, max video/capture 60 min, concurrency 1, AssemblyAI budget 7200 sec/UTC day, STT audio mono 16 kHz approximately 32 kbps, separate beta GPT/backend, production isolation.

## 2026-08-17 - Dedicated Free Render beta service

Created `voicebridge-krc-media-beta-kolemasakar`, ID `srv-da1kic5bedkc73d6fk60`, on plan `free`. Production VoiceBridge was not modified.

A3 final verification run `32055491376`: beta health/configuration PASS and production health PASS.

## 2026-08-17 - A4.1 server-side YouTube attempts

Acceptance URL:
`https://www.youtube.com/watch?v=DZLzmQ2kwaA`

Three server-side attempts failed before AssemblyAI with YouTube `Sign in to confirm you're not a bot`:
- original route: `KRCB_1c137194-3b23-4ed9-ab1e-fa5a49255cc9`;
- R1 `web_embedded,android_vr`: `KRCB_03d37ccd-4059-4b0c-9675-6f2568d4c207`;
- R2 `mweb` + PO provider: `KRCB_981465dc-e400-470f-a236-c5414c26bd63`.

All three charged `0` STT seconds.

## 2026-08-17 - PO-provider diagnostic

Diagnostic run `32060462596`, job `95480351954` verified:
- bgutil `/ping`;
- yt-dlp `2026.07.04`;
- Node EJS runtime;
- `PO Token Providers: bgutil:http-1.3.1 (external)`.

The same YouTube anti-bot challenge remained. Conclusion: blocker is cloud/datacenter ingress, not missing PO-provider wiring. Blind server-side retries stopped.

## 2026-08-17 - D016 client-assisted architecture approved

User approved browser/client-assisted ingestion for the closed beta.

Initial path:
```text
YouTube URL
 -> KRCC_ job / AWAITING_CLIENT
 -> separate browser helper
 -> active YouTube tab captured through tester network path
 -> compressed audio upload
 -> isolated beta backend
 -> AssemblyAI async STT
 -> timestamped transcript
```

No personal YouTube cookies or paid residential proxy introduced.

## 2026-08-17 - VoiceBridge A4.2 implementation

Added:
- `src/cloud/src/media_client_ingest.ts`;
- `src/cloud/src/media_client_http.ts`;
- additive client route integration in `src/cloud/src/server.ts`;
- tests `src/cloud/tests/media_client_ingest.test.ts`;
- separate `src/media_beta_helper/` Chrome/Edge MV3 helper.

Implemented controls:
- `KRCC_` client job IDs and `AWAITING_CLIENT`;
- same-video matching;
- per-tester temporary ownership digest;
- 32 MiB upload limit;
- duration validation and 60-minute limit;
- ffmpeg mono 16 kHz approximately 32 kbps STT normalization;
- AssemblyAI auto/uk/ru/en;
- timestamped segments;
- provider delete request;
- temporary media cleanup.

The existing validated VoiceBridge translation extension was not replaced or modified by the helper feature.

VoiceBridge CI run `32062552003` on commit `923389b3fdd89eef4a57b308b8fe2a98d41ce8e5`: SUCCESS.

Helper artifact `KRC_MEDIA_BETA_Helper_0.1.0` was produced by CI.

## 2026-08-17 - KRC beta contract switched to A4.2

Closed-beta Action uses:
- `startMediaBetaClientTranscription`;
- `getMediaBetaClientTranscriptionStatus`;
- `getMediaBetaClientTranscriptSegments`.

Media beta manifest advanced to `0.2-beta`. Browser upload/status endpoints remain intentionally absent from the GPT Action schema.

KRC CI run `32063557028` after these updates: SUCCESS.

## 2026-08-17 - A4.2 explicit Render deployment

An explicit isolated deployment targeted only service `srv-da1kic5bedkc73d6fk60` and exact VoiceBridge commit `923389b3fdd89eef4a57b308b8fe2a98d41ce8e5`.

Deploy workflow run `32063396120`: SUCCESS.

Evidence:
- deploy ID `dep-da1mgebutv3s73fd2grg`;
- exact commit reached `live`;
- beta health HTTP 200;
- `media_client_ingest.mode=client_assisted`;
- `media_client_ingest.configured=true`;
- `requires_browser_helper=true`.

Production VoiceBridge was not targeted.

## 2026-08-17 - First real KRCC owner browser test

Created client job:
`KRCC_aa3b2cbc-4d4e-4f89-b6e6-4549766f34f5`.

Initial response PASS:
- `AWAITING_CLIENT`;
- `client_upload_required=true`;
- `stt_seconds_charged=0`;
- daily quota remaining 7200 sec.

Owner loaded helper 0.1.0 in Edge and the helper successfully reached `CAPTURING` on the same YouTube video. Audio capture and upload reached backend processing.

Stop result:
`MEDIA_DURATION_UNKNOWN: The browser-captured audio duration could not be determined.`

No AssemblyAI STT charge was recorded for this failure.

## 2026-08-17 - MediaRecorder WebM duration incident resolved

Root cause: browser MediaRecorder streaming WebM/Opus blobs can omit container-level duration metadata. The initial A4.2 backend probed raw WebM with ffprobe before normalization.

Backend correction:
- normalize first to mono 16 kHz approximately 32 kbps MP3;
- hard-bound processing around the 60-minute limit;
- probe duration on normalized MP3;
- reserve STT quota only after duration validation.

VoiceBridge duration-fix CI run `32067365619`: SUCCESS.

Explicit isolated redeploy:
- deploy ID `dep-da1n5rou01pc73b5v73g`;
- commit `772901a167611f0197d1bc05cea8091da211dc47` reached `live`;
- health HTTP 200.

## 2026-08-17 - D017 captions-first priority approved

User asked why the system was not taking text from YouTube subtitles. The architecture was revised so browser captions are the primary A4.2 path and audio/AssemblyAI is fallback only.

Approved order:
```text
open YouTube tab
 -> browser caption track if usable
 -> timestamped captions / STT=0
 -> otherwise browser audio
 -> AssemblyAI fallback
```

Reasons recorded:
- captions avoid normal-speed playback for transcript acquisition;
- captions avoid AssemblyAI quota;
- captions reduce Render bandwidth/CPU;
- YouTube caption timestamps already provide claim traceability;
- browser origin avoids the Render/datacenter anti-bot blocker.

## 2026-08-17 - Helper 0.2.0 captions-first implementation

VoiceBridge branch added:
- browser-only `POST /api/v1/media/client-transcriptions/{KRCC_job_id}/captions`;
- backend `acceptCaptions` validation and completion path;
- `transcript_source=youtube_captions`;
- `caption_type=manual|auto_generated`;
- `provider=youtube`;
- `stt_seconds_charged=0`;
- caption segment/timestamp/text bounds;
- same-video and per-tester ownership checks.

Helper 0.2.0 added:
- Manifest V3 `scripting` permission with existing `activeTab`;
- user-initiated caption extraction in the active YouTube player context;
- best-effort caption-track selection;
- timed-text `json3` fetch through the tester browser;
- `Use subtitles` primary action;
- `Audio fallback` retained;
- source/caption-type/language/segment/STT status display.

YouTube player internals are not a stable public API. Caption extraction is therefore explicitly best-effort and falls back to audio if unavailable.

## 2026-08-17 - Captions-first automated validation and deployment

VoiceBridge captions-first CI:
- run `32069122559`;
- commit `92f809440098fd42eb562a36c6feddeaa9c17155`;
- cloud build/tests PASS;
- browser/helper JS + manifest PASS;
- Helper 0.2.0 package PASS;
- repository docs PASS.

Unit test verified caption completion with timestamped segments and zero STT quota charge.

Explicit isolated Render deployment:
- workflow run `32069270467`: SUCCESS;
- deploy ID `dep-da1nf76gekts738dst5g`;
- exact commit `92f809440098fd42eb562a36c6feddeaa9c17155` reached `live`;
- health HTTP 200;
- `media_client_ingest.mode=client_assisted`;
- `configured=true`;
- `requires_browser_helper=true`.

Production VoiceBridge was not targeted.

KRC beta Action contract advanced to `0.3.0-beta` to represent `youtube_captions` and `assemblyai_stt`. Media beta manifest advanced to `0.3-beta` with client captions-first marked implemented pending live browser acceptance.

## 2026-08-17 - Current next gate

Install/reload Helper 0.2.0 and create a NEW `KRCC_...` job for the same acceptance URL.

Press `Use subtitles` first and require:
- `COMPLETED`;
- `transcript_source=youtube_captions`;
- manual/auto-generated caption type;
- non-empty timestamped segments;
- source/detected language;
- `stt_seconds_charged=0`;
- unchanged AssemblyAI beta quota.

Only if captions are unavailable/unusable should `Audio fallback` be tested.

## Logging rule

Append only material implementation, deployment, acceptance, failure, architecture/provider, resource-limit, promotion, or rollback events. Never log credential values, tester codes, hidden reasoning, or full transcripts.
