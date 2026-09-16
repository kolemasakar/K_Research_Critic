# KRC MEDIA — CURRENT HANDOFF

Version: 12.2
Status: **ACTIVE_HANDOFF / R3-A_PASS / R3-B_IN_PROGRESS / OAUTH_ENDPOINT_LIVE / OWNER_SECRET_PROVISIONED / CHATGPT_OAUTH_CONNECTION_GATE_READY / PUBLICATION_HOLD**
Date: 2026-09-16

## Recovery command

`Віднови K-Research & Critic MEDIA з subprojects/media_beta/CURRENT_HANDOFF.md. R3-B OAuth endpoint live, owner secret provisioned server-side, post-secret validation PASS. Continue with owner-account ChatGPT OAuth connection to the isolated one-tool MCP only.`

## Canonical recovery files

1. `subprojects/media_beta/CURRENT_HANDOFF.md`
2. `subprojects/media_beta/115_R3B_OWNER_SECRET_PROVISIONED_AUTH_READY_FOR_CHATGPT_CONNECTION_2026_09_16.md`
3. `subprojects/media_beta/114_R3B_OAUTH_ENDPOINT_PRESECRET_PASS_OWNER_SECRET_ACTION_REQUIRED_2026_09_16.md`
4. `subprojects/media_beta/113_R3A_CONTRACT_FREEZE_SECURE_ADAPTER_BASELINE_PASS_2026_09_16.md`
5. `subprojects/media_beta/02_ROADMAP.md` — v5.2
6. current PR #22 head/CI and current non-secret account/control-plane evidence

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
implementation_head=2c6dd94527997507c4e77844a4d36383e1d281ef
workflow=35133705040
Python_3_13=PASS
Python_3_14=PASS
Quality_Gates=PASS
```

Frozen MEDIA contract remains:

```text
selected_surface=custom_remote_mcp
transport=remote_mcp_http
protocol_version=2026-07-28
MEDIA_OPERATION_COUNT=13
NON_EXECUTION_COUNT=9
EXECUTION_COUNT=4
VOICEBRIDGE_BEARER_SERVER_SIDE_ONLY=true
```

## R3-B implementation

```text
implementation_head=057f748a204f8ad0878090a85a8adc8e49de73ed
workflow=35135397654
Python_3_13=PASS
Python_3_14=PASS
Quality_Gates=PASS
coverage=PASS
AUTH_PROTOCOL=OAuth authorization-code + PKCE S256
DYNAMIC_CLIENT_REGISTRATION=YES
REFRESH_TOKEN_ROTATION=YES
MCP_SCOPE=krc.mcp.read
LIVE_TOOL_COUNT=1
LIVE_TOOL=krc_media_capabilities_canary
```

The one-tool MCP remains deterministic, read-only and provider-free. No MEDIA backend operation is bound.

## Isolated authenticated service

```text
service=krc-mcp-auth-sentinel
service_id=srv-dale3r942hec73c5t9hg
region=frankfurt
plan=free
autoDeploy=off
deployed_commit=057f748a204f8ad0878090a85a8adc8e49de73ed
base_url=https://krc-mcp-auth-sentinel.onrender.com
mcp_url=https://krc-mcp-auth-sentinel.onrender.com/mcp
auth_mode=oauth
owner_secret_configured=YES
post_secret_deploy=dep-daleakp42hec73c6jq80
post_secret_deploy_status=live
```

The earlier no-auth evidence canary `krc-mcp-canary-sentinel` remains unchanged and separate.

## R3-B auth acceptance to date

```text
healthz=200
mutation=false
provider_work=false
protected_resource_metadata=200
authorization_server_metadata=200
PKCE_S256=advertised
dynamic_registration=201
unauthenticated_mcp=401
WWW_AUTHENTICATE_RESOURCE_METADATA=present
OWNER_AUTH_CONFIGURED_UI=PASS
OWNER_AUTH_CONTROL_DISABLED=NO
WRONG_OWNER_CODE=403
FAIL_CLOSED_ON_WRONG_SECRET=PASS
SECRET_REFLECTION=NO
```

## Secret boundary

The owner provisioned `KRC_MCP_OWNER_CODE` directly in Render. Its value was not requested, read, logged, committed, passed in tool arguments or recorded in project evidence.

```text
OWNER_SECRET_SERVER_SIDE_ONLY=true
MODEL_VISIBLE_SECRET=false
REPOSITORY_SECRET=false
TOOL_ARGUMENT_SECRET=false
CHECKPOINT_SECRET=false
VOICEBRIDGE_BEARER_REUSE=false
```

## Current manual gate

Create/connect a second private ChatGPT custom MCP for the authenticated endpoint:

```text
Name=KRC MCP Auth Sentinel
URL=https://krc-mcp-auth-sentinel.onrender.com/mcp
Authentication=OAuth
```

Complete OAuth only in the server-hosted authorization page. Enter the owner code there directly; never paste it into ChatGPT conversation text.

Acceptance after connection:

```text
CHATGPT_OAUTH_CONNECTION=PASS
DISCOVERED_TOOL_COUNT=1
DISCOVERED_TOOL_NAME=krc_media_capabilities_canary
READ_ONLY_CANARY_INVOCATION=PASS
```

After this evidence, close R3-B PASS and STOP before R3-C.

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

`KRC_MEDIA_CURRENT_HANDOFF_V12_2_R3B_AUTH_READY_FOR_CHATGPT_OAUTH_CONNECTION_2026_09_16`
