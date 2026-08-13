# K_Supervisor
Базовий опис K_Supervisor як GPT Store-first мультиагентної системи для дослідження та незалежної перевірки.

Version: 0.2
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

K_Supervisor is now **GPT Store-first**.

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

See `docs/GPT_STORE_DEPLOYMENT.md`.

## Current Status

```text
Phase 0-10                                           COMPLETE
Post-MVP Hybrid Domain Resolver                     COMPLETE
Phase 11 - Configuration, Cost, Quality Controls    IN PROGRESS
  11.1 Configuration Core                           COMPLETE
  11.2 Task Configuration Snapshot                  COMPLETE
  11.3 Provider / Model Factory                     COMPLETE
  11.4 Runtime Controls                             COMPLETE
  11.4A GPT Store-first Distribution Policy         COMPLETE
  11.5 Usage, Cost, and Quality Metrics             NEXT
  11.6 Logging / Secret Redaction                   PLANNED
  11.7 GPT Store Packaging / Publication Readiness  PLANNED
```

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

The same logical workflow is preserved across Store and standalone editions.

## Distribution and Model Policy

Tracked defaults in `config/settings.yaml` now include:

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

For the GPT Store Edition, semantic reasoning must use the ChatGPT host runtime and must not require a developer secret.

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

GPT Store Edition does not depend on private server-side SQLite. Baseline state is conversation-local. Cross-chat continuity is planned through an explicit checkpoint/recovery artifact during Store packaging.

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

Example template:

```text
copy .env.example .env
```

## End-to-End Local CLI

The bundled CLI currently uses `JsonCorpusProvider`, a deterministic local corpus provider for reproducible tests/offline execution.

```text
python -m scripts.run_research --task "Explain software architecture behavior" --corpus examples/sample_corpus.json
```

Explicit non-interactive approval:

```text
python -m scripts.run_research --task "Explain software architecture behavior" --corpus examples/sample_corpus.json --approve-profile
```

The local CLI is an engineering/reference runtime, not the final GPT Store execution surface.

## Audit CLI

```text
python -m scripts.audit_task --task-id TASK_EXAMPLE --database runtime/k_supervisor.db
```

## Repository Structure

```text
agents/       agent implementations
supervisor/   orchestration core
persistence/  storage-neutral persistence and SQLite store
providers/    optional concrete external provider adapters
models/       domain and transport contracts
tools/        external capability adapters and evidence utilities
config/       tracked non-secret configuration
prompts/      prompt assets
tests/        automated tests
scripts/      local commands and maintenance utilities
examples/     deterministic sample inputs
output/       generated standalone artifacts
runtime/      local SQLite runtime data; ignored by Git
logs/         standalone operational logs
docs/         canonical project documentation
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
```

## Current Known Boundaries

- GPT Store packaging/instructions are not yet implemented; scheduled for Phase 11.7.
- Store Edition has no mandatory private backend, so SQLite restart semantics do not directly apply inside ChatGPT.
- The Python reference CLI still uses deterministic local corpus research rather than ChatGPT-native live tools.
- CriticAgent's current Python implementation uses conservative deterministic evidence-relation heuristics rather than full semantic LLM fact checking.
- Provider token/cost telemetry is only meaningful for optional standalone/API providers that expose it.
- Store Edition must not assume access to provider token/cost data.

## Output Artifacts

Logical workflow outputs remain:

```text
<TASK_ID>_FINAL_REPORT.md
<TASK_ID>_REVIEW_PROTOCOL.md
```

Store packaging will define the equivalent ChatGPT-native artifact and checkpoint experience without requiring an external service.
