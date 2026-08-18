# MEDIA BETA A4.4 Restart Durability Acceptance
Живе підтвердження збереження client-assisted KRCC job після навмисного redeploy/restart beta backend, продовження цього самого job до COMPLETED та незмінності created_at.

Version: 1.4
Status: PASS
Acceptance date: 2026-08-18

## Scope

A4.4 verifies that a client-assisted `KRCC_...` job no longer depends exclusively on web-process RAM and can survive an isolated Render beta redeploy/restart, remain visible through the Action API, continue through the browser captions path to completion, and preserve its original `created_at` across rehydration.

Production VoiceBridge and the published K-Research & Critic GPT were not modified.

## Durable infrastructure

The isolated MEDIA BETA service is configured with a Postgres durable store.

Verified health flags:

```text
durable_store=postgres
restart_resilient_waiting_jobs=true
durable_quota_ledger=true
```

## Initial restart-resume durability

Initial accepted restart test job:

`KRCC_d37e26da-069d-43d6-a98f-7608e544c43e`

Before restart:

```text
status=AWAITING_CLIENT
created_at=2026-08-18T02:55:59.880Z
client_upload_required=true
stt_seconds_charged=0
```

After intentional beta redeploy/restart, the same Action-facing job remained `AWAITING_CLIENT`. Helper 0.2.2 then resumed the same Job ID through `Use subtitles` and completed with:

```text
status=COMPLETED
transcript_source=youtube_captions
caption_type=auto_generated
detected_language=uk
segment_count=227
stt_seconds_charged=0
```

This proved restart-resume durability of the waiting-job captions path.

## Metadata continuity defect and remediation

The first completed Action readback exposed a metadata defect: a rehydrated in-memory job could replace the external job's original `created_at`.

Remediation was implemented in two layers:
- Postgres upsert preserves the existing durable payload's `created_at` on conflict;
- live HTTP projections for snapshot, captions-resume, and audio-resume explicitly preserve `record.job.created_at`.

VoiceBridge HTTP projection remediation code commit:

`db57575b11638ae2a6123e9bebe78a53b1144394`

The remediation was validated and deployed only to the isolated MEDIA BETA service. Production was not targeted.

## Durable completed-job readback

Continuity job:

`KRCC_f76e37ab-84bb-439c-9226-c1baaa2e561d`

Original timestamp:

```text
created_at=2026-08-18T03:18:59.441Z
```

After later process replacement, the Action API returned the completed job from durable state with the same original timestamp:

```text
status=COMPLETED
created_at=2026-08-18T03:18:59.441Z
updated_at=2026-08-18T03:21:37.038Z
transcript_source=youtube_captions
segment_count=227
stt_seconds_charged=0
```

This confirmed that the durable record itself preserved the original `created_at`.

## Final end-to-end metadata regression

Final regression job:

`KRCC_cad52723-cbf0-4bd6-b195-44902d11bc6b`

Before restart:

```text
status=AWAITING_CLIENT
created_at=2026-08-18T03:38:41.045Z
```

An intentional isolated MEDIA BETA restart/redeploy was then performed. The same Job ID was resumed through Helper 0.2.2 using `Use subtitles`.

Helper result:

```text
status=COMPLETED
transcript_source=youtube_captions
caption_type=auto_generated
detected_language=uk
segment_count=227
stt_seconds_charged=0
provider_cleanup=not applicable
```

Final Action-facing readback:

```text
job_id=KRCC_cad52723-cbf0-4bd6-b195-44902d11bc6b
status=COMPLETED
created_at=2026-08-18T03:38:41.045Z
updated_at=2026-08-18T03:45:29.320Z
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

Critical equality:

```text
created_at BEFORE restart  = 2026-08-18T03:38:41.045Z
created_at AFTER COMPLETED = 2026-08-18T03:38:41.045Z
```

Result: exact match. The `created_at` continuity defect is closed.

## Acceptance conclusion

A4.4 restart durability is PASS.

Confirmed:
- KRCC waiting state survives beta web-process replacement;
- external Job ID survives restart;
- Action-facing readback restores waiting state correctly;
- a restored job can be resumed by Helper 0.2.2 after restart;
- the same Job ID reaches `COMPLETED` through captions-first;
- 227 caption segments remain available;
- captions remain zero-STT-cost;
- completed job state remains readable after process replacement;
- original `created_at` is immutable across restart, rehydration, completion, and subsequent Action readback;
- production was not modified.

## Residual durability/release work

A4.4 is closed. Separate release hardening still includes:
- audio fallback restart-boundary behavior if a process is replaced while upload/transcription is active;
- durable quota-ledger restart acceptance after a newly charged audio job;
- Free Postgres lifecycle/expiry management for the closed beta;
- migration away from temporary Free Postgres for a future public/free architecture.

`A4_4_WAITING_JOB_RESTART_DURABILITY_PASS`

`A4_4_RESTORED_JOB_CAPTIONS_COMPLETION_PASS`

`A4_4_COMPLETED_ACTION_READBACK_PASS`

`A4_4_CREATED_AT_DURABLE_READBACK_PASS`

`A4_4_CREATED_AT_FINAL_E2E_REGRESSION_PASS`

`A4_4_PASS`
