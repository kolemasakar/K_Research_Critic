# KRC MEDIA — CURRENT HANDOFF

Version: 18.1
Status: **ACTIVE_HANDOFF / R3-A_PASS / R3-B_PASS / R3-C_PASS / R3-D_PASS / R3-E1_PASS_COMPLETE / R3-E2_PASS_COMPLETE / R3-E3_STAGING_READY / R3-E4_STAGING_READY / OAUTH_PERSISTENCE_STAGING_READY / R3-F_LOCAL_PARITY_READY / FREE_ONLY / ACTIONS_HOLD / PUBLICATION_HOLD**
Date: 2026-09-19

## Recovery command

`Віднови K-Research & Critic MEDIA з subprojects/media_beta/CURRENT_HANDOFF.md та checkpoint 139. R3-E1 і R3-E2 PASS / COMPLETE. R3-E3 Facebook, R3-E4 Telegram, restart-safe OAuth та R3-F parity підготовлені в integration branches, але runtime deploy/CI acceptance для них HOLD до reset GitHub Actions або окремого owner-рішення. PROJECT_COST_POLICY=FREE_ONLY. Локальні диски HP-OMEN не є сховищем проєкту; authoritative state має бути в GitHub.`

## Canonical current authority

1. `CURRENT_HANDOFF.md` — v18.1.
2. `139_R3E2_COMPLETE_R3E3_R3E4_OAUTH_R3F_STAGING_READY_ACTIONS_HOLD_2026_09_19.md`.
3. `138_R3E2_RESTART_REPLAY_STATUS_SEGMENTS_PASS_2026_09_19.md`.
4. `137_R3E2_INSTAGRAM_LIVE_CANARY_DURABLE_FREE_ONLY_PASS_2026_09_19.md`.
5. `134_R3E2_CHATGPT_CONFIRMATION_UI_PASS_ZERO_SIDE_EFFECT_2026_09_19.md`.
6. `133_FREE_ONLY_INFRASTRUCTURE_POLICY_RENDER_WEB_ALLOWED_POSTGRES_REJECTED_2026_09_19.md`.
7. `129_R3E1_YOUTUBE_LIVE_DURABLE_REPLAY_IDEMPOTENCY_PASS_2026_09_19.md`.
8. `02_ROADMAP.md`.
9. current PR #22 / PR #45 heads and current runtime evidence.

## Repository / PR

```text
KRC repository=kolemasakar/K_Research_Critic
branch=agent/krc-public-media-r3-integration
PR=22
state=OPEN / DRAFT / UNMERGED

VoiceBridge repository=kolemasakar/VoiceBridge
branch=agent/krc-media-gemini-migration
PR=45
state=OPEN / DRAFT / UNMERGED
```

## Accepted phase state

```text
R3_A=PASS
R3_B=PASS
R3_C=PASS
R3_D=PASS
R3_E1=PASS / COMPLETE
R3_E2=PASS / COMPLETE
R3_E3=LOCAL_STAGING_READY / RUNTIME_DEPLOY_PENDING
R3_E4=LOCAL_STAGING_READY / RUNTIME_DEPLOY_PENDING
R3_F=LOCAL_PARITY_PACKAGE_READY / CI_PENDING
R3_G_OAUTH_PERSISTENCE=LOCAL_STAGING_READY / DEPLOY_PENDING
MEDIA_OPERATION_COUNT=13
NON_EXECUTION_COUNT=9
EXECUTION_COUNT=4
```

## R3-E2 closure

Accepted owner evidence:

```text
R3_E2_CHATGPT_CONFIRMATION_UI=PASS
R3_E2_CANCEL_PATH=PASS
R3_E2_APPROVE_PATH=PASS
R3_E2_LIVE_CANARY=PASS
R3_E2_DURABLE_NEON=PASS
R3_E2_RESTART_REPLAY=PASS
R3_E2_STATUS_SEGMENTS_AFTER_RESTART=PASS
R3_E2_DUPLICATE_START_IDEMPOTENCY=PASS
R3_E2_DUPLICATE_PROVIDER_WORK=NO
R3_E2_NEW_PROVIDER_CHARGE=0
R3_E2_ERROR_SCAN=PASS
R3_E2=PASS / COMPLETE
```

Accepted Instagram job:

```text
job_id=KRCM_04e6d847-449c-4d0f-82c7-b494871d9322
status=COMPLETED
provider=assemblyai
provider_mode=cobalt_retrieval_stt
retrieval_provider=cobalt
segment_count=1
media_duration_seconds=42.24
stt_seconds_charged=43
credits_charged=0
retrieval_credits_charged=0
metadata_credits_charged=0
credit_charge_uncertain=false
provider_data_deleted=true
```

## R3-E3 Facebook staging

Prepared in the KRC / VoiceBridge integration branches:

- dedicated R3-E3 route-scoped bearer;
- isolated Facebook MCP surface;
- exactly one execution tool: `media_facebook_start`;
- Facebook durable lookup;
- Facebook-only status/segments scope isolation;
- paid/AI continuation routes blocked for the R3-E3 bearer;
- zero-side-effect confirmation probe;
- bounded health warmup before consequential POST;
- no automatic retry of consequential POST;
- restart/replay probe.

No R3-E3 runtime deployment or live Facebook provider work has been accepted yet.

## R3-E4 Telegram staging

Prepared:

- dedicated Telegram-scoped bearer;
- isolated R3-E4 MCP surface;
- exactly one execution tool: `media_telegram_start`;
- Telegram durable lookup;
- Telegram-only status/segments isolation;
- zero-side-effect confirmation probe;
- bounded health warmup;
- restart/replay probe.

No R3-E4 runtime deployment or live Telegram provider work has been accepted yet.

## OAuth restart-safe staging

Optional `KRC_MCP_OAUTH_SIGNING_KEY` support is prepared.

When configured:
- DCR client registration survives restart;
- access tokens survive restart;
- refresh tokens survive restart;
- tampered/expired tokens fail closed;
- signing-key rotation invalidates old restart-safe credentials;
- authorization codes remain short-lived, single-use and in-memory.

This replaces the previous `OAUTH_STATE_PERSISTENCE=NOT_IMPLEMENTED` design debt at the implementation stage, but runtime deployment acceptance remains pending.

## R3-F local parity

Prepared regression contract:

```text
READ_OPERATIONS=9
EXECUTION_OPERATIONS=4
TOTAL_OPERATIONS=13
R3C_EXECUTION_TOOLS=0
R3E1_OWN_START_ONLY=true
R3E2_OWN_START_ONLY=true
R3E3_OWN_START_ONLY=true
R3E4_OWN_START_ONLY=true
```

Local validation before repository transfer:

```text
KRC_R3_COMBINED=65/65 PASS
VOICEBRIDGE_RELEVANT_REGRESSION=23/23 PASS
FACEBOOK_TELEGRAM_SCOPED_TARGETED=11/11 PASS
```

## Cost / infrastructure policy

```text
PROJECT_COST_POLICY=FREE_ONLY
RENDER_FREE_WEB_SERVICES=ACCEPTED
RENDER_ONRENDER_COM_ENDPOINTS=ACCEPTED
RENDER_POSTGRES=REJECTED_FOR_DURABLE_STATE
NEON_FREE_POSTGRES=PRIMARY_DURABLE_DATABASE
OCI_ALWAYS_FREE=ACCEPTED
SELF_HOSTED_COBALT_ON_OCI=ACCEPTED
PAID_HOSTING_FALLBACK=DENIED
PAID_PROVIDER_FALLBACK=DENIED
PAID_ACTIONS_USAGE=DENIED
```

## GitHub Actions temporary constraint

```text
GITHUB_ACTIONS_MINUTES=2000/2000
ACTIONS_RESET=2026-10-01
NEW_PAID_ACTIONS_USAGE=DENIED
```

Staging commits made while this constraint is active must avoid intentionally consuming Actions minutes. Full CI for the new E3/E4/OAuth/R3-F batch is deferred until reset or a separate owner decision.

## Storage rule

```text
HP_OMEN_LOCAL_DISK_AS_PROJECT_STORAGE=DENIED
AUTHORITATIVE_PROJECT_STATE=GITHUB_REPOSITORIES
LOCAL_WORKTREE_USE=TRANSIENT_ONLY
```

After verified repository push, temporary HP-OMEN staging worktrees/artifacts must be removed.

## Durable backend

```text
provider=Neon Free
project=krc-media-beta-neon
project_id=plain-snow-71973546
branch=production
branch_id=br-summer-union-b2qlszfv
database=krc_media_beta
subscription=free_v3
```

## Secret boundary

The intended secret-handling policy is server-side only. Do not claim that secrets were never model-visible historically.

```text
VOICEBRIDGE_BEARER_SERVER_SIDE_ONLY=true
DATABASE_CREDENTIAL_SERVER_SIDE_ONLY=true
RAW_SECRET_REEXPOSURE=FORBIDDEN
REPOSITORY_SECRET=false
CHECKPOINT_SECRET=false
```

## Next gate

After GitHub Actions reset or separate owner override:

1. run CI on VoiceBridge staging head;
2. run CI on KRC staging head;
3. deploy OAuth signing key and route-scoped bearers server-side;
4. deploy isolated R3-E3 and R3-E4 sentinels on Render Free;
5. run authenticated read-only preflight/lookup;
6. validate ChatGPT Cancel/Allow-once in zero-side-effect mode;
7. request separate owner approval for one bounded Facebook canary and one bounded Telegram canary;
8. run Neon persistence, restart/replay and duplicate-start idempotency acceptance.

## Hard boundary

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

`KRC_MEDIA_CURRENT_HANDOFF_V18_1_R3E2_COMPLETE_E3_E4_OAUTH_R3F_STAGING_READY_ACTIONS_HOLD_2026_09_19`
