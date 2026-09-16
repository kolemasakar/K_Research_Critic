# KRC MEDIA — CURRENT HANDOFF

Version: 12.1
Status: **ACTIVE_HANDOFF / R3-A_PASS / R3-B_IN_PROGRESS / OAUTH_ENDPOINT_LIVE / PRESECRET_PASS / OWNER_SECRET_ACTION_REQUIRED / PUBLICATION_HOLD**
Date: 2026-09-16

## Recovery command

`Віднови K-Research & Critic MEDIA з subprojects/media_beta/CURRENT_HANDOFF.md. R3-B OAuth endpoint live and pre-secret validation PASS. Continue only after owner manually provisions KRC_MCP_OWNER_CODE in Render without revealing it in chat.`

## Canonical recovery files

1. `subprojects/media_beta/CURRENT_HANDOFF.md`
2. `subprojects/media_beta/114_R3B_OAUTH_ENDPOINT_PRESECRET_PASS_OWNER_SECRET_ACTION_REQUIRED_2026_09_16.md`
3. `subprojects/media_beta/113_R3A_CONTRACT_FREEZE_SECURE_ADAPTER_BASELINE_PASS_2026_09_16.md`
4. `subprojects/media_beta/02_ROADMAP.md` — v5.2
5. current PR #22 head/CI and current non-secret account/control-plane evidence

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

## R3-B implementation state

R3-B owner execution approval has been received and implementation is in progress.

Accepted auth implementation:

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

The one-tool MCP remains read-only and provider-free. No MEDIA backend operation is bound.

## Isolated R3-B service

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
owner_secret_configured=NO
```

The earlier no-auth evidence canary `krc-mcp-canary-sentinel` remains unchanged and separate.

## R3-B pre-secret acceptance

External checks passed:

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
OWNER_AUTH_UNCONFIGURED_UI=PASS
OWNER_AUTH_POST_WITHOUT_SECRET=503_FAIL_CLOSED
TEST_VALUE_REFLECTION=NO
```

## Current owner action

The only current manual action is to provision `KRC_MCP_OWNER_CODE` directly in the Render environment UI for `krc-mcp-auth-sentinel`.

Secret rules:

```text
never paste value into ChatGPT
never commit value to Git
never pass value in connector/tool arguments
never record value in evidence/checkpoints
never log or return value
never reuse as VoiceBridge bearer
```

Use a strong locally generated value and store it in the owner's password manager.

After provisioning, the owner should report only `готово` / `done`, never the secret value.

## Next R3-B sequence after owner confirms

```text
verify service remains live and OAuth fail-closed externally
create/connect private custom MCP in ChatGPT with Authentication=OAuth
URL=https://krc-mcp-auth-sentinel.onrender.com/mcp
complete authorization in browser using owner secret directly there
Scan Tools / discovery -> exactly one krc_media_capabilities_canary
invoke the read-only canary once
record non-secret evidence
close R3-B PASS
STOP before R3-C
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

`KRC_MEDIA_CURRENT_HANDOFF_V12_1_R3B_PRESECRET_PASS_OWNER_SECRET_ACTION_REQUIRED_2026_09_16`
