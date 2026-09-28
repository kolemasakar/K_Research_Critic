# KRC MEDIA — ChatGPT Custom MCP Connection / Discovery PASS — 2026-09-16

Status: **CHATGPT_CONNECTION_PASS / ONE_TOOL_DISCOVERY_PASS / INVOCATION_PENDING / PUBLICATION_HOLD**

## Scope

This checkpoint records owner-account ChatGPT evidence after the live bounded Remote MCP canary had already passed external protocol validation.

## Owner-account connection evidence

The owner connected the private plugin/custom MCP:

```text
NAME=KRC MCP Canary Sentinel
SERVER_URL=https://krc-mcp-canary-sentinel.onrender.com/mcp
AUTHENTICATION=No authentication
CONNECTION=PASS
```

The ChatGPT UI displayed a successful connection confirmation:

```text
KRC MCP Canary Sentinel connected
```

This was a private owner-account connection only. No publication, sharing, GPT migration, public GPT mutation, production MEDIA binding, VoiceBridge credential binding, or provider work was performed.

## Tool discovery evidence

The connected plugin settings page showed exactly one action:

```text
TOOL_COUNT=1
TOOL=krc_media_capabilities_canary
```

Displayed description:

```text
Returns deterministic KRC MEDIA canary metadata. It does not call providers, VoiceBridge, or mutate external state.
```

Therefore the authenticated ChatGPT-side discovery requirement is accepted:

```text
CHATGPT_MCP_CONNECTION=PASS
SCAN_TOOLS_EQUIVALENT_DISCOVERY=PASS
DISCOVERED_TOOL_COUNT=1
DISCOVERED_TOOL_NAME=krc_media_capabilities_canary
```

The UI surfaced the action directly after connection; no separate Scan Tools button was required for this connection flow.

## Live canary state retained

```text
DEPLOYMENT_TARGET=render/krc-mcp-canary-sentinel
SOURCE_COMMIT=2a91c6c4a982909717fb5b4e1dda7a04af1b388c
AUTO_DEPLOY=off
LIVE_ENDPOINT=https://krc-mcp-canary-sentinel.onrender.com
MCP_PATH=/mcp
AUTH_MODE=none
```

Existing external validation remains:

```text
healthz=PASS
server/discover=PASS
tools/list=PASS
tools/call=PASS
CANARY_TOOL_COUNT=1
CANARY_MUTATION=false
CANARY_PROVIDER_WORK=false
CANARY_VOICEBRIDGE_BINDING=false
CANARY_EXECUTION_TOOLS=false
```

## Remaining step in this gate

One owner-account ChatGPT invocation is still pending:

```text
invoke only krc_media_capabilities_canary
-> require success
-> require mutation=false
-> require provider_work=false
-> require voicebridge_binding=not_enabled
-> require execution_tools=not_enabled
-> record non-secret evidence
-> STOP
```

No other action or tool may be invoked in this gate.

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

`KRC_CHATGPT_CUSTOM_MCP_CONNECTION_DISCOVERY_PASS_INVOCATION_PENDING_2026_09_16`
