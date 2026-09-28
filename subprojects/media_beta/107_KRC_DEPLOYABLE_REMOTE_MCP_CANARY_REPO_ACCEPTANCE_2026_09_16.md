# KRC — Deployable Remote MCP Canary Repository Acceptance — 2026-09-16

Status: **DEPLOYABLE_CANARY_REPO_ACCEPTED / SENTINEL_CONNECTION_GATE_READY / NO_DEPLOY / NO_CONNECT**

## Trigger

Checkpoint 106 transferred MCP canary application engineering ownership from Sentinel Remote to K_Research_Critic and required KRC to turn the accepted repository-only protocol core into a deployable, still bounded remote MCP candidate.

Canonical predecessor:

`subprojects/media_beta/106_SENTINEL_TO_KRC_MCP_CANARY_HANDOFF_2026_09_16.md`

## Implemented package

The accepted canary package now contains:

```text
plugins/krc_migration_candidate/mcp_canary/server.py
plugins/krc_migration_candidate/mcp_canary/http_server.py
plugins/krc_migration_candidate/mcp_canary/Dockerfile
plugins/krc_migration_candidate/mcp_canary/README.md
tests/test_krc_mcp_canary.py
tests/test_krc_mcp_canary_http.py
```

No deployment target, public endpoint, tunnel, cloud service, credential, OAuth client, VoiceBridge secret, provider integration or production MEDIA binding was created.

## Protocol behavior

Modern target:

```text
MCP_PROTOCOL_VERSION=2026-07-28
TRANSPORT_MODEL=STATELESS_HTTP
SERVER_DISCOVER=SUPPORTED
MCP_PROTOCOL_HEADER_VALIDATION=ENABLED
MCP_METHOD_HEADER_VALIDATION=ENABLED
MCP_NAME_HEADER_VALIDATION=ENABLED_FOR_TOOL_CALL
REQUEST_META_VERSION_VALIDATION=ENABLED
ORIGIN_VALIDATION=FAIL_CLOSED_IF_ORIGIN_PRESENT_AND_NOT_ALLOWLISTED
```

Bounded fallback compatibility:

```text
LEGACY_PROTOCOL_VERSION=2025-11-25
LEGACY_INITIALIZE_COMPATIBILITY=SUPPORTED
LEGACY_MODERN_VERSION_NEGOTIATION_VIA_INITIALIZE=DENIED
```

The modern implementation follows the current stateless MCP lifecycle: `server/discover` advertises only the modern version, modern requests carry per-request metadata, and HTTP header/body mismatches fail closed.

## Canary surface

Exactly one tool remains exposed:

```text
name=krc_media_capabilities_canary
CANARY_TOOL_COUNT=1
read_only=true
mutation=false
provider_work=false
network_provider_work=false
voicebridge_binding=not_enabled
execution_tools=not_enabled
media_operation_target_count=13
```

The tool accepts no arguments and returns deterministic structured content. Unknown tools and unexpected arguments remain fail-closed.

## Deployment packaging

Repository packaging is now intentionally present:

```text
HTTP_ENTRYPOINT=mcp_canary.http_server
MCP_PATH=/mcp
HEALTH_PATH=/healthz
CONTAINER_PACKAGING=Dockerfile
TLS_TERMINATION=EXTERNAL_DEPLOYMENT_PLATFORM_OR_TUNNEL
DEPLOYMENT_TARGET=NOT_SELECTED
LIVE_ENDPOINT=NO
```

The HTTP implementation uses only Python standard-library runtime components and adds no new provider dependency.

Authentication remains connection-stage pluggable:

```text
AUTH_MODE=PLUGGABLE
SUPPORTED_PACKAGE_MODES=none|bearer_env
VOICEBRIDGE_BEARER_REUSE=FORBIDDEN
REPOSITORY_SECRET=NO
MODEL_VISIBLE_SECRET=NO
```

`none` is not accepted as a production security model. It may only be considered by Sentinel for a specifically isolated bounded canary test or when an authenticated outer tunnel/proxy provides the access boundary. Any final ChatGPT-to-MCP auth selection remains a control-plane decision and must match the actually supported owner-account surface.

## Regression coverage

Repository tests now verify:

- modern `server/discover` response and one-tool discovery;
- modern `tools/list` and `tools/call` behavior;
- read-only/non-destructive annotations;
- deterministic no-provider/no-VoiceBridge result;
- header/body mismatch rejection with MCP protocol error semantics;
- unsupported protocol rejection;
- Origin fail-closed behavior;
- optional env-backed bearer boundary without committed secret material;
- health endpoint remains non-mutating;
- modern MCP GET stream is not enabled for this bounded stateless canary;
- bounded legacy initialize fallback;
- deployment packaging remains isolated and contains no production provider binding;
- existing 13-operation MEDIA contract remains unchanged;
- exact Core skill snapshot remains unchanged.

## CI evidence

Validated implementation head:

```text
4a75f53d6da956d9b2eb7acc1b6f788824bb6e03
```

Workflow:

```text
35126692392
```

Result:

```text
Tests / Python 3.13 = PASS
Tests / Python 3.14 = PASS
Quality gates = PASS
Dependency integrity = PASS
Ruff = PASS
Mypy = PASS
Repository policy = PASS
GPT Store package validation = PASS
Coverage gate = PASS
```

An earlier implementation workflow `35126490732` failed only because the new transport test import generated `__pycache__` inside the candidate subtree and an older generic secret-scan test attempted to decode that `.pyc` as UTF-8. The test harness was corrected to suppress bytecode creation for this import path. No canary runtime/security behavior failed in that workflow.

## Acceptance

```text
MCP_CANARY_DEPLOYABLE=PASS
CANARY_TOOL_COUNT=1
CANARY_MUTATION=false
CANARY_PROVIDER_WORK=false
CANARY_SECRET_REQUIRED=false
CANARY_VOICEBRIDGE_BINDING=false
CANARY_EXECUTION_TOOLS=false
MODERN_MCP_2026_07_28=PASS
LEGACY_2025_11_25_FALLBACK=BOUNDED
DEPLOYMENT_PACKAGE=PASS
LIVE_DEPLOYMENT=NO
REMOTE_ENDPOINT_READY_FOR_CONNECTION_TEST=NO
DEPLOYMENT_TARGET=NOT_SELECTED
CHATGPT_MCP_CONNECTION=NO
SCAN_TOOLS=NO
PUBLIC_GPT_MUTATION=NO
MAIN_MUTATION=NO
PR22_MERGE=NO
PR45_MERGE=NO
```

## Handback to Sentinel Remote

KRC application engineering for the deployable read-only canary is complete for this gate.

Sentinel Remote may resume only after separate owner authorization for the state-changing connection stage, with responsibilities limited to:

```text
select/verify isolated deployment target
-> deploy only this accepted canary package
-> verify network exposure and auth boundary
-> connect owner-account custom remote MCP
-> Scan Tools / discover exactly one canary tool
-> invoke only krc_media_capabilities_canary if permitted
-> record non-secret connection evidence
-> STOP
```

The deployment/connection gate must not expose the full 13 MEDIA operations or any VoiceBridge/provider credential.

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

`KRC_DEPLOYABLE_REMOTE_MCP_CANARY_REPO_ACCEPTED_2026_09_16`
