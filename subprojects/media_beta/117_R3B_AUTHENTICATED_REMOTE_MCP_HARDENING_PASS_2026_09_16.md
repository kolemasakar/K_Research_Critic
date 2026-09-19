# KRC MEDIA — R3-B Authenticated Remote MCP Hardening PASS

Date: 2026-09-16
Status: **R3_B_PASS / AUTHENTICATED_REMOTE_MCP_VALIDATED / STOP_BEFORE_R3_C**

## Scope

R3-B was limited to inbound authentication and secret-boundary hardening on an isolated Remote MCP endpoint. No VoiceBridge credential was bound, no MEDIA provider was called, no 9-tool backend binding was enabled, and no execution tool was exposed.

## Accepted implementation

```text
service=krc-mcp-auth-sentinel
service_id=srv-dale3r942hec73c5t9hg
region=frankfurt
plan=free
autoDeploy=off
mcp_url=https://krc-mcp-auth-sentinel.onrender.com/mcp
auth_mode=oauth
AUTH_PROTOCOL=authorization_code+PKCE_S256
DYNAMIC_CLIENT_REGISTRATION=YES
MCP_SCOPE=krc.mcp.read
OWNER_SECRET_SERVER_SIDE_ONLY=true
LIVE_TOOL_COUNT=1
LIVE_TOOL=krc_media_capabilities_canary
```

Current live auth implementation includes the OAuth callback CSP fix:

```text
live_commit=4b8d172a23b88415839ada0da84357c1538614db
workflow=35138526850
Python_3_13=PASS
Python_3_14=PASS
Quality_Gates=PASS
coverage=PASS
live_deploy=dep-dalei1id0e5s73f4hu10
```

## OAuth acceptance

Observed owner-account flow:

```text
POST /oauth/register   -> 201
GET  /oauth/authorize  -> 200
POST /oauth/authorize  -> 302
POST /oauth/token      -> 200
POST /mcp              -> 401  # initial unauthenticated probe
POST /mcp              -> 200  # authenticated MCP
POST /mcp              -> 200  # authenticated MCP
```

The initial callback failure was traced to authorization-page CSP `form-action 'self'`. The fix restricts form-action to self plus the validated origin of the registered OAuth redirect URI. Regression coverage and CI are PASS.

## ChatGPT connection and discovery

Owner-account plugin connection:

```text
PLUGIN_NAME=KRC MCP Auth Sentinel R3B
CHATGPT_OAUTH_CONNECTION=PASS
DISCOVERED_TOOL_COUNT=1
DISCOVERED_TOOL_NAME=krc_media_capabilities_canary
TOOL_CLASS=READ_ONLY
```

## Authenticated invocation evidence

A real ChatGPT tool invocation completed successfully through the OAuth-protected MCP. The returned structured result was:

```json
{
  "execution_tools": "not_enabled",
  "media_operation_target_count": 13,
  "mutation": false,
  "provider_work": false,
  "service": "krc-media-mcp-canary",
  "status": "ok",
  "voicebridge_binding": "not_enabled"
}
```

Acceptance:

```text
AUTHENTICATED_CANARY_INVOCATION=PASS
mutation=false
provider_work=false
voicebridge_binding=not_enabled
execution_tools=not_enabled
media_operation_target_count=13
```

## Secret boundary

`KRC_MCP_OWNER_CODE` was provisioned directly by the owner in Render. Its value was never requested, read, committed, passed in tool arguments, recorded in evidence, or reused as the VoiceBridge bearer.

```text
MODEL_VISIBLE_SECRET=false
REPOSITORY_SECRET=false
TOOL_ARGUMENT_SECRET=false
CHECKPOINT_SECRET=false
VOICEBRIDGE_BEARER_REUSE=false
SECRET_REFLECTION=NO
```

## Known operational debt

OAuth DCR clients, authorization codes and tokens are currently process-memory state. Restart/redeploy invalidates them.

```text
OAUTH_STATE_PERSISTENCE=NOT_IMPLEMENTED
PRODUCTION_READY=NO
R3_G_DEBT=YES
```

This does not invalidate the bounded R3-B functional acceptance, but it must be resolved before production-like operational readiness.

## Hard boundary preserved

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
```

## Closure

```text
R3_A=PASS
R3_B=PASS
R3_C=HOLD
R3_C_EXECUTION_APPROVAL=REQUIRED
```

Terminal marker:

`KRC_MEDIA_R3B_AUTHENTICATED_REMOTE_MCP_HARDENING_PASS_2026_09_16`
