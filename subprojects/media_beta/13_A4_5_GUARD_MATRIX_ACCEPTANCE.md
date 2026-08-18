# MEDIA BETA A4.5 Guard Matrix Acceptance
Живе підтвердження захисних перевірок closed MEDIA BETA для доступу, джерела, тривалості, конкурентності та квоти.

Version: 1.3
Status: IN_PROGRESS
Acceptance date: 2026-08-18

## Scope

A4.5 validates negative-path guards for the isolated closed MEDIA BETA without modifying production VoiceBridge or the published K-Research & Critic GPT.

Target matrix:
- invalid beta access code;
- browser source mismatch;
- source duration above 60 minutes;
- concurrent active-job rejection;
- daily STT quota exhaustion/rejection.

## Guard 1 - invalid beta access code

Live request used an intentionally invalid beta code against:

`POST /api/v1/media/client-transcriptions`

Observed HTTP response:

```text
HTTP/1.1 403 Forbidden
```

Observed error contract:

```text
error.code=MEDIA_BETA_ACCESS_DENIED
error.category=MEDIA
error.retryable=false
message=The closed media beta access code is invalid.
```

Result: PASS.

`A4_5_INVALID_BETA_CODE_PASS`

## Guard 2 - browser source mismatch

A fresh waiting job was created for YouTube video ID `DZLzmQ2kwaA`:

`KRCC_03bda620-95c1-4ed1-9f4b-d24235363f02`

A browser-only captions submission then intentionally declared a different active YouTube source ID `dQw4w9WgXcQ`.

Observed HTTP response:

```text
HTTP/1.1 409 Conflict
```

Observed error contract:

```text
error.code=MEDIA_CLIENT_SOURCE_MISMATCH
error.category=MEDIA
error.retryable=false
message=The active browser tab does not match the YouTube URL for this job.
```

Result: PASS. The captions payload was rejected before source content could be accepted for the wrong video.

`A4_5_SOURCE_MISMATCH_PASS`

## Guard 3 - concurrent active-job rejection

The source-mismatch test job remained active in `AWAITING_CLIENT`. A second client-transcription request for a different YouTube video was submitted while `max_concurrent_jobs=1`.

Observed HTTP response:

```text
HTTP/1.1 429 Too Many Requests
```

Observed error contract:

```text
error.code=MEDIA_TRANSCRIPT_BUSY
error.category=MEDIA
error.retryable=true
message=The closed media beta is processing another video.
```

Result: PASS. The isolated beta rejected a second active job while one waiting job already occupied the single concurrency slot.

`A4_5_CONCURRENCY_PASS`

## Guard 4 - source duration above 60 minutes

The same waiting job was used with the correct YouTube source. A synthetic caption segment ended at `3602000 ms` (60 minutes 2 seconds), exceeding the configured `3600` second maximum.

Observed HTTP response:

```text
HTTP/1.1 413 Payload Too Large
```

Observed error contract:

```text
error.code=MEDIA_DURATION_LIMIT
error.category=MEDIA
error.retryable=false
message=Closed beta videos are limited to 3600 seconds.
```

Result: PASS. The request was rejected before transcript completion and consumed no STT quota.

`A4_5_OVER_60_MIN_PASS`

## Remaining guards

Pending:
- `A4_5_QUOTA_EXHAUSTION_PENDING`
