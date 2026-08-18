# MEDIA BETA A4.5 Guard Matrix Acceptance
Живе підтвердження захисних перевірок closed MEDIA BETA для доступу, джерела, тривалості, конкурентності та квоти.

Version: 1.1
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

## Remaining guards

Pending:
- `A4_5_OVER_60_MIN_PENDING`
- `A4_5_CONCURRENCY_PENDING`
- `A4_5_QUOTA_EXHAUSTION_PENDING`
