# ROADMAP
План поетапної реалізації K_Supervisor від базового каркаса до GPT Store-first мультиагентного продукту.

Version: 1.1
Status: ACTIVE

## 1. Purpose

This roadmap defines the implementation sequence for K_Supervisor.

The completed core is a research and independent critique workflow. The primary public product target is now a GPT Store Edition that preserves the same workflow semantics without requiring a developer API key or mandatory external backend.

## 2. Delivery Principles

- Build orchestration before domain complexity.
- Keep Supervisor independent from domain research/critique logic.
- Use explicit validated contracts.
- Require user approval of CriticProfile before autonomous execution.
- Keep CriticAgent generic and profile-driven.
- Preserve task_id/run_id semantics and explicit state transitions.
- Keep agents independent from storage implementation.
- Preserve auditability and explicit failure states.
- Keep the free GPT Store core independent from developer-funded API calls.
- Do not pin a ChatGPT model identifier as a core dependency.
- Keep documentation compliant with PROJECT_FILE_STANDARD.md.

## 3. Phase 0 - Repository Bootstrap

Goal: establish the project foundation.

Delivered: repository structure, docs, environment template, dependencies, ignored runtime data, and local setup.

Status: COMPLETE

## 4. Phase 1 - Core Domain Models and Contracts

Goal: define stable machine-readable contracts.

Delivered: Task, AgentRunRequest/AgentResult, CriticProfile, Claim, Source, CriticReview, WorkflowRun, StateTransition, Artifact, identifiers, statuses, errors, warnings, and metrics.

Status: COMPLETE

## 5. Phase 2 - Supervisor Foundation

Goal: implement orchestration without domain logic.

Delivered: TaskManager, StateMachine, WorkflowEngine, AgentRegistry, run tracking, state transitions, iteration counters, failure/termination handling.

Core states:

```text
NEW
PROFILE_GENERATING
PROFILE_REVIEW_REQUIRED
PROFILE_APPROVED
RESEARCHING
DRAFT_READY
REVIEWING
REVISE_REQUIRED
APPROVED
FINALIZING
FINALIZED
FAILED
MAX_ITERATIONS_REACHED
COMPLETED_WITH_LIMITATIONS
```

Status: COMPLETE

## 6. Phase 3 - Domain Resolver and CriticProfile Workflow

Goal: dynamic critic configuration with mandatory user approval.

Delivered: domain/task/risk assessment, multi-domain support, CriticProfile generation, approve/edit/reject gate, immutable approved profiles, material amendment flow.

Required rule:

```text
Supervisor proposes.
User approves or edits.
Critic executes.
```

Status: COMPLETE

## 7. Phase 4 - ResearchAgent MVP

Goal: produce evidence-backed draft research results.

Delivered: research planning, source collection, Claim extraction, uncertainty/limitation tracking, draft generation, structured revision feedback handling.

Status: COMPLETE

## 8. Phase 5 - Tools and Evidence Layer

Goal: isolate external information access and evidence handling.

Delivered: provider-neutral web_search/web_fetch, metadata extraction, normalization/deduplication, reliability classes, Claim-Source linking, citations, freshness metadata.

Default reliability:

```text
A - primary or official
B - authoritative independent
C - secondary
D - weak or unverified
```

Status: COMPLETE

## 9. Phase 6 - CriticAgent MVP

Goal: independent profile-driven verification and critique.

Delivered: generic CriticAgent, independent verification search, source authority/freshness checks, unsupported claims, contradictions, missing topics, evidence consistency, machine-readable PASS/REVISE.

Status: COMPLETE

## 10. Phase 7 - Autonomous Research-Critic Loop

Goal: connect ResearchAgent and CriticAgent through Supervisor.

Delivered: autonomous revision cycles, structured feedback propagation, iteration versioning, max_iterations, threshold enforcement, deterministic stop, failure and COMPLETED_WITH_LIMITATIONS paths.

Logical workflow:

```text
PROFILE_APPROVED
      |
      v
 RESEARCHING
      |
      v
 DRAFT_READY
      |
      v
  REVIEWING
      |
   +--+--+
   |     |
REVISE  PASS
   |     |
   v     v
RESEARCHING APPROVED
```

Status: COMPLETE

## 11. Phase 8 - ReportGenerator and Final Artifacts

Goal: produce final user-facing outputs.

Delivered:

```text
<TASK_ID>_FINAL_REPORT.md
<TASK_ID>_REVIEW_PROTOCOL.md
```

Artifacts include evidence/uncertainty/review status and exclude hidden chain-of-thought.

Status: COMPLETE

## 12. Phase 9 - End-to-End MVP

Goal: deliver the first complete usable system.

Delivered: local CLI, explicit CriticProfile approval/edit/reject, autonomous loop, final artifacts, SUCCESS/LIMITATION/FAILURE, deterministic E2E scenarios.

MVP boundary: Phase 9.

Status: COMPLETE

## 12.1 Post-MVP Enhancement - Hybrid Domain Resolver

Goal: improve classification while preserving deterministic safety.

Delivered: RuleBasedResolver, LLMSemanticResolver, HybridResolver, semantic schema validation, confidence/fallback/fail-closed behavior, deterministic risk floors, conflict audit, unchanged user approval boundary.

Primary document:

```text
HYBRID_RESOLVER_PLAN.md
```

Status: COMPLETE

## 13. Phase 10 - Persistence and Audit

Goal: preserve execution history and restart-safe recovery.

Delivered: storage-neutral PersistenceStore, SQLitePersistenceStore, write-through persistence for task/workflow/profile/evidence/review/artifact records, TaskAuditSnapshot, conservative recovery, audit CLI.

Safe automatic checkpoints:

```text
PROFILE_REVIEW_REQUIRED
PROFILE_APPROVED
REVISE_REQUIRED
```

Ambiguous mid-agent states are not auto-replayed.

Primary document:

```text
PERSISTENCE.md
```

Implementation validation:

```text
Commit: 24377e5370b60efd92e86bae8229d200b72bedb3
GitHub Actions run: 31658626453
119 tests passed
```

Status: COMPLETE

## 14. Product Distribution Decision - GPT Store First

Goal: define the primary public delivery model before completing Phase 11.

Decision:

```text
Primary channel: chatgpt_store
Free-user compatible: yes
Developer API key required: no
Model policy: user_plan
Pinned/recommended model dependency: none
User model switching: allowed when the plan exposes alternatives
Mandatory external backend: no
```

The existing Python/SQLite/provider implementation is retained as an optional standalone/API edition and engineering reference runtime.

Primary document:

```text
GPT_STORE_DEPLOYMENT.md
```

Required consequences:

- Store Edition uses ChatGPT-managed models/capabilities;
- model names may change without changing core workflow contracts;
- Free users use the model/capabilities available to their account;
- paid users may switch to additional available models;
- no developer-funded OpenAI API call is required for the free core path;
- SQLite/provider secrets remain optional standalone infrastructure;
- cross-chat Store recovery must use an explicit checkpoint artifact unless a future backend is separately approved.

Status: COMPLETE

## 15. Phase 11 - Configuration, Cost, and Quality Controls

Goal: make runtime behavior controlled, deployment-aware, measurable, and compatible with GPT Store-first distribution.

Scope:

- central configuration loader/validation;
- tracked settings plus environment handling;
- immutable effective task configuration snapshot;
- workflow/research/critic/resource limits;
- timeouts and retries;
- provider/model isolation for optional standalone execution;
- GPT Store distribution invariants;
- usage/cost/quality metrics according to runtime capability;
- logging/redaction;
- GPT Store packaging/publication readiness.

Implementation steps:

```text
11.1 Configuration Core                         COMPLETE
11.2 Task Configuration Snapshot                COMPLETE
11.3 Provider / Model Factory                   COMPLETE
     Standalone OpenAI adapter remains OPTIONAL
     GPT Store model policy = user_plan          COMPLETE
11.4 Runtime Controls                           COMPLETE
11.4A GPT Store-first Distribution Policy       COMPLETE
11.5 Usage, Cost, and Quality Metrics           NEXT
11.6 Logging / Secret Redaction                 PLANNED
11.7 GPT Store Packaging / Publication Readiness PLANNED
```

Implemented through 11.4A:

- frozen typed settings and explicit invariants;
- tracked defaults plus optional environment secrets;
- immutable secret-free task configuration snapshots;
- restart-safe snapshot reconstruction;
- role-based provider factory for optional standalone runtime;
- concrete OpenAI semantic adapter retained as optional standalone capability;
- frozen research/critic limits and runtime controls;
- GPT Store is now the tracked primary distribution channel;
- Store defaults prohibit mandatory developer API key/backend and prohibit pinned model identifiers;
- Store defaults use user-plan model policy and permit user model switching.

### Step 11.5 - Usage, Cost, and Quality Metrics

GPT Store Edition:

- record workflow quality metrics that can be derived from K_Supervisor state/artifacts;
- record iteration count, PASS/REVISE history, reliability scores, unresolved issues, source/claim coverage;
- do not assume access to provider token counts or developer API cost telemetry.

Standalone/API Edition:

- additionally capture API calls, input/output tokens, and estimated cost where providers expose them and pricing configuration is available.

The Store free path must not create developer-funded API usage merely to collect metrics.

### Step 11.6 - Logging / Secret Redaction

- finalize structured operational logging for standalone runtime;
- redact all configured secret values and secret-like fields;
- keep private chain-of-thought out of logs/artifacts;
- define Store Edition user-visible audit/checkpoint equivalents without requiring a private backend.

### Step 11.7 - GPT Store Packaging / Publication Readiness

- create Custom GPT instruction package;
- define conversation starters and Store description;
- map research tools to ChatGPT built-in capabilities;
- implement/define conversation-local state and checkpoint artifact behavior;
- validate fresh-chat recovery;
- validate Free-plan execution;
- validate paid-plan model switching;
- ensure no Action/external backend is required for core functionality;
- verify current OpenAI GPT Store publication requirements immediately before release.

Exit criteria for Phase 11:

- operational limits are configuration-driven where runtime exposes them;
- GPT Store defaults validate without any developer secret;
- model/provider selection does not require editing agent business logic;
- effective standalone task configuration remains frozen/auditable;
- quality metrics are available in both editions at the level their runtime exposes;
- token/cost metrics are optional standalone telemetry only;
- secrets are redacted;
- Store packaging is ready for publication testing;
- full CI suite passes.

Interim validation before GPT Store policy update:

```text
Implementation commit: fc64e407a2f69179e69fe4df9d3b1562a725886e
Snapshot restart hardening: 5482ac0c5fe2aa294a94585aef8d147d08c19e62
GitHub Actions run: 31661584051
134 tests passed
```

Status: IN PROGRESS

## 16. Phase 12 - Test and CI Hardening

Goal: establish a hardened engineering workflow.

Scope:

- broaden unit/contract/integration/E2E coverage;
- linting and type checks;
- coverage/reporting policy;
- GitHub Actions maintenance;
- branch/PR checks;
- dependency/action maintenance;
- Store packaging regression tests where practical.

Status: PLANNED

## 17. Phase 13 - Modular Agent Platform

Goal: evolve beyond the first research workflow.

Scope:

- capability discovery in AgentRegistry;
- capability-based agent selection;
- additional workflow definitions;
- multiple critic instances where needed;
- Supervisor remains independent from domain-specific code.

Possible future agents:

```text
FactCheckAgent
DataAnalysisAgent
TechnicalAgent
FinancialAgent
LegalAgent
PlanningAgent
```

Status: PLANNED

## 18. Deferred Capabilities

Deferred until separate approval:

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

## 19. Canonical Project Documents

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

## 20. Current Implementation Order

Completed:

```text
Phase 0-10                                      COMPLETE
Post-MVP Hybrid Domain Resolver                COMPLETE
GPT Store-first Distribution Decision          COMPLETE
Phase 11.1-11.4A                               COMPLETE
```

Current:

```text
Phase 11.5 - Usage, Cost, and Quality Metrics  NEXT
```

Later:

```text
Phase 11.6 - Logging / Secret Redaction
Phase 11.7 - GPT Store Packaging / Publication Readiness
Phase 12   - Test and CI Hardening
Phase 13   - Modular Agent Platform
```

## 21. Roadmap Decision Summary

- The first complete research/critic MVP is finished.
- CriticProfile approval remains mandatory.
- Hybrid resolver and SQLite persistence are complete for the Python reference runtime.
- GPT Store Edition is the primary public product target.
- The Store core requires no developer API key and no mandatory external backend.
- The Store model is selected by ChatGPT/user plan rather than pinned in K_Supervisor.
- Paid users may use additional model choices when available.
- Existing provider/API code is retained as optional standalone infrastructure.
- Phase 11.5 must distinguish workflow quality metrics from provider token/cost telemetry.
- Phase 11.7 will package the approved workflow for GPT Store publication testing.
