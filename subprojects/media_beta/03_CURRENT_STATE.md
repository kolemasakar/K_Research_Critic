# MEDIA BETA Current State
Канонічний знімок фактичного стану реалізації для відновлення роботи без припущень.

Version: 2.3
Status: ACTIVE_CHECKPOINT
Checkpoint date: 2026-08-18

## Executive state

Current phase: `A4 - Live transcript validation`

Current state:

`A3_COMPLETE / A4_1_SERVER_INGRESS_BLOCKED / A4_2_CAPTIONS_FIRST_OWNER_ACCEPTANCE_PASS / GPT_STATUS_READBACK_PASS / SEGMENT_PAGINATION_227_OF_227_PASS / A4_3_AUDIO_FALLBACK_OWNER_ACCEPTANCE_PASS / ASSEMBLYAI_CLEANUP_PASS / AUDIO_GPT_STATUS_READBACK_PASS / AUDIO_GPT_SEGMENT_READBACK_PASS`

The approved MEDIA BETA architecture is captions-first browser-assisted YouTube ingestion. Direct Render/datacenter YouTube acquisition remains unsuitable because of YouTube anti-bot enforcement. The browser helper now uses the tester browser path, prefers YouTube captions, and uses browser audio plus AssemblyAI only as fallback.

Production VoiceBridge and the published K-Research & Critic GPT remain unchanged. PR #8 and PR #28 remain draft and unmerged.

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

Verified controls:
- Render plan: free;
- max duration: 3600 sec;
- max concurrent jobs: 1;
- AssemblyAI fallback budget: 7200 sec per UTC day;
- language hints: auto/uk/ru/en;
- browser helper required for client-assisted ingestion.

## A4.1 server-side conclusion

Acceptance URL:
`https://www.youtube.com/watch?v=DZLzmQ2kwaA`

Three server-side attempts failed before transcript acquisition with YouTube `Sign in to confirm you're not a bot`:
- `KRCB_1c137194-3b23-4ed9-ab1e-fa5a49255cc9`;
- `KRCB_03d37ccd-4059-4b0c-9675-6f2568d4c207`;
- `KRCB_981465dc-e400-470f-a236-c5414c26bd63`.

All charged 0 STT seconds. Diagnostic run `32060462596`, job `95480351954`, confirmed PO-provider/runtime wiring. Repeated server-side cloud-ingress retries are not an approved beta path.

## Approved A4.2/A4.3 flow

```text
YouTube URL
 -> KRC MEDIA BETA Action creates KRCC_ job
 -> AWAITING_CLIENT
 -> KRC MEDIA BETA Helper in tester Chrome/Edge
 -> try direct YouTube caption track
 -> if direct timed-text is unusable, use YouTube transcript-panel fallback
 -> if timestamped captions are obtained:
      POST browser-only /captions
      COMPLETED
      transcript_source=youtube_captions
      stt_seconds_charged=0
 -> otherwise or under an explicit controlled fallback test:
      Audio fallback
      tabCapture
      bounded ffmpeg normalization
      measured-duration quota reservation
      AssemblyAI async STT
      timestamped transcript
      provider delete request
 -> GPT reads status and paginated segments
 -> KRC claim inventory
 -> CriticProfile gate
 -> user approval
 -> independent Research / Critic
```

Transcript text is source content only. It is evidence of what the video represents as being said, not independent evidence that a claim is true.

## Browser helper

Current helper: `KRC MEDIA BETA Helper 0.2.2`.

Helper 0.2.2 includes:
- direct timed-text captions path;
- detection of empty/blocked direct caption responses;
- YouTube transcript-panel fallback;
- timestamped segment extraction from the panel;
- `Use subtitles` as the primary action;
- `Audio fallback` only when captions are unavailable/unusable, except controlled acceptance tests;
- immediate persistence of a newly entered Job ID;
- stale COMPLETED-state isolation so a prior job does not disable buttons for a new job;
- no Action bearer token or AssemblyAI key in the extension.

VoiceBridge helper packaging/validation for 0.2.2 passed on branch `agent/krc-media-transcript`.

## Live owner captions acceptance

Accepted job:
`KRCC_c4d0b996-9500-4a39-a47c-0a873049cfea`

Accepted result:

```text
status=COMPLETED
transcript_source=youtube_captions
caption_type=auto_generated
provider=youtube
detected_language=uk
duration_seconds=663
transcript_characters=8235
segment_count=227
stt_seconds_charged=0
beta_quota.used_seconds=0
error=null
```

The direct timed-text route did not provide usable data. Helper 0.2.1 successfully completed through the YouTube transcript-panel fallback.

## GPT-facing captions readback acceptance

The Action-facing status endpoint returned the same completed result.

Full segment pagination was accepted:

```text
cursor=0   -> next=50   count=50 indices=0..49
cursor=50  -> next=100  count=50 indices=50..99
cursor=100 -> next=150  count=50 indices=100..149
cursor=150 -> next=200  count=50 indices=150..199
cursor=200 -> next=null count=27 indices=200..226
```

Result:
- all 227/227 segments readable through the GPT-facing contract;
- cursor progression correct;
- final cursor null correct;
- no STT quota consumed.

Canonical acceptance record:
`subprojects/media_beta/10_A4_2_CAPTIONS_ACCEPTANCE.md`

## Live owner audio fallback acceptance

Accepted fresh job:
`KRCC_07774204-5a71-4b79-8129-f73cf4dc164d`

Accepted Helper 0.2.2 flow:

```text
AWAITING_CLIENT
 -> CAPTURING
 -> UPLOADING
 -> TRANSCRIBING
 -> COMPLETED
```

Final helper result:

```text
status=COMPLETED
detected_language=uk
segment_count=2
stt_seconds_charged=98
provider_cleanup=deleted
```

The Action-facing status readback confirmed:

```text
status=COMPLETED
client_upload_required=false
transcript_source=assemblyai_stt
provider=assemblyai
provider_model=universal-2
provider_data_deleted=true
detected_language=uk
language_confidence=0.7404
duration_seconds=97.056
transcript_characters=1141
segment_count=2
stt_seconds_charged=98
beta_quota.used_seconds=98
beta_quota.remaining_seconds=7102
error=null
```

The Action-facing segment readback confirmed:

```text
status=COMPLETED
cursor=0
next_cursor=null
segment_count=2
segment 0: index=0 start_ms=5347  end_ms=64032 confidence~=0.8694
segment 1: index=1 start_ms=64032 end_ms=96917 confidence~=0.8469
```

This live test confirms:
- active-tab audio capture works;
- browser upload works;
- WebM/Opus normalization and duration probing work;
- quota charging uses measured normalized capture duration;
- AssemblyAI async transcription reaches COMPLETED;
- provider transcript deletion succeeds and is visible through the GPT-facing contract;
- exact post-test daily quota is visible through the GPT-facing contract;
- all audio transcript segments are readable through the GPT-facing Action route;
- timestamps are ordered and final `next_cursor=null` is correct.

Two `U+FFFD` replacement-character artifacts were visible inside the returned STT text. This is recorded as a text-quality anomaly for later provider/pipeline investigation. It does not invalidate A4.3 transport, quota, cleanup, or Action-readback acceptance.

Canonical acceptance record:
`subprojects/media_beta/11_A4_3_AUDIO_FALLBACK_ACCEPTANCE.md`

## Render restart durability finding

A prior fresh audio job reached browser `UPLOADING` and then returned `MEDIA_TRANSCRIPT_NOT_FOUND` before the 3600-second configured TTL.

Client-assisted jobs are currently stored only in the backend process-memory `Map`. Render restart/spin cycles therefore lose `KRCC_...` state even when the logical job TTL has not expired.

This is now a known beta durability limitation, not an AssemblyAI/audio implementation failure.

Required hardening before broader rollout:
- persist KRCC job state outside process RAM, or
- replace the waiting-job dependency with a signed stateless upload ticket/session design.

Until hardened, live fallback tests should create a fresh KRCC job immediately before capture and avoid long idle gaps.

## Backend routes

Action-facing:
```text
POST /api/v1/media/client-transcriptions
GET  /api/v1/media/client-transcriptions/{KRCC_job_id}
GET  /api/v1/media/client-transcriptions/{KRCC_job_id}/segments
```

Browser-only:
```text
POST /api/v1/media/client-transcriptions/{KRCC_job_id}/captions
POST /api/v1/media/client-transcriptions/{KRCC_job_id}/audio
GET  /api/v1/media/client-transcriptions/{KRCC_job_id}/client-status
```

Browser-only routes remain intentionally absent from the GPT Action schema.

## Remaining A4 validation

A4.2 captions-first owner acceptance and A4.3 audio-fallback owner acceptance are both complete for the primary Ukrainian acceptance video.

Remaining A4/release gates:
- additional UK/RU/EN/auto cases;
- manual-caption classification case;
- >60 minute rejection;
- source mismatch rejection;
- concurrency rejection;
- quota exhaustion simulation;
- STT text-quality investigation for observed replacement-character artifacts;
- GPT Builder closed-beta end-to-end test;
- AssemblyAI model-training/no-training and privacy verification;
- hosted public privacy policy URL;
- Free-plan/paid runtime tests before public promotion;
- job-state durability across Render restart/spin-down.

## Known beta limitations

- YouTube caption interfaces are internal browser-page behavior and may change;
- direct timed-text may return empty data even when captions exist;
- transcript-panel fallback is therefore part of the accepted browser path;
- audio fallback still requires normal-speed playback for timestamp alignment;
- process-memory jobs/quota can reset on Render restart/redeploy/spin cycle;
- AssemblyAI STT returned two replacement-character text artifacts in the accepted sample; quality investigation remains open;
- AssemblyAI privacy/public-release checks are not yet closed.

Do not merge PR #8 or PR #28, modify the public GPT, add personal YouTube cookies, or introduce paid residential proxy ingress merely to continue A4 testing.
