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

Next implementation phase:

```text
Phase 2 - Supervisor Foundation
```

The repository now contains architecture and contract documentation, development bootstrap configuration, validated Pydantic contract models, identifier generation, and Phase 1 contract tests. A runnable end-to-end application entry point is not implemented yet.

## Repository Structure

```text
agents/       agent implementations
supervisor/   orchestration core
models/       domain and transport models
tools/        external capability adapters
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
```

## Output Artifacts

The first complete workflow is expected to generate:

```text
<TASK_ID>_FINAL_REPORT.md
<TASK_ID>_REVIEW_PROTOCOL.md
```

Generated runtime files are not committed by default.
