# K_Supervisor
Базовий опис мультиагентної системи K_Supervisor та локального запуску проєкту.

Version: 0.1
Status: DEVELOPMENT

## Overview

K_Supervisor is a reusable multi-agent orchestration system.

The first product workflow is a research and independent critique pipeline controlled by Supervisor.

Core rule:

```text
Supervisor proposes.
User approves or edits.
Critic executes.
```

The CriticAgent is generic and receives a task-specific approved CriticProfile instead of using a hard-coded domain role.

## Current Status

Phase 0 - Repository Bootstrap: COMPLETE.
Phase 1 - Core Domain Models and Contracts: COMPLETE.
Phase 2 - Supervisor Foundation: COMPLETE.
Phase 3 - Domain Resolver and CriticProfile Workflow: COMPLETE.
Phase 4 - ResearchAgent MVP: COMPLETE.

Next implementation phase:

```text
Phase 5 - Tools and Evidence Layer
```

The repository now includes deterministic domain resolution, multi-domain detection, dynamic CriticProfile approval workflows, a generic ResearchAgent, structured ResearchResult output, claim-to-source validation, revision-feedback handling, provider-neutral research tool interfaces, and explicit partial/failure behavior.

Concrete web_search/web_fetch adapters and evidence normalization are intentionally deferred to Phase 5.

Hybrid semantic domain resolution is scheduled as a post-MVP enhancement after Phase 9. See `docs/HYBRID_RESOLVER_PLAN.md`.

A runnable end-to-end application entry point is not implemented yet.

## Repository Structure

```text
agents/       agent implementations
supervisor/   orchestration core
models/       domain and transport models
tools/        external capability adapters and interfaces
prompts/      prompt assets
config/       tracked non-secret configuration
tests/        automated tests
scripts/      development and maintenance scripts
output/       generated user-facing artifacts
logs/         runtime logs
docs/         project specifications and standards
```

## Local Development Setup

Clone the repository and enter the project directory:

```text
git clone https://github.com/kolemasakar/K_Supervisor.git
cd K_Supervisor
```

Create a virtual environment:

```text
python -m venv .venv
```

Windows activation:

```text
.venv\Scripts\activate
```

Install the initial dependencies:

```text
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Create a local environment file:

```text
copy .env.example .env
```

Run tests:

```text
python -m pytest
```

## Configuration

Tracked runtime defaults:

```text
config/settings.yaml
```

Local secrets and environment-specific values:

```text
.env
```

Never commit `.env` or real secret values.

## Documentation

Canonical project documents:

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
```

## Output Artifacts

The first complete workflow is expected to generate:

```text
<TASK_ID>_FINAL_REPORT.md
<TASK_ID>_REVIEW_PROTOCOL.md
```

Generated runtime files are not committed by default.
