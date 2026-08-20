# MEDIA BETA A4 Active-Audio Process-Replacement Acceptance
Живе підтвердження retry-safe поведінки client-assisted audio job при фактичній втраті beta web-process під час `TRANSCRIBING`.

Version: 1.0
Status: PASS
Acceptance date: 2026-08-20

## Scope

This acceptance closes the remaining A4 active-audio process-replacement boundary. The objective was to prove that a real beta backend process loss during active AssemblyAI transcription does not leave a durable KRCC job stuck in `TRANSCRIBING`, does not silently resume the interrupted browser operation, and returns an explicit retry-safe terminal state after the backend is restored.

Production VoiceBridge, `main`, and the published K-Research & Critic GPT were not modified.

## Why normal restart attempts were insufficient

Multiple earlier attempts using normal Render restart/redeploy completed the active transcription before the old process disappeared. Those attempts were therefore recorded as inconclusive for forced process loss.

The final test used the isolated beta service only and removed human timing from the critical boundary:
- a local watcher polled the Action-facing job once per second;
- when the job first became `TRANSCRIBING`, the watcher immediately called the Render API suspend endpoint;
- Render accepted the suspend request with HTTP 202;
- the Helper then observed HTTP 503 while the service was actually unavailable;
- the service was resumed through the Render API;
- the same external KRCC Job ID was read back after health returned.

## Accepted job

`KRCC_8da975c7-e338-4d02-8783-3b30d7071dce`

Source:
`https://youtu.be/DZLzmQ2kwaA?si=active-audio-api-suspend-retry2-20260820`

Initial durable state:

```text
status=AWAITING_CLIENT
created_at=2026-08-20T10:37:49.820Z
reused=false
beta_quota.used_seconds=172
beta_quota.remaining_seconds=7028
```

Captured audio duration after upload/normalization:

```text
duration_seconds=249.444
stt_seconds_charged=250
provider=assemblyai
provider_model=universal-2
```

## Forced process-loss evidence

Observed live sequence:

```text
CAPTURING
 -> TRANSCRIBING
 -> watcher detects TRANSCRIBING
 -> POST Render suspend
 -> HTTP 202
 -> beta backend unavailable
 -> Helper HTTP 503
 -> POST Render resume
 -> HTTP 202
 -> health status=ok
 -> same KRCC job Action readback
```

This is materially different from the earlier normal restart attempts because the isolated beta backend became unavailable before transcription could complete.

## Final durable readback

After resume, the same external Job ID returned:

```text
job_id=KRCC_8da975c7-e338-4d02-8783-3b30d7071dce
status=FAILED
error.code=MEDIA_CLIENT_INTERRUPTED_RETRY_REQUIRED
error.retryable=true
client_upload_required=false
provider=assemblyai
provider_model=universal-2
duration_seconds=249.444
stt_seconds_charged=250
segment_count=0
transcript_characters=0
provider_data_deleted=null
```

Error message:

```text
The browser media operation was interrupted by a backend restart. Create a fresh KRCC job and retry.
```

## Quota accounting

Before the accepted job:

```text
beta_quota.used_seconds=172
```

After durable failure readback:

```text
beta_quota.used_seconds=422
```

Delta:

```text
422 - 172 = 250 seconds
```

This exactly matches:

```text
ceil(249.444) = 250
```

No duplicate STT charge appeared after service resume/readback.

## Acceptance conclusion

Status: PASS.

Confirmed:
- actual beta service unavailability occurred while the job was active;
- durable job state did not remain stuck in `TRANSCRIBING`;
- the same external Job ID remained readable after resume;
- the interrupted job became explicit terminal `FAILED`;
- failure code is `MEDIA_CLIENT_INTERRUPTED_RETRY_REQUIRED`;
- `retryable=true`;
- the user must create a fresh KRCC job instead of resuming the interrupted browser operation;
- STT charge remained exactly one measured reservation of 250 seconds;
- no duplicate quota charge appeared after restart recovery;
- production was not targeted.

## Residual provider-cleanup note

`provider_data_deleted=null` after forced process death because the killed runtime did not survive long enough to record a provider-delete result. This does not invalidate process-replacement retry-safety acceptance, but provider-side orphan cleanup after hard process loss remains a separate release-hardening concern.

Acceptance markers:

`A4_ACTIVE_AUDIO_FORCED_PROCESS_LOSS_PASS`

`A4_ACTIVE_AUDIO_RETRY_SAFE_FAILURE_PASS`

`A4_ACTIVE_AUDIO_NO_DUPLICATE_QUOTA_CHARGE_PASS`
