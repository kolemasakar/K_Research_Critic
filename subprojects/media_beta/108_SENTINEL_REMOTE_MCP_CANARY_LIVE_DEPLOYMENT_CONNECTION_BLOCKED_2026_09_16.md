# KRC — Sentinel Remote MCP Canary Live Deployment / Connection Blocked — 2026-09-16

Status: **LIVE_CANARY_DEPLOYMENT_PASS / EXTERNAL_PROTOCOL_VALIDATION_PASS / CHATGPT_CONNECTION_BLOCKED_AUTH_CONTEXT / NO_SCAN_TOOLS**

## Trigger

Owner explicitly authorized the bounded Sentinel connection gate after checkpoint 107 accepted the deployable one-tool Remote MCP canary.

Canonical predecessor:

`subprojects/media_beta/107_KRC_DEPLOYABLE_REMOTE_MCP_CANARY_REPO_ACCEPTANCE_2026_09_16.md`

## Deployment target

An isolated non-production Render web service was created for the canary only:

```text
DEPLOYMENT_TARGET=render/krc-mcp-canary-sentinel
REGION=frankfurt
PLAN=free
SOURCE_REPO=kolemasakar/K_Research_Critic
SOURCE_BRANCH=agent/krc-public-media-r3-integration
SOURCE_COMMIT=2a91c6c4a982909717fb5b4e1dda7a04af1b388c
AUTO_DEPLOY=off
RUNTIME=python
LIVE_ENDPOINT=https://krc-mcp-canary-sentinel.onrender.com
MCP_PATH=/mcp
HEALTH_PATH=/healthz
AUTH_MODE=none
```

`AUTH_MODE=none` is used only for this bounded read-only canary validation. The service exposes no provider credentials, VoiceBridge binding, mutation capability, execution tools, or request arguments.

No existing VoiceBridge, KRC Cobalt, KGM or other service was modified.

## Render deployment evidence

The initial deployment completed successfully and reached `live` state from exact source commit `2a91c6c4a982909717fb5b4e1dda7a04af1b388c`.

Build/start boundary:

```text
BUILD=python -m compileall -q plugins/krc_migration_candidate/mcp_canary
START=python -m plugins.krc_migration_candidate.mcp_canary.http_server
KRC_MCP_BIND_HOST=0.0.0.0
PYTHONDONTWRITEBYTECODE=1
```

No production dependency or provider package was installed for the canary runtime.

## External endpoint validation

External public-browser health validation returned:

```json
{
  "mutation": false,
  "provider_work": false,
  "service": "krc-media-mcp-canary",
  "status": "ok"
}
```

A separate authorized KRC command-access host then performed real HTTPS POST protocol checks against the public endpoint.

### server/discover

```text
HTTP=200
supportedVersions=[2026-07-28]
capabilities.tools={}
resultType=complete
cacheScope=public
serverInfo.name=krc-media-mcp-canary
serverInfo.version=0.2.0
```

### tools/list

```text
HTTP=200
TOOL_COUNT=1
TOOL_NAME=krc_media_capabilities_canary
readOnlyHint=true
destructiveHint=false
idempotentHint=true
openWorldHint=false
inputSchema.additionalProperties=false
```

### tools/call

```text
HTTP=200
isError=false
service=krc-media-mcp-canary
status=ok
mutation=false
provider_work=false
media_operation_target_count=13
voicebridge_binding=not_enabled
execution_tools=not_enabled
```

Therefore the deployed endpoint is protocol-reachable and preserves the accepted canary boundary.

## ChatGPT owner-account connection attempt

A separate authenticated-browser automation path was attempted for the owner-account ChatGPT custom MCP management surface with the approved goal:

```text
create/connect private custom remote MCP only
-> URL https://krc-mcp-canary-sentinel.onrender.com/mcp
-> No authentication
-> Scan Tools
-> discover exactly one canary tool
-> optionally invoke only the read-only canary
-> STOP
```

The browser automation context did not have a configured authenticated ChatGPT credential/profile. It therefore could not enter the owner-account custom MCP management surface.

This is classified as a **control-plane browser authentication blocker**, not an MCP endpoint/runtime failure.

No Plugin/App/custom MCP connection was created in ChatGPT, `Scan Tools` was not executed, and no GPT/plugin publication, sharing, migration, or write/execution capability was changed.

## Acceptance state

```text
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
CHATGPT_MCP_CONNECTION=BLOCKED_AUTH_CONTEXT
SCAN_TOOLS=NO
CHATGPT_CANARY_INVOCATION=NO
```

## Required continuation

Resume from an authenticated owner-account ChatGPT browser context only:

```text
open custom MCP management surface
-> create/connect private MCP to https://krc-mcp-canary-sentinel.onrender.com/mcp
-> choose No authentication for this bounded canary only
-> Scan Tools
-> require exactly one discovered tool: krc_media_capabilities_canary
-> invoke only that read-only canary if permitted
-> record non-secret evidence
-> STOP
```

If the authenticated ChatGPT surface presents different auth/tool semantics from the previously inspected account surface, stop and reclassify before connection.

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

`KRC_SENTINEL_REMOTE_MCP_CANARY_LIVE_DEPLOYMENT_PASS_CHATGPT_AUTH_BLOCKED_2026_09_16`
