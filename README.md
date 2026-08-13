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
Phase 8 - ReportGenerator and Final Artifacts: COMPLETE.

Next implementation phase:

```text
Phase 9 - End-to-End MVP
```

The repository now includes deterministic domain resolution, multi-domain detection, dynamic CriticProfile approval workflows, a generic ResearchAgent, structured ResearchResult output, provider-neutral web tool adapters, normalized tool errors, source metadata extraction, URL/source deduplication, source validation, reliability classification with explicit override support, bidirectional claim-to-source linking, citation management, a generic profile-driven CriticAgent, a Supervisor-owned autonomous Research-Critic revision loop, and ReportGenerator finalization.

The Phase 7 loop versions research results by iteration, feeds structured CriticReview recommendations back to ResearchAgent, enforces the approved confidence threshold and max_iterations, rejects incomplete PARTIAL critic execution as an accepted PASS, records agent runs and completed iteration records, stops on accepted PASS, and terminates explicitly with FAILED or COMPLETED_WITH_LIMITATIONS where appropriate.

Phase 8 generates UTF-8 `<TASK_ID>_FINAL_REPORT.md` and `<TASK_ID>_REVIEW_PROTOCOL.md` artifacts. The final report contains structured findings, source citations, uncertainty, limitations, and bibliography. The review protocol records iteration decisions, reliability scores, critical issues, requested changes, applied changes, unresolved items, and final status without exposing hidden chain-of-thought or private model reasoning.

Artifact metadata includes type, path, UTF-8 encoding, checksum, creation run, and final task status. Approved research finalization is routed through FINALIZING to FINALIZED. Useful results that reached COMPLETED_WITH_LIMITATIONS can still produce explicit limitation artifacts without changing that terminal status.

Iteration, agent-run, and artifact audit data is in-memory in the current MVP implementation. Durable restart-safe persistence remains scheduled for Phase 10.

Concrete external search/fetch providers remain pluggable behind the provider-neutral adapters rather than being embedded in agent logic.

The Phase 6 CriticAgent uses conservative deterministic evidence-relation heuristics for the MVP. Semantic LLM-based verification remains a later enhancement and does not change the approved CriticProfile boundary.

Hybrid semantic domain resolution is scheduled as a post-MVP enhancement after Phase 9. See `docs/HYBRID_RESOLVER_PLAN.md`.

A runnable end-to-end application entry point is not implemented yet; this is the scope of Phase 9.

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

The first complete workflow generates:

```text
<TASK_ID>_FINAL_REPORT.md
<TASK_ID>_REVIEW_PROTOCOL.md
```

Generated runtime files are not committed by default.
