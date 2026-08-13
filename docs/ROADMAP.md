# ROADMAP
План поетапної реалізації K_Supervisor від базового каркаса до GPT Store-first мультиагентного продукту.

Version: 1.5
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
- Private chain-of-thought is never required for auditability.
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

The post-MVP Hybrid Domain Resolver enhancement is COMPLETE.

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

The Python/provider runtime is retained as optional standalone infrastructure and as the engineering reference implementation.

Primary documents:

```text
GPT_STORE_DEPLOYMENT.md
GPT_STORE_PACKAGE.md
```

## 5. Phase 11 - Configuration, Cost, and Quality Controls

Status: COMPLETE

```text
11.1 Configuration Core                          COMPLETE
11.2 Task Configuration Snapshot                 COMPLETE
11.3 Provider / Model Factory                    COMPLETE
11.4 Runtime Controls                            COMPLETE
11.4A GPT Store-first Distribution Policy        COMPLETE
11.5 Usage, Cost, and Quality Metrics            COMPLETE
11.6 Logging / Sensitive-data Redaction          COMPLETE
11.7 GPT Store Packaging / Publication Readiness COMPLETE
```

Delivered:

- validated frozen configuration;
- immutable task configuration snapshots and restart-safe reconstruction;
- role-based provider isolation for optional standalone execution;
- frozen research and critic limits;
- tool call budgets, timeouts, retries, runtime ceilings, and output-size limits;
- GPT Store distribution invariants and user-plan model policy;
- `TaskQualityMetrics` and `ProviderUsageRecord`;
- restart-safe metric reconstruction from TaskAuditSnapshot;
- structured operational logging and sensitive-data redaction;
- GPT Store manifest, instructions, checkpoint contract, release validator, and operator documentation.

Release state:

```text
ready_for_manual_publication_test
```

This state means repository packaging and CI are complete. It does not mean the Custom GPT has already been published. GPT Builder Preview, real Free-account use, paid-account model switching, Builder Profile/category/policy checks, and the final Publish action remain manual release operations in ChatGPT.

## 6. Phase 12 - Test and CI Hardening

Status: COMPLETE

### 6.1 Goal

Turn the MVP and Phase 11 controls into a repeatable quality baseline that detects regressions without requiring live paid providers.

### 6.2 Delivered

- broader orchestration, profile, loop, report, failure, Store-package, and configuration regression coverage;
- deterministic offline reference benchmark in `examples/reference_benchmark.json`;
- end-to-end benchmark runner in `tests/test_reference_benchmark.py`;
- four reference domains: literary analysis, software engineering, medicine, and geodesy;
- explicit benchmark checks for domain resolution, profile approval, autonomous completion, critic PASS/reliability floor, evidence, artifacts, and no-private-reasoning review protocol;
- full pytest matrix on Python 3.13 and Python 3.14;
- dependency integrity gate with `python -m pip check`;
- Ruff correctness gate using E9, F63, F7, and F82 rule families;
- Mypy typed-boundary gate for `models`, `config`, and `gpt_store`;
- tracked repository policy validation;
- GPT Store package regression validation;
- blocking coverage floor of 70 percent;
- weekly Dependabot maintenance for pip and GitHub Actions;
- synchronized README, TEST_PLAN, and CI_QUALITY documentation.

### 6.3 Validated Baseline

The Phase 12 implementation baseline was validated with:

```text
Python 3.13 full suite: 169 passed
Python 3.14 full suite: PASS
Quality gates: PASS
Total coverage: 85 percent
Blocking coverage floor: 70 percent
Reference benchmark cases: 4
```

The reference benchmark is synthetic, offline, deterministic, and provider-independent. Live ChatGPT account/UI validation is intentionally not represented as an automated CI PASS condition.

### 6.4 Exit Criteria

All Phase 12 exit criteria are satisfied:

- critical edge cases have automated regression coverage;
- reference end-to-end behavior is reproducibly benchmarked;
- generated artifacts are validated;
- CI and local quality gates pass;
- dependency integrity is checked;
- architecture remains modular and contract-driven;
- Store-package regressions are blocked automatically where repository CI can prove them;
- manual ChatGPT publication/account checks remain explicitly separated from repository automation.

## 7. Phase 13 - Modular Agent Platform

Status: PLANNED

Goal: extend beyond the first research workflow through capability discovery and capability-based agent selection while keeping Supervisor independent from domain-specific implementations.

Expected direction:

- capability-oriented agent metadata and discovery;
- executable agent registration rather than definition-only registration;
- capability-based selection and routing;
- explicit compatibility contracts between Supervisor and optional agents;
- preservation of current approval, evidence, audit, configuration, and quality boundaries.

Possible future agents:

```text
FactCheckAgent
DataAnalysisAgent
TechnicalAgent
FinancialAgent
LegalAgent
PlanningAgent
```

Phase 13 must not weaken the completed Phase 0-12 invariants merely to add new agent types.

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
CI_QUALITY.md
HYBRID_RESOLVER_PLAN.md
PERSISTENCE.md
GPT_STORE_DEPLOYMENT.md
GPT_STORE_PACKAGE.md
LOGGING.md
```

## 10. Current Implementation Order

```text
Phase 0-10                               COMPLETE
Post-MVP Hybrid Domain Resolver         COMPLETE
GPT Store-first Product Decision        COMPLETE
Phase 11                                COMPLETE
Phase 12                                COMPLETE
Phase 13                                PLANNED
```
