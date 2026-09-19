# MEDIA BETA Roadmap

Version: 5.7
Status: **PLUGIN_FIRST / R3-A_PASS / R3-B_PASS / R3-C_PASS / R3-D_PASS / R3-E1_NEON_CUTOVER_COMPLETE_DURABLE_ACCEPTANCE_PENDING / FREE_ONLY / PUBLICATION_HOLD**
Updated: 2026-09-19

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

1. `CURRENT_HANDOFF.md` — v17.0.
2. `127_R3E1_NEON_CUTOVER_COMPLETE_DURABLE_ACCEPTANCE_PENDING_2026_09_19.md`.
3. `126_CHAT_TRANSITION_R3E1_FREE_ONLY_NEON_MIGRATION_GATE_2026_09_17.md` — historical transition.
4. `125_FREE_ONLY_INFRASTRUCTURE_POLICY_AND_POSTGRES_AUDIT_2026_09_17.md` — policy/incident baseline.
5. `124_R3D_CONSEQUENTIAL_ACTION_CONFIRMATION_PASS_2026_09_17.md`.
6. `121_R3C_NINE_TOOL_READONLY_VOICEBRIDGE_BINDING_PASS_2026_09_16.md`.
7. current PR #22 head/CI.

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

## Target architecture

```text
ChatGPT Plugin/App
-> authenticated Remote MCP adapter
-> server-side VoiceBridge credential injection
-> VoiceBridge MEDIA API
-> free-only providers
-> Neon Free PostgreSQL durable state
```

## Canonical MEDIA operation target

```text
13 total operations
9 non-execution/read/preflight/lookup/status/segments
4 start/execution operations
```

Execution operations remain `media_youtube_start`, `media_instagram_start`, `media_facebook_start`, `media_telegram_start`.

## R3-A — Contract freeze and secure adapter baseline

Status: **PASS / COMPLETE**.

## R3-B — Inbound authentication and secret-boundary hardening

Status: **PASS / COMPLETE**.

Known R3-G debt remains: OAuth client/code/token persistence is in-memory; restart/redeploy requires reconnect.

## R3-C — 9-tool non-execution VoiceBridge binding

Status: **PASS / COMPLETE / NOT PART OF CURRENT RECOVERY EXECUTION**.

The accepted historical read-only contour remains valid evidence. The owner instructed not to use R3-C during the current recovery sequence.

## R3-D — Consequential-action confirmation semantics

Status: **PASS / COMPLETE**.

Approve and cancel paths were previously proven with no provider work, charge, or external mutation before confirmation.

## R3-E — Staged execution binding

### R3-E1 — YouTube

Status: **AUTHORIZED / PREPARED / NEON CUTOVER COMPLETE / DURABLE RUNTIME ACCEPTANCE PENDING**.

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

No real `media_youtube_start` acceptance call is authorized until the database gate closes.

### Durable-state migration status

Render Free PostgreSQL remains rejected after expiry/suspension. Paid upgrade remains denied.

Neon Free is now the configured VoiceBridge durable target:

```text
project=krc-media-beta-neon
project_id=plain-snow-71973546
database=krc_media_beta
subscription=free_v3
schema_parity=PASS
VOICEBRIDGE_DATABASE_CUTOVER=COMPLETE
cutover_deploy=dep-dan5uf0ae00c73dke480
cutover_commit=3e8cb29b3815e1bf98f143682644899b801826e0
deploy_status=LIVE
health=PASS
post_deploy_error_scan=PASS
```

Post-cutover Neon state remains:

```text
managed_jobs=0
client_jobs=0
stt_charges=10
stt_seconds_total=285
```

### R3-E1 database gate — remaining work

```text
1. authenticated no-provider-work durable lookup/status probe
2. app-level Neon read proof
3. bounded durable create/read/status/segments acceptance
4. restart/cold-wake replay/idempotency validation
5. zero-paid-fallback and audit/charge validation
6. close database gate
7. resume YouTube live execution acceptance only after PASS
```

### R3-E2 / E3 / E4

```text
R3_E2_INSTAGRAM=HOLD
R3_E3_FACEBOOK=HOLD
R3_E4_TELEGRAM=HOLD
```

## R3-F — Full 13-operation parity regression

Status: **HOLD until all staged R3-E gates pass**.

## R3-G — Private operational hardening

Status: **HOLD**.

## R3-H — Migration/publication readiness

Status: **HOLD**.

## R4 — Owner-approved cutover / migration / publication

Status: **HOLD**.

## Current gate model

```text
R3-A: PASS
R3-B: PASS
R3-C: PASS
R3-D: PASS
R3-E1: AUTHORIZED / NEON CUTOVER COMPLETE / DURABLE RUNTIME ACCEPTANCE PENDING
R3-E2: HOLD
R3-E3: HOLD
R3-E4: HOLD
R3-F: HOLD
R3-G: HOLD
R3-H: HOLD
R4: HOLD
```

## Recovery command

`Віднови K-Research & Critic MEDIA з subprojects/media_beta/CURRENT_HANDOFF.md та checkpoint 127. Neon DATABASE_URL cutover COMPLETE; continue with authenticated no-provider durable runtime acceptance; real media_youtube_start remains HOLD.`
