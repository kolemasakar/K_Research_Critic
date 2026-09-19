# MEDIA BETA Roadmap

Version: 6.5
Status: **PLUGIN_FIRST / R3-A_PASS / R3-B_PASS / R3-C_PASS / R3-D_PASS / R3-E1_PASS / R3-E2_LIVE_CANARY_PASS_RESTART_IDEMPOTENCY_PENDING / FREE_ONLY / PUBLICATION_HOLD**
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
Render Free Web        -> accepted hosting layer
Render PostgreSQL      -> rejected for durable state
Neon Free PostgreSQL   -> primary durable database
paid infrastructure    -> not accepted as required dependency
paid provider fallback -> forbidden
```

## Canonical current authority

1. `CURRENT_HANDOFF.md` — v17.9.
2. `137_R3E2_INSTAGRAM_LIVE_CANARY_DURABLE_FREE_ONLY_PASS_2026_09_19.md`.
3. `136_R3E2_ATTEMPT1_TRANSIENT_COLD_START_REMEDIATION_PASS_RECONNECT_REQUIRED_2026_09_19.md`.
4. `135_R3E2_CREDENTIAL_ROTATION_PROBE_DISABLED_LIVE_CANARY_READY_2026_09_19.md`.
5. `134_R3E2_CHATGPT_CONFIRMATION_UI_PASS_ZERO_SIDE_EFFECT_2026_09_19.md`.
5. `133_FREE_ONLY_INFRASTRUCTURE_POLICY_RENDER_WEB_ALLOWED_POSTGRES_REJECTED_2026_09_19.md`.
6. `132_R3E2_ISOLATED_SENTINEL_AUTHENTICATED_PREFLIGHT_PASS_CONFIRMATION_PENDING_2026_09_19.md`.
7. `131_R3E2_INSTAGRAM_READONLY_FREE_ONLY_PREFLIGHT_2026_09_19.md`.
8. `130_POST_R3E1_CONTROL_POINT_BEFORE_R3E2_2026_09_19.md`.
9. `129_R3E1_YOUTUBE_LIVE_DURABLE_REPLAY_IDEMPOTENCY_PASS_2026_09_19.md`.
10. `128_R3E1_RESTART_CONNECTIVITY_PASS_RECORD_REPLAY_PENDING_2026_09_19.md`.
11. `127_R3E1_NEON_CUTOVER_COMPLETE_DURABLE_ACCEPTANCE_PENDING_2026_09_19.md`.
12. `125_FREE_ONLY_INFRASTRUCTURE_POLICY_AND_POSTGRES_AUDIT_2026_09_17.md`.
13. `124_R3D_CONSEQUENTIAL_ACTION_CONFIRMATION_PASS_2026_09_17.md`.
14. `121_R3C_NINE_TOOL_READONLY_VOICEBRIDGE_BINDING_PASS_2026_09_16.md`.
15. current PR #22 / PR #45 head and CI.

## Proven baseline

```text
R3_A=PASS
R3_B=PASS
R3_C=PASS
R3_D=PASS
R3_E1=PASS
```

R3-E1 proves a consented YouTube Free-Tier start, Neon durable persistence, VoiceBridge+R3-E1 restart replay, status+segments reads, duplicate-start reuse, zero paid fallback evidence and zero error logs in the acceptance window.

## Cost and provider policy

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
AUTOMATIC_PAID_RETRIEVAL=false
AUTOMATIC_PAID_STT=false
AUTOMATIC_PAID_PROXY=false
UNEXPECTED_BILLING_RISK=DENIED
```

Render Free Web Services remain part of the target architecture. The rejected Render dependency is specifically Render PostgreSQL as durable storage.

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

Known R3-G debt: OAuth client/code/token persistence is in-memory; restart/redeploy requires reconnect.

## R3-C — 9-tool non-execution VoiceBridge binding

Status: **PASS / COMPLETE / HISTORICAL ACCEPTED EVIDENCE**.

R3-C was intentionally not used during the 2026-09-19 Neon/R3-E1 recovery path.

## R3-D — Consequential-action confirmation semantics

Status: **PASS / COMPLETE**.

## R3-E — Staged execution binding

### R3-E1 — YouTube

Status: **PASS / COMPLETE**.

Accepted contour:

```text
service=krc-mcp-r3e1-youtube-sentinel
surface=r3e1_youtube_execution
tool_count=10
execution_tool_count=1
execution_tool=media_youtube_start
other_execution_tools=not_enabled
Neon_durable_backend=PASS
live_start=PASS
restart_replay=PASS
duplicate_start_reuse=PASS
paid_fallback=NO
```

Temporary acceptance startup probes are disabled in the final runtime.

### R3-E2 — Instagram

Status: **LIVE CANARY PASS / DURABLE NEON PASS / FREE-ONLY PASS / RESTART + IDEMPOTENCY PENDING**.

Accepted:

```text
route=Instagram -> OCI self-hosted Cobalt -> AssemblyAI universal-2 -> Neon
route-scoped bearer=PASS
isolated MCP surface=PASS
tool_count=5
execution_tool=media_instagram_start only
authenticated preflight=PASS
durable lookup=PASS_EMPTY
retrieval_credits=0
automatic_paid_fallback=false
provider_work=false
start_called=false
server-side confirmation contract=PASS
ChatGPT confirmation UI=PASS
cancel path=PASS
no execution after deny=PASS
approve path=PASS
exactly one invocation after approve=PASS
zero-side-effect confirmation probe=PASS
provider work=false
real media start=false
```

Attempt 1 / remediation:

```text
attempt_1=HTTP 429 retryable
failure_stage=PRE_PROVIDER
Neon_job=false
Cobalt_work=false
AssemblyAI_work=false
VoiceBridge_health_during_incident=503

VoiceBridge_health_outside_global_limiter=PASS
R3E2_health_warmup_before_start=PASS
AUTO_RETRY_CONSEQUENTIAL_POST=false
VoiceBridge_Validate_822=SUCCESS
R3E2_Tests_1717=SUCCESS
patched_runtimes=LIVE
```

Live retry accepted:

```text
job_id=KRCM_04e6d847-449c-4d0f-82c7-b494871d9322
status=COMPLETED
provider=assemblyai
provider_mode=cobalt_retrieval_stt
retrieval_provider=cobalt
segment_count=1
credits_charged=0
retrieval_credits_charged=0
metadata_credits_charged=0
credit_charge_uncertain=false
provider_data_deleted=true
```

Remaining acceptance:

```text
1. VoiceBridge restart replay
2. R3-E2 restart/reconnect replay
3. status + segments read after restart
4. duplicate-start idempotency with separate owner confirmation
5. final error scan and R3-E2 closure
```

### R3-E3 — Facebook

Status: **HOLD**.

### R3-E4 — Telegram

Status: **HOLD**.

## R3-F — Full 13-operation parity regression

Status: **HOLD until R3-E2/E3/E4 close**.

## R3-G — Private operational hardening

Status: **HOLD**.

Known debt includes OAuth-state persistence across restart/redeploy.

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
R3-E1: PASS
R3-E2: LIVE CANARY PASS / RESTART + IDEMPOTENCY PENDING
R3-E3: HOLD
R3-E4: HOLD
R3-F: HOLD
R3-G: HOLD
R3-H: HOLD
R4: HOLD
```

## Recovery command

`Віднови K-Research & Critic MEDIA з subprojects/media_beta/CURRENT_HANDOFF.md та checkpoint 137. R3-E1 PASS; R3-E2 live Instagram canary PASS via Cobalt -> AssemblyAI -> Neon; durable COMPLETED job with one segment and zero paid/retrieval credits; restart replay and duplicate-start idempotency remain pending.`
