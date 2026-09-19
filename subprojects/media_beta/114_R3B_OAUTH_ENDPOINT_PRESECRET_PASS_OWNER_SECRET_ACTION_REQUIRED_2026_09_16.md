# KRC MEDIA — R3-B OAuth Endpoint Pre-Secret Gate — 2026-09-16

Status: **R3-B_IN_PROGRESS / OAUTH_ENDPOINT_LIVE / PRESECRET_VALIDATION_PASS / OWNER_SECRET_ACTION_REQUIRED / NO_VOICEBRIDGE_BINDING / PUBLICATION_HOLD**

## Authorization

The owner explicitly approved R3-B execution after R3-A PASS.

R3-B scope remains limited to inbound authentication and secret-boundary hardening on an isolated Remote MCP endpoint. It does not authorize VoiceBridge credential binding, provider work, 9-tool backend binding, execution-tool exposure, public GPT mutation, publication/sharing/migration, main mutation, or PR merges.

## Repository implementation

R3-B added an isolated OAuth boundary to the existing one-tool canary package:

```text
authorization-code flow
PKCE S256
dynamic client registration
protected-resource metadata
authorization-server metadata
rotating refresh tokens
scope=krc.mcp.read
one read-only canary tool only
```

The first CI attempt failed only because an existing canary guard prohibits literal live/HTTP endpoint strings inside the canary package. The documentation placeholder was changed without weakening that guard.

Accepted implementation head:

```text
057f748a204f8ad0878090a85a8adc8e49de73ed
workflow=35135397654
Tests / Python 3.13=PASS
Tests / Python 3.14=PASS
Quality gates=PASS
coverage=PASS
```

## Isolated deployment

A separate Render service was created. The existing evidence-only no-auth canary was not modified.

```text
service=krc-mcp-auth-sentinel
service_id=srv-dale3r942hec73c5t9hg
region=frankfurt
plan=free
autoDeploy=off
deployed_commit=057f748a204f8ad0878090a85a8adc8e49de73ed
endpoint=https://krc-mcp-auth-sentinel.onrender.com
mcp_path=/mcp
auth_mode=oauth
owner_secret_configured=NO
```

No VoiceBridge, Cobalt, KGM, existing canary, or other Render service was mutated.

## External pre-secret validation

Observed from an independent external host:

```text
GET /healthz -> 200
mutation=false
provider_work=false

GET /.well-known/oauth-protected-resource -> 200
resource=https://krc-mcp-auth-sentinel.onrender.com/mcp
authorization_servers=[https://krc-mcp-auth-sentinel.onrender.com]
scopes_supported=[krc.mcp.read]

GET /.well-known/oauth-authorization-server -> 200
response_types_supported=[code]
grant_types_supported=[authorization_code, refresh_token]
code_challenge_methods_supported=[S256]
token_endpoint_auth_methods_supported=[none]
registration_endpoint present

POST /mcp without access token -> 401
WWW-Authenticate includes resource_metadata and scope=krc.mcp.read
body={status: unauthorized}
```

Dynamic registration returned 201 and a client id. Before owner secret provisioning, the authorization page explicitly reported that owner authorization was not configured, controls were disabled, and authorization POST failed closed with 503. The test input was not reflected in the response.

## Secret boundary

The owner authorization secret must be provisioned directly by the owner in the Render environment UI under:

```text
KRC_MCP_OWNER_CODE
```

Rules:

```text
DO NOT paste the value into ChatGPT
DO NOT commit the value to Git
DO NOT pass the value in tool arguments
DO NOT record the value in checkpoints/evidence
DO NOT emit the value in logs/responses
```

The secret is not the VoiceBridge bearer and must never be reused as the VoiceBridge bearer.

Until the owner provisions this value, authorization remains intentionally fail-closed.

## Next bounded action

Owner manually provisions a strong locally generated `KRC_MCP_OWNER_CODE` in the Render dashboard for `krc-mcp-auth-sentinel`, without revealing the value in chat.

After the owner confirms completion, R3-B may continue with:

```text
verify non-secret post-provision state
create/connect private ChatGPT custom MCP with Authentication=OAuth
complete owner authorization in browser without revealing secret
require exactly one discovered tool: krc_media_capabilities_canary
invoke that read-only canary once
record non-secret evidence
STOP before R3-C
```

Terminal marker:

`KRC_R3B_OAUTH_PRESECRET_PASS_OWNER_SECRET_ACTION_REQUIRED_2026_09_16`
