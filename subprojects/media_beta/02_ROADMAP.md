# MEDIA BETA Roadmap

Current roadmap for K-Research & Critic MEDIA after successful Remote Custom MCP canary validation, R3-A contract freeze, and R3-B authenticated Remote MCP hardening.

Version: 5.3
Status: **PLUGIN_FIRST / BOUNDED_CANARY_CLOSED_PASS / R3-A_PASS / R3-B_PASS / R3-C_AWAITING_OWNER_APPROVAL / PUBLICATION_HOLD**
Updated: 2026-09-16

## Product position

```text
public KRC Custom GPT: published / unchanged / protected
private MEDIA migration candidate: Remote Custom MCP / Plugin surface
backend: existing VoiceBridge MEDIA API
MEDIA semantic parity target: 13 operations
current authenticated MCP: isolated / one read-only canary tool / OAuth / no VoiceBridge binding
```

Critical invariant:

```text
MEDIA unavailable/fails -> MEDIA fails closed
Core KRC               -> remains usable
```

## Canonical current authority

1. `CURRENT_HANDOFF.md`
2. `117_R3B_AUTHENTICATED_REMOTE_MCP_HARDENING_PASS_2026_09_16.md`
3. `113_R3A_CONTRACT_FREEZE_SECURE_ADAPTER_BASELINE_PASS_2026_09_16.md`
4. `111_POST_CANARY_PLUGIN_MEDIA_ROADMAP_DECISION_2026_09_16.md`
5. current PR #22 head/CI

Historical checkpoints remain evidence, not the current continuation point.

## Proven baseline

```text
BOUNDED_CANARY_GATE=CLOSED_PASS
R3_A=PASS
R3_B=PASS
CHATGPT_OAUTH_CONNECTION=PASS
DISCOVERED_TOOL_COUNT=1
AUTHENTICATED_CANARY_INVOCATION=PASS
AUTH_LIVE_COMMIT=4b8d172a23b88415839ada0da84357c1538614db
AUTH_WORKFLOW=35138526850
AUTH_CI=PASS
```

## Target architecture

```text
ChatGPT Plugin/App
-> authenticated remote MCP adapter
-> server-side VoiceBridge credential injection
-> existing VoiceBridge MEDIA API
-> existing free-only provider routes + durable state
```

The no-auth canary remains evidence only and must never receive VoiceBridge credentials or become the production MEDIA surface.

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

Accepted:

- exact 13 tool identities and OpenAPI operation/path/method mappings;
- MCP classifications and annotations;
- request/response schema mapping;
- consent/retry/idempotency/audit/error/secret boundaries;
- Core failure isolation;
- execution tools contractually defined but not live-exposed.

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
one-tool discovery=PASS
authenticated canary invocation=PASS
VoiceBridge binding=NO
provider work=NO
execution tools=NO
```

The authorization callback CSP defect found during live owner flow was corrected with bounded callback-origin allowlisting; regression coverage and workflow `35138526850` PASS.

Known debt carried forward to R3-G:

```text
OAuth client/code/token persistence=in-memory only
restart/redeploy reconnect required
production readiness=NO
```

## R3-C — 9-tool non-execution VoiceBridge binding

Status: **PLANNED / NOT STARTED / SEPARATE OWNER EXECUTION APPROVAL REQUIRED**.

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

- use the authenticated MCP boundary proven in R3-B;
- inject the VoiceBridge bearer only server-side;
- never expose the bearer in model context, repo, schemas, tool arguments, errors, logs or evidence;
- exact schema/error mapping to the frozen R3-A contract;
- bounded timeout and fail-closed backend behavior;
- no automatic retry where contract forbids it;
- no start/execution operation exposed;
- no provider action beyond what the nine non-execution VoiceBridge operations inherently perform;
- real ChatGPT discovery/invocation validation of the 9-tool surface;
- preserve Core KRC availability if MEDIA backend fails.

Exit:

```text
AUTHENTICATED_9_TOOL_SURFACE=PASS
VOICEBRIDGE_SERVER_SIDE_BINDING=PASS
EXECUTION_TOOL_COUNT=0
SECRET_LEAKAGE=NO
CORE_ISOLATION=PASS
```

## R3-D — Consequential-action confirmation semantics

Status: HOLD until R3-C PASS and separate owner authorization.

Use a no-provider/no-charge execution probe or equivalent isolated mechanism to verify execution classification, confirmation/review, cancellation, replay behavior, and account-specific permissions without provider work.

## R3-E — Staged 4-route execution binding

Status: HOLD until R3-D PASS; each route requires a separate bounded execution gate.

Order:

```text
E1 YouTube
E2 Instagram
E3 Facebook
E4 Telegram
```

Each route must preserve authenticated MCP, server-side-only VoiceBridge secret, explicit confirmation/action review, durable idempotency, free-only/fail-closed provider policy, no automatic paid fallback, audit/charge evidence, and Core isolation.

## R3-F — Full 13-operation parity regression

Status: HOLD until R3-E PASS.

Required: exact 13-tool discovery/schema parity, positive/negative flows, consent, quota/provider unavailable, durable-state unavailable, replay/idempotency, error/secret sanitization, no paid fallback, Core regression and forced MEDIA-failure isolation.

## R3-G — Private operational hardening

Status: HOLD until R3-F PASS.

Required:

- durable OAuth client/token state or a production-grade external authorization service;
- restart/redeploy/reconnect validation;
- observability without secret leakage;
- rate/timeout/concurrency controls;
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
R3-C: PLANNED / NOT STARTED / OWNER APPROVAL REQUIRED
R3-D: HOLD
R3-E: HOLD
R3-F: HOLD
R3-G: HOLD
R3-H: HOLD
R4: HOLD
```

## Immediate decision point

No subsequent state-changing phase starts automatically.

The next executable block, only if separately approved, is **R3-C**:

```text
bind only 9 non-execution VoiceBridge operations
server-side bearer only
0 execution/start tools
no Plugin publish/share/migrate
no public GPT mutation
no PR #22 merge
no PR #45 merge
```

Recovery command:

`Віднови K-Research & Critic MEDIA з subprojects/media_beta/CURRENT_HANDOFF.md. R3-A PASS, R3-B PASS; continue only after owner approval for R3-C.`
