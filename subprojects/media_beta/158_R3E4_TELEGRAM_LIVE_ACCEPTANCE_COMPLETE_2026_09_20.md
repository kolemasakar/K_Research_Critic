# KRC MEDIA — R3-E4 Telegram live acceptance COMPLETE

Date: 2026-09-20
Status: **R3_E4_COMPLETE / REPLACEMENT_LIVE_CANARY_PASS / RESTART_DURABILITY_PASS / DUPLICATE_START_IDEMPOTENCY_PASS / FREE_ONLY**

## Accepted completed Telegram canary

```text
source_url=https://t.me/Ingiliz_tili_kanalim/731
job_id=KRCM_c1cbb41b-497d-472c-b6c2-10d1128b4eda
status=COMPLETED
provider=assemblyai
provider_mode=telegram_public_retrieval_stt
retrieval_provider=telegram_public_web
retrieval_credits_charged=0
credits_charged=0
metadata_credits_charged=0
credit_charge_uncertain=false
provider_data_deleted=true
detected_language=en
language_confidence=0.9537
media_duration_seconds=68
stt_seconds_charged=68
segment_count=1
transcript_characters=330
```

## Restart durability

VoiceBridge redeployed on validated head `751f83f2b1aca79f58e9a5f615296404836ada06`:

```text
deploy=dep-danj6uuk1f9s738u1670
deploy_status=live
health=HTTP_200 / status=ok / version=0.6.0
```

The same completed Telegram job and segment remained present after restart.

## Duplicate-start idempotency

The exact same `media_telegram_start` was executed after restart.

Returned:

```text
same_job_id=true
status=COMPLETED
reused=true
```

Independent Neon verification:

```text
candidate_jobs=1
only_job_id=KRCM_c1cbb41b-497d-472c-b6c2-10d1128b4eda
status=COMPLETED
updated_at=2026-09-20T01:13:52.809Z
retrieval_provider=telegram_public_web
retrieval_credits_charged=0
credits_charged=0
```

The persisted timestamp did not change on duplicate start, proving provider work was not replayed.

## Safe post-acceptance state

E4 was returned to probe-only mode:

```text
deploy=dep-danj7s6k1f9s738u450g
deploy_status=live
KRC_R3E4_CONFIRMATION_PROBE_ONLY=true
provider_work_started=false
```

## Acceptance

```text
R3_E4_LIVE_CANARY=PASS
R3_E4_DURABLE_PERSISTENCE=PASS
R3_E4_RESTART_DURABILITY=PASS
R3_E4_DUPLICATE_START_IDEMPOTENCY=PASS
R3_E4_ZERO_PAID_FALLBACK=PASS
R3_E4_COMPLETE=PASS
```

The earlier `techcrimes/12101` no-spoken-audio job remains as a valid bounded failed-content record and does not affect acceptance of the completed replacement canary.

Terminal marker:

`KRC_MEDIA_CHECKPOINT_158_R3E4_TELEGRAM_LIVE_ACCEPTANCE_COMPLETE_2026_09_20`
