# KRC MEDIA — R3-E4 replacement Telegram live canary PASS / restart durability PASS

Date: 2026-09-20
Status: **R3_E4_REPLACEMENT_LIVE_CANARY_PASS / DURABLE_PERSISTENCE_PASS / RESTART_DURABILITY_PASS / DUPLICATE_IDEMPOTENCY_PENDING / FREE_ONLY**

## Replacement live canary

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

## Durable-state verification

Neon contains exactly one job for the replacement URL:

```text
candidate_jobs=1
job_status=COMPLETED
segment_count=1
retrieval_provider=telegram_public_web
retrieval_credits_charged=0
credits_charged=0
```

## Controlled restart

VoiceBridge redeployed on the exact validated head:

```text
service=voicebridge-krc-media-beta-kolemasakar
commit=751f83f2b1aca79f58e9a5f615296404836ada06
deploy=dep-danj6uuk1f9s738u1670
deploy_status=live
health=HTTP_200 / status=ok / version=0.6.0
```

After restart the Telegram job remains unchanged and COMPLETED.

Therefore:

```text
R3_E4_REPLACEMENT_LIVE_CANARY=PASS
R3_E4_DURABLE_PERSISTENCE=PASS
R3_E4_RESTART_DURABILITY=PASS
R3_E4_ZERO_RETRIEVAL_CREDITS=PASS
R3_E4_ZERO_PROVIDER_CHARGE=PASS
R3_E4_DUPLICATE_START_IDEMPOTENCY=PENDING
```

## Next bounded gate

Repeat the exact same `media_telegram_start` once after restart.

Expected:

```text
same job_id
status=COMPLETED
reused=true
candidate_jobs remains 1
no provider replay
credits_charged=0
retrieval_credits_charged=0
```

This repeat is part of the already owner-approved replacement canary acceptance and is solely for idempotency verification.

Terminal marker:

`KRC_MEDIA_CHECKPOINT_157_R3E4_REPLACEMENT_LIVE_PASS_RESTART_PASS_IDEMPOTENCY_PENDING_2026_09_20`
