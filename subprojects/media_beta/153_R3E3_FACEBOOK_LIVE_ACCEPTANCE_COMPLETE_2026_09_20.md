# KRC MEDIA — R3-E3 Facebook live acceptance COMPLETE

Date: 2026-09-20
Status: **R3_E3_COMPLETE / LIVE_CANARY_PASS / RESTART_DURABILITY_PASS / DUPLICATE_START_IDEMPOTENCY_PASS / FREE_ONLY**

## Accepted Facebook live canary

```text
job_id=KRCM_2dbbe3ba-c2da-49c4-9941-f64b22630880
status=COMPLETED
provider=assemblyai
provider_mode=facebook_retrieval_stt
retrieval_provider=cobalt
retrieval_credits_charged=0
credits_charged=0
metadata_credits_charged=0
credit_charge_uncertain=false
provider_data_deleted=true
segment_count=1
stt_seconds_charged=23
```

## Restart durability

VoiceBridge was redeployed on validated head `751f83f2b1aca79f58e9a5f615296404836ada06`.

After restart:

```text
job_present=true
job_status=COMPLETED
persisted_segment_count=1
```

## Duplicate-start idempotency

The exact same `media_facebook_start` was executed after restart.

Returned result:

```text
same_job_id=true
status=COMPLETED
reused=true
```

Independent Neon verification:

```text
facebook_jobs=1
only_job_id=KRCM_2dbbe3ba-c2da-49c4-9941-f64b22630880
status=COMPLETED
retrieval_provider=cobalt
retrieval_credits_charged=0
credits_charged=0
updated_at=2026-09-20T00:57:54.239Z
```

The persisted update timestamp did not change on duplicate start, proving the existing completed result was reused rather than provider work being replayed.

Runtime:

```text
E3_PROVIDER_WORK_STARTED=false
POST_IDEMPOTENCY_ERROR_LEVEL_LOGS=0
```

## Acceptance

```text
R3_E3_LIVE_CANARY=PASS
R3_E3_DURABLE_PERSISTENCE=PASS
R3_E3_RESTART_DURABILITY=PASS
R3_E3_DUPLICATE_START_IDEMPOTENCY=PASS
R3_E3_ZERO_PAID_FALLBACK=PASS
R3_E3_COMPLETE=PASS
```

Terminal marker:

`KRC_MEDIA_CHECKPOINT_153_R3E3_FACEBOOK_LIVE_ACCEPTANCE_COMPLETE_2026_09_20`
