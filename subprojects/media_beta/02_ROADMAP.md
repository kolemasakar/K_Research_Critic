# MEDIA BETA Roadmap

Current roadmap for K-Research & Critic MEDIA after successful Remote Custom MCP canary validation, R3-A contract freeze, R3-B authenticated Remote MCP hardening, R3-C nine-tool read-only VoiceBridge binding, and R3-D consequential-action confirmation validation.

Version: 5.5
Status: **PLUGIN_FIRST / BOUNDED_CANARY_CLOSED_PASS / R3-A_PASS / R3-B_PASS / R3-C_PASS / R3-D_PASS / R3-E_AWAITING_OWNER_APPROVAL / PUBLICATION_HOLD**
Updated: 2026-09-17

## Product position

```text
public KRC Custom GPT: published / unchanged / protected
private MEDIA migration candidate: Remote Custom MCP / Plugin surface
backend: existing VoiceBridge MEDIA API
MEDIA semantic parity target: 13 operations
accepted R3-C surface: OAuth / 9 non-execution VoiceBridge tools / 0 execution tools
accepted R3-D surface: OAuth / 1 isolated no-op write-style confirmation probe
```

Critical invariant:

```text
MEDIA unavailable/fails -> MEDIA fails closed
Core KRC               -> remains usable
```

## Canonical current authority

1. `CURRENT_HANDOFF.md`
2. `124_R3D_CONSEQUENTIAL_ACTION_CONFIRMATION_PASS_2026_09_17.md`
3. `121_R3C_NINE_TOOL_READONLY_VOICEBRIDGE_BINDING_PASS_2026_09_16.md`
4. `117_R3B_AUTHENTICATED_REMOTE_MCP_HARDENING_PASS_2026_09_16.md`
5. `113_R3A_CONTRACT_FREEZE_SECURE_ADAPTER_BASELINE_PASS_2026_09_16.md`
6. current PR #22 head/CI

Historical checkpoints remain evidence, not the current continuation point.

## Proven baseline

```text
BOUNDED_CANARY_GATE=CLOSED_PASS
R3_A=PASS
R3_B=PASS
R3_C=PASS
R3_D=PASS
CHATGPT_OAUTH_CONNECTION=PASS
R3C_DISCOVERED_TOOL_COUNT=9
R3C_EXECUTION_TOOL_COUNT=0
VOICEBRIDGE_SERVER_SIDE_BINDING=PASS
R3D_CHATGPT_CONFIRMATION_UI=PASS
R3D_APPROVE_PATH=PASS
R3D_CANCEL_PATH=PASS
R3D_NO_PRECONFIRM_EXECUTION=PASS
```

## Target architecture

```text
ChatGPT Plugin/App
-> authenticated remote MCP adapter
-> server-side VoiceBridge credential injection
-> existing VoiceBridge MEDIA API
-> existing free-only provider routes + durable state
```

The no-auth canary and the isolated R3-D confirmation sentinel remain evidence-only surfaces. Neither is the production MEDIA execution surface.

## Canonical MEDIA operation target

13 operations total:

```text
9 non-execution/read/preflight/lookup/status/segments
4 execution/start operations
```

Execution operations:

```text
media_youtube_start
media_instagram_start
media_facebook_start
media_telegram_start
```

Canonical frozen contracts remain under `plugins/krc_migration_candidate/contracts/` at v0.2.

## R3-A — Contract freeze and secure adapter baseline

Status: **PASS / COMPLETE**.

Accepted exact 13-tool identities, mappings, schemas, annotations, consent/retry/idempotency/audit/error/secret boundaries, Core failure isolation, and execution tools contractually defined but not live-exposed.

Evidence: implementation head `2c6dd94527997507c4e77844a4d36383e1d281ef`, workflow `35133705040`, Python 3.13/3.14 and Quality Gates PASS.

## R3-B — Inbound authentication and secret-boundary hardening

Status: **PASS / COMPLETE**.

Accepted authenticated contour:

```text
service=krc-mcp-auth-sentinel
auth=OAuth authorization-code + PKCE S256
DCR=YES
scope=krc.mcp.read
owner secret=server-side only
ChatGPT OAuth connection=PASS
authenticated canary invocation=PASS
```

Known debt carried forward to R3-G: OAuth client/code/token persistence is in-memory only; restart/redeploy requires reconnect.

## R3-C — 9-tool non-execution VoiceBridge binding

Status: **PASS / COMPLETE**.

```text
surface=r3c_readonly
VOICEBRIDGE_BEARER=SERVER_SIDE_ONLY
AUTHENTICATED_9_TOOL_SURFACE=PASS
DISCOVERED_TOOL_COUNT=9
EXECUTION_TOOL_COUNT=0
START_OPERATIONS_EXPOSED=NO
SECRET_LEAKAGE=NO
```

Accepted live invocation evidence:

```text
media_get_capabilities=PASS
media_youtube_preflight=PASS
media_youtube_lookup=PASS_EXPECTED_404_NOT_FOUND
provider_work_started=false
new_job_created=false
start_execution_tools_called=false
```

The initial `media_get_capabilities` attempt surfaced a sanitized retryable `429` while the Render free VoiceBridge service was cold/asleep. No automatic retry occurred. After a read-only wake, one owner-controlled manual retry passed. The lookup `404` was confirmed as canonical `MEDIA_TRANSCRIPT_NOT_FOUND`, `retryable=false`.

Closure evidence: `121_R3C_NINE_TOOL_READONLY_VOICEBRIDGE_BINDING_PASS_2026_09_16.md`.

## R3-D — Consequential-action confirmation semantics

Status: **PASS / COMPLETE**.

Owner-approved isolated no-op write-style probe:

```text
service=krc-mcp-r3d-confirmation-sentinel
surface=r3d_confirmation_probe
tool=krc_r3d_noop_action_probe
readOnlyHint=false
destructiveHint=false
voicebridge_binding=not_enabled
provider_work=false
provider_charge=false
real_media_start=false
external_mutation=false
```

Accepted ChatGPT owner-account evidence:

```text
DISCOVERED_TOOL_COUNT=1
TOOL_CLASSIFICATION=WRITE
PRE_FIRST_CONFIRM_INVOCATION_COUNT=0
CHATGPT_CONFIRMATION_UI=PASS
APPROVE_PATH=PASS
POST_CONFIRM_INVOCATION_COUNT=1
CANCEL_PATH=PASS
POST_CANCEL_INVOCATION_COUNT=1
NO_PRECONFIRM_EXECUTION=PASS
NO_EXECUTION_AFTER_DENY=PASS
NO_PROVIDER_WORK=PASS
NO_PROVIDER_CHARGE=PASS
NO_EXTERNAL_MUTATION=PASS
NO_REAL_MEDIA_START=PASS
```

The first confirmed action used **Allow once** and produced exactly one no-op probe invocation. A second requested action was **Denied** in the confirmation UI; server-side invocation count remained exactly one.

Closure evidence: `124_R3D_CONSEQUENTIAL_ACTION_CONFIRMATION_PASS_2026_09_17.md`.

## R3-E — Staged 4-route execution binding

Status: **PLANNED / NOT STARTED / SEPARATE OWNER APPROVAL REQUIRED**.

Order:

```text
E1 YouTube
E2 Instagram
E3 Facebook
E4 Telegram
```

Each route is a separate bounded execution gate. Each must preserve authenticated MCP, server-side-only VoiceBridge secret, explicit confirmation/action review, durable idempotency, free-only/fail-closed provider policy, no automatic paid fallback, audit/charge evidence, and Core isolation.

R3-D PASS does **not** authorize any real `*_start` route by itself.

## R3-F — Full 13-operation parity regression

Status: HOLD until R3-E PASS.

Required: exact 13-tool discovery/schema parity, positive/negative flows, consent, quota/provider unavailable, durable-state unavailable, replay/idempotency, error/secret sanitization, no paid fallback, Core regression and forced MEDIA-failure isolation.

## R3-G — Private operational hardening

Status: HOLD until R3-F PASS.

Required:

- durable OAuth client/token state or production-grade external authorization service;
- restart/redeploy/reconnect validation;
- observability without secret leakage;
- rate/timeout/concurrency controls;
- Render cold/wake behavior handling;
- rollback and credential-rotation procedure;
- deployment provenance/pinning;
- multi-session/web validation;
- permission behavior re-check.

## R3-H — Migration/publication readiness

Status: HOLD until R3-G PASS.

Validate Core semantic parity, assets, sharing/audience model, metadata/privacy/distribution, old-link behavior, migration consequences and rollback/reconstruction package. Exit is only `READY_FOR_OWNER_CUTOVER_DECISION`.

## R4 — Owner-approved cutover / migration / publication

Status: HOLD.

Separate consequential gate. Only explicit owner approval after R3-H PASS may authorize Plugin publication/share, Custom GPT migration, public user switch, main merge, PR #22 merge, or VoiceBridge merge/promotion.

## Current gate model

```text
Bounded Remote MCP canary: CLOSED PASS
R3-A: PASS / COMPLETE
R3-B: PASS / COMPLETE
R3-C: PASS / COMPLETE
R3-D: PASS / COMPLETE
R3-E: PLANNED / NOT STARTED / OWNER APPROVAL REQUIRED
R3-F: HOLD
R3-G: HOLD
R3-H: HOLD
R4: HOLD
```

## Immediate decision point

No subsequent state-changing phase starts automatically.

The next executable block, only if separately approved, is **R3-E1 YouTube staged execution binding**. That approval would be limited to the YouTube route and must not implicitly authorize Instagram, Facebook, Telegram, publication, sharing, migration, or merges.

Recovery command:

`Віднови K-Research & Critic MEDIA з subprojects/media_beta/CURRENT_HANDOFF.md. R3-A, R3-B, R3-C and R3-D PASS; continue only after explicit owner approval for the next bounded R3-E execution gate.`
