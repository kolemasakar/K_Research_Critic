# MEDIA BETA Documentation Index

Canonical documentation index for K-Research & Critic MEDIA BETA / Plugin migration work.

Version: 7.1
Status: **ACTIVE / PLUGIN_FIRST / BOUNDED_CANARY_CLOSED_PASS / R3-A_PLANNED_NOT_STARTED / PUBLICATION_HOLD**
Updated: 2026-09-16

## Product boundary

```text
public KRC Custom GPT: published / unchanged
MEDIA migration candidate: private Remote Custom MCP / Plugin surface
backend authority: existing VoiceBridge MEDIA API
canonical MEDIA parity target: 13 operations
```

Critical invariant:

```text
MEDIA unavailable/fails -> MEDIA fails closed
Core KRC               -> remains usable and accessible
```

## Canonical current reading order

1. `CURRENT_HANDOFF.md` — v11.1; current recovery authority.
2. `111_POST_CANARY_PLUGIN_MEDIA_ROADMAP_DECISION_2026_09_16.md` — approved post-canary roadmap.
3. `02_ROADMAP.md` — v5.1; active gate sequence R3-A through R4.
4. `110_CHATGPT_CUSTOM_MCP_CANARY_INVOCATION_PASS_2026_09_16.md` — completed ChatGPT-side invocation PASS.
5. `109_CHATGPT_CUSTOM_MCP_CONNECTION_DISCOVERY_PASS_2026_09_16.md` — owner-account connection and one-tool discovery PASS.
6. `108_SENTINEL_REMOTE_MCP_CANARY_LIVE_DEPLOYMENT_CONNECTION_BLOCKED_2026_09_16.md` — live endpoint validation and historical auth-context blocker.
7. `107_KRC_DEPLOYABLE_REMOTE_MCP_CANARY_REPO_ACCEPTANCE_2026_09_16.md` — deployable package acceptance.
8. `102_KRC_P100_ACCOUNT_SURFACE_INSPECTION_RESULT_2026_09_16.md` — account-specific Plugin/custom MCP surface evidence.
9. `102_OPENAI_RETIREMENT_RESEARCH_INTEGRATION_ACCEPTANCE_HARDENING_2026_09_16.md` — migration acceptance hardening.

Older checkpoints remain historical evidence and are not the current continuation point.

## Current repository / PR

```text
repository: kolemasakar/K_Research_Critic
branch: agent/krc-public-media-r3-integration
PR: #22
base: main
state: OPEN / DRAFT / UNMERGED
```

Final bounded-canary baseline before roadmap planning:

```text
head: 75a4b30e9f478fad892fafc017fea069ce949aec
workflow: 35131580138
result: SUCCESS
Python 3.13: PASS
Python 3.14: PASS
Quality gates: PASS
```

## Proven Remote MCP canary state

```text
MCP_CANARY_DEPLOYABLE=PASS
LIVE_MCP_DEPLOYMENT=PASS
EXTERNAL_PROTOCOL_VALIDATION=PASS
CHATGPT_MCP_CONNECTION=PASS
CHATGPT_DISCOVERED_TOOL_COUNT=1
CHATGPT_CANARY_INVOCATION=PASS
BOUNDED_CANARY_GATE=CLOSED_PASS
```

Live evidence-only canary:

```text
name: KRC MCP Canary Sentinel
endpoint: https://krc-mcp-canary-sentinel.onrender.com/mcp
autoDeploy: off
authentication: No authentication, bounded canary only
tool: krc_media_capabilities_canary
VoiceBridge binding: not enabled
execution tools: not enabled
provider work: false
```

This canary must not receive VoiceBridge credentials or become the production MEDIA surface.

## Target architecture

```text
ChatGPT Plugin/App
-> authenticated remote MCP adapter
-> server-side VoiceBridge credential injection
-> existing VoiceBridge MEDIA API
-> existing free-only provider routes + durable state
```

## Canonical migration contracts

```text
plugins/krc_migration_candidate/contracts/media_tools.yaml
plugins/krc_migration_candidate/contracts/media_adapter.yaml
plugins/krc_migration_candidate/contracts/auth_transport_binding.yaml
plugins/krc_migration_candidate/contracts/migration_acceptance.yaml
plugins/krc_migration_candidate/contracts/surface_decision_matrix.yaml
```

Current semantic target:

```text
13 total MEDIA operations
9 non-execution operations
4 start/execution operations
```

## Active roadmap gates

```text
R3-A  Contract freeze / secure adapter baseline            PLANNED / NOT STARTED
R3-B  Inbound auth + secret-boundary hardening             HOLD
R3-C  9-tool non-execution VoiceBridge binding             HOLD
R3-D  Consequential-action confirmation semantics          HOLD
R3-E  Staged 4-route execution binding                     HOLD
R3-F  Full 13-operation parity regression                  HOLD
R3-G  Private operational hardening                        HOLD
R3-H  Migration/publication readiness                      HOLD
R4    Owner-approved cutover/migration/publication         HOLD
```

Roadmap planning approval does not automatically authorize R3-A implementation. A separate execution approval is required.

## Immediate decision point

If separately approved, R3-A is repository-only.

Required:

- freeze/reconcile exact 13-tool names and schemas;
- freeze annotations, consent, retry/idempotency, audit, error and secret boundaries;
- preserve exact Core skill parity;
- pass repository CI.

Forbidden in R3-A:

```text
new live deployment
live canary mutation
VoiceBridge secret binding
provider calls
real execution/start tools
public GPT mutation
Plugin publish/share/migrate
main mutation
PR #22 merge
VoiceBridge PR #45 merge
```

## Historical backend/provider evidence

Earlier backend/provider checkpoints remain valid historical evidence for VoiceBridge, Cobalt, Gemini, Instagram/Facebook/Telegram routing, free-only policy, durable KRCM jobs, and Core isolation requirements. They do not override the current Plugin-first continuation point.

Current policy remains:

```text
paid retrieval fallback: false
paid STT fallback: false
paid proxy fallback: false
automatic retry loop: false
user cookies/login fallback: forbidden
YouTube paid/Cobalt/AssemblyAI fallback: forbidden
```

## Recovery command

`Віднови K-Research & Critic MEDIA з subprojects/media_beta/CURRENT_HANDOFF.md. Roadmap approved; R3-A planned but not started.`
