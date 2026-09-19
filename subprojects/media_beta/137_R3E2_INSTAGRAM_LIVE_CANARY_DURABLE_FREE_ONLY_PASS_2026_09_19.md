# KRC MEDIA — R3-E2 Instagram live canary PASS / durable Neon evidence

Date: 2026-09-19  
Status: **AUTHORITATIVE CHECKPOINT / R3-E2 LIVE CANARY PASS / DURABLE PERSISTENCE PASS / FREE-ONLY EVIDENCE PASS / RESTART+IDEMPOTENCY PENDING**

## Scope

This checkpoint records the successful bounded retry of the owner-approved R3-E2 Instagram live canary after checkpoint 136 cold-start remediation.

Exactly one consequential tool was invoked through ChatGPT:

```text
media_instagram_start
url=https://www.instagram.com/reel/DF1CIrPSVmf/
```

The owner used the ChatGPT consequential-action confirmation UI and selected **Allow once**.

No other MEDIA tool was invoked as part of the start request.

## Runtime path

Accepted route:

```text
ChatGPT Plugin/App
-> R3-E2 authenticated MCP
-> bounded VoiceBridge health warmup
-> exactly one VoiceBridge POST
-> OCI self-hosted Cobalt
-> AssemblyAI universal-2 Free
-> Neon Free PostgreSQL
```

R3-E2 MCP observed an authenticated POST /mcp returning HTTP 200 at the completion boundary.

## Durable job

Neon project:

```text
project=krc-media-beta-neon
project_id=plain-snow-71973546
branch=production
branch_id=br-summer-union-b2qlszfv
database=krc_media_beta
```

Persisted job:

```text
job_id=KRCM_04e6d847-449c-4d0f-82c7-b494871d9322
request_key=3ecbf9fde62196a5b88326f5dcc9a12806f2bdd1f5452a86731c68a2750dc870
status=COMPLETED
source_url=https://www.instagram.com/reel/DF1CIrPSVmf/
created_at=2026-09-19T15:22:00.798Z
updated_at=2026-09-19T15:22:17.648Z
reused=false
```

Persistence uniqueness:

```text
job_count=1
segment_count=1
charge_rows=1
```

## Provider / retrieval evidence

```text
provider=assemblyai
provider_mode=cobalt_retrieval_stt
retrieval_provider=cobalt
detected_language=en
language_confidence=0.9982
media_duration_seconds=42.24
stt_seconds_charged=43
segment_count=1
transcript_characters=899
provider_data_deleted=true
```

The transcript segment was durably persisted in the job row.

## Free-only / billing evidence

```text
credits_charged=0
retrieval_credits_charged=0
metadata_credits_charged=0
credit_charge_uncertain=false
ai_credit_ceiling=null
ai_fallback_requires_new_consent=false
```

STT quota ledger:

```text
job_id=KRCM_04e6d847-449c-4d0f-82c7-b494871d9322
day_utc=2026-09-19
seconds=43
```

The ledger row records free-tier STT seconds consumption; it is not evidence of a monetary charge.

Therefore:

```text
R3_E2_LIVE_CANARY=PASS
NEON_JOB_PERSISTENCE=PASS
TERMINAL_STATE=COMPLETED
COBALT_RETRIEVAL=PASS
ASSEMBLYAI_STT=PASS
PROVIDER_DATA_DELETED=PASS
PAID_RETRIEVAL=false
PAID_STT=false
PAID_FALLBACK=false
PROVIDER_CHARGE=0
CREDIT_CHARGE_UNCERTAIN=false
```

## Cold-start remediation outcome

The retry succeeded after the checkpoint 136 remediation:

```text
VoiceBridge health outside global limiter=PASS
R3-E2 health warmup before consequential POST=PASS
AUTO_RETRY_CONSEQUENTIAL_POST=false
```

The first attempt remained a pre-provider transient failure and did not create a durable job. The successful retry created exactly one durable job.

## Remaining R3-E2 acceptance gates

The following are intentionally not performed by this checkpoint:

```text
VOICEBRIDGE_RESTART_REPLAY=PENDING
R3E2_RESTART_REPLAY=PENDING
STATUS_READ_AFTER_RESTART=PENDING
SEGMENTS_READ_AFTER_RESTART=PENDING
DUPLICATE_START_IDEMPOTENCY=PENDING
DUPLICATE_START_REUSED=PENDING
DUPLICATE_PROVIDER_WORK_ZERO=PENDING
FINAL_ERROR_SCAN=PENDING
```

A duplicate consequential start is not authorized by this checkpoint and requires a separate owner-approved confirmation path.

## Preserved boundaries

```text
PROJECT_COST_POLICY=FREE_ONLY
PAID_DATABASE_UPGRADE=DENIED
PAID_HOSTING_FALLBACK=DENIED
PAID_PROVIDER_FALLBACK=DENIED
PUBLIC_GPT_MUTATION=NO
PLUGIN_PUBLICATION=NO
PLUGIN_SHARING=NO
MAIN_MUTATION=NO
PR22_MERGE=NO
PR45_MERGE=NO
R3_E3_E4=HOLD
R4=HOLD
```

Terminal marker:

`KRC_MEDIA_CHECKPOINT_137_R3E2_INSTAGRAM_LIVE_CANARY_DURABLE_FREE_ONLY_PASS_2026_09_19`
