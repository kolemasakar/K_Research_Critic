# KRC MEDIA — CURRENT HANDOFF

Version: 12.3
Status: **ACTIVE_HANDOFF / R3-A_PASS / R3-B_IN_PROGRESS / CHATGPT_OAUTH_CONNECTION_PASS / DISCOVERY_PASS / FINAL_CANARY_INVOCATION_PENDING / PUBLICATION_HOLD**
Date: 2026-09-16

## Recovery command

`Віднови K-Research & Critic MEDIA з subprojects/media_beta/CURRENT_HANDOFF.md. R3-B authenticated ChatGPT OAuth connection and one-tool discovery PASS. Execute only one authenticated read-only krc_media_capabilities_canary invocation, record non-secret evidence, close R3-B PASS, then STOP before R3-C.`

## Canonical recovery files

1. `subprojects/media_beta/CURRENT_HANDOFF.md`
2. `subprojects/media_beta/116_R3B_CHATGPT_OAUTH_CONNECTION_DISCOVERY_PASS_2026_09_16.md`
3. `subprojects/media_beta/115_R3B_OWNER_SECRET_PROVISIONED_AUTH_READY_FOR_CHATGPT_CONNECTION_2026_09_16.md`
4. `subprojects/media_beta/114_R3B_OAUTH_ENDPOINT_PRESECRET_PASS_OWNER_SECRET_ACTION_REQUIRED_2026_09_16.md`
5. `subprojects/media_beta/113_R3A_CONTRACT_FREEZE_SECURE_ADAPTER_BASELINE_PASS_2026_09_16.md`
6. `subprojects/media_beta/02_ROADMAP.md` — v5.2
7. current PR #22 head/CI and current non-secret account/control-plane evidence

## Repository / PR

```text
repository=kolemasakar/K_Research_Critic
PR=22
branch=agent/krc-public-media-r3-integration
base=main
state=OPEN / DRAFT / UNMERGED
```

## R3-A baseline

```text
R3_A=PASS
MEDIA_OPERATION_COUNT=13
NON_EXECUTION_COUNT=9
EXECUTION_COUNT=4
selected_surface=custom_remote_mcp
transport=remote_mcp_http
protocol_version=2026-07-28
VOICEBRIDGE_BEARER_SERVER_SIDE_ONLY=true
```

## R3-B authenticated service

```text
service=krc-mcp-auth-sentinel
service_id=srv-dale3r942hec73c5t9hg
region=frankfurt
plan=free
autoDeploy=off
base_url=https://krc-mcp-auth-sentinel.onrender.com
mcp_url=https://krc-mcp-auth-sentinel.onrender.com/mcp
auth_mode=oauth
AUTH_PROTOCOL=authorization_code+PKCE_S256
DYNAMIC_CLIENT_REGISTRATION=YES
REFRESH_TOKEN_ROTATION=YES
MCP_SCOPE=krc.mcp.read
OWNER_SECRET_SERVER_SIDE_ONLY=true
LIVE_TOOL_COUNT=1
LIVE_TOOL=krc_media_capabilities_canary
```

The earlier no-auth evidence canary remains unchanged and separate.

## R3-B implementation / CSP callback fix

Current live auth service includes the callback-CSP fix:

```text
current_live_commit=4b8d172a23b88415839ada0da84357c1538614db
workflow=35138526850
Python_3_13=PASS
Python_3_14=PASS
Quality_Gates=PASS
coverage=PASS
live_deploy=dep-dalei1id0e5s73f4hu10
live_deploy_status=live
```

The authorization page permits form redirects only to self plus the validated origin of the registered OAuth redirect URI.

## ChatGPT OAuth connection evidence

Owner-account connection is now established under `KRC MCP Auth Sentinel R3B`.

Observed server sequence:

```text
POST /oauth/register   -> 201
GET  /oauth/authorize  -> 200
POST /oauth/authorize  -> 302
POST /oauth/token      -> 200
POST /mcp              -> 401  # initial probe
POST /mcp              -> 200  # authenticated MCP
POST /mcp              -> 200  # authenticated MCP
```

ChatGPT UI: `Підключено`.

## Discovery evidence

ChatGPT displays exactly one action:

```text
CHATGPT_OAUTH_CONNECTION=PASS
DISCOVERED_TOOL_COUNT=1
DISCOVERED_TOOL_NAME=krc_media_capabilities_canary
TOOL_CLASS=READ_ONLY
```

The tool remains deterministic, provider-free, VoiceBridge-unbound and non-mutating.

## Secret boundary

The owner provisioned `KRC_MCP_OWNER_CODE` directly in Render. Its value was never requested, read, logged, committed, passed in connector/tool arguments or recorded in evidence.

```text
MODEL_VISIBLE_SECRET=false
REPOSITORY_SECRET=false
TOOL_ARGUMENT_SECRET=false
CHECKPOINT_SECRET=false
VOICEBRIDGE_BEARER_REUSE=false
SECRET_REFLECTION=NO
```

## Known operational debt

OAuth DCR clients, authorization codes and tokens are currently process-memory state. Restart/redeploy resets them.

```text
OAUTH_STATE_PERSISTENCE=NOT_IMPLEMENTED
PRODUCTION_READY=NO
R3_G_DEBT=YES
```

Do not redeploy the auth service during the remaining R3-B invocation gate.

## Current final R3-B action

Use the connected `KRC MCP Auth Sentinel R3B` in ChatGPT and invoke only:

```text
krc_media_capabilities_canary
```

Acceptance result must include:

```text
status=ok
mutation=false
provider_work=false
voicebridge_binding=not_enabled
execution_tools=not_enabled
media_operation_target_count=13
```

After that evidence:

```text
R3_B=PASS
R3_C=HOLD
STOP
```

## Hard boundary

```text
VOICEBRIDGE_CREDENTIAL_BINDING=NO
VOICEBRIDGE_RUNTIME_CHANGE=NO
PROVIDER_CALL=NO
NINE_TOOL_BACKEND_BINDING=NO
REAL_EXECUTION_TOOL_EXPOSURE=NO
PUBLIC_GPT_MUTATION=NO
PLUGIN_PUBLICATION=NO
PLUGIN_SHARING=NO
GPT_MIGRATION=NO
MAIN_MUTATION=NO
PR22_MERGE=NO
PR45_MERGE=NO
R3_C=HOLD
```

Terminal marker:

`KRC_MEDIA_CURRENT_HANDOFF_V12_3_R3B_OAUTH_CONNECTION_DISCOVERY_PASS_FINAL_INVOCATION_PENDING_2026_09_16`
