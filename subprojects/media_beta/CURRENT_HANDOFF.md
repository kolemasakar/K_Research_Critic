# KRC MEDIA — CURRENT HANDOFF

Version: 9.0
Status: ACTIVE_HANDOFF / LIVE_REMOTE_MCP_CANARY_PASS / CHATGPT_CONNECTION_PASS / ONE_TOOL_DISCOVERY_PASS / INVOCATION_PENDING / PUBLICATION_HOLD
Date: 2026-09-16

## Recovery command

`Віднови K-Research & Critic MEDIA з subprojects/media_beta/CURRENT_HANDOFF.md і продовжуй з one-tool owner-account ChatGPT canary invocation gate.`

## Canonical recovery files

1. `subprojects/media_beta/CURRENT_HANDOFF.md`
2. `subprojects/media_beta/109_CHATGPT_CUSTOM_MCP_CONNECTION_DISCOVERY_PASS_2026_09_16.md`
3. `subprojects/media_beta/108_SENTINEL_REMOTE_MCP_CANARY_LIVE_DEPLOYMENT_CONNECTION_BLOCKED_2026_09_16.md`
4. `subprojects/media_beta/107_KRC_DEPLOYABLE_REMOTE_MCP_CANARY_REPO_ACCEPTANCE_2026_09_16.md`
5. current PR #22 head/CI and current non-secret account/control-plane evidence

Older handoffs remain historical recovery evidence only and are superseded for current phase selection.

## Repository / PR

```text
repository=kolemasakar/K_Research_Critic
PR=22
branch=agent/krc-public-media-r3-integration
base=main
state=OPEN / DRAFT / UNMERGED
```

Validated deployable implementation state:

```text
implementation_head=4a75f53d6da956d9b2eb7acc1b6f788824bb6e03
implementation_workflow=35126692392
implementation_conclusion=SUCCESS
pre_live_documentation_head=2a91c6c4a982909717fb5b4e1dda7a04af1b388c
pre_live_documentation_workflow=35126878869
pre_live_documentation_conclusion=SUCCESS
live_gate_documentation_head=16acbb81cb46d4da672ad79e8eb18105e1ab5269
live_gate_workflow=35129121125
live_gate_conclusion=SUCCESS
```

At recovery always refetch current PR metadata and latest CI because documentation commits advance the branch.

## Accepted current state

```text
PROJECT=ACTIVE
PLUGIN_FIRST_STRATEGY=ACCEPTED
SURFACE_CLASSIFICATION=REMOTE_CUSTOM_MCP_CANDIDATE
MCP_CANARY_DEPLOYABLE=PASS
LIVE_MCP_DEPLOYMENT=PASS
REMOTE_ENDPOINT_READY_FOR_CONNECTION_TEST=YES
EXTERNAL_HEALTH=PASS
EXTERNAL_SERVER_DISCOVER=PASS
EXTERNAL_TOOLS_LIST=PASS
EXTERNAL_TOOLS_CALL=PASS
CANARY_TOOL_COUNT=1
CANARY_MUTATION=false
CANARY_PROVIDER_WORK=false
CANARY_VOICEBRIDGE_BINDING=false
CANARY_EXECUTION_TOOLS=false
CHATGPT_MCP_CONNECTION=PASS
SCAN_TOOLS_EQUIVALENT_DISCOVERY=PASS
CHATGPT_DISCOVERED_TOOL_COUNT=1
CHATGPT_DISCOVERED_TOOL_NAME=krc_media_capabilities_canary
CHATGPT_CANARY_INVOCATION=PENDING
```

## Live bounded canary

```text
DEPLOYMENT_TARGET=render/krc-mcp-canary-sentinel
SOURCE_BRANCH=agent/krc-public-media-r3-integration
SOURCE_COMMIT=2a91c6c4a982909717fb5b4e1dda7a04af1b388c
AUTO_DEPLOY=off
LIVE_ENDPOINT=https://krc-mcp-canary-sentinel.onrender.com
MCP_PATH=/mcp
HEALTH_PATH=/healthz
AUTH_MODE=none
```

`AUTH_MODE=none` is authorized only for this bounded one-tool canary validation. The endpoint contains no provider credential, VoiceBridge binding, mutation tool, execution tool, or user-controlled arguments.

No existing VoiceBridge, Cobalt, KGM or other Render service was modified.

## ChatGPT owner-account evidence

The owner created and connected the private custom MCP/plugin:

```text
NAME=KRC MCP Canary Sentinel
SERVER_URL=https://krc-mcp-canary-sentinel.onrender.com/mcp
AUTHENTICATION=No authentication
CONNECTION=PASS
```

The authenticated ChatGPT settings page displayed exactly one action:

```text
TOOL_COUNT=1
TOOL=krc_media_capabilities_canary
DESCRIPTION=Returns deterministic KRC MEDIA canary metadata. It does not call providers, VoiceBridge, or mutate external state.
```

No separate `Scan Tools` button was required by this UI flow; successful connection immediately surfaced the discovered action. This is accepted as the one-tool discovery evidence for this gate.

## Required next gate

In a normal owner-account ChatGPT chat with the private plugin enabled/selected:

```text
invoke only krc_media_capabilities_canary once
-> require successful result
-> require mutation=false
-> require provider_work=false
-> require voicebridge_binding=not_enabled
-> require execution_tools=not_enabled
-> record non-secret evidence
-> STOP
```

Do not invoke any other action or expand scope during this gate.

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

## Hard boundary

```text
FULL_MEDIA_13_TOOL_DEPLOYMENT=DENIED
VOICEBRIDGE_SECRET_BINDING=DENIED
MEDIA_PROVIDER_WORK=DENIED
WRITE_EXECUTION_TOOL_TEST=DENIED
PUBLIC_GPT_CHANGE=DENIED
GPT_MIGRATION_EXECUTION=DENIED
PLUGIN_PUBLICATION=DENIED
PLUGIN_SHARING=DENIED
MAIN_MUTATION=DENIED
PR22_MERGE=DENIED
PR45_MERGE=DENIED
```

Terminal marker:

`KRC_MEDIA_CURRENT_HANDOFF_V9_0_CHATGPT_MCP_CONNECTION_DISCOVERY_PASS_INVOCATION_PENDING_2026_09_16`
