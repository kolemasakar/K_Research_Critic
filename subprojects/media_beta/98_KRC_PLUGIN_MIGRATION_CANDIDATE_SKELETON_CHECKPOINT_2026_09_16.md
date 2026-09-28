# KRC — Plugin Migration Candidate Skeleton Checkpoint — 2026-09-16

Status: CANDIDATE_SKELETON_READY / DESIGN_ONLY / NOT_INSTALLABLE / PUBLICATION_HOLD

## Purpose

This checkpoint records the first concrete repository-side replacement skeleton for K-Research & Critic after the planned Custom GPT -> Plugin transition. It does not migrate, install, connect, deploy, publish, or replace the current public GPT.

## Current OpenAI platform facts used for this design

As of 2026-09-16, current OpenAI guidance states that:
- existing Custom GPTs remain usable until the applicable retirement date;
- migration is planned to convert GPT instructions into a Plugin skill;
- Custom GPT Actions do not transfer automatically and required integrations must be rebuilt using a supported connector or custom MCP server;
- Plugins may package skills and connected apps;
- account/workspace migration availability and permissions can vary;
- imported plugins that declare their own MCP server configuration can be limited to Desktop-only surfaces, so final packaging must not be guessed before the target account surface is inspected.

Therefore the candidate is deliberately platform-neutral.

## New candidate assets

```text
plugins/krc_migration_candidate/README.md
plugins/krc_migration_candidate/skills/krc_core/SKILL.md
plugins/krc_migration_candidate/contracts/media_tools.yaml
tests/test_krc_plugin_migration_candidate.py
```

## Core skill candidate

`skills/krc_core/SKILL.md` contains an exact snapshot of:
`prompts/GPT_STORE_INSTRUCTIONS.md`

A regression test extracts the marked snapshot and requires exact parity with the canonical Core source after newline normalization. The skill candidate therefore cannot silently drift from the accepted CriticProfile, research, cross-check, traceability, review-protocol, language, checkpoint, and privacy rules.

No MEDIA instructions are injected into the Core snapshot.

## MEDIA integration candidate

The MEDIA contract preserves all **13** current R3 Action operation IDs and their HTTP method/path mapping.

The earlier conversational statement that R3 exposed 12 operations was incorrect; the canonical parity count is 13:
- 1 capability operation;
- 5 YouTube operations;
- 3 Instagram operations;
- 1 Facebook operation;
- 1 Telegram operation;
- 2 shared non-YouTube status/segment operations.

The contract preserves:
- free-only / fail-closed policy;
- no automatic retry loop;
- FAILED free-only fresh retry only on a new explicit retry request;
- charge-uncertain replay blocked;
- explicit Gemini Free consent before YouTube provider work;
- YouTube Gemini-direct only;
- Instagram Cobalt -> AssemblyAI;
- Facebook Cobalt video+audio -> ffmpeg mono PCM WAV 16 kHz -> AssemblyAI;
- Telegram public web -> AssemblyAI;
- audit fields needed for durable-state evidence.

## Authentication boundary

No authentication scheme has been invented for the future Plugin/App surface.

```text
final_strategy=TBD_AFTER_ACCOUNT_MIGRATION_SURFACE_INSPECTION
secret_visibility=SERVER_SIDE_ONLY
model_visible_secret=false
repository_secret=false
```

No bearer token, API key, concrete Browser Context Profile identifier, cookie, session material, or signed media URL is added.

## Packaging boundary

The candidate intentionally contains no:
- `mcp.json`;
- `.mcp.json`;
- `.app.json`;
- MCP server implementation;
- app connection;
- deployment configuration.

This prevents an unverified packaging choice from accidentally creating a Desktop-only or otherwise incompatible replacement before the actual migration surface is available for this account.

## Regression gate

`tests/test_krc_plugin_migration_candidate.py` requires:
1. exact Core snapshot parity;
2. exact 13-operation OpenAPI parity;
3. free-only/fail-closed policy;
4. YouTube explicit consent semantics;
5. platform hard guards;
6. no premature MCP/app packaging;
7. no concrete browser profile or common secret prefixes;
8. future authentication remains explicitly unfinalized and server-side only.

## Canonical state

```text
PROJECT=ACTIVE
CUSTOM_GPT_RETIREMENT_PREP=ACTIVE
PLUGIN_MIGRATION_PREP=READY
PLUGIN_CANDIDATE_SKELETON=READY
CORE_SKILL_CANDIDATE=READY
MEDIA_TOOL_CONTRACT_CANDIDATE=READY
MEDIA_OPERATION_PARITY_COUNT=13
PLUGIN_APP_IMPLEMENTATION=NOT_STARTED
CUSTOM_MCP_IMPLEMENTATION=NOT_STARTED
GPT_MIGRATION=NOT_STARTED
PLUGIN_INSTALLATION=NOT_STARTED
PLUGIN_PUBLICATION=NOT_AUTHORIZED
PUBLIC_GPT=UNCHANGED
BROWSER_AUTOMATION_START=BLOCKED_BY_OPENAI_SAFETY_LAYER
MAIN_MUTATION=DENIED
RENDER_CHANGE=DENIED
PR22_MERGE=DENIED
PR45_MERGE=DENIED
```

## Resume point

After CI acceptance, the next useful step is read-only inspection of the account-specific migration/plugin surface when it becomes available. Only then select the supported app/MCP packaging and authentication mechanism. Existing VoiceBridge/R3 semantics remain the parity baseline.
