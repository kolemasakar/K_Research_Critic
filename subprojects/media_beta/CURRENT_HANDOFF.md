# KRC MEDIA — CURRENT HANDOFF

Version: 7.0
Status: ACTIVE_HANDOFF / DEPLOYABLE_REMOTE_MCP_CANARY_ACCEPTED / SENTINEL_CONNECTION_GATE_READY / PUBLICATION_HOLD
Date: 2026-09-16

## Recovery command

`Віднови K-Research & Critic MEDIA з subprojects/media_beta/CURRENT_HANDOFF.md і продовжуй з Sentinel bounded Remote MCP canary deployment/connection gate.`

## Canonical recovery files

1. `subprojects/media_beta/CURRENT_HANDOFF.md`
2. `subprojects/media_beta/107_KRC_DEPLOYABLE_REMOTE_MCP_CANARY_REPO_ACCEPTANCE_2026_09_16.md`
3. `subprojects/media_beta/106_SENTINEL_TO_KRC_MCP_CANARY_HANDOFF_2026_09_16.md`
4. `subprojects/media_beta/105_KRC_REMOTE_MCP_CANARY_SENTINEL_SYNC_2026_09_16.md`
5. `subprojects/media_beta/104_KRC_REMOTE_MCP_CANARY_REPO_ACCEPTANCE_2026_09_16.md`
6. current PR #22 head/CI and current non-secret account/control-plane evidence

Older P101 handoffs remain historical recovery evidence only and are superseded for current phase selection.

## Repository / PR

```text
repository=kolemasakar/K_Research_Critic
PR=22
branch=agent/krc-public-media-r3-integration
base=main
state=OPEN / DRAFT / UNMERGED
```

Validated implementation state before checkpoint 107 documentation:

```text
head=4a75f53d6da956d9b2eb7acc1b6f788824bb6e03
workflow=35126692392
conclusion=SUCCESS
Tests / Python 3.13=PASS
Tests / Python 3.14=PASS
Quality gates=PASS
```

At recovery always refetch current PR metadata and latest CI because documentation commits advance the branch.

## Accepted state

```text
PROJECT=ACTIVE
PLUGIN_FIRST_STRATEGY=ACCEPTED
LEGACY_MEDIA_ACTION_CREATION=HOLD
SURFACE_CLASSIFICATION=REMOTE_CUSTOM_MCP_CANDIDATE
MCP_CANARY_REPO_ACCEPTED=PASS
MCP_CANARY_DEPLOYABLE=PASS
CANARY_TOOL_COUNT=1
CANARY_MUTATION=false
CANARY_PROVIDER_WORK=false
CANARY_VOICEBRIDGE_BINDING=false
CANARY_EXECUTION_TOOLS=false
MODERN_MCP_2026_07_28=PASS
DEPLOYMENT_PACKAGE=PASS
LIVE_DEPLOYMENT=NO
REMOTE_ENDPOINT_READY_FOR_CONNECTION_TEST=NO
CHATGPT_MCP_CONNECTION=NO
SCAN_TOOLS=NO
```

## Deployable canary package

Canonical files:

```text
plugins/krc_migration_candidate/mcp_canary/server.py
plugins/krc_migration_candidate/mcp_canary/http_server.py
plugins/krc_migration_candidate/mcp_canary/Dockerfile
plugins/krc_migration_candidate/mcp_canary/README.md
tests/test_krc_mcp_canary.py
tests/test_krc_mcp_canary_http.py
```

Canary endpoint contract after deployment:

```text
MCP_PATH=/mcp
HEALTH_PATH=/healthz
TRANSPORT=remote stateless HTTP behind HTTPS termination
TOOL=krc_media_capabilities_canary
```

No live endpoint or deployment target exists yet.

## Protocol / security boundary

```text
MCP_PROTOCOL_VERSION=2026-07-28
SERVER_DISCOVER=SUPPORTED
HEADER_BODY_VALIDATION=ENABLED
ORIGIN_VALIDATION=FAIL_CLOSED_WHEN_ORIGIN_PRESENT
LEGACY_INITIALIZE_2025_11_25=BOUNDED_COMPATIBILITY
AUTH_MODE=CONNECTION_STAGE_SELECTION_REQUIRED
REPOSITORY_SECRET=NO
MODEL_VISIBLE_SECRET=NO
VOICEBRIDGE_BEARER_REUSE=FORBIDDEN
```

The package supports `none` only for an explicitly isolated bounded canary test or an authenticated outer tunnel/proxy, and env-backed bearer as an implementation option. Final owner-account compatible authentication remains a Sentinel connection-stage decision.

## Core / MEDIA invariants

```text
CURRENT_PUBLIC_GPT=UNCHANGED
MEDIA_OPERATION_PARITY_COUNT=13
FULL_13_MEDIA_BINDING=NOT_STARTED
MEDIA_PROVIDER_WORK=DENIED_FOR_CANARY
VOICEBRIDGE_SECRET_BINDING=DENIED
CORE_SKILL_PARITY=PASS
MEDIA_FREE_ONLY_FAIL_CLOSED=UNCHANGED
MEDIA_FAILURE_CORE_ISOLATION=UNCHANGED
```

Canonical contracts remain:

- `plugins/krc_migration_candidate/contracts/migration_acceptance.yaml`
- `plugins/krc_migration_candidate/contracts/surface_decision_matrix.yaml`
- `plugins/krc_migration_candidate/contracts/auth_transport_binding.yaml`
- `plugins/krc_migration_candidate/contracts/media_tools.yaml`
- `plugins/krc_migration_candidate/contracts/media_adapter.yaml`
- `prompts/GPT_STORE_INSTRUCTIONS.md`
- `plugins/krc_migration_candidate/skills/krc_core/SKILL.md`

## Ownership / next gate

KRC application engineering for the first deployable read-only canary is complete.

Sentinel Remote owns the next state-changing control-plane phase only after explicit owner authorization:

```text
select isolated deployment target
-> verify target is non-production
-> deploy only accepted canary package
-> verify HTTPS/network/auth boundary
-> connect owner-account custom remote MCP
-> Scan Tools and discover exactly one canary tool
-> optionally invoke only krc_media_capabilities_canary
-> record non-secret evidence
-> STOP
```

If the account/tool surface has changed, revalidate it before connection. Do not reuse old sessions, URLs, tunnel IDs or credentials.

## Hard boundary

```text
FULL_MEDIA_13_TOOL_DEPLOYMENT=DENIED
VOICEBRIDGE_SECRET_BINDING=DENIED
MEDIA_PROVIDER_WORK=DENIED
WRITE_EXECUTION_TOOL_TEST=DENIED
PUBLIC_GPT_CHANGE=DENIED
GPT_MIGRATION_EXECUTION=DENIED
PLUGIN_PUBLICATION=DENIED
MAIN_MUTATION=DENIED
PR22_MERGE=DENIED
PR45_MERGE=DENIED
```

Terminal marker:

`KRC_MEDIA_CURRENT_HANDOFF_V7_0_DEPLOYABLE_MCP_CANARY_SENTINEL_GATE_READY_2026_09_16`
