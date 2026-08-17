# MEDIA BETA Chat Handoff
Канонічний документ відновлення та переходу між чатами для продовження MEDIA BETA.

Version: 1.7
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

Production branches, production VoiceBridge, and the published KRC GPT remain unchanged.

## Current checkpoint

`A3_COMPLETE / A4_1_CLOUD_INGRESS_BLOCKED / A4_2_CAPTIONS_FIRST_IMPLEMENTED / VOICEBRIDGE_CI_GREEN / CAPTIONS_FIRST_RENDER_LIVE / HELPER_0_2_OWNER_ACCEPTANCE_NEXT`

Dedicated beta service:
- `voicebridge-krc-media-beta-kolemasakar`;
- ID `srv-da1kic5bedkc73d6fk60`;
- Free plan.

Acceptance URL:
`https://www.youtube.com/watch?v=DZLzmQ2kwaA`

## A4.1 conclusion

Three server-side attempts ended with YouTube `Sign in to confirm you're not a bot`, all before AssemblyAI and all with `stt_seconds_charged=0`.

PO-provider diagnostic run `32060462596` / job `95480351954` verified bgutil provider, yt-dlp 2026.07.04 and Node EJS runtime were correctly wired. Server-side cloud/datacenter YouTube ingestion is closed as the current beta acceptance architecture.

## Approved A4.2 captions-first architecture

```text
YouTube URL
 -> beta GPT Action creates KRCC_ job
 -> AWAITING_CLIENT
 -> Helper 0.2.0 on same YouTube tab
 -> Use subtitles first
    -> browser caption track + timestamps
    -> browser-only /captions upload
    -> backend validation
    -> COMPLETED / youtube_captions / STT=0
 -> captions unavailable/unusable
    -> Audio fallback
    -> tabCapture via tester browser/network path
    -> backend normalization/duration/quota validation
    -> AssemblyAI async STT
 -> timestamped transcript
 -> claim inventory
 -> CriticProfile
 -> user approval
 -> independent Research / Critic
```

The caption transcript is source content only, not independent corroboration of the video's claims.

## Current VoiceBridge implementation

Current feature/deployed commit:
`92f809440098fd42eb562a36c6feddeaa9c17155`

Captions-first CI:
- run `32069122559`: SUCCESS;
- cloud build/tests PASS;
- browser/helper JS and manifest validation PASS;
- Helper 0.2.0 package PASS;
- repository docs PASS.

Current browser-only routes:
```text
POST /api/v1/media/client-transcriptions/{KRCC_job_id}/captions
POST /api/v1/media/client-transcriptions/{KRCC_job_id}/audio
GET  /api/v1/media/client-transcriptions/{KRCC_job_id}/client-status
```

Action-facing routes remain unchanged and do not expose browser upload endpoints.

Caption completion semantics:
```text
status=COMPLETED
transcript_source=youtube_captions
caption_type=manual|auto_generated
provider=youtube
stt_seconds_charged=0
provider_data_deleted=null
```

Audio fallback semantics remain:
```text
transcript_source=assemblyai_stt
provider=assemblyai
stt_seconds_charged=<captured duration reservation>
provider_data_deleted=true|false
```

## Live Render state

Captions-first deployment:
- workflow run `32069270467`: SUCCESS;
- deploy ID `dep-da1nf76gekts738dst5g`;
- exact commit `92f809440098fd42eb562a36c6feddeaa9c17155` reached `live`;
- health HTTP 200;
- service `status=ok`;
- `media_client_ingest.mode=client_assisted`;
- `configured=true`;
- `requires_browser_helper=true`.

Production VoiceBridge was not targeted.

## Previous browser/audio evidence

Previous owner job:
`KRCC_aa3b2cbc-4d4e-4f89-b6e6-4549766f34f5`.

Helper 0.1.0 installation, active-tab capture and backend upload were proven. The job then failed with `MEDIA_DURATION_UNKNOWN` because streaming WebM/Opus lacked reliable container duration metadata.

That backend issue was fixed in commit `772901a167611f0197d1bc05cea8091da211dc47` by normalizing first and probing duration afterward. The fix is included in the current captions-first commit. The old failed job must not be reused.

## Helper 0.2.0

New user flow:
- install/reload Helper 0.2.0;
- enter a fresh KRCC job and tester code;
- press `Use subtitles` first;
- only use `Audio fallback` when captions are reported unavailable/unusable.

Caption extraction relies on best-effort access to YouTube player caption metadata inside the open browser tab. These YouTube internals are not a stable public API, so failure is expected to degrade to audio fallback rather than terminate the media architecture.

## KRC beta contract

Action schema advanced to `0.3.0-beta` and recognizes:
- `youtube_captions`;
- `assemblyai_stt`;
- `caption_type=manual|auto_generated`;
- `provider=youtube|assemblyai`.

Media beta manifest advanced to `0.3-beta` with client captions-first marked implemented pending live browser acceptance.

The three GPT Action operations remain:
- `startMediaBetaClientTranscription`;
- `getMediaBetaClientTranscriptionStatus`;
- `getMediaBetaClientTranscriptSegments`.

## Beta resource/security baseline

- owner + up to 3 testers;
- 60-minute source/capture limit;
- concurrency 1;
- captions path consumes 0 AssemblyAI seconds;
- AssemblyAI fallback budget 7200 sec/UTC day;
- audio helper upload max 32 MiB;
- no personal YouTube cookies;
- no paid residential proxy;
- browser helper never receives Action bearer secret or AssemblyAI key;
- plaintext tester code excluded from backend job state; temporary SHA-256 digest enforces ownership;
- full transcript and tester code excluded from KRC checkpoint.

## Exact next task

1. Install/reload `KRC MEDIA BETA Helper 0.2.0`.
2. Create a NEW KRCC job for the acceptance URL.
3. Verify pre-helper state: `AWAITING_CLIENT`, `client_upload_required=true`, `stt_seconds_charged=0`.
4. Open the same YouTube video and press `Use subtitles`.
5. Require:
   - `COMPLETED`;
   - `transcript_source=youtube_captions`;
   - manual/auto-generated caption type;
   - non-empty timestamped segments;
   - detected/source language;
   - `stt_seconds_charged=0`;
   - unchanged STT quota.
6. Only if captions fail, test `Audio fallback` and require AssemblyAI completion plus cleanup evidence.

## Do-not-do list

Do not merge PR #8/#28 automatically, modify public GPT/production VoiceBridge, expose credentials/tester codes, use personal YouTube cookies, add paid proxy infrastructure, claim captions-first browser acceptance before evidence, or bypass CriticProfile approval.

## Terminal markers

`MEDIA_BETA_HANDOFF_V1_7`

`A4_2_CAPTIONS_FIRST_RENDER_LIVE`

`HELPER_0_2_OWNER_ACCEPTANCE_NEXT`

`PRODUCTION_ISOLATED_DRAFT_PRS_UNMERGED`
