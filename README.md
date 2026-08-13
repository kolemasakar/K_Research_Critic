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

```text
Phase 0  - Repository Bootstrap                         COMPLETE
Phase 1  - Core Domain Models and Contracts             COMPLETE
Phase 2  - Supervisor Foundation                        COMPLETE
Phase 3  - Domain Resolver and CriticProfile Workflow   COMPLETE
Phase 4  - ResearchAgent MVP                            COMPLETE
Phase 5  - Tools and Evidence Layer                     COMPLETE
Phase 6  - CriticAgent MVP                              COMPLETE
Phase 7  - Autonomous Research-Critic Loop              COMPLETE
Phase 8  - ReportGenerator and Final Artifacts          COMPLETE
Phase 9  - End-to-End MVP                               COMPLETE
Post-MVP - Hybrid Domain Resolver                       COMPLETE
Phase 10 - Persistence and Audit                        COMPLETE
```

The MVP boundary was reached at Phase 9. The current implementation also includes the scheduled Hybrid Domain Resolver enhancement and restart-safe SQLite persistence/audit support.

Next implementation phase:

```text
Phase 11 - Configuration, Cost, and Quality Controls
```

## Implemented Workflow

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

`KSupervisorApplication` composes task intake, domain assessment, CriticProfile review, explicit user approval, autonomous Research-Critic iterations, deterministic termination, final artifact generation, and optional persistence into one programmatic workflow.

Overall application statuses are:

```text
SUCCESS
LIMITATION
FAILURE
```

## Domain Resolution

Hybrid domain resolution is implemented through:

```text
DomainResolverProtocol
  |
  +-- RuleBasedResolver
  +-- LLMSemanticResolver
  +-- HybridResolver
```

The semantic resolver is provider-neutral and validates structured `SemanticDomainResult` output before merge. HybridResolver preserves deterministic fallback, prevents matched deterministic risk from being silently lowered, merges compatible multi-domain results, records material disagreements, and exposes `HybridResolutionAudit` without changing the stable `DomainAssessment` schema.

`ProfileWorkflow` uses `HybridResolver` by default. When no semantic provider is configured, the deterministic Phase 3 result is returned unchanged. A concrete LLM provider is intentionally not hard-coded into Supervisor; provider/model factory wiring is scheduled for Phase 11.

## Persistence and Audit

Phase 10 adds a storage-neutral `PersistenceStore` boundary and a SQLite implementation:

```text
persistence/
  base.py
  sqlite_store.py
```

Default local database:

```text
runtime/k_supervisor.db
```

The SQLite store persists validated JSON snapshots for:

```text
tasks
workflow_runs
state_transitions
agent_runs
domain_assessments
critic_profiles
user_approvals
research_results
claims
sources
reviews
artifacts
```

Persistence is write-through at Supervisor orchestration boundaries. Agent business logic does not import or depend on SQLite APIs.

`TaskAuditSnapshot` reconstructs the persisted history of one task after process restart. Approved CriticProfiles retain their exact identifiers, version, approval metadata, and immutable content.

Restart recovery is intentionally conservative. Automatic continuation is supported from explicit safe checkpoints:

```text
PROFILE_REVIEW_REQUIRED
PROFILE_APPROVED
REVISE_REQUIRED
```

Terminal tasks remain fully auditable after restart. Automatic mid-step replay is not performed from `RESEARCHING`, `DRAFT_READY`, or `REVIEWING`, because the last external agent/tool side effect may be ambiguous. This avoids duplicate or uncertain execution.

## Local Development Setup

Clone the repository and enter the project directory:

```text
git clone https://github.com/kolemasakar/K_Supervisor.git
cd K_Supervisor
```

Create and activate a virtual environment, then install dependencies:

```text
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Create local environment configuration:

```text
copy .env.example .env
```

Run tests:

```text
python -m pytest
```

## End-to-End CLI

The bundled CLI uses `JsonCorpusProvider`, a deterministic local provider intended for reproducible integration tests and offline evidence-corpus execution. It is not a live Internet search provider. Live external search/fetch providers remain pluggable through provider-neutral tool boundaries.

Interactive profile approval:

```text
python -m scripts.run_research --task "Explain software architecture behavior" --corpus examples/sample_corpus.json
```

Non-interactive explicit approval:

```text
python -m scripts.run_research --task "Explain software architecture behavior" --corpus examples/sample_corpus.json --approve-profile
```

Use a custom SQLite audit database:

```text
python -m scripts.run_research --task "Explain software architecture behavior" --corpus examples/sample_corpus.json --approve-profile --database runtime/custom.db
```

Profile edits can be supplied with explicit approval:

```text
python -m scripts.run_research --task "Explain software architecture behavior" --corpus examples/sample_corpus.json --approve-profile --profile-edits '{"critic_role":"Independent software reviewer"}'
```

CLI exit codes:

```text
0  SUCCESS
1  FAILURE or invalid input
2  LIMITATION
4  profile rejected or explicit approval not supplied
```

## Audit CLI

A persisted task can be inspected after process restart:

```text
python -m scripts.audit_task --task-id TASK_EXAMPLE --database runtime/k_supervisor.db
```

The audit command reports task/workflow status and persisted counts for transitions, profiles, approvals, agent runs, research results, claims, sources, reviews, and artifacts.

## Local Corpus Format

`JsonCorpusProvider` accepts either a JSON list of documents or an object with a `documents` list. Example:

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

The sample corpus is synthetic and must not be treated as factual research evidence.

## Repository Structure

```text
agents/       agent implementations
supervisor/   orchestration core
persistence/  storage-neutral persistence boundary and SQLite store
models/       domain and transport models
tools/        external capability adapters and evidence utilities
prompts/      prompt assets
config/       tracked non-secret configuration
tests/        automated tests
scripts/      runnable local commands and maintenance scripts
examples/     deterministic sample inputs
output/       generated user-facing artifacts
runtime/      local SQLite runtime data; ignored by Git
logs/         runtime logs
docs/         project specifications and standards
```

## Configuration

Tracked runtime defaults:

```text
config/settings.yaml
```

Current persistence defaults:

```text
backend: sqlite
path: runtime/k_supervisor.db
schema_version: "1"
```

Local secrets and environment-specific values belong in `.env`. Never commit `.env` or real secret values.

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
docs/PERSISTENCE.md
```

## Current Known Boundaries

- The bundled research CLI still uses the deterministic local corpus provider rather than live Internet search.
- A concrete semantic LLM provider is not wired by default; provider/model configuration is scheduled for Phase 11.
- CriticAgent still uses conservative deterministic evidence-relation heuristics rather than full LLM semantic fact checking.
- Recovery does not automatically replay ambiguous mid-agent states.
- Configuration snapshots, model/cost controls, and full role-based provider factories are Phase 11 scope.

## Output Artifacts

The complete workflow generates:

```text
<TASK_ID>_FINAL_REPORT.md
<TASK_ID>_REVIEW_PROTOCOL.md
```

Generated runtime files and SQLite databases are not committed by default.
