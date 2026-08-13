# ROADMAP
План поетапної реалізації K_Supervisor від базового каркаса до GPT Store-first мультиагентного продукту.

Version: 1.2
Status: ACTIVE

## 1. Purpose

This roadmap records the approved implementation order for K_Supervisor. The primary public target is the GPT Store Edition, while the Python runtime remains an engineering and optional standalone reference implementation.

## 2. Stable Delivery Principles

- Supervisor coordinates but does not replace domain research or critique.
- CriticProfile approval is mandatory before autonomous execution.
- Approved profiles remain immutable unless a material amendment is approved.
- Research-Critic revision cycles are autonomous after approval.
- Contracts, task states, evidence, limitations, and failures remain explicit.
- The public Store workflow must not depend on a fixed model identifier or a mandatory external service.
- Project documentation follows PROJECT_FILE_STANDARD.md.

## 3. Completed Core

```text
Phase 0  Repository Bootstrap                         COMPLETE
Phase 1  Core Domain Models and Contracts             COMPLETE
Phase 2  Supervisor Foundation                        COMPLETE
Phase 3  Domain Resolver and CriticProfile Workflow   COMPLETE
Phase 4  ResearchAgent MVP                            COMPLETE
Phase 5  Tools and Evidence Layer                     COMPLETE
Phase 6  CriticAgent MVP                              COMPLETE
Phase 7  Autonomous Research-Critic Loop              COMPLETE
Phase 8  ReportGenerator and Final Artifacts          COMPLETE
Phase 9  End-to-End MVP                               COMPLETE
Phase 10 Persistence and Audit                        COMPLETE
```

MVP boundary: Phase 9.

The post-MVP Hybrid Domain Resolver enhancement is also COMPLETE.

Phase 10 includes storage-neutral persistence, SQLite reference storage, TaskAuditSnapshot, conservative restart recovery, and audit CLI support.

## 4. GPT Store-first Product Decision

Status: COMPLETE

Primary public behavior:

```text
channel: chatgpt_store
free-user compatible: yes
model policy: user_plan
fixed model dependency: none
user model switching: allowed when available
mandatory external backend: no
```

The existing Python/provider runtime is retained as optional standalone infrastructure and as the engineering reference implementation.

Primary document: `GPT_STORE_DEPLOYMENT.md`.

## 5. Phase 11 - Configuration, Cost, and Quality Controls

Status: IN PROGRESS

```text
11.1 Configuration Core                          COMPLETE
11.2 Task Configuration Snapshot                 COMPLETE
11.3 Provider / Model Factory                    COMPLETE
11.4 Runtime Controls                            COMPLETE
11.4A GPT Store-first Distribution Policy        COMPLETE
11.5 Usage, Cost, and Quality Metrics            COMPLETE
11.6 Logging / Sensitive-data Redaction          NEXT
11.7 GPT Store Packaging / Publication Readiness PLANNED
```

### 5.1 Steps 11.1-11.4A

Delivered:

- validated frozen configuration;
- immutable task configuration snapshots;
- restart-safe snapshot reconstruction;
- role-based provider isolation for optional standalone execution;
- frozen research and critic limits;
- tool call budgets, timeouts, retries, runtime ceilings, and output-size limits;
- GPT Store distribution invariants and user-plan model policy.

### 5.2 Step 11.5 - Usage, Cost, and Quality Metrics

Status: COMPLETE

Delivered:

- `TaskQualityMetrics`;
- `ProviderUsageRecord`;
- task-level aggregation from ResearchResult, CriticReview, and AgentResult;
- iteration count and PASS/REVISE history;
- reliability history and final reliability score;
- claim/source coverage and claim verification ratios;
- unresolved claims, critical issues, contradictions, and missing topics;
- search/fetch, retry, warning, error, and agent-run counts;
- restart-safe metric reconstruction from TaskAuditSnapshot;
- quality fields in the persisted-task audit CLI;
- optional standalone provider telemetry for usage counts and cost estimation when source data is available.

The GPT Store path derives quality metrics from existing workflow state and does not make additional external calls merely to calculate those metrics. Standalone provider telemetry is optional and does not affect Store workflow semantics.

Validation:

```text
Implementation: 9018a75b7e932a270fb3e26e81a6d72d03841477
Compatibility fix: 79d1d8b93b723fa56de32d66b432867e40432613
GitHub Actions: 31664525682
144 tests passed
```

### 5.3 Step 11.6 - Logging / Sensitive-data Redaction

Status: NEXT

Scope:

- structured operational logging for the standalone runtime;
- consistent task/workflow/run identifiers;
- redaction of sensitive values and sensitive-looking fields;
- no private reasoning in logs or artifacts;
- Store Edition user-visible audit/checkpoint equivalents without a private backend.

### 5.4 Step 11.7 - GPT Store Packaging / Publication Readiness

Status: PLANNED

Scope:

- create the Custom GPT instruction package;
- define description and conversation starters;
- map research behavior to built-in ChatGPT capabilities;
- define conversation-local state and checkpoint behavior;
- validate fresh-chat recovery;
- validate Free-plan execution;
- validate paid-plan model switching;
- confirm the core Store experience has no mandatory external backend;
- re-check current Store publication requirements immediately before release.

Phase 11 completes when 11.6 and 11.7 are complete and the full CI suite is green.

## 6. Phase 12 - Test and CI Hardening

Status: PLANNED

Scope:

- broader contract, integration, and E2E coverage;
- linting and type checks;
- coverage policy;
- CI workflow maintenance;
- branch/PR checks;
- dependency maintenance;
- Store packaging regression checks where practical.

## 7. Phase 13 - Modular Agent Platform

Status: PLANNED

Goal: extend beyond the first research workflow through capability discovery and capability-based agent selection while keeping Supervisor independent from domain-specific implementations.

Possible future agents:

```text
FactCheckAgent
DataAnalysisAgent
TechnicalAgent
FinancialAgent
LegalAgent
PlanningAgent
```

## 8. Deferred Capabilities

```text
custom Web UI
distributed execution
complex parallel orchestration
vector database
complex long-term memory
automatic agent generation
large-scale workflow scheduling
mandatory external backend for GPT Store Edition
```

## 9. Canonical Project Documents

```text
PROJECT_FILE_STANDARD.md
ARCHITECTURE.md
ROADMAP.md
AGENT_INTERFACE.md
DATA_MODELS.md
RESEARCH_WORKFLOW.md
CONFIGURATION.md
TEST_PLAN.md
HYBRID_RESOLVER_PLAN.md
PERSISTENCE.md
GPT_STORE_DEPLOYMENT.md
```

## 10. Current Implementation Order

```text
Phase 0-10                               COMPLETE
Post-MVP Hybrid Domain Resolver         COMPLETE
GPT Store-first Product Decision        COMPLETE
Phase 11.1-11.5                         COMPLETE
Phase 11.6                              NEXT
Phase 11.7                              PLANNED
Phase 12                                PLANNED
Phase 13                                PLANNED
```
