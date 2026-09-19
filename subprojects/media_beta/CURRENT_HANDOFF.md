# KRC MEDIA — CURRENT HANDOFF

Version: 17.8
Status: **ACTIVE_HANDOFF / R3-A_PASS / R3-B_PASS / R3-C_PASS / R3-D_PASS / R3-E1_PASS / R3-E2_ATTEMPT1_TRANSIENT_REMEDIATED_RECONNECT_PENDING / FREE_ONLY / PUBLICATION_HOLD**
Date: 2026-09-19

## Recovery command

`Віднови K-Research & Critic MEDIA з subprojects/media_beta/CURRENT_HANDOFF.md та checkpoint 136. R3-E1 PASS. R3-E2 confirmation UI PASS; live canary attempt 1 failed transiently pre-provider with HTTP 429 while VoiceBridge was cold/stopped; no Neon job/provider work. VoiceBridge health was moved outside the global limiter and R3-E2 now performs bounded side-effect-free health warmup before exactly one consequential POST. Both CI and deploys PASS/LIVE. Fresh DCR/reconnect is required after redeploy before retry. Do not use R3C unless separately requested.`

## Canonical recovery files

1. `subprojects/media_beta/CURRENT_HANDOFF.md` — v17.8; current authority.
2. `subprojects/media_beta/136_R3E2_ATTEMPT1_TRANSIENT_COLD_START_REMEDIATION_PASS_RECONNECT_REQUIRED_2026_09_19.md` — current R3-E2 incident/remediation checkpoint.
3. `subprojects/media_beta/135_R3E2_CREDENTIAL_ROTATION_PROBE_DISABLED_LIVE_CANARY_READY_2026_09_19.md` — current R3-E2 live-canary readiness checkpoint.
4. `subprojects/media_beta/134_R3E2_CHATGPT_CONFIRMATION_UI_PASS_ZERO_SIDE_EFFECT_2026_09_19.md` — current R3-E2 confirmation UI checkpoint.
5. `subprojects/media_beta/133_FREE_ONLY_INFRASTRUCTURE_POLICY_RENDER_WEB_ALLOWED_POSTGRES_REJECTED_2026_09_19.md` — current infrastructure policy clarification.
6. `subprojects/media_beta/132_R3E2_ISOLATED_SENTINEL_AUTHENTICATED_PREFLIGHT_PASS_CONFIRMATION_PENDING_2026_09_19.md` — current R3-E2 implementation/runtime checkpoint.
7. `subprojects/media_beta/131_R3E2_INSTAGRAM_READONLY_FREE_ONLY_PREFLIGHT_2026_09_19.md` — R3-E2 read-only preflight.
8. `subprojects/media_beta/130_POST_R3E1_CONTROL_POINT_BEFORE_R3E2_2026_09_19.md` — pre-R3-E2 control point.
9. `subprojects/media_beta/129_R3E1_YOUTUBE_LIVE_DURABLE_REPLAY_IDEMPOTENCY_PASS_2026_09_19.md` — R3-E1 closure.
10. `subprojects/media_beta/128_R3E1_RESTART_CONNECTIVITY_PASS_RECORD_REPLAY_PENDING_2026_09_19.md` — restart-connectivity checkpoint.
11. `subprojects/media_beta/127_R3E1_NEON_CUTOVER_COMPLETE_DURABLE_ACCEPTANCE_PENDING_2026_09_19.md` — Neon cutover checkpoint.
12. `subprojects/media_beta/126_CHAT_TRANSITION_R3E1_FREE_ONLY_NEON_MIGRATION_GATE_2026_09_17.md` — historical transition.
13. `subprojects/media_beta/125_FREE_ONLY_INFRASTRUCTURE_POLICY_AND_POSTGRES_AUDIT_2026_09_17.md` — free-only policy / Render DB incident.
14. `subprojects/media_beta/124_R3D_CONSEQUENTIAL_ACTION_CONFIRMATION_PASS_2026_09_17.md`.
15. `subprojects/media_beta/121_R3C_NINE_TOOL_READONLY_VOICEBRIDGE_BINDING_PASS_2026_09_16.md`.
16. `subprojects/media_beta/117_R3B_AUTHENTICATED_REMOTE_MCP_HARDENING_PASS_2026_09_16.md`.
17. `subprojects/media_beta/113_R3A_CONTRACT_FREEZE_SECURE_ADAPTER_BASELINE_PASS_2026_09_16.md`.
18. `subprojects/media_beta/02_ROADMAP.md`.
19. current PR #22 / PR #45 head and CI plus current Render/Neon non-secret evidence.

## Repository / PR

```text
repository=kolemasakar/K_Research_Critic
branch=agent/krc-public-media-r3-integration
PR=22
state=OPEN / DRAFT / UNMERGED

VoiceBridge repository=kolemasakar/VoiceBridge
branch=agent/krc-media-gemini-migration
PR=45
state=OPEN / DRAFT / UNMERGED
```

## Accepted phase baseline

```text
R3_A=PASS
R3_B=PASS
R3_C=PASS
R3_D=PASS
R3_E1=PASS / COMPLETE
R3_E2=CONFIRMATION_UI_PASS / ATTEMPT1_TRANSIENT_PRE_PROVIDER_FAILURE / COLD_START_REMEDIATION_PASS / RECONNECT_PENDING / RETRY_READY
R3_E3=HOLD
R3_E4=HOLD
R3_F_AND_LATER=HOLD
MEDIA_OPERATION_COUNT=13
NON_EXECUTION_COUNT=9
EXECUTION_COUNT=4
```

R3-E1 authorization and acceptance apply only to YouTube. They do not authorize Instagram/Facebook/Telegram execution, publication, sharing, migration, `main` mutation, PR #22 merge, or VoiceBridge PR #45 merge.

## Owner cost policy — hard invariant

```text
PROJECT_COST_POLICY=FREE_ONLY
RENDER_FREE_WEB_SERVICES=ACCEPTED
RENDER_ONRENDER_COM_ENDPOINTS=ACCEPTED
RENDER_POSTGRES=REJECTED_FOR_DURABLE_STATE
RENDER_PAID_UPGRADE=DENIED
NEON_FREE_POSTGRES=PRIMARY_DURABLE_DATABASE
OCI_ALWAYS_FREE=ACCEPTED
SELF_HOSTED_COBALT_ON_OCI=ACCEPTED
PAID_HOSTING_FALLBACK=DENIED
PAID_PROVIDER_FALLBACK=DENIED
UNEXPECTED_BILLING_RISK=DENIED
```

Render is **not** rejected as a platform. Render Free Web Services remain accepted for VoiceBridge and isolated MCP sentinels while they remain on free plans. `.onrender.com` endpoints are therefore expected in the accepted architecture.

## Durable backend

Only Render PostgreSQL is rejected for durable state after expiry/suspension.

Primary durable backend:

```text
provider=Neon Free
project=krc-media-beta-neon
project_id=plain-snow-71973546
branch=production
branch_id=br-summer-union-b2qlszfv
database=krc_media_beta
subscription=free_v3
VOICEBRIDGE_DATABASE_CUTOVER=PASS
```

Schema/constraint/index parity is PASS.

`krc_media_stt_charges` is a bounded quota ledger, not an immutable audit trail. Current code purges rows older than two days.

## R3-E1 accepted runtime

Isolated service:

```text
service=krc-mcp-r3e1-youtube-sentinel
service_id=srv-dall4qv40ujc73ednpqg
surface=r3e1_youtube_execution
tool_count=10
non_execution_tool_count=9
execution_tool_count=1
execution_tool=media_youtube_start
other_execution_tools=not_enabled
```

A dedicated server-side R3-E1 bearer is accepted only by the VoiceBridge YouTube Gemini handler.

Accepted VoiceBridge head:

```text
head=4054ef56603265dabd97a759662019efcf947cac
Validate #816=SUCCESS
current restart deploy=dep-dan6m1mgekts73ftdcfg
status=LIVE
```

Accepted KRC R3-E1 implementation:

```text
implementation_head=88cdc465dd6b74c4941d1d2a15654e4adb29d608
Tests #1655=SUCCESS
final clean deploy=dep-dan6nc3tqb8s73aqdbug
status=LIVE
health=HTTP 200 / status=ok
voicebridge_binding_configured=true
```

## R3-E1 live acceptance evidence

Owner explicitly acknowledged Gemini Developer API Free Tier data-use terms before execution.

First live job:

```text
job_id=KRCM_3f4e62c1-2518-4815-839b-ece80935d794
status=COMPLETED
provider=gemini
provider_mode=youtube_gemini_direct
provider_model=gemini-3.7-flash
retrieval_provider=gemini_youtube_url
retrieval_credits_charged=0
stt_seconds_charged=0
credits_charged=0
segment_count=1
reused=false
gemini_free_data_use_acknowledged=true
```

Durable-state acceptance:

```text
APP_LEVEL_DURABLE_LOOKUP=PASS
NEON_JOB_PERSISTENCE=PASS
VOICEBRIDGE_RESTART=PASS
R3E1_RESTART=PASS
STATUS_READ_AFTER_RESTART=PASS
SEGMENTS_READ_AFTER_RESTART=PASS
RECORD_REPLAY_WITHOUT_PROVIDER_WORK=PASS
DUPLICATE_START_IDEMPOTENCY=PASS
DUPLICATE_START_REUSED=true
DUPLICATE_PROVIDER_WORK=false
ERROR_SCAN=PASS
```

The accepted job existed exactly once in Neon and remained COMPLETED with one segment after both process replacements. The runtime job is subject to normal TTL expiry; durable acceptance evidence remains in checkpoint 129.

## Acceptance cleanup

All temporary startup acceptance switches were disabled after evidence capture. The final R3-E1 service is running without automatic acceptance probes.

```text
KRC_R3E1_DURABLE_PROBE_URL=disabled
KRC_R3E1_EXECUTION_PROBE_URL=disabled
KRC_R3E1_EXECUTION_PROBE_CONSENT=disabled
KRC_R3E1_REPLAY_PROBE_JOB_ID=disabled
provider_work_started=false
```

## R3-C boundary

R3-C remains accepted historical evidence but was not used during the Neon cutover / R3-E1 live acceptance sequence after the owner instructed to leave it untouched.

## Current blocker / next stage

There is no remaining R3-E1 database or YouTube acceptance blocker.

```text
R3_E1=PASS
R3_E2_INSTAGRAM=ATTEMPT1_TRANSIENT_PRE_PROVIDER_FAILURE / COLD_START_REMEDIATION_PASS / RECONNECT_PENDING / RETRY_READY
R3_E3_FACEBOOK=HOLD
R3_E4_TELEGRAM=HOLD
```

R3-E2 implementation/runtime preflight is complete:

```text
VoiceBridge scoped bearer code/runtime=PASS
isolated R3-E2 service=PASS
service=krc-mcp-r3e2-instagram-sentinel-v2
service_id=srv-dan7vsijnfac73fmrtl0
deploy=dep-dan800dii2qc73bm47k0
tool_count=5
execution_tool_count=1
execution_tool=media_instagram_start
authenticated Instagram preflight=PASS
durable lookup=PASS_EMPTY
provider work=false
start_called=false
confirmation contract=PASS
ChatGPT confirmation UI=PASS
CANCEL path=PASS
APPROVE path=PASS
no execution after deny=PASS
approve invocation count=1
zero-side-effect confirmation probe=PASS
provider work=false
real media start=false
```

Post-confirmation preparation:
- scoped R3-E2 VoiceBridge credential rotation=PASS;
- `KRC_R3E2_CONFIRMATION_PROBE_ONLY=false`;
- R3-E2 runtime health=PASS;
- VoiceBridge runtime health=PASS;
- provider work=false;
- real media start=false.

Remaining live gates:
- establish fresh DCR/reconnect in owner ChatGPT after the restart;
- verify the authenticated isolated 5-tool surface;
- obtain explicit owner authorization for exactly one bounded live Instagram start;
- then prove Neon persistence, restart replay and duplicate-start idempotency.

R3-E2 live canary attempt 1 and remediation:

```text
attempt_1_result=HTTP_429 / retryable
failure_stage=PRE_PROVIDER
Neon_job_created=false
Cobalt_work=false
AssemblyAI_work=false
provider_charge=false

VoiceBridge_fix=health outside global rate limiter
VoiceBridge_head=e7b8ebb2803f46656ed07483f87beb31b740f436
VoiceBridge_Validate_822=SUCCESS
VoiceBridge_deploy=dep-danac9btqb8s73b77h40 / LIVE

R3E2_fix=bounded health warmup before exactly one consequential POST
R3E2_head=e0cf1b1c0c46f936df7524c2906b5f7be0b96f6a
R3E2_Tests_1717=SUCCESS
R3E2_deploy=dep-danace8ae00c73e3e940 / LIVE

AUTO_RETRY_CONSEQUENTIAL_POST=false
fresh_DCR_reconnect_required=true
```

Remaining live gates:
- recreate/reconnect the private R3-E2 MCP after redeploy;
- verify authenticated 5-tool surface;
- retry exactly one bounded Instagram canary with Allow once;
- prove Neon persistence, terminal state, restart replay and duplicate-start idempotency.

The first Render provisioning attempt `srv-dan7s6egekts7381bbj0` is not accepted and must not be used.

## Secret boundary

```text
VOICEBRIDGE_BEARER_SERVER_SIDE_ONLY=true
DATABASE_CREDENTIAL_SERVER_SIDE_ONLY=true
MODEL_VISIBLE_SECRET=false
REPOSITORY_SECRET=false
TOOL_ARGUMENT_SECRET=false
CHECKPOINT_SECRET=false
```

## Known operational debt

```text
OAUTH_STATE_PERSISTENCE=NOT_IMPLEMENTED
restart/redeploy=>reconnect_required
Render_free_service_cold_wake_transient_errors=MITIGATED_BY_R3E2_HEALTH_WARMUP
Render_Free_Postgres_expiration=REJECTED_DEPENDENCY
PRODUCTION_READY=NO
R3_G_DEBT=YES
```

## Hard release boundary

```text
PUBLIC_GPT_MUTATION=NO
PLUGIN_PUBLICATION=NO
PLUGIN_SHARING=NO
MAIN_MUTATION=NO
PR22_MERGE=NO
PR45_MERGE=NO
PAID_UPGRADE=NO
R4=HOLD
```

Terminal marker:

`KRC_MEDIA_CURRENT_HANDOFF_V17_8_R3E2_ATTEMPT1_REMEDIATED_RECONNECT_PENDING_2026_09_19`
