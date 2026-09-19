# MEDIA BETA Roadmap

Version: 5.8
Status: **PLUGIN_FIRST / R3-A_PASS / R3-B_PASS / R3-C_PASS / R3-D_PASS / R3-E1_PASS / FREE_ONLY / PUBLICATION_HOLD**
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

1. `CURRENT_HANDOFF.md` — v17.2.
2. `129_R3E1_YOUTUBE_LIVE_DURABLE_REPLAY_IDEMPOTENCY_PASS_2026_09_19.md`.
3. `128_R3E1_RESTART_CONNECTIVITY_PASS_RECORD_REPLAY_PENDING_2026_09_19.md`.
4. `127_R3E1_NEON_CUTOVER_COMPLETE_DURABLE_ACCEPTANCE_PENDING_2026_09_19.md`.
5. `125_FREE_ONLY_INFRASTRUCTURE_POLICY_AND_POSTGRES_AUDIT_2026_09_17.md`.
6. `124_R3D_CONSEQUENTIAL_ACTION_CONFIRMATION_PASS_2026_09_17.md`.
7. `121_R3C_NINE_TOOL_READONLY_VOICEBRIDGE_BINDING_PASS_2026_09_16.md`.
8. current PR #22 / PR #45 head and CI.

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

Status: **HOLD / NEXT CANDIDATE**.

Before any Instagram execution:

```text
1. read-only route/provider preflight
2. confirm free-only retrieval and STT path
3. confirm no automatic paid fallback
4. confirm durable-store compatibility on Neon
5. expose only the Instagram execution tool in an isolated stage
6. require consequential-action confirmation
7. run bounded live acceptance only after owner authorization
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
R3-E2: HOLD
R3-E3: HOLD
R3-E4: HOLD
R3-F: HOLD
R3-G: HOLD
R3-H: HOLD
R4: HOLD
```

## Recovery command

`Віднови K-Research & Critic MEDIA з subprojects/media_beta/CURRENT_HANDOFF.md та checkpoint 129. R3-E1 YouTube PASS on Neon; R3-E2/E3/E4 remain HOLD.`
