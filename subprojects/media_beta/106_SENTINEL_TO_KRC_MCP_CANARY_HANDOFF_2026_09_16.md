# Sentinel -> KRC MCP canary handoff — 2026-09-16
Український службовий handoff від Sentinel Remote до проекту-власника K_Research_Critic.

Status: **HANDOFF_COMPLETE / KRC_ENGINEERING_OWNS_NEXT_IMPLEMENTATION / SENTINEL_RETURNS_AT_CONNECTION_GATE**

## Scope correction

Sentinel Remote owns connection/access/control-plane work. It does not own KRC application engineering.

The following work completed by Sentinel is now transferred to KRC as engineering state/evidence. Future code implementation, MCP server work, MEDIA tool implementation, VoiceBridge adapter logic, and functional regression work belong to KRC.

## Completed account/control-plane work by Sentinel

- Confirmed ChatGPT Work Cloud Browser can open the authenticated KRC Builder.
- Confirmed KRC GPT identity and read-only Builder snapshot.
- Confirmed current published KRC has no existing Actions to preserve.
- Inspected the owner's account-specific Plugin/App/custom-MCP surface in read-only mode.
- Confirmed web-visible Plugin creation surface and custom remote MCP form.
- Confirmed remote server URL/tunnel choices are visible.
- Confirmed visible authentication choices include OAuth, No authentication, and Mixed.
- Confirmed write/execution capability is described by UI but remains unverified for the actual account/runtime.
- Classified the current integration candidate as:

```text
SURFACE_CLASSIFICATION=REMOTE_CUSTOM_MCP_CANDIDATE
EXECUTION_WRITE_ACTUAL=UNVERIFIED
```

## Repo-only MCP canary work already completed

Sentinel implemented a repository-only read-only MCP protocol canary before the project-boundary correction.

Canonical files:

```text
plugins/krc_migration_candidate/mcp_canary/server.py
plugins/krc_migration_candidate/mcp_canary/__init__.py
tests/test_krc_mcp_canary.py
```

Canary contract:

```text
name=krc_media_capabilities_canary
read_only=true
mutation=false
provider_work=false
network_io=false
secret_required=false
voicebridge_binding=not_enabled
execution_tools=not_enabled
media_operation_target_count=13
```

The canary supports MCP `tools/list` and `tools/call`, deterministic structured output, fail-closed argument handling, and explicit read-only annotations. It contains no live endpoint, no credentials, no provider calls, and no deployment packaging.

Final validated CI evidence before this handoff:

```text
head=4b4906d4e1b7f34b02e47dcdbc1a1bbdd0d0ad21
workflow=35123303282
Tests / Python 3.13=PASS
Tests / Python 3.14=PASS
Quality gates=PASS
```

## KRC-owned next implementation

KRC now owns all engineering required to turn the repo-only canary into a deployable remote MCP candidate.

Required next KRC work:

- package a minimal remote HTTPS MCP service around the accepted canary protocol core;
- keep the first deployable canary strictly read-only and provider-free;
- preserve `krc_media_capabilities_canary` as the only exposed tool for the first live compatibility test;
- keep authentication pluggable and do not expose VoiceBridge bearer material to the model, repository, browser evidence, or tool arguments;
- do not enable the four MEDIA start/execution operations during the canary connection phase;
- do not bind the full 13-operation MEDIA implementation until the account-specific MCP connection and tool-discovery path is accepted;
- maintain Core/MEDIA parity contracts and existing fail-closed/free-only/retry invariants;
- run KRC-owned unit/integration/CI validation for the deployable canary package;
- produce a KRC checkpoint when a bounded deployment artifact is ready for Sentinel connection work.

## Expected KRC handback to Sentinel

When KRC has a deployable read-only canary ready, hand back only non-secret deployment/connection metadata required for Sentinel control-plane work, for example:

```text
MCP_CANARY_DEPLOYABLE=PASS
CANARY_TOOL_COUNT=1
CANARY_MUTATION=false
CANARY_PROVIDER_WORK=false
AUTH_MODE=<non-secret classification>
REMOTE_ENDPOINT_READY_FOR_CONNECTION_TEST=YES|NO
DEPLOYMENT_TARGET=<non-secret service identifier>
```

Do not place credentials, bearer values, OAuth client secrets, cookies, signed URLs, browser profile identifiers, or reusable auth material in the public KRC repository.

## Sentinel-owned work after handback

Sentinel Remote resumes ownership at the connection gate:

```text
bounded deployment/control-path review
-> network exposure review
-> authentication/permission boundary review
-> ChatGPT custom MCP connection
-> Scan Tools / tool discovery
-> verify actual account read capability
-> verify write/execution capability separately
-> access/recovery/audit evidence
```

Sentinel must not implement KRC application logic, MEDIA tools, VoiceBridge adapter behavior, or KRC functional regressions.

## Current release boundary

```text
LIVE_MCP_DEPLOYMENT=NO
CHATGPT_MCP_CONNECTION=NO
SCAN_TOOLS=NO
VOICEBRIDGE_SECRET_BINDING=NO
FULL_13_MEDIA_BINDING=NO
PUBLIC_GPT_MUTATION=NO
PLUGIN_PUBLICATION=NO
GPT_MIGRATION=NO
RENDER_MUTATION=NO
MAIN_MUTATION=NO
PR22_MERGE=NO
PR45_MERGE=NO
```

## Ownership decision

```text
KRC_ENGINEERING_OWNER=K_Research_Critic
SENTINEL_OWNER=ACCESS_CONNECTION_CONTROL_PLANE_ONLY
HANDOFF=COMPLETE
NEXT_SENTINEL_ENTRY_GATE=KRC_DEPLOYABLE_READ_ONLY_MCP_CANARY_READY
```
