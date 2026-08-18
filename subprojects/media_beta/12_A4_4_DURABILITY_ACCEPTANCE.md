# MEDIA BETA A4.4 Restart Durability Acceptance
Живе підтвердження збереження client-assisted KRCC job після навмисного redeploy/restart beta backend і успішного продовження цього самого job до COMPLETED.

Version: 1.2
Status: PASS_WITH_METADATA_DEFECT
Acceptance date: 2026-08-18

## Scope

A4.4 verifies that a client-assisted `KRCC_...` job no longer depends exclusively on web-process RAM and can survive an isolated Render beta redeploy/restart, remain visible through the Action API, and continue through the browser captions path to completion.

Production VoiceBridge and the published K-Research & Critic GPT were not modified.

## Durable infrastructure

The isolated MEDIA BETA service is configured with a Postgres durable store.

Verified health flags:

```text
durable_store=postgres
restart_resilient_waiting_jobs=true
durable_quota_ledger=true
```

The durability provisioning/deploy workflow reached:

```text
SUCCESS
stage=health_pass
diagnostic=none
```

## Live restart test job

Created before the intentional redeploy/restart:

`KRCC_d37e26da-069d-43d6-a98f-7608e544c43e`

Initial state:

```text
status=AWAITING_CLIENT
reused=false
created_at=2026-08-18T02:55:59.880Z
client_upload_required=true
stt_seconds_charged=0
```

## Intentional isolated restart

The MEDIA BETA service was intentionally redeployed at commit:

`64815f7f3efc7de1e20523a4677d38b6ca5af86d`

The isolated durability workflow completed successfully with `health_pass`. Production was not targeted.

## Post-restart Action readback

After restart, the same Action-facing status route returned the same job:

```text
job_id=KRCC_d37e26da-069d-43d6-a98f-7608e544c43e
status=AWAITING_CLIENT
created_at=2026-08-18T02:55:59.880Z
client_upload_required=true
stt_seconds_charged=0
segment_count=0
error=null
```

This proves that the waiting KRCC job survived web-process replacement and remained available through the GPT-facing API.

## Post-restart continuation to completion

The same restored Job ID was then entered into Helper 0.2.2. The tester selected `Use subtitles` on the same YouTube source after the restart.

Observed final Helper state:

```text
status=COMPLETED
transcript_source=youtube_captions
caption_type=auto_generated
detected_language=uk
segment_count=227
stt_seconds_charged=0
provider_cleanup=not applicable
```

The helper reported that the transcript was loaded from the YouTube transcript panel. No AssemblyAI fallback was used and no STT quota was consumed.

## Completed Action-facing readback

The same external Job ID was then read again through the Action-facing status endpoint after completion:

```text
job_id=KRCC_d37e26da-069d-43d6-a98f-7608e544c43e
status=COMPLETED
transcript_source=youtube_captions
caption_type=auto_generated
detected_language=uk
provider=youtube
duration_seconds=663
transcript_characters=8235
segment_count=227
stt_seconds_charged=0
error=null
```

This confirms that the completed restored job remains readable through the GPT-facing contract.

## Metadata continuity defect

The completed Action readback exposed one residual defect:

```text
original created_at = 2026-08-18T02:55:59.880Z
completed created_at = 2026-08-18T03:00:23.361Z
```

The external Job ID remained stable, but `created_at` was replaced by the timestamp of the internally rehydrated in-memory job when the restored waiting job was resumed. This is a metadata continuity defect, not a transcript or durability failure.

Required fix before broader beta release:
- when persisting a live snapshot for a rehydrated job, preserve the durable external record's original `created_at` instead of the internal replacement job's `created_at`.

## Acceptance conclusion

PASS for complete restart-resume durability of the captions-first waiting-job path, with one metadata continuity defect remaining.

Confirmed:
- KRCC waiting state is no longer lost merely because the beta web process is replaced;
- job identity survives restart;
- Action-facing readback restores `AWAITING_CLIENT` correctly;
- the restored job can be resumed by Helper 0.2.2 after restart;
- the same Job ID reaches `COMPLETED` through the captions-first path;
- 227 caption segments are accepted after restart;
- the completed result remains readable through the Action API;
- captions remain zero-STT-cost;
- production was not modified.

Not yet accepted as correct:
- immutable `created_at` continuity across rehydration and completion.

## Residual durability work

A4.4 transport/state durability is closed. Separate release hardening still includes:
- fix immutable `created_at` continuity for rehydrated jobs;
- completed-job status/segment readback after a later restart;
- audio fallback restart-boundary behavior if a process is replaced while upload/transcription is active;
- durable quota-ledger restart acceptance after a newly charged audio job;
- Free Postgres lifecycle/expiry management for the closed beta;
- migration away from temporary Free Postgres for a future public/free architecture.

`A4_4_WAITING_JOB_RESTART_DURABILITY_PASS`

`A4_4_RESTORED_JOB_CAPTIONS_COMPLETION_PASS`

`A4_4_COMPLETED_ACTION_READBACK_PASS`

`A4_4_CREATED_AT_CONTINUITY_DEFECT_OPEN`
