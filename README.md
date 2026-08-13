# K_Supervisor
Базовий опис K_Supervisor як GPT Store-first мультиагентної системи для дослідження та незалежної перевірки.

Version: 0.3
Status: DEVELOPMENT

## Overview

K_Supervisor is a reusable multi-agent orchestration system.

Core rule:

```text
Supervisor proposes.
User approves or edits.
Critic executes.
```

The first product workflow combines ResearchAgent, independent CriticAgent review, autonomous revision cycles, and final report generation.

## Primary Product Target

K_Supervisor is **GPT Store-first**.

Primary public edition:

```text
GPT Store Edition
  - intended for public ChatGPT use
  - free-user compatible
  - no developer-owned API key required
  - no mandatory external backend
  - model policy follows the user's ChatGPT plan
  - no pinned model identifier
  - user may switch models when their plan exposes alternatives
```

The current Python/SQLite/provider implementation remains available as an optional **Standalone/API Edition** and engineering reference runtime. It is not a dependency of the free GPT Store core path.

See `docs/GPT_STORE_DEPLOYMENT.md` and `docs/GPT_STORE_PACKAGE.md`.

## Current Status

```text
Phase 0-10                                           COMPLETE
Post-MVP Hybrid Domain Resolver                     COMPLETE
Phase 11 - Configuration, Cost, Quality Controls    COMPLETE
  11.1 Configuration Core                           COMPLETE
  11.2 Task Configuration Snapshot                  COMPLETE
  11.3 Provider / Model Factory                     COMPLETE
  11.4 Runtime Controls                             COMPLETE
  11.4A GPT Store-first Distribution Policy         COMPLETE
  11.5 Usage, Cost, and Quality Metrics             COMPLETE
  11.6 Logging / Secret Redaction                   COMPLETE
  11.7 GPT Store Packaging / Publication Readiness  COMPLETE
Phase 12 - Test and CI Hardening                    NEXT
```

Store package release state:

```text
ready_for_manual_publication_test
```

This means the repository package is ready for GPT Builder Preview and real Free/paid account release checks. It does **not** mean the GPT is already published in the GPT Store.

## Logical Workflow

```text
User task
   |
   v
Domain resolution
   |
   v
CriticProfile proposal
   |
   v
USER APPROVAL / EDIT / REJECT
   |
   v
ResearchAgent
   |
   v
CriticAgent
   |
   +---- REVISE ----> ResearchAgent
   |
   +---- PASS ------> ReportGenerator
                         |
                         +-- <TASK_ID>_FINAL_REPORT.md
                         +-- <TASK_ID>_REVIEW_PROTOCOL.md
```

The same logical workflow is preserved across Store and standalone editions. In the Store Edition, Research and Critic are separated logical passes inside one ChatGPT runtime rather than process-isolated model instances.

## GPT Store Package

The publication package is tracked in the repository:

```text
gpt_store/manifest.yaml
prompts/GPT_STORE_INSTRUCTIONS.md
gpt_store/checkpoint.py
gpt_store/checkpoint_example.json
scripts/validate_store_package.py
docs/GPT_STORE_PACKAGE.md
```

Static validation:

```text
python -m scripts.validate_store_package
python -m pytest
```

Builder configuration from the manifest:

```text
Name: K_Supervisor
Recommended model: unset
Model policy: user_plan
Web search: enabled
Code Interpreter & Data Analysis: enabled
Image generation: disabled
Apps: disabled
Actions: disabled
Knowledge files required: no
Developer API key: no
External backend: no
```

The actual GPT Store publication action and real Free/paid account tests are manual release operations in ChatGPT.

## Distribution and Model Policy

Tracked defaults in `config/settings.yaml` include:

```yaml
distribution:
  primary_channel: chatgpt_store
  free_user_compatible: true
  developer_api_key_required: false
  model_policy: user_plan
  recommended_model: null
  allow_user_model_switch: true
  external_backend_required: false
```

These are validated as system-level distribution invariants for the Store profile.

`recommended_model: null` is intentional. K_Supervisor does not hard-code a ChatGPT model name that could be retired or unavailable to a user.

## Domain Resolution

Logical domain resolution supports:

```text
RuleBasedResolver
LLMSemanticResolver
HybridResolver
```

HybridResolver preserves deterministic fallback, risk floors, semantic schema validation, and material-conflict audit.

For the Python reference runtime, Phase 11.3 includes an optional `OpenAISemanticDomainProvider` behind the provider-neutral boundary. That adapter may require `OPENAI_API_KEY` when explicitly selected for standalone/API execution.

For the GPT Store Edition, semantic reasoning uses the ChatGPT host runtime and requires no developer secret.

## Persistence and Recovery

Standalone/API Edition provides storage-neutral persistence plus SQLite:

```text
runtime/k_supervisor.db
```

Persisted records include tasks, workflows, transitions, agent runs, domain assessments, CriticProfiles, approvals, ResearchResults, Claims, Sources, CriticReviews, and artifact metadata.

Safe automatic standalone recovery checkpoints:

```text
PROFILE_REVIEW_REQUIRED
PROFILE_APPROVED
REVISE_REQUIRED
```

GPT Store Edition does not depend on private server-side SQLite. Each separate GPT conversation starts fresh, so cross-chat continuity is implemented with the explicit user-controlled `K_SUPERVISOR_CHECKPOINT` contract.

Safe Store checkpoint states:

```text
PROFILE_REVIEW_REQUIRED
PROFILE_APPROVED
REVISE_REQUIRED
APPROVED
FINALIZED
COMPLETED_WITH_LIMITATIONS
FAILED
```

Ambiguous mid-agent states are not replayed automatically.

## Configuration and Runtime Controls

Phase 11.1-11.4A provide:

```text
validated frozen configuration
tracked distribution policy
secret-free TaskConfigurationSnapshot
research/critic limits
search/fetch call budgets
timeouts
retry/backoff
runtime ceilings
artifact size limits
optional standalone provider/model factory
```

The free Store path requires no `.env` secret.

## Usage and Quality Metrics

Phase 11.5 adds runtime-independent `TaskQualityMetrics` derived from existing workflow state rather than from new model calls. Metrics include iteration count, PASS/REVISE history, reliability scores, claim/source coverage, claim verification, unresolved claims, critical issues, contradictions, missing topics, agent-run counts, tool calls, warnings, errors, and retries.

Quality metrics can be reconstructed from `TaskAuditSnapshot` after restart. The standalone audit CLI displays the key quality fields together with the persisted task audit.

The GPT Store Edition does not request provider token or billing telemetry and does not create developer-funded API calls merely to collect metrics.

Optional Standalone/API integrations may use `ProviderUsageRecord` and `MeteredOpenAISemanticDomainProvider` to capture API attempts and provider-reported token usage. Estimated cost is produced only when the provider exposes token counts and pricing is supplied explicitly. The metered provider is opt-in and is not the default GPT Store path.

## Logging and Sensitive-data Redaction

Phase 11.6 adds a standalone `OperationalLogger` that writes structured UTF-8 JSONL events to `logs/k_supervisor.jsonl` by default. Runtime events correlate task, workflow, agent run, agent, and request identifiers without requiring raw task or report content in the log.

`SensitiveDataRedactor` recursively removes configured RuntimeSecrets, secret-like fields, Bearer credentials, API-key patterns, JWT-like values, URI credentials, and common secret assignments. Private reasoning fields such as chain-of-thought or scratchpad content are removed before persistence.

`logging.redact_secrets: true` is a validated system invariant and cannot be disabled by a normal settings file.

The GPT Store Edition does not require a private logging backend. Its audit equivalent is user-visible workflow state, CriticProfile approval, PASS/REVISE history, quality metrics, final/review artifacts, explicit limitations, and the checkpoint artifact.

See `docs/LOGGING.md`.

## Optional Local / Standalone Setup

The Python runtime is useful for engineering, automated tests, persistence validation, and optional external deployments.

```text
git clone https://github.com/kolemasakar/K_Supervisor.git
cd K_Supervisor
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m pytest
```

`.env` is optional and is needed only when a selected standalone integration requires a secret.

## End-to-End Local CLI

The bundled CLI uses `JsonCorpusProvider`, a deterministic local corpus provider for reproducible tests/offline execution.

```text
python -m scripts.run_research --task "Explain software architecture behavior" --corpus examples/sample_corpus.json
```

Explicit non-interactive approval:

```text
python -m scripts.run_research --task "Explain software architecture behavior" --corpus examples/sample_corpus.json --approve-profile
```

The local CLI is an engineering/reference runtime, not the GPT Store execution surface.

## Audit CLI

```text
python -m scripts.audit_task --task-id TASK_EXAMPLE --database runtime/k_supervisor.db
```

## Repository Structure

```text
agents/         agent implementations
supervisor/     orchestration core
persistence/    storage-neutral persistence and SQLite store
providers/      optional concrete external provider adapters
observability/  structured operational logging and redaction
gpt_store/      GPT Store manifest and checkpoint contract
models/         domain and transport contracts
tools/          external capability adapters and evidence utilities
config/         tracked non-secret configuration
prompts/        GPT Store and future prompt assets
tests/          automated tests
scripts/        local commands and package validators
examples/       deterministic sample inputs
output/         generated standalone artifacts
runtime/        local SQLite runtime data; ignored by Git
logs/           standalone operational logs
docs/           canonical project documentation
```

## Canonical Documentation

```text
docs/PROJECT_FILE_STANDARD.md
docs/ARCHITECTURE.md
docs/ROADMAP.md
docs/AGENT_INTERFACE.md
docs/DATA_MODELS.md
docs/RESEARCH_WORKFLOW.md
docs/CONFIGURATION.md
docs/TEST_PLAN.md
docs/HYBRID_RESOLVER_PLAN.md
docs/PERSISTENCE.md
docs/GPT_STORE_DEPLOYMENT.md
docs/GPT_STORE_PACKAGE.md
docs/LOGGING.md
```

## Current Known Boundaries

- The repository package is ready for manual GPT Builder Preview/publication testing but has not been published automatically.
- Live Free-account execution and paid-account model-switch behavior must be verified in real ChatGPT accounts before public release.
- Store Edition has no mandatory private backend, SQLite, or private operational-log dependency.
- Each separate Custom GPT conversation starts fresh; cross-chat continuation depends on the explicit checkpoint artifact.
- The Python reference CLI still uses deterministic local corpus research rather than ChatGPT-native live tools.
- CriticAgent's Python reference implementation uses conservative deterministic evidence-relation heuristics rather than full semantic LLM fact checking.
- Provider token/cost telemetry is only meaningful for optional standalone/API providers that expose it.
- `MeteredOpenAISemanticDomainProvider` remains opt-in and is not automatically selected by the provider factory.

## Validation

Phase 11.7 static validation:

```text
Validated head: fb0d84468dddab88f15f425fda217cbabe1b057f
GitHub Actions: 31666028204
156 tests passed
```

## Output Artifacts

Logical workflow outputs remain:

```text
<TASK_ID>_FINAL_REPORT.md
<TASK_ID>_REVIEW_PROTOCOL.md
```

The GPT Store instructions define the equivalent ChatGPT-native final report/review protocol and the `K_SUPERVISOR_CHECKPOINT` continuity artifact without requiring an external service.
