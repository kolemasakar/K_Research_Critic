# MEDIA BETA Current State
Канонічний знімок фактичного стану реалізації для відновлення роботи без припущень.

Version: 2.9
Status: ACTIVE_CHECKPOINT
Checkpoint date: 2026-08-18

## Executive state

Current phase: `A4 - Live transcript validation`

Current state:

`A3_COMPLETE / A4_1_SERVER_INGRESS_BLOCKED / A4_2_CAPTIONS_FIRST_OWNER_ACCEPTANCE_PASS / GPT_STATUS_READBACK_PASS / SEGMENT_PAGINATION_227_OF_227_PASS / A4_3_AUDIO_FALLBACK_OWNER_ACCEPTANCE_PASS / ASSEMBLYAI_CLEANUP_PASS / AUDIO_GPT_STATUS_READBACK_PASS / AUDIO_GPT_SEGMENT_READBACK_PASS / A4_4_RESTART_DURABILITY_PASS / CREATED_AT_CONTINUITY_PASS / A4_5_GUARD_MATRIX_PASS / A4_RU_CAPTIONS_PASS / A4_LARGE_CAPTION_PAYLOAD_PERSISTENCE_DEFECT_CLOSED / A4_EN_CAPTIONS_PASS / A4_MANUAL_CAPTIONS_CLASSIFICATION_PASS / A4_AUTO_LANGUAGE_IT_PASS / A4_LANGUAGE_SOURCE_MATRIX_PASS / A4_DURABLE_QUOTA_LEDGER_RESTART_PASS`

The approved MEDIA BETA architecture is captions-first browser-assisted YouTube ingestion. Direct Render/datacenter YouTube acquisition remains unsuitable because of YouTube anti-bot enforcement. The browser helper uses the tester browser path, prefers YouTube captions, and uses browser audio plus AssemblyAI only as fallback.

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
- browser helper required for client-assisted ingestion;
- durable store: Postgres;
- waiting jobs survive beta process replacement;
- STT charge ledger is durable and live restart restoration after a real charge is accepted.

The temporary A4.5 quota-test limit of 60 sec/day was restored to the normal 7200 sec/day after acceptance. Restore commit: `ab43973a1328c043c382f2e8ead81587964b9a46`.

## A4.1 server-side conclusion

Acceptance URL:
`https://www.youtube.com/watch?v=DZLzmQ2kwaA`

Repeated server-side YouTube acquisition from Render failed with `Sign in to confirm you're not a bot` despite working PO-provider/runtime wiring. This path is not approved for the closed beta.

Approved ingress is browser-assisted.

## Approved media flow

```text
YouTube URL
 -> KRC MEDIA BETA Action creates KRCC_ job
 -> durable AWAITING_CLIENT
 -> KRC MEDIA BETA Helper in tester Chrome/Edge
 -> captions first
      direct timed-text if usable
      otherwise YouTube transcript-panel fallback
 -> if captions obtained:
      POST /captions
      COMPLETED
      transcript_source=youtube_captions
      stt_seconds_charged=0
 -> otherwise or controlled fallback test:
      Audio fallback
      active-tab capture
      WebM/Opus upload
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

Transcript text is evidence of what the video represents as being said, not independent evidence that the claims are true.

## Browser helper

Current helper: `KRC MEDIA BETA Helper 0.2.2`.

Accepted helper functions:
- direct timed-text captions attempt;
- empty/blocked caption response detection;
- YouTube transcript-panel fallback;
- timestamped segment extraction;
- `Use subtitles` primary path;
- `Audio fallback` secondary path;
- immediate persistence of changed Job ID;
- stale terminal-state isolation;
- no Action bearer token or AssemblyAI key stored in the extension.

## A4.2 captions-first owner acceptance

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
error=null
```

Full Action-facing pagination accepted:

```text
0..49
50..99
100..149
150..199
200..226
next_cursor=null
```

All 227/227 segments were readable with zero STT cost.

Canonical record:
`subprojects/media_beta/10_A4_2_CAPTIONS_ACCEPTANCE.md`

## A4.3 audio fallback owner acceptance

Accepted job:
`KRCC_07774204-5a71-4b79-8129-f73cf4dc164d`

Accepted flow:

```text
AWAITING_CLIENT
 -> CAPTURING
 -> UPLOADING
 -> TRANSCRIBING
 -> COMPLETED
```

Action-facing result:

```text
status=COMPLETED
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
error=null
```

The two returned segments were readable with ordered timestamps and final `next_cursor=null`.

Two `U+FFFD` replacement-character artifacts were observed in STT text. This remains a text-quality issue but does not invalidate transport, quota, cleanup, or Action-readback acceptance.

Canonical record:
`subprojects/media_beta/11_A4_3_AUDIO_FALLBACK_ACCEPTANCE.md`

## A4.4 restart durability acceptance

The beta backend was hardened with a durable Postgres job store and durable STT charge ledger after the earlier RAM-only implementation lost a waiting job during process replacement.

Verified health state:

```text
durable_store=postgres
restart_resilient_waiting_jobs=true
durable_quota_ledger=true
```

Accepted behavior:
- `AWAITING_CLIENT` job survives intentional beta redeploy/restart;
- same external `KRCC_...` remains readable through Action API;
- same Job ID can be resumed by Helper 0.2.2 after restart;
- resumed captions job reaches `COMPLETED` with 227 segments and zero STT cost;
- completed durable job remains readable after later process replacement;
- original `created_at` remains immutable across restart, resume and completion;
- real AssemblyAI STT charge survives restart and is restored into the active runtime quota gate.

Final created_at regression job:
`KRCC_cad52723-cbf0-4bd6-b195-44902d11bc6b`

```text
created_at BEFORE restart  = 2026-08-18T03:38:41.045Z
created_at AFTER COMPLETED = 2026-08-18T03:38:41.045Z
status=COMPLETED
transcript_source=youtube_captions
segment_count=227
stt_seconds_charged=0
error=null
```

Canonical job-state record:
`subprojects/media_beta/12_A4_4_DURABILITY_ACCEPTANCE.md`

## A4.5 guard matrix acceptance

All five live negative-path guards passed.

Accepted contracts:

```text
invalid beta code:
HTTP 403
MEDIA_BETA_ACCESS_DENIED
retryable=false

source mismatch:
HTTP 409
MEDIA_CLIENT_SOURCE_MISMATCH
retryable=false

concurrency=1:
HTTP 429
MEDIA_TRANSCRIPT_BUSY
retryable=true

>60 min:
HTTP 413
MEDIA_DURATION_LIMIT
retryable=false

STT quota exhaustion:
status=FAILED
MEDIA_DAILY_STT_QUOTA_EXHAUSTED
retryable=true
stt_seconds_charged=0
```

Quota test used a temporary isolated-beta limit of 60 sec/day and a 61.092-second synthetic audio file. Rejection occurred before AssemblyAI use. The configured daily limit was then restored to 7200 sec/day with a successful isolated redeploy. Production was not targeted.

Canonical record:
`subprojects/media_beta/13_A4_5_GUARD_MATRIX_ACCEPTANCE.md`

## A4 language/source matrix

Status: PASS.

Accepted cases:

```text
UK auto_generated captions   PASS
RU auto_generated captions   PASS
EN manual captions           PASS
manual classification        PASS
auto -> IT manual captions   PASS
```

Russian case:
- source `https://www.youtube.com/watch?v=j_R7sBXyRyE`;
- job `KRCC_eabd86f0-5205-4311-b063-2bb04d4fe1c5`;
- `detected_language=ru`;
- `caption_type=auto_generated`;
- 524 segments / 19206 characters;
- STT charge zero.

The Russian payload exposed the large-argument durable persistence defect. VoiceBridge commit `8962a323abd2d549ad372c51a054f9f5371e9ada` changed SQL transport to stdin. Validation and isolated deployment passed, and the same job then completed durably.

English/manual case:
- source `https://www.youtube.com/watch?v=eIho2S0ZahI`;
- job `KRCC_cbd47a08-2ea6-4097-961d-c6993107579b`;
- `detected_language=en`;
- `caption_type=manual`;
- 247 segments / 8872 characters;
- STT charge zero.

Italian auto-selection case:
- source `https://www.youtube.com/watch?v=lLxb3lYI3lI`;
- job `KRCC_99ef05c6-da65-4190-ae9f-db3e1cff07ab`;
- `language_hint=auto`;
- `detected_language=it`;
- `caption_type=manual`;
- duration 465 sec;
- 74 segments / 5269 characters;
- STT charge zero;
- original `created_at=2026-08-18T05:11:36.054Z` preserved.

Acceptance markers:

```text
A4_RU_CAPTIONS_PASS
A4_LARGE_CAPTION_PAYLOAD_PERSISTENCE_DEFECT_CLOSED
A4_EN_CAPTIONS_PASS
A4_MANUAL_CAPTIONS_CLASSIFICATION_PASS
A4_AUTO_LANGUAGE_IT_PASS
A4_LANGUAGE_SOURCE_MATRIX_PASS
```

Canonical record:
`subprojects/media_beta/14_A4_LANGUAGE_SOURCE_MATRIX_ACCEPTANCE.md`

## A4 durable quota-ledger restart

Status: PASS.

Charged audio job before restart:
`KRCC_493fcc82-adea-4de2-aee3-a671c0c54073`

```text
status=COMPLETED
transcript_source=assemblyai_stt
provider=assemblyai
provider_data_deleted=true
duration_seconds=56.376
stt_seconds_charged=57
beta_quota.used_seconds=57
beta_quota.remaining_seconds=7143
```

Controlled isolated restart/deploy commit:
`beebe6a638637e5d4d81a13826371810048d1407`

After restart the same charged job remained durable with `stt_seconds_charged=57` and quota snapshot 57/7143.

Fresh post-restart job:
`KRCC_adc4c232-d2df-4382-8bbd-72d7736142ac`

```text
status=AWAITING_CLIENT
language_hint=auto
beta_quota.daily_limit_seconds=7200
beta_quota.used_seconds=57
beta_quota.remaining_seconds=7143
```

The fresh job proves the restarted runtime restored the durable daily charge from Postgres into `MediaBetaGate`.

Acceptance marker:
`A4_DURABLE_QUOTA_LEDGER_RESTART_PASS`

Canonical record:
`subprojects/media_beta/15_A4_QUOTA_LEDGER_RESTART_ACCEPTANCE.md`

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

## Next A4 validation block

Captions language/source validation and durable quota-ledger restart validation are complete. Remaining A4 validation before A5:
- audio fallback process-replacement behavior during active upload/transcription;
- STT replacement-character investigation.

The fresh waiting job `KRCC_adc4c232-d2df-4382-8bbd-72d7736142ac` is available for the next isolated active-audio restart test unless it expires first.

Release gates that follow/overlap later phases:
- GPT Builder closed-beta end-to-end test;
- AssemblyAI privacy/no-training verification;
- hosted public privacy policy URL;
- Free-plan/paid runtime tests before public promotion;
- Free Postgres lifecycle/expiry management and future migration.

## Known beta limitations

- YouTube browser caption interfaces may change;
- direct timed-text may return empty data even when captions exist;
- transcript-panel fallback is part of the accepted browser path;
- audio fallback requires real-time/normal-speed playback for timestamp alignment;
- Free Postgres is temporary beta infrastructure and needs lifecycle management;
- AssemblyAI STT text-quality anomaly with replacement characters remains open;
- AssemblyAI privacy/public-release checks remain open.

Do not merge PR #8 or PR #28, modify the public GPT, add personal YouTube cookies, or introduce paid residential proxy ingress merely to continue A4 testing.
