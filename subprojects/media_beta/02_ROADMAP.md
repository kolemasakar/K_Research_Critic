# MEDIA BETA Roadmap

Current roadmap for K-Research & Critic MEDIA after successful Remote Custom MCP canary deployment, ChatGPT connection, one-tool discovery, and real ChatGPT-side invocation.

Version: 5.0
Status: **PLUGIN_FIRST / BOUNDED_CANARY_CLOSED_PASS / R3-A_READY / PUBLICATION_HOLD**
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
2. `111_POST_CANARY_PLUGIN_MEDIA_ROADMAP_DECISION_2026_09_16.md`
3. `110_CHATGPT_CUSTOM_MCP_CANARY_INVOCATION_PASS_2026_09_16.md`
4. current PR #22 head/CI

Historical checkpoints 78-109 remain evidence, not the current continuation point.

## Proven canary baseline

```text
MCP_CANARY_DEPLOYABLE=PASS
LIVE_MCP_DEPLOYMENT=PASS
EXTERNAL_PROTOCOL_VALIDATION=PASS
CHATGPT_MCP_CONNECTION=PASS
DISCOVERED_TOOL_COUNT=1
CHATGPT_CANARY_INVOCATION=PASS
BOUNDED_CANARY_GATE=CLOSED_PASS
```

Live evidence-only canary:

```text
service: krc-mcp-canary-sentinel
endpoint: https://krc-mcp-canary-sentinel.onrender.com/mcp
autoDeploy: off
auth: none, bounded canary only
tool: krc_media_capabilities_canary
VoiceBridge binding: not enabled
execution tools: not enabled
```

Final canary documentation head before roadmap planning:

```text
75a4b30e9f478fad892fafc017fea069ce949aec
workflow=35131580138
conclusion=SUCCESS
Python 3.13=PASS
Python 3.14=PASS
Quality gates=PASS
```

## Target architecture

```text
ChatGPT Plugin/App
-> authenticated remote MCP adapter
-> server-side VoiceBridge credential injection
-> existing VoiceBridge MEDIA API
-> existing free-only provider routes + durable state
```

The current no-auth canary must never receive VoiceBridge credentials or become the production MEDIA surface.

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

Canonical contracts:

```text
plugins/krc_migration_candidate/contracts/media_tools.yaml
plugins/krc_migration_candidate/contracts/media_adapter.yaml
plugins/krc_migration_candidate/contracts/auth_transport_binding.yaml
plugins/krc_migration_candidate/contracts/migration_acceptance.yaml
```

## R3-A — Contract freeze and secure adapter baseline

Status: **READY / NEXT IMPLEMENTATION GATE**.

Repository-only scope:

- freeze exact 13-tool names and schemas;
- reconcile the contracts with the proven Remote MCP surface;
- classify tool annotations and action semantics;
- freeze structured error, retry/idempotency, consent, audit, and secret boundaries;
- preserve exact Core skill parity;
- no deployment, provider call, VoiceBridge credential, or public surface mutation.

Exit: repository/CI PASS.

## R3-B — Inbound authentication and secret-boundary hardening

Status: HOLD until R3-A PASS.

Before any real VoiceBridge binding:

- revalidate current account authentication options;
- move away from canary-only `No authentication`;
- require authenticated access to any MCP that can reach VoiceBridge;
- keep VoiceBridge bearer server-side only;
- prove no secret leakage through args/descriptions/repo/logs/evidence/errors.

Exit: authenticated isolated MCP connection PASS with no provider/backend binding yet.

## R3-C — 9-tool non-execution VoiceBridge binding

Status: HOLD until R3-B PASS.

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

Status: HOLD until R3-C PASS.

Use a no-provider/no-charge execution probe or equivalent isolated mechanism to verify:

- execution is not classified as read-only;
- ChatGPT asks/reviews where required;
- cancellation produces no provider work;
- replay does not duplicate execution;
- permission behavior is recorded as account-specific evidence.

Exit: action-confirmation semantics PASS without provider work.

## R3-E — Staged 4-route execution binding

Status: HOLD until R3-D PASS.

Order:

```text
E1 YouTube
E2 Instagram
E3 Facebook
E4 Telegram
```

Each route is an independent owner-gated real-execution canary and must preserve:

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
Historical R0-R2 backend/product work: preserved as evidence
Bounded Remote MCP canary: CLOSED PASS
R3-A: READY
R3-B: HOLD
R3-C: HOLD
R3-D: HOLD
R3-E: HOLD
R3-F: HOLD
R3-G: HOLD
R3-H: HOLD
R4: HOLD
```

## Immediate continuation point

```text
R3-A ONLY
- repository-only contract freeze
- secure adapter baseline
- no deployment
- no VoiceBridge secret binding
- no provider work
- no execution tools
- no public GPT change
- no Plugin publish/share/migrate
- no PR #22 merge
- no PR #45 merge
```

Recovery command:

`Віднови K-Research & Critic MEDIA з subprojects/media_beta/CURRENT_HANDOFF.md і продовжуй з R3-A contract freeze / secure adapter baseline.`
