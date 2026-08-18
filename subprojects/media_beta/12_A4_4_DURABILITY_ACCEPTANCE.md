# MEDIA BETA A4.4 Restart Durability Acceptance
Живе підтвердження збереження client-assisted KRCC job після навмисного redeploy/restart beta backend і успішного продовження цього самого job до COMPLETED.

Version: 1.1
Status: PASS
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

## Acceptance conclusion

PASS for complete restart-resume durability of the captions-first waiting-job path.

Confirmed:
- KRCC waiting state is no longer lost merely because the beta web process is replaced;
- job identity and original `created_at` survive restart;
- Action-facing readback restores `AWAITING_CLIENT` correctly;
- the restored job can be resumed by Helper 0.2.2 after restart;
- the same Job ID reaches `COMPLETED` through the captions-first path;
- 227 caption segments are accepted after restart;
- captions remain zero-STT-cost;
- production was not modified.

## Residual durability work

A4.4 waiting-job restart durability is closed. Separate release hardening still includes:
- completed-job status/segment readback after a later restart;
- audio fallback restart-boundary behavior if a process is replaced while upload/transcription is active;
- Free Postgres lifecycle/expiry management for the closed beta;
- migration away from temporary Free Postgres for a future public/free architecture.

`A4_4_WAITING_JOB_RESTART_DURABILITY_PASS`

`A4_4_RESTORED_JOB_CAPTIONS_COMPLETION_PASS`

`A4_4_RESTART_RESUME_OWNER_ACCEPTANCE_PASS`
