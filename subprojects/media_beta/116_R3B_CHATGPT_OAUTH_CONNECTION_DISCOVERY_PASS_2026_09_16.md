# KRC MEDIA — R3-B ChatGPT OAuth Connection / Discovery PASS

Date: 2026-09-16
Status: **PASS / FINAL READ-ONLY INVOCATION PENDING / R3-C HOLD**

## Scope

This checkpoint records owner-account ChatGPT OAuth connection and MCP discovery for the isolated authenticated one-tool R3-B endpoint only.

## Authenticated service

```text
service=krc-mcp-auth-sentinel
url=https://krc-mcp-auth-sentinel.onrender.com/mcp
auth=OAuth authorization-code + PKCE S256
DCR=YES
scope=krc.mcp.read
owner_secret=SERVER_SIDE_ONLY
```

## OAuth flow evidence

Server-side request sequence observed after the owner authorized the connection:

```text
POST /oauth/register   -> 201
GET  /oauth/authorize  -> 200
POST /oauth/authorize  -> 302
POST /oauth/token      -> 200
POST /mcp              -> 401  # initial unauthenticated probe
POST /mcp              -> 200  # authenticated MCP
POST /mcp              -> 200  # authenticated MCP
```

ChatGPT UI status: `Підключено`.

## Discovery evidence

ChatGPT developer surface displays exactly one action:

```text
DISCOVERED_TOOL_COUNT=1
DISCOVERED_TOOL_NAME=krc_media_capabilities_canary
TOOL_CLASS=READ_ONLY
```

Tool description states that it returns deterministic KRC MEDIA canary metadata and does not call providers, VoiceBridge, or mutate external state.

## OAuth defect/fix encountered during gate

Initial authorization succeeded server-side but browser navigation was blocked because the authorization page CSP used `form-action 'self'` while successful authorization redirects to the registered ChatGPT callback origin.

Fix deployed on R3-B auth service:

```text
commit=4b8d172a23b88415839ada0da84357c1538614db
workflow=35138526850
Python_3_13=PASS
Python_3_14=PASS
Quality_Gates=PASS
coverage=PASS
live_deploy=dep-dalei1id0e5s73f4hu10
live_deploy_status=live
```

The CSP now permits only self plus the validated origin of the registered redirect URI for the authorization form response.

## Known operational debt

OAuth clients, authorization codes and tokens are currently held in process memory. A Render restart/redeploy resets DCR/tokens. This is acceptable only for the bounded R3-B functional gate and MUST be resolved before production/private operational hardening.

```text
OAUTH_STATE_PERSISTENCE=NOT_IMPLEMENTED
PRODUCTION_READY=NO
R3_G_DEBT=YES
```

## Secret boundary

No owner secret value was requested, read, logged, committed, passed as a tool argument, or recorded in evidence.

```text
OWNER_SECRET_SERVER_SIDE_ONLY=true
MODEL_VISIBLE_SECRET=false
REPOSITORY_SECRET=false
TOOL_ARGUMENT_SECRET=false
SECRET_REFLECTION=NO
```

## Remaining R3-B acceptance item

One authenticated read-only invocation remains:

```text
invoke only krc_media_capabilities_canary
require status=ok
require mutation=false
require provider_work=false
require voicebridge_binding=not_enabled
require execution_tools=not_enabled
then close R3-B PASS and STOP before R3-C
```

## Hard boundary remains

```text
VOICEBRIDGE_CREDENTIAL_BINDING=NO
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

`KRC_MEDIA_R3B_CHATGPT_OAUTH_CONNECTION_DISCOVERY_PASS_FINAL_INVOCATION_PENDING_2026_09_16`
