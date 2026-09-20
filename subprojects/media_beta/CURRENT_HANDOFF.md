# KRC MEDIA — CURRENT HANDOFF

Version: 19.1
Status: **ACTIVE_HANDOFF / R3-E1_COMPLETE / R3-E2_COMPLETE / R3-E3_FACEBOOK_COMPLETE / R3-E4_FIRST_CANARY_BOUNDED_TERMINAL / REPLACEMENT_APPROVAL_HOLD / R3-F_CI_PASS / R3-G_OAUTH_RUNTIME_ACTIVE / FREE_ONLY / PUBLICATION_HOLD**
Date: 2026-09-20

## Recovery command

`Віднови K-Research & Critic MEDIA з subprojects/media_beta/CURRENT_HANDOFF.md та checkpoint 155. R3-E1/E2 COMPLETE. R3-E3 Facebook COMPLETE. R3-E4 Telegram: перший owner-approved live canary https://t.me/techcrimes/12101 створив durable job KRCM_59d7bdc2-9ea0-4028-b8c6-dfe3f39828f9 через telegram_public_web, charge=0, але завершився FAILED/non-retryable через no spoken audio; restart durability PASS. Це контентний bounded terminal state, не transport/provider failure. E4 повернуто в CONFIRMATION_PROBE_ONLY=true. Replacement candidate https://t.me/Ingiliz_tili_kanalim/731 preflight PASS: exact post, native video, trusted media URL, duration 1:08; новий provider call потребує окремого owner approval. PROJECT_COST_POLICY=FREE_ONLY.`

## Canonical current authority

1. `CURRENT_HANDOFF.md` — v19.1.
2. `155_R3E4_FIRST_CANARY_BOUNDED_FAILURE_RESTART_PASS_REPLACEMENT_PREFLIGHT_2026_09_20.md`.
3. `154_R3E3_COMPLETE_R3E4_TELEGRAM_LIVE_CANARY_ARMED_2026_09_20.md`.
4. `153_R3E3_FACEBOOK_LIVE_ACCEPTANCE_COMPLETE_2026_09_20.md`.
5. `152_R3E3_FACEBOOK_LIVE_CANARY_RESTART_DURABILITY_PASS_IDEMPOTENCY_PENDING_2026_09_20.md`.
6. `149_R3E4_TELEGRAM_CHATGPT_ALLOW_ONCE_ZERO_SIDE_EFFECT_PASS_2026_09_20.md`.
7. `02_ROADMAP.md`.
8. current PR #22 / PR #45 heads and current runtime evidence.

## Repository / PR authority

```text
KRC repository=kolemasakar/K_Research_Critic
branch=agent/krc-public-media-r3-integration
PR=22
state=OPEN / DRAFT / UNMERGED
ci_validated_code_head=4c834382e18dfce1bea86dee26614a38a3428817
latest_runtime_checkpoint=006767febf898290b8f00a345e6bedcef7c88a26

VoiceBridge repository=kolemasakar/VoiceBridge
branch=agent/krc-media-gemini-migration
PR=45
state=OPEN / DRAFT / UNMERGED
ci_validated_and_deployed_head=751f83f2b1aca79f58e9a5f615296404836ada06
```

## Phase state

```text
R3_A=PASS
R3_B=PASS
R3_C=PASS
R3_D=PASS
R3_E1=PASS / COMPLETE
R3_E2=PASS / COMPLETE
R3_E3=PASS / COMPLETE
R3_E4=ZERO_SIDE_EFFECT_CONFIRMATION_COMPLETE / FIRST_LIVE_CANARY_BOUNDED_TERMINAL / RESTART_DURABILITY_PASS / REPLACEMENT_APPROVAL_HOLD
R3_F=LOCAL_PASS / CI_PASS / RUNTIME_ACCEPTANCE_PENDING
R3_G_OAUTH=DEPLOYED / E3_TOKEN_FLOW_PASS / E4_TOKEN_FLOW_PASS / TOKEN_RESTART_ACCEPTANCE_PENDING
R3_H=HOLD
R4=HOLD
```

## R3-E3 Facebook acceptance

```text
job_id=KRCM_2dbbe3ba-c2da-49c4-9941-f64b22630880
status=COMPLETED
retrieval_provider=cobalt
retrieval_credits_charged=0
credits_charged=0
restart_durability=PASS
duplicate_start_idempotency=PASS
duplicate_reused=true
facebook_jobs=1
current_E3_probe_only=true
R3_E3_COMPLETE=PASS
```

## R3-E4 first live canary

```text
source_url=https://t.me/techcrimes/12101
job_id=KRCM_59d7bdc2-9ea0-4028-b8c6-dfe3f39828f9
status=FAILED
provider=assemblyai
provider_mode=telegram_public_retrieval_stt
retrieval_provider=telegram_public_web
retrieval_credits_charged=0
credits_charged=0
stt_seconds_charged=0
credit_charge_uncertain=false
error_code=STT_TRANSCRIPTION_FAILED
error_retryable=false
error_message=language_detection cannot be performed on files with no spoken audio.
durable_persistence=PASS
restart_durability=PASS
current_E4_probe_only=true
```

The failure is a deterministic content terminal state. Existing VoiceBridge tests intentionally permit a fresh explicit retry after a failed free-only Telegram job; completed Telegram jobs use same-job `reused=true` duplicate idempotency.

## Replacement candidate

```text
url=https://t.me/Ingiliz_tili_kanalim/731
exact_post_present=true
native_video_player=true
media_url_found=true
trusted_media_host=true
duration=1:08
provider_call_performed=false
```

Public description identifies the clip as an IELTS interview. A replacement live start is consequential and requires a new explicit owner approval.

## VoiceBridge

```text
service=voicebridge-krc-media-beta-kolemasakar
service_id=srv-da1kic5bedkc73d6fk60
head=751f83f2b1aca79f58e9a5f615296404836ada06
restart_deploy=dep-danj3urm8hqs73bgfaug
restart_status=live
health=PASS
version=0.6.0
```

## Durable Neon state

```text
provider=Neon Free
project=krc-media-beta-neon
project_id=plain-snow-71973546
branch=production
branch_id=br-summer-union-b2qlszfv
database=krc_media_beta

total_jobs=3
instagram_jobs=1
facebook_jobs=1
telegram_jobs=1
telegram_completed_jobs=0
telegram_failed_jobs=1
```

## CI acceptance

```text
KRC_RUN=35466720921
KRC_PYTHON_3_13=PASS
KRC_PYTHON_3_14=PASS
KRC_QUALITY=PASS

VOICEBRIDGE_RUN=35466722002
VOICEBRIDGE_CLOUD=PASS
VOICEBRIDGE_IMAGE_PARITY=PASS
VOICEBRIDGE_BROWSER_EXTENSION=PASS
VOICEBRIDGE_REPOSITORY_DOCS=PASS
```

## Next gate

1. Obtain explicit owner approval for one replacement bounded Telegram live canary using `https://t.me/Ingiliz_tili_kanalim/731`.
2. Arm E4 only after approval and warm VoiceBridge.
3. Execute exactly one replacement `media_telegram_start`.
4. If COMPLETED, verify Neon persistence, restart durability, then one duplicate start with same job id and `reused=true`.
5. Return E4 to `CONFIRMATION_PROBE_ONLY=true`.
6. Close R3-E4.
7. Complete R3-F runtime parity and R3-G token-restart acceptance.
8. Proceed to R3-H only after all prior gates pass.

## Hard release boundary

```text
PROJECT_COST_POLICY=FREE_ONLY
PUBLIC_GPT_MUTATION=NO
PLUGIN_PUBLICATION=NO
PLUGIN_SHARING=NO
MAIN_MUTATION=NO
PR22_MERGE=NO
PR45_MERGE=NO
FACEBOOK_ADDITIONAL_LIVE_STARTS=NO
TELEGRAM_REPLACEMENT_LIVE_START=NOT_YET_AUTHORIZED
R4=HOLD
```

Terminal marker:

`KRC_MEDIA_CURRENT_HANDOFF_V19_1_R3E4_BOUNDED_FAILURE_REPLACEMENT_APPROVAL_HOLD_2026_09_20`
