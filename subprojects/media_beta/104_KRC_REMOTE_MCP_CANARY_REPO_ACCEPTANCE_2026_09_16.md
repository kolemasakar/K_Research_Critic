# KRC — Remote MCP Canary Repository Acceptance — 2026-09-16
Репозиторний MCP canary реалізовано та перевірено без розгортання, підключення до ChatGPT, credentials або змін production runtime.

Status: **MCP_CANARY_REPO_ACCEPTED / LIVE_DEPLOYMENT_HOLD / CHATGPT_CONNECTION_HOLD / PUBLICATION_HOLD**

## Scope

This checkpoint closes the repository-only implementation package from checkpoint 103.

Implemented under:

```text
plugins/krc_migration_candidate/mcp_canary/__init__.py
plugins/krc_migration_candidate/mcp_canary/server.py
tests/test_krc_mcp_canary.py
```

Candidate documentation was synchronized in:

```text
plugins/krc_migration_candidate/README.md
```

No repository-root implementation file was introduced.

## Canary behavior

Canonical tool:

```text
name=krc_media_capabilities_canary
```

Accepted properties:

```text
read_only=true
mutation=false
provider_work=false
voicebridge_binding=not_enabled
execution_tools=not_enabled
secret_required=false
network_io=false
live_endpoint=false
media_operation_target_count=13
```

The canary response is deterministic and locally derived. It does not call VoiceBridge, Gemini, AssemblyAI, Cobalt, Instagram, Facebook, Telegram, YouTube, Render, or any other external service.

## MCP protocol core

The implementation is intentionally transport-neutral and dependency-free.

Repository validation covers:
- tool discovery through `tools/list`;
- deterministic tool invocation through `tools/call`;
- explicit MCP read-only annotations;
- fail-closed rejection of unknown tools and unexpected arguments;
- current protocol target `2026-07-28` plus bounded legacy initialize compatibility for `2025-11-25`;
- no network/process-execution imports;
- no live endpoint URL;
- no deployment packaging.

This protocol core is not itself a deployed HTTPS MCP server.

## Security and isolation

No credentials or operational access material were added.

Forbidden material remains absent from the canary package:
- bearer/API secrets;
- OAuth client secrets;
- cookies/session state;
- Browser Context Profile IDs;
- public endpoint URLs;
- Render deployment config;
- Docker/Compose deployment config;
- `mcp.json`, `.mcp.json`, `.app.json`.

The existing 13-operation MEDIA contract and exact Core skill snapshot remain unchanged.

## CI evidence

Initial workflow `35122784116` identified a test-harness issue only: Python bytecode cache files created under the candidate directory were being read as UTF-8 by generic secret-scan tests.

No canary behavior failed. The harness was corrected to load the canary source without creating candidate `__pycache__` artifacts and to scan only text source/config suffixes.

Validated implementation commit:

```text
883829d4fc3dd353481c1115ade9a2e95aeca9f0
```

Workflow:

```text
35122967418
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

A final branch workflow after this documentation checkpoint must also remain green before treating the current head as fully synchronized.

## Acceptance

```text
MCP_CANARY_IMPLEMENTATION=PASS
MCP_CANARY_TESTS=PASS
CANARY_MUTATION=false
CANARY_PROVIDER_WORK=false
CANARY_SECRET_REQUIRED=false
CANARY_NETWORK_IO=false
LIVE_DEPLOYMENT=NO
CHATGPT_CONNECTION=NO
RENDER_MUTATION=NO
PUBLIC_GPT_MUTATION=NO
VOICEBRIDGE_MUTATION=NO
MEDIA_OPERATION_PARITY_COUNT=13
CORE_SKILL_PARITY=PASS
```

## Stop boundary

Repository-only implementation is complete. STOP before the first state-changing infrastructure/product step.

The following remain separately owner-gated:

```text
LIVE_MCP_DEPLOYMENT=DENIED
LIVE_MCP_CONNECTION=DENIED
MCP_SCAN_TOOLS=DENIED_UNTIL_DEPLOYMENT_APPROVAL
LIVE_CREDENTIALS=DENIED
VOICEBRIDGE_SECRET_BINDING=DENIED
FULL_MEDIA_MCP_EXECUTION_TOOLS=NOT_STARTED
PLUGIN_INSTALLATION=DENIED
PLUGIN_PUBLICATION=DENIED
MIGRATION_EXECUTION=DENIED
PUBLIC_GPT_CHANGE=DENIED
RENDER_CHANGE=DENIED
MAIN_MUTATION=DENIED
PR22_MERGE=DENIED
PR45_MERGE=DENIED
```

## Next owner gate

The next phase, if authorized, is a **bounded canary deployment** that exposes only this read-only canary tool, followed by ChatGPT `Scan Tools` / connection testing. It must not expose the 13 production MEDIA operations or any VoiceBridge bearer until the account capability and security model are validated.
