# MEDIA BETA A4.5 Guard Matrix Acceptance
Живе підтвердження захисних перевірок closed MEDIA BETA для доступу, джерела, тривалості, конкурентності та квоти.

Version: 1.4
Status: PASS
Acceptance date: 2026-08-18

## Scope

A4.5 validates negative-path guards for the isolated closed MEDIA BETA without modifying production VoiceBridge or the published K-Research & Critic GPT.

Accepted matrix:
- invalid beta access code;
- browser source mismatch;
- source duration above 60 minutes;
- concurrent active-job rejection;
- daily STT quota exhaustion/rejection.

## Guard 1 - invalid beta access code

Live request used an intentionally invalid beta code against:

`POST /api/v1/media/client-transcriptions`

Observed:

```text
HTTP/1.1 403 Forbidden
error.code=MEDIA_BETA_ACCESS_DENIED
error.category=MEDIA
error.retryable=false
message=The closed media beta access code is invalid.
```

Result: PASS.

`A4_5_INVALID_BETA_CODE_PASS`

## Guard 2 - browser source mismatch

Waiting job:

`KRCC_03bda620-95c1-4ed1-9f4b-d24235363f02`

The job was created for YouTube video ID `DZLzmQ2kwaA`. A captions submission intentionally declared a different active source ID `dQw4w9WgXcQ`.

Observed:

```text
HTTP/1.1 409 Conflict
error.code=MEDIA_CLIENT_SOURCE_MISMATCH
error.category=MEDIA
error.retryable=false
message=The active browser tab does not match the YouTube URL for this job.
```

Result: PASS. Wrong-video content was rejected before acceptance.

`A4_5_SOURCE_MISMATCH_PASS`

## Guard 3 - concurrent active-job rejection

The source-mismatch job remained `AWAITING_CLIENT`. A second transcription request for another YouTube video was submitted while `max_concurrent_jobs=1`.

Observed:

```text
HTTP/1.1 429 Too Many Requests
error.code=MEDIA_TRANSCRIPT_BUSY
error.category=MEDIA
error.retryable=true
message=The closed media beta is processing another video.
```

Result: PASS.

`A4_5_CONCURRENCY_PASS`

## Guard 4 - source duration above 60 minutes

The same waiting job was used with the correct source. A synthetic caption segment ended at `3602000 ms` (60 minutes 2 seconds), above the configured 3600-second maximum.

Observed:

```text
HTTP/1.1 413 Payload Too Large
error.code=MEDIA_DURATION_LIMIT
error.category=MEDIA
error.retryable=false
message=Closed beta videos are limited to 3600 seconds.
```

Result: PASS. No STT quota was consumed.

`A4_5_OVER_60_MIN_PASS`

## Guard 5 - daily STT quota exhaustion

For this isolated negative-path test only, the beta service daily STT limit was temporarily changed from 7200 to 60 seconds and redeployed. Production was not targeted.

A locally generated 61-second MP3 was submitted to the same waiting job through the browser-only audio route.

Initial upload response:

```text
status=UPLOADING
stt_seconds_charged=0
beta_quota.daily_limit_seconds=60
beta_quota.used_seconds=0
beta_quota.remaining_seconds=60
```

Final Action-facing readback:

```text
job_id=KRCC_03bda620-95c1-4ed1-9f4b-d24235363f02
status=FAILED
media.duration_seconds=61.092
stt_seconds_charged=0
beta_quota.daily_limit_seconds=60
beta_quota.used_seconds=0
beta_quota.remaining_seconds=60
error.code=MEDIA_DAILY_STT_QUOTA_EXHAUSTED
error.retryable=true
message=The closed beta daily STT budget is exhausted.
```

Result: PASS. The quota guard rejected the request before AssemblyAI submission and no STT seconds were charged.

After acceptance, the isolated beta limit was restored to:

```text
MEDIA_DAILY_STT_SECONDS=7200
```

Restore workflow result:

```text
SUCCESS
commit=ab43973a1328c043c382f2e8ead81587964b9a46
production_not_targeted=true
```

`A4_5_QUOTA_EXHAUSTION_PASS`

## Acceptance conclusion

All five A4.5 live guards passed with the expected HTTP/error contracts and resource behavior.

Confirmed:
- invalid tester code is denied;
- wrong YouTube source is denied;
- over-60-minute content is denied;
- a second concurrent job is denied while one slot is active;
- exhausted daily STT capacity is denied before provider use;
- quota rejection charges zero STT seconds;
- normal 7200-second daily beta limit was restored after the test;
- production VoiceBridge was not targeted.

`A4_5_INVALID_BETA_CODE_PASS`

`A4_5_SOURCE_MISMATCH_PASS`

`A4_5_CONCURRENCY_PASS`

`A4_5_OVER_60_MIN_PASS`

`A4_5_QUOTA_EXHAUSTION_PASS`

`A4_5_GUARD_MATRIX_PASS`
