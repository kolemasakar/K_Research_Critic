# KRC MEDIA — R3-E4 Telegram first live canary bounded terminal state / restart durability PASS / replacement candidate preflight PASS

Date: 2026-09-20
Status: **R3_E4_FIRST_LIVE_CANARY_BOUNDED_FAILED / DURABLE_PERSISTENCE_PASS / RESTART_DURABILITY_PASS / ZERO_CHARGE / REPLACEMENT_OWNER_APPROVAL_REQUIRED**

## First owner-approved Telegram live canary

```text
source_url=https://t.me/techcrimes/12101
job_id=KRCM_59d7bdc2-9ea0-4028-b8c6-dfe3f39828f9
status=FAILED
provider=assemblyai
provider_mode=telegram_public_retrieval_stt
retrieval_provider=telegram_public_web
retrieval_credits_charged=0
credits_charged=0
metadata_credits_charged=0
stt_seconds_charged=0
credit_charge_uncertain=false
segment_count=0
error_code=STT_TRANSCRIPTION_FAILED
error_retryable=false
error_message=language_detection cannot be performed on files with no spoken audio.
```

This is a deterministic content terminal state, not a transport or provider-network failure.

## Durable persistence and restart

VoiceBridge was redeployed on validated head:

```text
deploy=dep-danj3urm8hqs73bgfaug
commit=751f83f2b1aca79f58e9a5f615296404836ada06
deploy_status=live
health=HTTP_200 / status=ok
```

After restart, Neon preserved the exact failed job and error unchanged.

```text
R3_E4_DURABLE_PERSISTENCE=PASS
R3_E4_RESTART_DURABILITY=PASS
R3_E4_PUBLIC_TELEGRAM_RETRIEVAL=PASS
R3_E4_ZERO_RETRIEVAL_CREDITS=PASS
R3_E4_ZERO_PROVIDER_CHARGE=PASS
```

## Retry/idempotency contract

Existing VoiceBridge test contract explicitly allows a fresh explicit retry for a failed free-only Telegram job. Completed Telegram jobs are the state for which duplicate-start must return the same job with `reused=true`.

No second provider call was made against the failed `techcrimes/12101` job.

## Safe runtime state

R3-E4 was returned to probe-only mode:

```text
KRC_R3E4_CONFIRMATION_PROBE_ONLY=true
provider_work_started=false
```

## Replacement candidate read-only preflight

Candidate:

```text
https://t.me/Ingiliz_tili_kanalim/731
```

Public-web preflight from the dedicated KRC host:

```text
exact_post_present=true
video_player_found=true
media_url_found=true
duration=1:08
trusted_media_host=true
```

The public post is described as an IELTS interview, making spoken audio materially more likely than the prior silent/no-speech fixture.

No provider/STT call was made for the replacement candidate.

## Next gate

A second Telegram live start is consequential and is not covered by the already consumed one-canary authorization.

Required: explicit owner approval for one replacement bounded Telegram live canary using the preflighted candidate.

Terminal marker:

`KRC_MEDIA_CHECKPOINT_155_R3E4_FIRST_CANARY_BOUNDED_FAILURE_RESTART_PASS_REPLACEMENT_PREFLIGHT_2026_09_20`
