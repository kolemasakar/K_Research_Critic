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
Phase 5 - Tools and Evidence Layer: COMPLETE.
Phase 6 - CriticAgent MVP: COMPLETE.
Phase 7 - Autonomous Research-Critic Loop: COMPLETE.

Next implementation phase:

```text
Phase 8 - ReportGenerator and Final Artifacts
```

The repository now includes deterministic domain resolution, multi-domain detection, dynamic CriticProfile approval workflows, a generic ResearchAgent, structured ResearchResult output, provider-neutral web tool adapters, normalized tool errors, source metadata extraction, URL/source deduplication, source validation, reliability classification with explicit override support, bidirectional claim-to-source linking, citation management, a generic profile-driven CriticAgent, and a Supervisor-owned autonomous Research-Critic revision loop.

The Phase 7 loop versions research results by iteration, feeds structured CriticReview recommendations back to ResearchAgent, enforces the approved confidence threshold and max_iterations, rejects incomplete PARTIAL critic execution as an accepted PASS, records agent runs and completed iteration records, stops on accepted PASS, and terminates explicitly with FAILED or COMPLETED_WITH_LIMITATIONS where appropriate.

Iteration and agent-run audit data is in-memory in the current MVP implementation. Durable restart-safe persistence remains scheduled for Phase 10.

Concrete external search/fetch providers remain pluggable behind the provider-neutral adapters rather than being embedded in agent logic.

The Phase 6 CriticAgent uses conservative deterministic evidence-relation heuristics for the MVP. Semantic LLM-based verification remains a later enhancement and does not change the approved CriticProfile boundary.

Hybrid semantic domain resolution is scheduled as a post-MVP enhancement after Phase 9. See `docs/HYBRID_RESOLVER_PLAN.md`.

A runnable end-to-end application entry point is not implemented yet.

## Repository Structure

```text
agents/       agent implementations
supervisor/   orchestration core
models/       domain and transport models
tools/        external capability adapters and evidence utilities
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
