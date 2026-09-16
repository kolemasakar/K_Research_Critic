# KRC Plugin Migration Candidate

Status: DESIGN_ONLY / NOT_INSTALLABLE / NOT_DEPLOYED / PUBLICATION_HOLD

This directory is a repository-side migration candidate for moving K-Research & Critic from the retiring Custom GPT surface to the OpenAI Plugin model. The final live binding remains account-surface dependent, but the repository now includes a minimal read-only MCP canary protocol core for bounded compatibility testing.

## Why this is not an installable plugin yet

Current OpenAI guidance says plugins can combine reusable skills with connected apps, while Custom GPT Actions do not migrate automatically. A replacement MEDIA integration therefore needs an explicit supported app/connector or custom MCP implementation and its permissions must be reviewed before use.

This candidate still intentionally does **not** contain `mcp.json`, `.mcp.json`, `.app.json`, a deployable remote HTTPS listener, provider credentials, bearer tokens, cookies, browser-profile identifiers, or deployment configuration. Raw deployment declarations can change product-surface availability, so live packaging and authentication must be derived from the inspected account surface and activated only behind a separate owner approval gate.

The repository-only canary under `mcp_canary/` is different: it is a transport-neutral protocol core that exposes one deterministic read-only tool and performs no network I/O, provider work, VoiceBridge call, credential lookup, or external mutation.

## Candidate assets

- `skills/krc_core/SKILL.md` — exact snapshot of the current accepted Core instructions, wrapped only with migration metadata.
- `contracts/media_tools.yaml` — 1:1 parity contract for the 13 accepted R3 MEDIA Action operations.
- `contracts/media_adapter.yaml` — transport-neutral request/response, auth, retry, error and platform-boundary contract between the future Plugin/App/MCP surface and the existing VoiceBridge MEDIA API.
- `contracts/surface_decision_matrix.yaml` — fail-closed account-surface selection rules.
- `contracts/auth_transport_binding.yaml` — authentication/transport requirements for future live binding.
- `mcp_canary/server.py` — repository-only deterministic MCP protocol core exposing `krc_media_capabilities_canary`.
- `regression/core_cases.yaml` — machine-readable Core behavioral fixtures covering CriticProfile, cross-check, traceability, checkpoint recovery, language, final protocol and MEDIA failure isolation.
- `regression/media_negative_cases.yaml` — negative/boundary MEDIA fixtures covering consent, wrong-platform routing, paid fallback prohibition, deterministic retry, charge uncertainty, reuse/concurrency, input validation, secret sanitization and platform-specific hard guards.
- `tests/test_krc_plugin_migration_candidate.py` — repository guards for Core parity, exact 13-operation parity, transport-neutral adapter invariants, regression coverage, free-only policy, consent/retry semantics, and secret/config boundaries.
- `tests/test_krc_mcp_canary.py` — canary discovery/call/read-only/no-network/no-secret/no-deployment acceptance tests.

Canonical sources remain authoritative:

- `prompts/GPT_STORE_INSTRUCTIONS.md`
- `prompts/GPT_STORE_MEDIA_R3_PUBLIC_ADDENDUM.md`
- `gpt_store/actions/media_public_r3_openapi.yaml`
- `subprojects/media_beta/96_R3_MEDIA_ACTION_TO_PLUGIN_MCP_COMPATIBILITY_MAP_2026_09_16.md`
- `subprojects/media_beta/97_KRC_GPT_TO_PLUGIN_MIGRATION_INVENTORY_2026_09_16.md`
- `subprojects/media_beta/103_KRC_REMOTE_MCP_CANARY_IMPLEMENTATION_PACKAGE_2026_09_16.md`

## P99 hardening result

The design candidate has three independent validation layers:

1. **Source parity** — the Core skill snapshot must equal the canonical Core instructions and all 13 MEDIA operation IDs/methods/paths must equal the accepted OpenAPI.
2. **Behavioral regression fixtures** — Core protocol and MEDIA negative/boundary cases are machine-readable and checked for required dimensions.
3. **Transport boundary** — the adapter contract keeps VoiceBridge stable while live Plugin/App/MCP packaging and authentication remain separately gated.

The adapter deliberately requires no Render mutation and no backend API redesign. A future platform binding should therefore be a thin translation layer rather than a rewrite of MEDIA provider logic.

## Repository-only MCP canary

Current canary properties:

```text
name=krc_media_capabilities_canary
read_only=true
mutation=false
provider_work=false
voicebridge_binding=not_enabled
execution_tools=not_enabled
secret_required=false
network_io=false
live_endpoint=false
```

The protocol core supports deterministic tool discovery/call behavior and preserves the current 13-operation target count without enabling any of those production MEDIA operations.

It is **not** authorization to deploy, expose, connect, install, publish, or add credentials to a remote MCP server.

## Boundary

```text
PLUGIN_CANDIDATE_DESIGN=ACTIVE
CORE_REGRESSION_PACK=READY
MEDIA_NEGATIVE_REGRESSION_PACK=READY
MEDIA_ADAPTER_CONTRACT=READY
MCP_CANARY_PROTOCOL_CORE=READY
MCP_CANARY_LIVE_DEPLOYMENT=DENIED
MCP_CANARY_CHATGPT_CONNECTION=DENIED
FULL_MEDIA_MCP_IMPLEMENTATION=NOT_STARTED
GPT_MIGRATION=NOT_STARTED
PLUGIN_INSTALLATION=NOT_STARTED
PLUGIN_PUBLICATION=NOT_AUTHORIZED
PUBLIC_GPT=UNCHANGED
MAIN_MUTATION=DENIED
RENDER_CHANGE=DENIED
PR22_MERGE=DENIED
PR45_MERGE=DENIED
```

The next state-changing step requires separate owner authorization: bounded canary deployment followed by a ChatGPT custom-MCP tool-scan/connection test. Until then, the canary remains repository-only.
