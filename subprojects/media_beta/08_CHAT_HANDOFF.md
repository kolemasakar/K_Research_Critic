# MEDIA BETA Chat Handoff
Канонічний документ відновлення та переходу між чатами для продовження MEDIA BETA.

Version: 1.6
Status: ACTIVE_HANDOFF
Checkpoint date: 2026-08-17

## Recovery command

`recover MEDIA BETA`

## Mandatory recovery order

1. `subprojects/media_beta/00_INDEX.md`
2. `subprojects/media_beta/03_CURRENT_STATE.md`
3. `subprojects/media_beta/06_DECISION_LOG.md`
4. `subprojects/media_beta/02_ROADMAP.md`
5. `subprojects/media_beta/01_ARCHITECTURE.md`
6. `subprojects/media_beta/04_OPERATIONS_RUNBOOK.md`
7. `subprojects/media_beta/05_TEST_PLAN.md`
8. `subprojects/media_beta/07_FREE_MODE_TARGET.md`

Then verify live GitHub state for both draft PRs before writes.

## Repository context

KRC: `kolemasakar/K_Research_Critic`, branch `agent/video-url-research`, draft PR #8.

VoiceBridge: `kolemasakar/VoiceBridge`, branch `agent/krc-media-transcript`, draft PR #28.

Production branches and published products remain unchanged.

## Current checkpoint

`A3_COMPLETE / A4_1_CLOUD_INGRESS_BLOCKED / A4_2_CLIENT_ASSISTED_LIVE / FIRST_BROWSER_CAPTURE_REACHED_BACKEND / WEBM_DURATION_FIX_DEPLOYED / NEW_KRCC_RETEST_NEXT`

Dedicated beta service:
- `voicebridge-krc-media-beta-kolemasakar`;
- ID `srv-da1kic5bedkc73d6fk60`;
- Free plan.

## A4.1 conclusion

Acceptance URL:
`https://www.youtube.com/watch?v=DZLzmQ2kwaA`

Three server-side attempts ended with YouTube `Sign in to confirm you're not a bot`, all before AssemblyAI and all with `stt_seconds_charged=0`.

PO-provider diagnostic run `32060462596` / job `95480351954` verified bgutil provider, yt-dlp 2026.07.04 and Node EJS runtime were correctly wired. Server-side cloud/datacenter YouTube ingestion is therefore closed as the current beta acceptance architecture.

## Approved A4.2 architecture

User approved client/browser-assisted ingress.

```text
YouTube URL
 -> beta GPT Action creates KRCC_ job
 -> AWAITING_CLIENT
 -> separate KRC MEDIA BETA browser helper
 -> same active YouTube tab captured via tester browser/network path
 -> compressed audio upload to isolated beta backend
 -> bounded ffmpeg normalization
 -> reliable normalized-audio duration/source/quota validation
 -> AssemblyAI async STT
 -> timestamped transcript
 -> claim inventory
 -> CriticProfile
 -> user approval
 -> independent Research / Critic
```

Direct reliable transcript/caption acquisition remains preferred when already available. Client-side caption extraction is not implemented in helper 0.1.0 and remains a planned optimization.

## A4.2 implementation evidence

VoiceBridge initial client-assisted implementation:
- commit `923389b3fdd89eef4a57b308b8fe2a98d41ce8e5`;
- CI run `32062552003`: SUCCESS;
- backend `media_client_ingest.ts` and `media_client_http.ts`;
- additive `server.ts` integration;
- separate `src/media_beta_helper/` Chrome/Edge MV3 helper.

Current VoiceBridge duration-fix deployment:
- commit `772901a167611f0197d1bc05cea8091da211dc47`;
- CI run `32067365619`: SUCCESS.

KRC beta Action:
- `startMediaBetaClientTranscription`;
- `getMediaBetaClientTranscriptionStatus`;
- `getMediaBetaClientTranscriptSegments`;
- `KRCC_` job IDs;
- `AWAITING_CLIENT` state;
- browser-only upload/status endpoints intentionally not exposed as GPT Actions.

KRC package CI run `32063557028`: SUCCESS.

## Live Render A4.2 state

Initial explicit A4.2 deployment:
- workflow run `32063396120`: SUCCESS;
- deploy ID `dep-da1mgebutv3s73fd2grg`;
- commit `923389b3fdd89eef4a57b308b8fe2a98d41ce8e5` reached `live`.

Current duration-fix deployment:
- workflow run `32067505039`: SUCCESS;
- deploy ID `dep-da1n5rou01pc73b5v73g`;
- exact commit `772901a167611f0197d1bc05cea8091da211dc47` reached `live`;
- health HTTP 200;
- service status `ok`;
- `media_client_ingest.mode=client_assisted`;
- `media_client_ingest.configured=true`;
- `requires_browser_helper=true`.

Temporary patch/deploy workflow files were removed after verification. Production VoiceBridge was not targeted.

## First real owner browser test

Created job:
`KRCC_aa3b2cbc-4d4e-4f89-b6e6-4549766f34f5`.

Initial state PASS:
```text
status=AWAITING_CLIENT
client_upload_required=true
stt_seconds_charged=0
remaining daily STT=7200 sec
```

Owner installed helper 0.1.0 in Edge. Helper reached `CAPTURING` on the correct YouTube tab and browser audio upload reached backend processing.

First Stop result:
`MEDIA_DURATION_UNKNOWN: The browser-captured audio duration could not be determined.`

Root cause: MediaRecorder streaming WebM/Opus may omit container-level duration metadata. Initial backend probed raw WebM before ffmpeg normalization.

Fix now live:
- normalize raw capture first;
- hard-bound ffmpeg processing around the 60-minute limit;
- probe duration on normalized MP3;
- reserve STT quota only after successful duration validation.

Helper 0.1.0 is unchanged and does not need reinstall. The failed KRCC job is terminal and must not be reused.

## Beta resource/security baseline

- owner + up to 3 testers;
- max captured duration 60 min;
- concurrency 1;
- AssemblyAI budget 7200 sec/UTC day;
- helper upload max 32 MiB;
- helper audio approximately 32 kbps Opus;
- backend STT normalization mono 16 kHz approximately 32 kbps;
- no personal YouTube cookies;
- no paid residential proxy;
- browser helper never receives Action bearer secret or AssemblyAI key;
- plaintext tester code excluded from backend job state; temporary digest may enforce job ownership;
- full transcript and tester code excluded from KRC checkpoint.

## Exact next task

Create a NEW fresh client-assisted job for the same acceptance URL. Do not reuse `KRCC_aa3b2cbc-4d4e-4f89-b6e6-4549766f34f5` because it is terminal FAILED.

Expected new response:
```text
HTTP 202
job_id=KRCC_...
status=AWAITING_CLIENT
client_upload_required=true
stt_seconds_charged=0
```

Reuse the already installed `KRC MEDIA BETA Helper 0.1.0`. Enter the new KRCC job ID and the same tester code, capture approximately 60-90 seconds at normal speed, Stop, and require:
- upload accepted;
- `TRANSCRIBING`;
- `COMPLETED`;
- non-empty timestamped segments;
- detected language;
- sensible STT charge;
- provider cleanup evidence.

## Do-not-do list

Do not merge PR #8/#28 automatically, modify public GPT/production VoiceBridge, expose credentials/tester codes, use personal YouTube cookies, add paid proxy infrastructure, claim successful end-to-end browser transcription before evidence, or bypass CriticProfile approval.

## Terminal markers

`MEDIA_BETA_HANDOFF_V1_6`

`A4_2_CLIENT_ASSISTED_LIVE`

`WEBM_DURATION_FIX_DEPLOYED`

`NEW_KRCC_OWNER_RETEST_NEXT`

`PRODUCTION_ISOLATED_DRAFT_PRS_UNMERGED`
