# MEDIA BETA A4.4 Restart Durability Acceptance
Живе підтвердження збереження client-assisted KRCC job після навмисного redeploy/restart beta backend.

Version: 1.0
Status: PARTIAL_PASS
Acceptance date: 2026-08-18

## Scope

A4.4 verifies that a client-assisted `KRCC_...` job no longer depends exclusively on web-process RAM and can survive an isolated Render beta redeploy/restart.

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

## Acceptance conclusion so far

PASS for waiting-job persistence across an intentional isolated Render redeploy/restart.

Confirmed:
- KRCC waiting state is no longer lost merely because the beta web process is replaced;
- job identity and original `created_at` survive restart;
- Action-facing readback restores `AWAITING_CLIENT` correctly;
- no STT quota was consumed by the restart test;
- production was not modified.

## Remaining live proof for full A4.4 closure

Use this same restored Job ID in Helper 0.2.2 and complete the captions path after restart:

```text
AWAITING_CLIENT
 -> Use subtitles
 -> COMPLETED
 -> transcript_source=youtube_captions
 -> segment_count>0
 -> stt_seconds_charged=0
```

Then verify Action-facing status/segments for the completed restored job.

`A4_4_WAITING_JOB_RESTART_DURABILITY_PASS`
