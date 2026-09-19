# KRC — Core + MEDIA Migration Hardening — Checkpoint 99 — 2026-09-16

Status: P99_IMPLEMENTED / CI_PENDING / DESIGN_ONLY / PUBLICATION_HOLD

## Objective

Harden the repository-side KRC replacement candidate in areas that do not depend on the final OpenAI account migration surface:

```text
B = MEDIA parity + negative tests
C = Core regression pack
D = platform-neutral migration adapter design
```

No public GPT, Render, VoiceBridge runtime, main branch, Plugin installation, MCP deployment, or publication is changed by this checkpoint.

## B — MEDIA parity and negative hardening

Canonical operation parity remains 13/13 against:
`gpt_store/actions/media_public_r3_openapi.yaml`

Added machine-readable negative/boundary fixtures:
`plugins/krc_migration_candidate/regression/media_negative_cases.yaml`

Coverage includes:
- wrong-platform rejection;
- YouTube explicit Gemini Free consent block;
- provider-free YouTube preflight;
- no automatic paid retrieval/STT/proxy fallback;
- no Supadata/ScrapeCreators fallback;
- FAILED free-only retry only on a new explicit retry request;
- charge-uncertain replay block;
- COMPLETED reuse;
- PROCESSING/in-flight reuse and concurrency protection;
- Facebook canonical Cobalt video+audio + ffmpeg mono PCM WAV 16 kHz;
- Telegram public-web only/no login/session/bot-token fallback;
- job-id validation;
- segment pagination bounds;
- secret/error sanitization;
- MEDIA failure isolation from Core.

## C — Core regression pack

Added:
`plugins/krc_migration_candidate/regression/core_cases.yaml`

Machine-readable Core fixtures cover:
- CriticProfile direct-run gate;
- CriticProfile review/edit gate;
- HIGH-risk cross-check SHORTFALL;
- traceable PASS case;
- recovered REVIEW_REQUIRED checkpoint gate;
- MEDIA failure isolation;
- explicit English report-language behavior;
- mandatory Ukrainian protocol table and columns.

Forbidden Core regressions are explicitly enumerated, including:
```text
independent_research_before_criticprofile_approval
silent_risk_floor_reduction
silent_cross_check_floor_reduction
hidden_unqualified_shortfall
untraceable_pass_count
request_log_silently_reenabled
media_failure_blocks_core
hidden_reasoning_exposed
```

## D — platform-neutral adapter contract

Added:
`plugins/krc_migration_candidate/contracts/media_adapter.yaml`

The adapter defines a stable contract between a future OpenAI Plugin/App/MCP surface and the existing VoiceBridge MEDIA API while intentionally deferring final transport packaging.

Key properties:
- all 13 accepted operation IDs have unique adapter bindings;
- current VoiceBridge API is preserved;
- no Render/backend mutation is required by the design candidate;
- request validation preserves supported language hints, KRCM job-id shape and pagination bounds;
- YouTube consent/preflight semantics remain unchanged;
- retry semantics remain unchanged;
- charge-uncertain replay remains blocked;
- structured/sanitized errors are required;
- authentication strategy remains TBD until account-specific surface inspection;
- all credentials remain server-side only;
- MEDIA failure never blocks Core;
- MEDIA transcript remains evidence, not an automatic fact verdict;
- CriticProfile gate remains required for fact-check workflow.

## Automated tests

Expanded:
`tests/test_krc_plugin_migration_candidate.py`

New guards validate:
- Core fixture coverage and mandatory Ukrainian protocol labels;
- MEDIA negative-case coverage;
- charge-uncertain and paid-fallback fail-closed behavior;
- exact 13 adapter operation bindings;
- job-id/language/pagination request bounds;
- consent/retry/Core-isolation contract;
- fail-closed error taxonomy;
- server-side-only secret boundary;
- transport neutrality and zero required backend mutation;
- continued absence of premature `mcp.json`, `.mcp.json`, `.app.json` packaging.

## Candidate documentation

Updated:
`plugins/krc_migration_candidate/README.md`

to include the P99 hardening assets and three validation layers:
1. source parity;
2. behavioral regression fixtures;
3. transport boundary.

## Current architecture after P99

```text
KRC Core Skill candidate
        |
        +-- native research/tool capabilities (future target surface)
        |
        +-- MEDIA semantic contract
               |
               v
        transport-neutral adapter
               |
               v
        existing VoiceBridge MEDIA API
          |       |        |        |
       YouTube Instagram Facebook Telegram
```

Final OpenAI binding may later be a supported App/Connector/MCP surface, but that choice is not guessed or implemented here.

## Current boundary

```text
PROJECT=ACTIVE
P99_CORE_MEDIA_MIGRATION_HARDENING=IMPLEMENTED
CORE_REGRESSION_PACK=READY
MEDIA_NEGATIVE_REGRESSION_PACK=READY
MEDIA_ADAPTER_CONTRACT=READY
MEDIA_OPERATION_PARITY_COUNT=13
PLUGIN_CANDIDATE_SKELETON=READY
PLUGIN_APP_IMPLEMENTATION=NOT_STARTED
CUSTOM_MCP_IMPLEMENTATION=NOT_STARTED
GPT_MIGRATION=NOT_STARTED
PLUGIN_INSTALLATION=NOT_STARTED
PLUGIN_PUBLICATION=NOT_AUTHORIZED
PUBLIC_GPT=UNCHANGED
PUBLICATION=HOLD
MAIN_MUTATION=DENIED
RENDER_CHANGE=DENIED
PR22_MERGE=DENIED
PR45_MERGE=DENIED
```

## Validation state

Full repository CI must pass on the final P99 head before this checkpoint is considered accepted.

Expected gates:
- Tests / Python 3.13
- Tests / Python 3.14
- Quality gates / dependency integrity
- Ruff
- Mypy
- repository policy
- GPT Store package validation
- coverage

## Next step after PASS

Keep the current public GPT unchanged. When the account-specific migration/app surface is available, perform read-only inspection first, then bind the already hardened Core/MEDIA candidate to the supported surface and run the regression pack before any activation.
