# MEDIA BETA Roadmap

Version: 5.6
Status: **PLUGIN_FIRST / R3-A_PASS / R3-B_PASS / R3-C_PASS / R3-D_PASS / R3-E1_AUTHORIZED_BLOCKED_INFRASTRUCTURE / FREE_ONLY / PUBLICATION_HOLD**
Updated: 2026-09-17

## Product position

```text
public KRC Custom GPT: published / unchanged / protected
private MEDIA migration candidate: Remote Custom MCP / Plugin surface
backend authority: VoiceBridge MEDIA API
MEDIA semantic parity target: 13 operations
project infrastructure policy: FREE_ONLY
```

Critical invariants:

```text
MEDIA unavailable/fails -> MEDIA fails closed
Core KRC               -> remains usable
paid infrastructure    -> not accepted as required dependency
paid provider fallback -> forbidden
```

## Canonical current authority

1. `CURRENT_HANDOFF.md` — v16.0.
2. `126_NEW_CHAT_TRANSITION_R3E1_FREE_ONLY_NEON_MIGRATION_GATE_2026_09_17.md`.
3. `125_FREE_ONLY_INFRASTRUCTURE_POLICY_AND_POSTGRES_AUDIT_2026_09_17.md`.
4. `124_R3D_CONSEQUENTIAL_ACTION_CONFIRMATION_PASS_2026_09_17.md`.
5. `121_R3C_NINE_TOOL_READONLY_VOICEBRIDGE_BINDING_PASS_2026_09_16.md`.
6. current PR #22 head/CI.

## Proven baseline

```text
R3_A=PASS
R3_B=PASS
R3_C=PASS
R3_D=PASS
R3C_DISCOVERED_TOOL_COUNT=9
R3C_EXECUTION_TOOL_COUNT=0
R3D_CHATGPT_CONFIRMATION_UI=PASS
R3D_APPROVE_PATH=PASS
R3D_CANCEL_PATH=PASS
R3D_NO_PRECONFIRM_EXECUTION=PASS
```

## Cost and provider policy

```text
PROJECT_COST_POLICY=FREE_ONLY
PAID_DATABASE_UPGRADE=DENIED
PAID_HOSTING_FALLBACK=DENIED
PAID_PROVIDER_FALLBACK=DENIED
AUTOMATIC_PAID_RETRIEVAL=false
AUTOMATIC_PAID_STT=false
AUTOMATIC_PAID_PROXY=false
UNEXPECTED_BILLING_RISK=DENIED
```

A backend that requires payment to preserve mandatory durable state is not acceptable for the target architecture.

## Target architecture

```text
ChatGPT Plugin/App
-> authenticated Remote MCP adapter
-> server-side VoiceBridge credential injection
-> VoiceBridge MEDIA API
-> free-only providers
-> durable PostgreSQL on accepted free infrastructure
```

## Canonical MEDIA operation target

```text
13 total operations
9 non-execution/read/preflight/lookup/status/segments
4 start/execution operations
```

Execution operations:

```text
media_youtube_start
media_instagram_start
media_facebook_start
media_telegram_start
```

## R3-A — Contract freeze and secure adapter baseline

Status: **PASS / COMPLETE**.

Exact tool identities, mappings, schemas, annotations, consent, retry/idempotency, audit, error and secret boundaries were frozen. Execution tools were contractually defined but not exposed.

## R3-B — Inbound authentication and secret-boundary hardening

Status: **PASS / COMPLETE**.

```text
auth=OAuth authorization-code + PKCE S256
DCR=YES
scope=krc.mcp.read
owner secrets=server-side only
ChatGPT OAuth connection=PASS
```

Known R3-G debt: OAuth client/code/token persistence remains in-memory; restart/redeploy requires reconnect.

## R3-C — 9-tool non-execution VoiceBridge binding

Status: **PASS / COMPLETE**.

```text
surface=r3c_readonly
DISCOVERED_TOOL_COUNT=9
EXECUTION_TOOL_COUNT=0
VOICEBRIDGE_BEARER=SERVER_SIDE_ONLY
media_get_capabilities=PASS
media_youtube_preflight=PASS
media_youtube_lookup=PASS_EXPECTED_404_NOT_FOUND
provider_work_started=false
```

## R3-D — Consequential-action confirmation semantics

Status: **PASS / COMPLETE**.

Isolated write-style no-op probe proved:

```text
CHATGPT_CONFIRMATION_UI=PASS
APPROVE_PATH=PASS
CANCEL_PATH=PASS
NO_PRECONFIRM_EXECUTION=PASS
NO_EXECUTION_AFTER_DENY=PASS
NO_PROVIDER_WORK=PASS
NO_PROVIDER_CHARGE=PASS
NO_EXTERNAL_MUTATION=PASS
NO_REAL_MEDIA_START=PASS
```

## R3-E — Staged execution binding

### R3-E1 — YouTube

Status: **AUTHORIZED / PREPARED / BLOCKED_INFRASTRUCTURE**.

Prepared isolated contour:

```text
service=krc-mcp-r3e1-youtube-sentinel
surface=r3e1_youtube_execution
tool_count=10
non_execution_tool_count=9
execution_tool_count=1
execution_tool=media_youtube_start
other_execution_tools=not_enabled
```

The YouTube start contract requires explicit Gemini Developer API Free Tier consent and preserves the server-side VoiceBridge secret boundary.

One R3-E1 regression test failed in the first CI run because the test monkeypatched the old R3-C backend symbol. The binding-aligned test correction was committed as `3529cef70c54265ae49ee6ef21e1619c3ee34924`. No provider work was performed.

### R3-E1 infrastructure blocker

Render Free PostgreSQL `voicebridge-krc-media-beta-db` expired on 2026-09-17 and is suspended by billing. Paid upgrade is denied by project policy.

```text
RENDER_FREE_POSTGRES=REJECTED_FOR_DURABLE_STATE
R3_E1=BLOCKED_INFRASTRUCTURE
REAL_YOUTUBE_START=HOLD
```

No live `media_youtube_start` acceptance may run until a replacement durable PostgreSQL backend passes the free-only database gate.

### Free durable-state replacement order

```text
PRIMARY_CANDIDATE=NEON_FREE
SECONDARY_CANDIDATE=SUPABASE_FREE
INFRA_CONTROLLED_FALLBACK=OCI_ALWAYS_FREE_SELF_HOSTED_POSTGRES
```

Existing Neon Free candidate:

```text
project=krc-media-beta-neon
subscription=free_v3
postgres=18
database=krc_media_beta
storage_limit=512MiB
current_storage≈32MB
managed_jobs=0
client_jobs=0
stt_charges=10
```

Neon has the expected VoiceBridge tables but is not a full copy of the suspended Render database.

### R3-E1 database gate — next work

```text
1. schema/constraint/index parity audit against VoiceBridge persistence contract
2. durable/idempotency field audit
3. prepare server-side DATABASE_URL cutover to Neon Free
4. validate scale-to-zero and fail-closed behavior
5. bounded cutover only with required consequential approval
6. restart-resilient create/read/status/segments/replay validation
7. zero-paid-fallback and audit/charge validation
8. resume YouTube live execution acceptance only after PASS
```

### R3-E2 / E3 / E4

```text
R3_E2_INSTAGRAM=HOLD
R3_E3_FACEBOOK=HOLD
R3_E4_TELEGRAM=HOLD
```

R3-E1 authorization does not authorize these routes.

## R3-F — Full 13-operation parity regression

Status: **HOLD until all staged R3-E gates pass**.

## R3-G — Private operational hardening

Status: **HOLD**.

Required later: durable OAuth state, restart/reconnect validation, observability without secret leakage, rate/timeout/concurrency controls, cold-wake handling, rollback/credential rotation, deployment provenance, multi-session/web validation and permission re-check.

## R3-H — Migration/publication readiness

Status: **HOLD**.

Exit may only be `READY_FOR_OWNER_CUTOVER_DECISION` after complete private validation.

## R4 — Owner-approved cutover / migration / publication

Status: **HOLD**.

Requires separate explicit owner approval. Nothing in R3 authorizes public GPT mutation, Plugin publication/share, migration, `main` merge, PR #22 merge or VoiceBridge PR #45 merge.

## Current gate model

```text
R3-A: PASS
R3-B: PASS
R3-C: PASS
R3-D: PASS
R3-E1: AUTHORIZED / PREPARED / BLOCKED_INFRASTRUCTURE
R3-E2: HOLD
R3-E3: HOLD
R3-E4: HOLD
R3-F: HOLD
R3-G: HOLD
R3-H: HOLD
R4: HOLD
```

## Recovery command

`Віднови K-Research & Critic MEDIA з subprojects/media_beta/CURRENT_HANDOFF.md та checkpoint 126. R3-E1 заблокований durable-state infrastructure; проект FREE-ONLY; продовжуй з Neon Free migration preflight.`
