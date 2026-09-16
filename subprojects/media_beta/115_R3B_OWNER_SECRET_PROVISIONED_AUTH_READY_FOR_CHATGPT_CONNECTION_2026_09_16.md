# KRC MEDIA — R3-B owner secret provisioned / auth ready for ChatGPT connection

Date: 2026-09-16
Status: **PASS — isolated OAuth MCP ready for owner-account ChatGPT connection**

## Scope

This checkpoint records only non-secret evidence after the owner provisioned `KRC_MCP_OWNER_CODE` directly in Render.

The secret value was not requested, read, transmitted to ChatGPT, committed to Git, passed through connector arguments, or written to evidence.

## Service

```text
service=krc-mcp-auth-sentinel
service_id=srv-dale3r942hec73c5t9hg
region=frankfurt
plan=free
autoDeploy=off
base_url=https://krc-mcp-auth-sentinel.onrender.com
mcp_url=https://krc-mcp-auth-sentinel.onrender.com/mcp
deployed_commit=057f748a204f8ad0878090a85a8adc8e49de73ed
auth_mode=oauth
```

Render applied the environment update and produced a fresh live deploy:

```text
deploy_id=dep-daleakp42hec73c6jq80
trigger=service_updated
status=live
```

## Post-secret non-secret validation

```text
dynamic_registration=201
authorize_get=200
OWNER_AUTH_CONFIGURED_UI=PASS
OWNER_AUTH_UNCONFIGURED_UI=ABSENT
OWNER_AUTH_CONTROL_DISABLED=NO
WRONG_OWNER_CODE=403
FAIL_CLOSED_ON_WRONG_SECRET=PASS
SECRET_REFLECTION=NO
```

Pre-secret protocol evidence remains valid:

```text
healthz=200
mutation=false
provider_work=false
protected_resource_metadata=200
authorization_server_metadata=200
PKCE_S256=advertised
unauthenticated_mcp=401
MCP_SCOPE=krc.mcp.read
```

## Secret boundary

```text
OWNER_SECRET_SERVER_SIDE_ONLY=true
MODEL_VISIBLE_SECRET=false
REPOSITORY_SECRET=false
TOOL_ARGUMENT_SECRET=false
CHECKPOINT_SECRET=false
VOICEBRIDGE_BEARER_REUSE=false
```

## Current boundary

The authenticated endpoint still exposes only the deterministic read-only canary. It does not bind VoiceBridge, MEDIA providers, nine backend read operations, or any execution/start operation.

```text
LIVE_TOOL_COUNT=1
LIVE_TOOL=krc_media_capabilities_canary
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

## Next gate

Owner-account ChatGPT connection only:

```text
create private custom MCP
Authentication=OAuth
URL=https://krc-mcp-auth-sentinel.onrender.com/mcp
complete OAuth authorization by entering owner code only in the server-hosted authorization page
Scan Tools / discover exactly one krc_media_capabilities_canary
invoke that read-only canary once
record non-secret evidence
close R3-B PASS
STOP before R3-C
```

Terminal marker:

`KRC_MEDIA_R3B_OWNER_SECRET_PROVISIONED_AUTH_READY_FOR_CHATGPT_CONNECTION_2026_09_16`
