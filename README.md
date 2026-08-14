# K-Research & Critic
Базовий опис завершеного production-продукту K-Research & Critic для дослідження та незалежної перевірки.

Version: 1.0
Status: PRODUCTION / MAINTENANCE

## Overview

K-Research & Critic is a published GPT Store product for structured research, independent critique, autonomous revision, and sourced final reporting.

Repository:

```text
kolemasakar/K_Research_Critic
```

Public product:

```text
K-Research & Critic
```

Stable legacy engineering identifiers intentionally retained for compatibility include:

```text
Checkpoint marker: K_SUPERVISOR_CHECKPOINT
Standalone database: runtime/k_supervisor.db
```

Core rule:

```text
Supervisor proposes.
User approves or edits.
Critic executes.
```

## Product Status

```text
Phase 0-10                                           COMPLETE
Post-MVP Hybrid Domain Resolver                     COMPLETE
Phase 11 - Configuration, Cost, Quality Controls    COMPLETE
Phase 12 - Test and CI Hardening                    COMPLETE
GPT Store publication                               COMPLETE
Free-account live validation                        PASS
Paid-account runtime/model-switch validation        PASS
Store discoverability                               PASS
Production smoke test                               PASS
Release line                                        v1.0.x
Repository mode                                     MAINTENANCE
```

The former planned Phase 13 Modular Agent Platform has been removed from this product roadmap. General modular multi-agent platform development continues in a separate new repository named `K_Supervisor`, with a new roadmap starting from Phase 0.

## Release

Canonical first production release:

```text
K-Research & Critic v1.0.0
Git tag: v1.0.0
```

The `v1.0.0` tag must point to the finalized maintenance-synchronization commit with fully green CI.

## Primary Product Target

K-Research & Critic is GPT Store-first.

```text
GPT Store Edition
  - public ChatGPT product
  - free-user compatible
  - no developer-owned API key required
  - no mandatory external backend
  - model policy follows the user's ChatGPT plan
  - no pinned model identifier
  - user may switch available models/runtimes when exposed by the plan
```

The Python/SQLite/provider implementation remains available as an optional standalone engineering reference runtime. It is not a dependency of the public Store path.

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
                         +-- FINAL REPORT
                         +-- REVIEW PROTOCOL
```

In the GPT Store Edition, Research and Critic are separated logical passes inside one ChatGPT runtime rather than process-isolated model instances.

## GPT Store Package

Canonical package files:

```text
gpt_store/manifest.yaml
prompts/GPT_STORE_INSTRUCTIONS.md
gpt_store/checkpoint.py
gpt_store/checkpoint_example.json
scripts/validate_store_package.py
docs/GPT_STORE_DEPLOYMENT.md
docs/GPT_STORE_PACKAGE.md
```

Production package state includes:

```text
publication_state: published
production_smoke_test_passed: true
```

## Quality Baseline

CI includes:

```text
Python 3.13 full pytest suite
Python 3.14 full pytest suite
python -m pip check
python -m ruff check . --select E9,F63,F7,F82
python -m mypy models config gpt_store
python -m scripts.validate_repository
python -m scripts.validate_store_package
coverage gate
```

The release baseline has passed Python 3.13, Python 3.14, repository validation, GPT Store package validation, lint/type gates, and coverage checks.

## Optional Local / Standalone Setup

```text
git clone https://github.com/kolemasakar/K_Research_Critic.git
cd K_Research_Critic
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m pytest
```

For development quality dependencies:

```text
python -m pip install -r requirements-dev.txt
```

`.env` is optional and is needed only when an optional standalone integration requires a secret.

## End-to-End Local CLI

The bundled CLI can use the deterministic local corpus provider for offline/reference execution:

```text
python -m scripts.run_research --task "Explain software architecture behavior" --corpus examples/sample_corpus.json
```

Explicit non-interactive profile approval:

```text
python -m scripts.run_research --task "Explain software architecture behavior" --corpus examples/sample_corpus.json --approve-profile
```

## Persistence and Recovery

Standalone/reference runtime persistence uses:

```text
runtime/k_supervisor.db
```

The database name is a stable legacy engineering identifier and is intentionally retained in the v1.0 line.

GPT Store cross-chat continuity uses the explicit user-controlled:

```text
K_SUPERVISOR_CHECKPOINT
```

## Repository Structure

```text
agents/         agent implementations
supervisor/     orchestration core
persistence/    persistence and SQLite reference store
providers/      optional provider adapters
observability/  logging and redaction
gpt_store/      GPT Store manifest and checkpoint contract
models/         domain and transport contracts
tools/          capability adapters and evidence utilities
config/         tracked non-secret configuration
prompts/        Store prompt assets
tests/          automated tests
scripts/        local commands and validators
examples/       deterministic sample and benchmark inputs
output/         generated standalone artifacts
runtime/        local SQLite runtime data; ignored by Git
logs/           standalone operational logs
docs/           canonical project documentation
```

## Maintenance Policy

This repository is no longer the development home of the general modular K_Supervisor platform.

Allowed work here:

```text
bug fixes
security fixes
GPT Store compatibility updates
OpenAI platform compatibility updates
regression fixes
documentation corrections
narrow UX improvements
maintenance releases v1.0.1, v1.0.2, ...
```

Out of scope here:

```text
general capability-based agent platform
automatic agent discovery
large modular agent catalog
capability router development
new platform roadmap phases
```

Those belong to the separate `K_Supervisor` project.

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

## Successor Project

The reusable modular multi-agent platform is developed separately as:

```text
K_Supervisor
```

That project starts with a clean repository, a new architecture decision set, and a new roadmap beginning at Phase 0. K-Research & Critic remains the completed production reference product and is not rewritten merely to follow future platform experiments.
