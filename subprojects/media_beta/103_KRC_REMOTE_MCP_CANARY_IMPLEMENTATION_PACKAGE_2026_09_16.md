# KRC — Remote MCP Canary Implementation Package — 2026-09-16

Status: **READY_FOR_KRC_REPO_IMPLEMENTATION / NO_DEPLOY / NO_CONNECT / PUBLICATION_HOLD**

## Trigger

P100 account inspection confirmed that the owner account exposes a web custom-MCP creation form with remote server URL/tunnel options and visible authentication choices. Checkpoint 102 classified the surface as:

```text
SURFACE_CLASSIFICATION=REMOTE_CUSTOM_MCP_CANDIDATE
EXECUTION_WRITE_ACTUAL=UNVERIFIED
```

The next engineering step belongs to KRC repository work, not Sentinel control-plane mutation.

## Objective

Implement a minimal repository-only remote MCP canary that can later be deployed and connected under a separate owner authorization gate.

The canary exists only to validate MCP packaging, tool discovery, authentication transport, and account compatibility before the full 13-operation MEDIA mapping is implemented or connected.

## Required canary tool

Canonical logical tool:

```text
name=krc_media_capabilities_canary
mutation=false
provider_work=false
write=false
voicebridge_secret_required=false
```

Expected behavior:
- deterministic static or locally derived response only;
- no VoiceBridge call required;
- no Gemini, AssemblyAI, Cobalt, Telegram, Facebook, Instagram or YouTube provider work;
- no durable job creation;
- no external state mutation;
- no credential material in response/log/tool schema.

Suggested response fields:

```text
service=krc-media-mcp-canary
status=ok
mutation=false
provider_work=false
media_operation_target_count=13
voicebridge_binding=not_enabled
execution_tools=not_enabled
```

## Implementation constraints

- Add implementation only under an appropriate project subdirectory; never repository root.
- Do not add real credentials, bearer tokens, OAuth client secrets, cookies or browser state.
- Do not change the current VoiceBridge API.
- Do not mutate Render configuration or deploy a new service.
- Do not connect the MCP to ChatGPT yet.
- Do not enable the four start/execution operations yet.
- Keep the canary transport compatible with a future remote HTTPS MCP endpoint.
- Keep auth pluggable; production authentication remains unresolved until connection-stage validation.
- `No authentication` may be used only for local/unit test fixtures, never as an accepted public production security model.

## Required tests

Repository CI should verify at minimum:

1. canary tool exists and is read-only;
2. no provider work or VoiceBridge network call occurs;
3. no secret-bearing constants/config are committed;
4. tool result is deterministic and sanitized;
5. future 13-operation MEDIA contract remains unchanged;
6. current Core skill parity remains unchanged;
7. no deployment configuration is introduced;
8. no MCP live endpoint/URL is asserted as deployed.

## Acceptance output

KRC should return a checkpoint with:

```text
MCP_CANARY_IMPLEMENTATION=PASS|FAIL
MCP_CANARY_TESTS=PASS|FAIL
CANARY_MUTATION=false
CANARY_PROVIDER_WORK=false
CANARY_SECRET_REQUIRED=false
LIVE_DEPLOYMENT=NO
CHATGPT_CONNECTION=NO
RENDER_MUTATION=NO
PUBLIC_GPT_MUTATION=NO
```

## After repository acceptance

STOP.

The next step requires a separate owner authorization because it will create a real remote endpoint and/or connect a custom MCP app in ChatGPT:

```text
repo-only canary PASS
-> owner authorization gate
-> bounded canary deployment
-> ChatGPT custom MCP Scan Tools / connection test
-> verify actual read capability
-> verify account execution/write capability separately
-> only then stage full 13-operation MEDIA MCP mapping
```

## Release boundary

```text
LIVE_MCP_DEPLOYMENT=DENIED
LIVE_MCP_CONNECTION=DENIED
PLUGIN_INSTALLATION=DENIED
PLUGIN_PUBLICATION=DENIED
MIGRATION_EXECUTION=DENIED
VOICEBRIDGE_SECRET_EXPOSURE=DENIED
PUBLIC_GPT_CHANGE=DENIED
RENDER_CHANGE=DENIED
MAIN_MUTATION=DENIED
PR22_MERGE=DENIED
PR45_MERGE=DENIED
```
