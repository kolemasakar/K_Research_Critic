# K_Supervisor
Базовий опис K_Supervisor як GPT Store-first мультиагентної системи для дослідження та незалежної перевірки.

Version: 0.4
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

K_Supervisor is GPT Store-first.

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

The Python/SQLite/provider implementation remains available as an optional Standalone/API Edition and engineering reference runtime. It is not a dependency of the free GPT Store core path.

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
Phase 12 - Test and CI Hardening                    COMPLETE
Phase 13 - Modular Agent Platform                   PLANNED
```

Store package release state:

```text
ready_for_manual_publication_test
```

This means the repository package is ready for GPT Builder Preview and real Free/paid account release checks. It does not mean the GPT is already published in the GPT Store.

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

Builder configuration keeps Web search and Code Interpreter & Data Analysis enabled while Apps, Actions, mandatory external backend, developer API keys, and pinned model identifiers are excluded from the core Store path.

The actual GPT Store publication action and real Free/paid account tests are manual release operations in ChatGPT.

## Configuration and Runtime Controls

Phase 11 provides:

```text
validated frozen configuration
tracked distribution policy
secret-free TaskConfigurationSnapshot
research and critic limits
search/fetch call budgets
timeouts
retry/backoff
runtime ceilings
artifact size limits
optional standalone provider/model factory
structured usage and quality metrics
operational logging with sensitive-data redaction
```

The free Store path requires no `.env` secret.

## Persistence and Recovery

Standalone/API Edition provides storage-neutral persistence plus SQLite:

```text
runtime/k_supervisor.db
```

Persisted records include tasks, workflows, transitions, agent runs, domain assessments, CriticProfiles, approvals, effective configuration snapshots, ResearchResults, Claims, Sources, CriticReviews, usage/quality records, and artifact metadata.

Safe automatic standalone recovery checkpoints:

```text
PROFILE_REVIEW_REQUIRED
PROFILE_APPROVED
REVISE_REQUIRED
```

GPT Store Edition does not depend on private server-side SQLite. Cross-chat continuity uses the explicit user-controlled `K_SUPERVISOR_CHECKPOINT` contract.

## Phase 12 Quality Baseline

Phase 12 hardens orchestration behavior and makes repository quality gates reproducible.

Automated CI now includes:

```text
Python 3.13 full pytest suite
Python 3.14 full pytest suite
python -m pip check
python -m ruff check . --select E9,F63,F7,F82
python -m mypy models config gpt_store
python -m scripts.validate_repository
python -m scripts.validate_store_package
python -m pytest --cov --cov-report=term-missing --cov-fail-under=70
```

The validated Phase 12 implementation baseline is:

```text
169 tests passed on Python 3.13
Python 3.14 test job passed
quality job passed
85 percent total coverage
70 percent blocking coverage floor
```

The deterministic offline reference benchmark is tracked in:

```text
examples/reference_benchmark.json
tests/test_reference_benchmark.py
```

It executes four end-to-end reference tasks across literary analysis, software engineering, medicine, and geodesy. Each case validates domain resolution, explicit profile approval, autonomous completion, Critic PASS/reliability floors, evidence presence, final artifacts, and the no-private-reasoning review-protocol boundary.

Run it locally with:

```text
python -m pytest -q tests/test_reference_benchmark.py
```

The benchmark uses synthetic local fixtures. It does not call live providers and therefore remains deterministic and cost-free in CI.

See `docs/TEST_PLAN.md` and `docs/CI_QUALITY.md`.

## Optional Local / Standalone Setup

```text
git clone https://github.com/kolemasakar/K_Supervisor.git
cd K_Supervisor
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m pytest
```

For all development quality dependencies:

```text
python -m pip install -r requirements-dev.txt
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
examples/       deterministic sample and benchmark inputs
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
docs/CI_QUALITY.md
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
- The Python reference CLI uses deterministic local corpus research rather than ChatGPT-native live tools.
- CriticAgent's Python reference implementation uses conservative deterministic evidence-relation heuristics rather than full semantic LLM fact checking.
- Provider token/cost telemetry is meaningful only for optional standalone/API providers that expose it.
- `MeteredOpenAISemanticDomainProvider` remains opt-in and is not automatically selected by the provider factory.

## Output Artifacts

Logical workflow outputs remain:

```text
<TASK_ID>_FINAL_REPORT.md
<TASK_ID>_REVIEW_PROTOCOL.md
```

The GPT Store instructions define the equivalent ChatGPT-native final report/review protocol and the `K_SUPERVISOR_CHECKPOINT` continuity artifact without requiring an external service.
