# MEDIA BETA A4.4 Restart Durability Acceptance
Живе підтвердження збереження client-assisted KRCC job після навмисного redeploy/restart beta backend і успішного продовження цього самого job до COMPLETED.

Version: 1.3
Status: PASS_WITH_FINAL_METADATA_REGRESSION_PENDING
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

## Initial live restart test

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

The MEDIA BETA service was intentionally redeployed at commit:

`64815f7f3efc7de1e20523a4677d38b6ca5af86d`

After restart, the same Action-facing status route returned the same job in `AWAITING_CLIENT`. The same restored Job ID was then entered into Helper 0.2.2 and completed through `Use subtitles` with:

```text
status=COMPLETED
transcript_source=youtube_captions
caption_type=auto_generated
detected_language=uk
segment_count=227
stt_seconds_charged=0
```

This proved restart-resume durability of the waiting-job captions path.

## Metadata continuity defect discovery

The first completed Action readback exposed one residual defect:

```text
original created_at = 2026-08-18T02:55:59.880Z
completed created_at = 2026-08-18T03:00:23.361Z
```

The external Job ID remained stable, but the live HTTP projection exposed the internally rehydrated job timestamp instead of the durable external job timestamp.

## Persistence-layer remediation

The Postgres upsert was hardened so an existing durable record preserves its original `payload.created_at` on update.

A regression test was added and the VoiceBridge validation workflow passed.

## HTTP projection remediation

A second live regression showed that the durable store retained the correct timestamp but the running HTTP projection could still expose the internal rehydrated timestamp. The HTTP-layer resume/snapshot paths were then remediated.

VoiceBridge remediation code commit:

`db57575b11638ae2a6123e9bebe78a53b1144394`

Isolated MEDIA BETA deployment result:

```text
SUCCESS
production_not_targeted=true
```

## Durable completed-job readback after remediation

Continuity test job:

`KRCC_f76e37ab-84bb-439c-9226-c1baaa2e561d`

Original timestamp before restart:

```text
created_at=2026-08-18T03:18:59.441Z
```

After the HTTP projection remediation and a later process replacement, the Action API returned the completed job from durable state with:

```text
job_id=KRCC_f76e37ab-84bb-439c-9226-c1baaa2e561d
status=COMPLETED
created_at=2026-08-18T03:18:59.441Z
updated_at=2026-08-18T03:21:37.038Z
transcript_source=youtube_captions
segment_count=227
stt_seconds_charged=0
```

This is a PASS for durable storage and post-restart completed-job readback of the immutable original `created_at`.

## Acceptance conclusion

Confirmed:
- KRCC waiting state survives beta web-process replacement;
- job identity survives restart;
- Action-facing readback restores waiting state correctly;
- a restored job can be resumed by Helper 0.2.2 after restart;
- the same Job ID reaches `COMPLETED` through captions-first;
- 227 caption segments remain available;
- captions remain zero-STT-cost;
- completed durable readback after remediation returns the original `created_at`;
- production was not modified.

One final end-to-end regression is still required before closing the metadata defect completely:

```text
new job
 -> record original created_at
 -> intentional beta restart
 -> resume same Job ID through Helper
 -> COMPLETED
 -> Action readback
 -> created_at exactly equals original value
```

## Residual durability work

After the final metadata regression, separate release hardening still includes:
- audio fallback restart-boundary behavior if a process is replaced while upload/transcription is active;
- durable quota-ledger restart acceptance after a newly charged audio job;
- Free Postgres lifecycle/expiry management for the closed beta;
- migration away from temporary Free Postgres for a future public/free architecture.

`A4_4_WAITING_JOB_RESTART_DURABILITY_PASS`

`A4_4_RESTORED_JOB_CAPTIONS_COMPLETION_PASS`

`A4_4_COMPLETED_ACTION_READBACK_PASS`

`A4_4_CREATED_AT_DURABLE_READBACK_PASS`

`A4_4_CREATED_AT_FINAL_E2E_REGRESSION_PENDING`
