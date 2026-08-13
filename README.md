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
Phase 9 - End-to-End MVP: COMPLETE.

MVP boundary reached.

Next scheduled implementation:

```text
Post-MVP Enhancement - Hybrid Domain Resolver
```

The repository now includes deterministic domain resolution, multi-domain detection, dynamic CriticProfile approval workflows, a generic ResearchAgent, structured ResearchResult output, provider-neutral web tool adapters, normalized tool errors, source metadata extraction, URL/source deduplication, source validation, reliability classification with explicit override support, bidirectional claim-to-source linking, citation management, a generic profile-driven CriticAgent, a Supervisor-owned autonomous Research-Critic revision loop, ReportGenerator finalization, and a runnable Phase 9 application layer.

`KSupervisorApplication` composes task intake, domain assessment, CriticProfile review, explicit user approval, autonomous Research-Critic iterations, deterministic termination, and final artifact generation into one programmatic workflow.

The Phase 9 application exposes explicit overall statuses:

```text
SUCCESS
LIMITATION
FAILURE
```

The built-in Phase 9 CLI uses `JsonCorpusProvider`, a deterministic local provider intended for a runnable MVP, reproducible integration tests, and offline evidence-corpus execution. It is not a live Internet search provider. Live external search/fetch providers remain pluggable through the existing `ResearchTools`, `WebSearchTool`, and `WebFetchTool` boundaries and are intentionally not hard-coded into agent logic.

The Phase 6 CriticAgent still uses conservative deterministic evidence-relation heuristics for the MVP. Semantic LLM-based verification remains a later enhancement and does not change the approved CriticProfile boundary.

Iteration, agent-run, profile, and artifact audit data is currently in-memory. Durable restart-safe persistence remains scheduled for Phase 10.

Hybrid semantic domain resolution is the next scheduled post-MVP enhancement. See `docs/HYBRID_RESOLVER_PLAN.md`.

## Repository Structure

```text
agents/       agent implementations
supervisor/   orchestration core
models/       domain and transport models
tools/        external capability adapters and evidence utilities
prompts/      prompt assets
config/       tracked non-secret configuration
tests/        automated tests
scripts/      runnable local commands and maintenance scripts
examples/     deterministic sample inputs
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

Install dependencies:

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

## End-to-End MVP CLI

The default CLI requires an explicit CriticProfile approval action before autonomous execution:

```text
python -m scripts.run_research --task "Explain software architecture behavior" --corpus examples/sample_corpus.json
```

The CLI prints the DomainAssessment and CriticProfile proposal and then requests one of:

```text
approve
edit
reject
```

For a non-interactive run, explicit approval can be supplied as part of the command invocation:

```text
python -m scripts.run_research --task "Explain software architecture behavior" --corpus examples/sample_corpus.json --approve-profile
```

Profile edits can be supplied together with explicit approval:

```text
python -m scripts.run_research --task "Explain software architecture behavior" --corpus examples/sample_corpus.json --approve-profile --profile-edits '{"critic_role":"Independent software reviewer"}'
```

The sample corpus is synthetic and exists only to validate the workflow. It must not be treated as factual research evidence.

CLI exit codes:

```text
0  SUCCESS
1  FAILURE or invalid input
2  LIMITATION
4  profile rejected or explicit approval not supplied
```

## Local Corpus Format

`JsonCorpusProvider` accepts either a JSON list of documents or an object with a `documents` list. Each document follows the provider-neutral `FetchedDocument` contract. Example:

```json
{
  "documents": [
    {
      "url": "https://example.org/source",
      "title": "Source title",
      "publisher": "Publisher",
      "publication_date": "2026-08-01",
      "source_type": "OFFICIAL",
      "primary_source": true,
      "independence_group": "source-a",
      "content": "Evidence text."
    }
  ]
}
```

For high-risk profiles, provide enough independent authoritative sources to satisfy the approved cross-check requirements.

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

The complete MVP workflow generates:

```text
<TASK_ID>_FINAL_REPORT.md
<TASK_ID>_REVIEW_PROTOCOL.md
```

Generated runtime files are not committed by default.
