# MEDIA BETA Current State
Канонічний знімок фактичного стану реалізації для відновлення роботи без припущень.

Version: 3.0
Status: ACTIVE_CHECKPOINT
Checkpoint date: 2026-08-20

## Executive state

Current phase state:

`A4_COMPLETE / A5_READY`

Accepted A4 markers:

`A4_1_SERVER_INGRESS_BLOCKED / A4_2_CAPTIONS_FIRST_OWNER_ACCEPTANCE_PASS / GPT_STATUS_READBACK_PASS / SEGMENT_PAGINATION_227_OF_227_PASS / A4_3_AUDIO_FALLBACK_OWNER_ACCEPTANCE_PASS / ASSEMBLYAI_CLEANUP_PASS / AUDIO_GPT_STATUS_READBACK_PASS / AUDIO_GPT_SEGMENT_READBACK_PASS / A4_4_RESTART_DURABILITY_PASS / CREATED_AT_CONTINUITY_PASS / A4_5_GUARD_MATRIX_PASS / A4_RU_CAPTIONS_PASS / A4_LARGE_CAPTION_PAYLOAD_PERSISTENCE_DEFECT_CLOSED / A4_EN_CAPTIONS_PASS / A4_MANUAL_CAPTIONS_CLASSIFICATION_PASS / A4_AUTO_LANGUAGE_IT_PASS / A4_LANGUAGE_SOURCE_MATRIX_PASS / A4_DURABLE_QUOTA_LEDGER_RESTART_PASS / A4_ACTIVE_AUDIO_FORCED_PROCESS_LOSS_PASS / A4_ACTIVE_AUDIO_RETRY_SAFE_FAILURE_PASS / A4_STT_TEXT_QUALITY_DISPOSITION_PASS`

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
- waiting/completed job state survives required process-replacement checks;
- STT charge ledger is durable and restored after runtime restart.

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
      provider delete request on normal completion
 -> GPT reads status and paginated segments
 -> KRC claim inventory
 -> CriticProfile gate
 -> user approval
 -> independent Research / Critic
```

Transcript text is evidence of what the video represents as being said, not independent evidence that the claims are true.

## Browser helper

Current helper:
`KRC MEDIA BETA Helper 0.2.2`

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

## A4 accepted evidence

### Captions-first

Ukrainian auto-generated captions:
- 227/227 Action-facing segments;
- zero STT charge.

Russian auto-generated captions:
- 524 segments / 19206 characters;
- zero STT charge.

English manual captions:
- 247 segments / 8872 characters;
- zero STT charge.

Italian AUTO-selection:
- `language_hint=auto`;
- `detected_language=it`;
- manual track selected;
- 74 segments / 5269 characters;
- zero STT charge.

The large Russian captions case exposed a durable SQL transport boundary that was fixed by moving SQL payload transport to stdin and then live-validated.

Canonical records:
- `subprojects/media_beta/10_A4_2_CAPTIONS_ACCEPTANCE.md`;
- `subprojects/media_beta/14_A4_LANGUAGE_SOURCE_MATRIX_ACCEPTANCE.md`.

### Audio fallback

Primary A4.3 accepted flow:

```text
AWAITING_CLIENT
 -> CAPTURING
 -> UPLOADING
 -> TRANSCRIBING
 -> COMPLETED
```

Accepted properties:
- active-tab WebM/Opus capture;
- bounded ffmpeg normalization;
- measured duration and quota charging;
- AssemblyAI `universal-2` transcription;
- timestamped segments;
- Action-facing status and segment readback;
- provider transcript DELETE confirmed on normal successful completion.

Canonical record:
`subprojects/media_beta/11_A4_3_AUDIO_FALLBACK_ACCEPTANCE.md`

### Guard matrix

Accepted live contracts:

```text
invalid beta code:
HTTP 403 / MEDIA_BETA_ACCESS_DENIED / retryable=false

source mismatch:
HTTP 409 / MEDIA_CLIENT_SOURCE_MISMATCH / retryable=false

concurrency=1:
HTTP 429 / MEDIA_TRANSCRIPT_BUSY / retryable=true

>60 min:
HTTP 413 / MEDIA_DURATION_LIMIT / retryable=false

STT quota exhaustion:
MEDIA_DAILY_STT_QUOTA_EXHAUSTED
retryable=true
stt_seconds_charged=0
```

Canonical record:
`subprojects/media_beta/13_A4_5_GUARD_MATRIX_ACCEPTANCE.md`

### Restart durability and quota ledger

Accepted:
- `AWAITING_CLIENT` survives isolated process replacement;
- same external Job ID can resume through Helper;
- completed durable state remains readable;
- original `created_at` remains immutable;
- real STT charge survives restart and restores into runtime quota accounting.

Canonical records:
- `subprojects/media_beta/12_A4_4_DURABILITY_ACCEPTANCE.md`;
- `subprojects/media_beta/15_A4_QUOTA_LEDGER_RESTART_ACCEPTANCE.md`.

### Active-audio forced process loss

Accepted job:
`KRCC_8da975c7-e338-4d02-8783-3b30d7071dce`

The final deterministic test used a local watcher to detect `TRANSCRIBING` and immediately call the Render API suspend endpoint. Render returned HTTP 202, Helper observed HTTP 503 while the beta backend was unavailable, the service was resumed with HTTP 202, and the same Job ID was read back after health returned.

Final durable result:

```text
status=FAILED
error.code=MEDIA_CLIENT_INTERRUPTED_RETRY_REQUIRED
error.retryable=true
client_upload_required=false
duration_seconds=249.444
stt_seconds_charged=250
segment_count=0
transcript_characters=0
```

Quota evidence:

```text
used before=172
used after=422
delta=250
ceil(249.444)=250
```

No duplicate STT charge appeared after resume/readback.

Canonical record:
`subprojects/media_beta/16_A4_ACTIVE_AUDIO_PROCESS_REPLACEMENT_ACCEPTANCE.md`

Residual release-hardening note:
`provider_data_deleted=null` after forced process death because the killed runtime cannot record a provider-delete result. This does not reopen retry-safety acceptance; orphan-provider cleanup after hard process loss remains separate release hardening.

### STT replacement-character disposition

The original A4.3 sample recorded two `U+FFFD` replacement-character artifacts.

Two fresh successful AssemblyAI control jobs were later scanned through the Action-facing segments route:

```text
KRCC_62dedd79-a1db-4e4d-84b8-e28ad44a6a78: segments=2, U+FFFD=0
KRCC_8b256d21-f190-4b45-a59a-8d092e0fbb43: segments=2, U+FFFD=0
```

The original A4.3 job had expired by the time of re-check and returned `MEDIA_TRANSCRIPT_NOT_FOUND`; therefore the historical raw provider payload cannot be re-inspected and root cause cannot be conclusively attributed.

Disposition:

`NON_REPRODUCIBLE QUALITY ANOMALY / NOT AN A4 BLOCKER`

No deterministic current VoiceBridge transport/segmentation/persistence encoding defect is supported by the available evidence. Continue monitoring during closed beta.

Canonical record:
`subprojects/media_beta/17_A4_STT_TEXT_QUALITY_DISPOSITION.md`

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

## A4 exit

Status: PASS / COMPLETE.

All defined A4 exit criteria are satisfied:
- captions-first browser jobs are usable across required language/source cases;
- audio fallback is live-validated;
- language/source metadata is usable;
- quota accounting is correct and durable across required restart checks;
- active-audio process replacement has deterministic retry-safe behavior;
- normal AssemblyAI completion cleanup is verified;
- STT replacement-character anomaly is investigated and dispositioned;
- acceptance records contain no beta/developer secret values.

## Next phase

A5 - Separate GPT Builder beta.

Status:
`READY`

Next implementation block:
- create `K-Research & Critic - MEDIA BETA` separately from the public GPT;
- import beta instructions and the client-assisted OpenAPI Action schema;
- configure Action bearer secret;
- point the Action to the dedicated beta Render endpoint;
- configure a hosted privacy policy URL;
- keep the public GPT unchanged.

## Release-hardening items after/alongside A5-A7

- AssemblyAI privacy/no-training verification;
- orphan-provider cleanup strategy after hard process loss;
- hosted public privacy policy URL;
- Free-plan/paid runtime compatibility tests before public promotion;
- Free Postgres lifecycle/expiry management and future migration;
- continued monitoring for recurrent STT text-quality artifacts.

## Known beta limitations

- YouTube browser caption interfaces may change;
- direct timed-text may return empty data even when captions exist;
- transcript-panel fallback is part of the accepted browser path;
- audio fallback requires real-time/normal-speed playback for timestamp alignment;
- Free Postgres is temporary beta infrastructure and needs lifecycle management;
- hard process death can leave provider cleanup state unconfirmed;
- AssemblyAI remains a finite-credit beta fallback and is not the intended mandatory sustainable public free dependency.

Do not merge PR #8 or PR #28, modify the public GPT, add personal YouTube cookies, or introduce paid residential proxy ingress merely to continue the beta.
