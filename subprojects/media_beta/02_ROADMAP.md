# MEDIA BETA Roadmap

Current roadmap for K-Research & Critic MEDIA after successful Remote Custom MCP canary validation and completion of the R3-A repository contract freeze.

Version: 5.2
Status: **PLUGIN_FIRST / BOUNDED_CANARY_CLOSED_PASS / R3-A_PASS / R3-B_AWAITING_OWNER_APPROVAL / PUBLICATION_HOLD**
Updated: 2026-09-16

## Product position

```text
public KRC Custom GPT: published / unchanged / protected
private MEDIA migration candidate: Remote Custom MCP / Plugin surface
backend: existing VoiceBridge MEDIA API
MEDIA semantic parity target: 13 operations
current live canary: evidence-only / one tool / no auth / no VoiceBridge binding
```

Critical invariant:

```text
MEDIA unavailable/fails -> MEDIA fails closed
Core KRC               -> remains usable
```

## Canonical current authority

1. `CURRENT_HANDOFF.md`
2. `113_R3A_CONTRACT_FREEZE_SECURE_ADAPTER_BASELINE_PASS_2026_09_16.md`
3. `111_POST_CANARY_PLUGIN_MEDIA_ROADMAP_DECISION_2026_09_16.md`
4. `110_CHATGPT_CUSTOM_MCP_CANARY_INVOCATION_PASS_2026_09_16.md`
5. current PR #22 head/CI

Historical checkpoints remain evidence, not the current continuation point.

## Proven baseline

```text
BOUNDED_CANARY_GATE=CLOSED_PASS
CHATGPT_MCP_CONNECTION=PASS
CHATGPT_CANARY_INVOCATION=PASS
R3_A_CONTRACT_FREEZE=PASS
R3_A_SECURE_ADAPTER_BASELINE=PASS
R3_A_IMPLEMENTATION_HEAD=2c6dd94527997507c4e77844a4d36383e1d281ef
R3_A_WORKFLOW=35133705040
R3_A_CI=PASS
```

## Target architecture

```text
ChatGPT Plugin/App
-> authenticated remote MCP adapter
-> server-side VoiceBridge credential injection
-> existing VoiceBridge MEDIA API
-> existing free-only provider routes + durable state
```

The current no-auth canary remains evidence only and must never receive VoiceBridge credentials or become the production MEDIA surface.

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

Canonical frozen contracts:

```text
plugins/krc_migration_candidate/contracts/media_tools.yaml              v0.2
plugins/krc_migration_candidate/contracts/media_adapter.yaml            v0.2
plugins/krc_migration_candidate/contracts/auth_transport_binding.yaml   v0.2
plugins/krc_migration_candidate/contracts/migration_acceptance.yaml     v0.2
plugins/krc_migration_candidate/contracts/surface_decision_matrix.yaml  v0.2
```

## R3-A — Contract freeze and secure adapter baseline

Status: **PASS / COMPLETE**.

Accepted evidence:

```text
selected_surface=custom_remote_mcp
transport=remote_mcp_http
protocol_version=2026-07-28
operation_count=13
non_execution_count=9
execution_count=4
inbound_auth=R3_B_REQUIRED_BEFORE_VOICEBRIDGE_BINDING
voicebridge_bearer=SERVER_SIDE_ONLY
execution_tools_exposed=NO
provider_work=NO
runtime_mutation=NO
```

R3-A froze:

- exact 13 tool identities and OpenAPI operation/path/method mappings;
- MCP classification and annotations;
- request/response schema mapping;
- YouTube explicit consent boundary;
- retry/idempotency semantics;
- audit fields;
- structured error and secret-sanitization boundaries;
- Core failure isolation;
- Remote MCP selection based on the proven owner-account canary.

Exit evidence: implementation head `2c6dd94527997507c4e77844a4d36383e1d281ef`, workflow `35133705040`, Python 3.13/3.14 and Quality Gates PASS.

## R3-B — Inbound authentication and secret-boundary hardening

Status: **PLANNED / NOT STARTED / SEPARATE OWNER EXECUTION APPROVAL REQUIRED**.

Goal: replace the canary-only `No authentication` model before any VoiceBridge binding.

Required:

- revalidate current owner-account Plugin authentication options at execution time;
- select and implement an authenticated isolated Remote MCP mode supported by the actual account surface;
- require authenticated access for any future endpoint that can reach VoiceBridge;
- preserve server-side-only VoiceBridge bearer boundary;
- prove no secret leakage through args, descriptions, repository, logs, evidence, or errors;
- prove auth failure fails closed without secret detail;
- keep the existing public no-auth canary separate and unchanged;
- do not bind VoiceBridge or call providers during R3-B.

Exit: authenticated isolated MCP endpoint/connection PASS + secret-sanitization PASS, with no VoiceBridge/provider binding.

## R3-C — 9-tool non-execution VoiceBridge binding

Status: HOLD until R3-B PASS and separate owner authorization.

Target operations:

```text
media_get_capabilities
media_youtube_preflight
media_youtube_lookup
media_youtube_status
media_youtube_segments
media_instagram_preflight
media_instagram_lookup
media_non_youtube_status
media_non_youtube_segments
```

Requirements:

- server-side VoiceBridge bearer injection;
- exact schema/error mapping;
- bounded timeout;
- no automatic retry;
- no start operation exposed;
- real ChatGPT discovery/invocation validation.

Exit: 9-tool parity PASS with zero execution-tool exposure.

## R3-D — Consequential-action confirmation semantics

Status: HOLD until R3-C PASS and separate owner authorization.

Use a no-provider/no-charge execution probe or equivalent isolated mechanism to verify:

- execution is not classified as read-only;
- ChatGPT asks/reviews where required;
- cancellation produces no provider work;
- replay does not duplicate execution;
- permission behavior is recorded as account-specific evidence.

Exit: action-confirmation semantics PASS without provider work.

## R3-E — Staged 4-route execution binding

Status: HOLD until R3-D PASS; each route requires a separate bounded execution gate.

Order:

```text
E1 YouTube
E2 Instagram
E3 Facebook
E4 Telegram
```

Each route must preserve:

- authenticated MCP boundary;
- server-side-only VoiceBridge secret;
- explicit confirmation/action review;
- durable job/idempotency behavior;
- free-only/fail-closed provider policy;
- no automatic paid fallback;
- audit/charge evidence;
- Core isolation.

YouTube additionally requires explicit Gemini Free data-use consent before start.

Exit: all four start routes independently PASS.

## R3-F — Full 13-operation parity regression

Status: HOLD until R3-E PASS.

Required:

- exact 13-tool discovery/schema parity;
- positive flow regression;
- invalid input/platform/job/pagination;
- consent missing;
- free quota/provider unavailable;
- durable-state unavailable;
- charge-uncertain replay block;
- retry/idempotency;
- secret/error sanitization;
- no paid/unapproved fallback;
- Core regression and forced MEDIA failure isolation;
- model-agnostic behavior and representative entry points.

Exit: private full-parity Plugin PASS.

## R3-G — Private operational hardening

Status: HOLD until R3-F PASS.

Required:

- production-like authenticated endpoint separate from canary;
- observability without secret leakage;
- rate/timeout/concurrency controls;
- rollback and credential-rotation procedure;
- deployment provenance/pinning;
- reconnect/recovery validation;
- multi-session/web validation;
- permission behavior re-check.

Exit: private operational readiness PASS.

## R3-H — Migration/publication readiness

Status: HOLD until R3-G PASS.

While public KRC remains unchanged:

- validate exact Core semantic parity;
- enumerate/validate reference assets;
- validate intended sharing/audience model;
- prepare Plugin metadata/privacy/distribution state;
- document old-link behavior;
- revalidate current migration consequences and account notice/UI;
- prepare rollback/reconstruction package.

Exit: `READY_FOR_OWNER_CUTOVER_DECISION` only.

## R4 — Owner-approved cutover / migration / publication

Status: HOLD.

Separate consequential gate. Only explicit owner approval after R3-H PASS may authorize any of:

```text
Plugin publication/share
Custom GPT migration
public user switch
main merge
PR #22 merge
VoiceBridge merge/promotion
```

## Current gate model

```text
Bounded Remote MCP canary: CLOSED PASS
R3-A: PASS / COMPLETE
R3-B: PLANNED / NOT STARTED / OWNER APPROVAL REQUIRED
R3-C: HOLD
R3-D: HOLD
R3-E: HOLD
R3-F: HOLD
R3-G: HOLD
R3-H: HOLD
R4: HOLD
```

## Immediate decision point

R3-A is closed. No subsequent state-changing phase starts automatically.

The next executable block, only if separately approved, is **R3-B**:

```text
authenticated isolated Remote MCP hardening
no VoiceBridge credential binding
no provider work
no 9-tool backend binding yet
no execution tools
no live canary mutation
no public GPT change
no Plugin publish/share/migrate
no PR #22 merge
no PR #45 merge
```

Recovery command:

`Віднови K-Research & Critic MEDIA з subprojects/media_beta/CURRENT_HANDOFF.md. R3-A PASS; continue only after owner approval for R3-B.`
