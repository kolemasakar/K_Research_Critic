# KRC MEDIA — R3-E1 Neon cutover complete / durable runtime acceptance pending

Date: 2026-09-19  
Status: **AUTHORITATIVE CHECKPOINT / NEON CUTOVER COMPLETE / DURABLE RUNTIME ACCEPTANCE PENDING / REAL MEDIA START HOLD**

## Scope

This checkpoint records the owner-approved migration of the VoiceBridge MEDIA durable database binding from expired Render Free PostgreSQL to the existing Neon Free project. It supersedes only the *current-state* portions of checkpoints 125/126; those files remain immutable historical evidence.

## Owner authorization

On 2026-09-19 the owner approved the bounded execution path:

```text
ACTION=NEON_TO_RENDER_DATABASE_CUTOVER
APPROVAL=EXPLICIT
PAID_UPGRADE=DENIED
PUBLIC_GPT_MUTATION=NO
PR_MERGE=NO
PROVIDER_WORK=NO
```

## Pre-cutover verification

```text
VoiceBridge repo=kolemasakar/VoiceBridge
branch=agent/krc-media-gemini-migration
PR=45 OPEN / DRAFT / UNMERGED
accepted_head=3e8cb29b3815e1bf98f143682644899b801826e0
Render service=voicebridge-krc-media-beta-kolemasakar
service_id=srv-da1kic5bedkc73d6fk60
pre_cutover_live_deploy=dep-dal6abdg1s2s73ed059g
autoDeploy=no
service_suspended=false
```

Preflight matched the accepted VoiceBridge head and live deployment before mutation.

## Neon target

```text
project=krc-media-beta-neon
project_id=plain-snow-71973546
subscription=free_v3
region=aws-eu-central-1
postgres=18
branch=production
branch_id=br-summer-union-b2qlszfv
database=krc_media_beta
role=krc_media_beta_owner
scale_to_zero=enabled
storage_limit=512MiB
```

Schema/constraint/index parity against the current VoiceBridge persistence contract was previously verified PASS.

## Cutover execution

Only the Render service variable `KRC_MEDIA_DATABASE_URL` was updated, using a server-side Neon connection string. The credential value was not printed into chat, committed to Git, written to project documentation, or exposed through a user-visible tool result.

The environment update automatically triggered a Render deploy:

```text
deploy=dep-dan5uf0ae00c73dke480
trigger=api
commit=3e8cb29b3815e1bf98f143682644899b801826e0
status=LIVE
started_at=2026-09-19T10:09:00Z
finished_at=2026-09-19T10:09:42Z
```

No second/manual deploy was triggered.

## Post-cutover runtime evidence

Direct owner-side health request after deployment:

```text
GET /api/v1/health
HTTP=200
status=ok
service=voicebridge-cloud
version=0.6.0
```

Render startup evidence:

```text
event=service_started
stt_provider=gemini
stt_model=gemini-3.5-transcribe-live
krc_media_stt_provider=assemblyai
```

Post-deploy Render error log query returned no error records and no durable/database/psql failure records in the checked window.

## Neon state after cutover

Read-only Neon verification:

```text
krc_managed_media_jobs=0
krc_media_client_jobs=0
krc_media_stt_charges=10
stt_seconds_total=285
invalid_negative_charge_rows=0
```

The 10 charge rows include previously accepted live R2 job identifiers, confirming historical VoiceBridge durable use of this Neon database. This does not prove a complete backup of the expired Render database.

## Current gate

```text
NEON_SCHEMA_PARITY=PASS
NEON_FREE_PLAN_IDENTITY=PASS
VOICEBRIDGE_DATABASE_CUTOVER=COMPLETE
RENDER_DEPLOY_AFTER_CUTOVER=PASS
VOICEBRIDGE_HEALTH_AFTER_CUTOVER=PASS
POST_DEPLOY_ERROR_SCAN=PASS

APP_LEVEL_DURABLE_LOOKUP_AFTER_CUTOVER=PENDING
APP_LEVEL_DURABLE_CREATE_READ_RESTART_ACCEPTANCE=PENDING
REAL_YOUTUBE_START=HOLD
R3_E1=AUTHORIZED / PREPARED / DURABLE_RUNTIME_ACCEPTANCE_PENDING
```

The remaining gap is deliberately narrow: authenticated VoiceBridge MEDIA access is required to prove the new runtime performs durable read/create/replay against Neon. Health alone does not exercise the lazy PostgreSQL store.

R3-C is not required for this recovery step and was intentionally not used after the owner instructed to leave it untouched.

## Next bounded work

```text
1. perform authenticated no-provider-work durable lookup/status probe against the post-cutover VoiceBridge runtime
2. confirm Neon receives/serves the expected durable access without MANAGED_DURABLE_STORE_UNAVAILABLE
3. perform bounded durable create/read/status/segments acceptance with a free-only route only when separately authorized where execution is consequential
4. validate restart/cold-wake replay/idempotency
5. verify zero paid fallback and charge/audit accounting
6. close the database gate
7. only then resume R3-E1 YouTube live execution acceptance
```

## Preserved boundaries

```text
PROJECT_COST_POLICY=FREE_ONLY
RENDER_FREE_POSTGRES=REJECTED_FOR_DURABLE_STATE
PAID_DATABASE_UPGRADE=DENIED
PAID_HOSTING_FALLBACK=DENIED
PAID_PROVIDER_FALLBACK=DENIED
PUBLIC_GPT_MUTATION=NO
PLUGIN_PUBLICATION=NO
PLUGIN_SHARING=NO
MAIN_MUTATION=NO
PR22_MERGE=NO
PR45_MERGE=NO
R3_E2_E3_E4=HOLD
R4=HOLD
```

Terminal marker:

`KRC_MEDIA_CHECKPOINT_127_R3E1_NEON_CUTOVER_COMPLETE_DURABLE_ACCEPTANCE_PENDING_2026_09_19`
