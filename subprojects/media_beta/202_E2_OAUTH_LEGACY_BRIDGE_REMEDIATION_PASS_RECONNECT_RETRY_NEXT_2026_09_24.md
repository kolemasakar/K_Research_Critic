# KRC MEDIA — E2 OAuth legacy bridge remediation PASS; reconnect retry next

Date: 2026-09-24  
Status: **AUTHORITATIVE CHECKPOINT / E2_OAUTH_REMEDIATION_PASS / RESTART_SAFE_OAUTH_PASS / LEGACY_CLIENT_AUTHORIZE_200 / ZERO_PROVIDER / RECONNECT_RETRY_NEXT**

## Target

```text
service=krc-mcp-r3e2-instagram-sentinel-v2
service_id=srv-dan7vsijnfac73fmrtl0
url=https://krc-mcp-r3e2-instagram-sentinel-v2.onrender.com
mcp=https://krc-mcp-r3e2-instagram-sentinel-v2.onrender.com/mcp
```

## Remediation applied

Server-side E2 OAuth configuration now includes:

```text
KRC_MCP_LEGACY_CLIENT_ID=CONFIGURED
KRC_MCP_LEGACY_REDIRECT_URI=CONFIGURED
KRC_MCP_OAUTH_SIGNING_KEY=CONFIGURED
```

Secret values are intentionally not stored in repository documentation.

Current live deploy:

```text
deploy=dep-daqmsg6gekts7398n0rg
commit=05498504171aa34815615f0ab11f8dc78705daaf
status=LIVE
```

## Runtime acceptance

Read-only/non-provider verification:

```text
HEALTH_STATUS=200
surface=r3e2_instagram_execution
tool_count=5
non_execution_tool_count=4
execution_tool_count=1
other_execution_tools=not_enabled
voicebridge_binding_configured=true
instagram_execution_enabled=true
provider_work_started=false

DCR_REGISTER_STATUS=201
DCR_CLIENT_PREFIX=krc1.
RESTART_SAFE_OAUTH=PASS

LEGACY_CHATGPT_CLIENT_AUTHORIZE_STATUS=200
OWNER_AUTHORIZATION_PAGE=PASS
```

The prior failure was therefore caused by stale OAuth runtime state before restart-safe + legacy-client compatibility configuration was fully active.

## Security hygiene

```text
SIGNING_KEY_VALUE_EXPOSED_IN_CHAT=NO
SIGNING_KEY_STORED_IN_REPO=NO
LOCAL_CLIPBOARD_SANITIZED=YES
```

## Next gate

Retry only the existing E2 Plugin connection:

```text
app_id=asdk_app_6aaeae197c9081918b90e46f5bb09615
name=KRC MCP R3E2 Instagram Sentinel-v5
action=Повторно підключити
```

Expected flow:

```text
GET /oauth/authorize -> 200
owner authorization form -> submit owner code
POST /oauth/authorize -> 302
POST /oauth/token -> 200
Plugin UI reconnect warning -> gone
```

Do not invoke MEDIA tools during this reconnect.

## Hard boundary

```text
OTHER_APP_CHANGES=NO
PLUGIN_PUBLICATION=NO
PLUGIN_SHARING_CHANGE=NO
MEDIA_PROVIDER_WORK=NO
PR22_MERGE=NO
PR45_MERGE=NO
MAIN_MUTATION=NO
```

## Resume

```text
RESUME_FROM=CHECKPOINT_202_E2_OAUTH_REMEDIATION_PASS
NEXT_GATE=RETRY_E2_RECONNECT
AFTER_GATE=PRIVATE_PLUGIN_SMOKE_ZERO_PROVIDER
```

Terminal marker:

`KRC_MEDIA_CHECKPOINT_202_E2_OAUTH_LEGACY_BRIDGE_REMEDIATION_PASS_RECONNECT_RETRY_NEXT_2026_09_24`
