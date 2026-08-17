# MEDIA BETA Work Log
Хронологічний журнал суттєвих робіт і перевірок підпроєкту для аудиту та відновлення контексту.

Version: 1.7
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

Current path:
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

Closed-beta Action now uses:
- `startMediaBetaClientTranscription`;
- `getMediaBetaClientTranscriptionStatus`;
- `getMediaBetaClientTranscriptSegments`.

Contract semantics:
- `KRCC_` job IDs;
- `AWAITING_CLIENT` before helper upload;
- browser upload/status endpoints are not GPT Actions;
- direct reliable transcript/captions remain preferred when available;
- client-side caption extraction is explicitly marked planned, not implemented.

Media beta manifest advanced to `0.2-beta`. Privacy policy advanced to 0.3 for browser-assisted processing and local helper-code storage disclosure.

KRC CI run `32063557028` after these updates: SUCCESS.

## 2026-08-17 - A4.2 explicit Render deployment

A read-only Render check first found the old R2 commit `d7864ad1625f815613deaea8043b4f1786768c61` still live because the beta service was created with auto-deploy disabled.

An explicit isolated deployment targeted only service `srv-da1kic5bedkc73d6fk60` and exact VoiceBridge commit `923389b3fdd89eef4a57b308b8fe2a98d41ce8e5`.

Deploy workflow run `32063396120`: SUCCESS.

Evidence:
- Render deploy request HTTP 201;
- deploy ID `dep-da1mgebutv3s73fd2grg`;
- exact commit reached `live`;
- beta health HTTP 200;
- `media_client_ingest.mode=client_assisted`;
- `media_client_ingest.configured=true`;
- `requires_browser_helper=true`;
- `upload_max_bytes=33554432`.

Temporary deployment workflow file was removed after verification. Production VoiceBridge was not targeted.

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

## 2026-08-17 - MediaRecorder WebM duration incident resolved in backend

Root cause: browser MediaRecorder streaming WebM/Opus blobs can omit container-level duration metadata. The initial A4.2 backend probed raw WebM with ffprobe before normalization, so a valid browser capture could return unknown duration.

Backend correction:
- write browser capture to temporary source file;
- normalize first with ffmpeg to mono 16 kHz approximately 32 kbps MP3;
- apply a hard processing cap of max duration plus approximately one second;
- verify normalized file size;
- probe duration on normalized MP3;
- enforce the 60-minute limit after the reliable probe;
- reserve STT quota only after duration validation succeeds.

Helper 0.1.0 was not changed and does not require reinstall.

VoiceBridge duration-fix CI:
- run `32067365619`;
- commit `772901a167611f0197d1bc05cea8091da211dc47`;
- browser-extension PASS;
- cloud build/tests PASS;
- repository-docs PASS;
- overall SUCCESS.

Explicit isolated Render redeploy:
- workflow run `32067505039`: SUCCESS;
- deploy ID `dep-da1n5rou01pc73b5v73g`;
- exact commit `772901a167611f0197d1bc05cea8091da211dc47` reached `live`;
- health HTTP 200;
- service status `ok`;
- `media_client_ingest.mode=client_assisted`;
- `configured=true`;
- `requires_browser_helper=true`.

The one-shot patch/deploy workflow files were removed after use. Production VoiceBridge was not targeted.

## 2026-08-17 - Current next gate

The failed KRCC job is terminal and must not be reused.

Create a NEW `KRCC_...` job for the same acceptance URL, reuse the already installed helper 0.1.0, capture approximately 60-90 seconds at normal speed, then require:
- upload accepted;
- `TRANSCRIBING`;
- `COMPLETED`;
- non-empty timestamped segments;
- detected language;
- sensible STT charge;
- provider cleanup evidence.

## Logging rule

Append only material implementation, deployment, acceptance, failure, architecture/provider, resource-limit, promotion, or rollback events. Never log credential values, tester codes, hidden reasoning, or full transcripts.
