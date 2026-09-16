# KRC Plugin Migration Candidate

Status: DESIGN_ONLY / NOT_INSTALLABLE / NOT_DEPLOYED / PUBLICATION_HOLD

This directory is a repository-side migration candidate for moving K-Research & Critic from the retiring Custom GPT surface to the OpenAI Plugin model. It is deliberately platform-neutral until the account-specific migration surface is available and inspected.

## Why this is not an installable plugin yet

Current OpenAI guidance says plugins can combine reusable skills with connected apps, while Custom GPT Actions do not migrate automatically. A replacement MEDIA integration therefore needs an explicit supported app/connector or custom MCP implementation and its permissions must be reviewed before use.

This candidate intentionally does **not** contain `mcp.json`, `.mcp.json`, `.app.json`, a remote MCP server implementation, provider credentials, bearer tokens, cookies, browser-profile identifiers, or deployment configuration. Raw MCP declarations can change product-surface availability, so the final packaging must be derived from the actual migration/app surface available to this account rather than guessed in advance.

## Candidate assets

- `skills/krc_core/SKILL.md` — exact snapshot of the current accepted Core instructions, wrapped only with migration metadata.
- `contracts/media_tools.yaml` — 1:1 parity contract for the 13 accepted R3 MEDIA Action operations.
- `contracts/media_adapter.yaml` — transport-neutral request/response, auth, retry, error and platform-boundary contract between the future Plugin/App/MCP surface and the existing VoiceBridge MEDIA API.
- `regression/core_cases.yaml` — machine-readable Core behavioral fixtures covering CriticProfile, cross-check, traceability, checkpoint recovery, language, final protocol and MEDIA failure isolation.
- `regression/media_negative_cases.yaml` — negative/boundary MEDIA fixtures covering consent, wrong-platform routing, paid fallback prohibition, deterministic retry, charge uncertainty, reuse/concurrency, input validation, secret sanitization and platform-specific hard guards.
- `tests/test_krc_plugin_migration_candidate.py` — repository guards for Core parity, exact 13-operation parity, transport-neutral adapter invariants, regression coverage, free-only policy, consent/retry semantics, and secret/config boundaries.

Canonical sources remain authoritative:

- `prompts/GPT_STORE_INSTRUCTIONS.md`
- `prompts/GPT_STORE_MEDIA_R3_PUBLIC_ADDENDUM.md`
- `gpt_store/actions/media_public_r3_openapi.yaml`
- `subprojects/media_beta/96_R3_MEDIA_ACTION_TO_PLUGIN_MCP_COMPATIBILITY_MAP_2026_09_16.md`
- `subprojects/media_beta/97_KRC_GPT_TO_PLUGIN_MIGRATION_INVENTORY_2026_09_16.md`

## P99 hardening result

The design candidate now has three independent validation layers:

1. **Source parity** — the Core skill snapshot must equal the canonical Core instructions and all 13 MEDIA operation IDs/methods/paths must equal the accepted OpenAPI.
2. **Behavioral regression fixtures** — Core protocol and MEDIA negative/boundary cases are machine-readable and checked for required dimensions.
3. **Transport boundary** — the adapter contract keeps VoiceBridge stable while deferring final Plugin/App/MCP packaging and authentication until the actual account-specific migration surface is inspected.

The adapter deliberately requires no Render mutation and no backend API redesign. A future platform binding should therefore be a thin translation layer rather than a rewrite of MEDIA provider logic.

## Boundary

```text
PLUGIN_CANDIDATE_DESIGN=ACTIVE
CORE_REGRESSION_PACK=READY
MEDIA_NEGATIVE_REGRESSION_PACK=READY
MEDIA_ADAPTER_CONTRACT=READY
PLUGIN_APP_IMPLEMENTATION=NOT_STARTED
CUSTOM_MCP_IMPLEMENTATION=NOT_STARTED
GPT_MIGRATION=NOT_STARTED
PLUGIN_INSTALLATION=NOT_STARTED
PLUGIN_PUBLICATION=NOT_AUTHORIZED
PUBLIC_GPT=UNCHANGED
MAIN_MUTATION=DENIED
RENDER_CHANGE=DENIED
PR22_MERGE=DENIED
PR45_MERGE=DENIED
```

The next implementation step is permitted only after the actual account migration/app surface is inspected and the required app/MCP permissions and authentication model are known.