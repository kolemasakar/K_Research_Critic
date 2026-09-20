# KRC MEDIA — R3-E3 Facebook bounded live canary PASS / restart durability PASS

Date: 2026-09-20
Status: **R3_E3_FACEBOOK_LIVE_CANARY_PASS / FREE_ONLY / RESTART_DURABILITY_PASS / DUPLICATE_START_IDEMPOTENCY_PENDING**

## Live canary result

Owner-authorized bounded Facebook live canary completed successfully.

```text
job_id=KRCM_2dbbe3ba-c2da-49c4-9941-f64b22630880
status=COMPLETED
source_url=https://www.facebook.com/reel/1114235920664408/
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
media_duration_seconds=22.03575
reused=false
```

No paid Facebook retrieval provider was used.

## Independent durable-state verification

Neon contains the completed Facebook record and one persisted segment:

```text
NEON_FACEBOOK_JOBS=1
job_status=COMPLETED
job_id=KRCM_2dbbe3ba-c2da-49c4-9941-f64b22630880
retrieval_provider=cobalt
retrieval_credits_charged=0
credits_charged=0
segment_count=1
```

## Controlled restart

VoiceBridge was redeployed on the exact validated head:

```text
service=voicebridge-krc-media-beta-kolemasakar
deploy=dep-danivg2jnfac738q65gg
commit=751f83f2b1aca79f58e9a5f615296404836ada06
deploy_status=live
health=HTTP_200 / status=ok / version=0.6.0
```

After restart, the same Neon job remains present and COMPLETED with its persisted segment.

Therefore:

```text
R3_E3_LIVE_CANARY=PASS
R3_E3_FREE_RETRIEVAL=cobalt
R3_E3_PAID_FALLBACK_USED=NO
R3_E3_PROVIDER_CHARGE=0
R3_E3_DURABLE_PERSISTENCE=PASS
R3_E3_RESTART_DURABILITY=PASS
R3_E3_DUPLICATE_START_IDEMPOTENCY=PENDING
```

## Next bounded gate

Repeat the same `media_facebook_start` request once after restart. Expected result:

```text
same job_id
status=COMPLETED
reused=true
no new Facebook job
no provider work replay
no provider charge
```

This repeat is part of the already owner-approved bounded Facebook canary acceptance and is solely for idempotency verification.

Telegram remains unarmed until Facebook idempotency closes.

Terminal marker:

`KRC_MEDIA_CHECKPOINT_152_R3E3_FACEBOOK_LIVE_CANARY_RESTART_DURABILITY_PASS_IDEMPOTENCY_PENDING_2026_09_20`
