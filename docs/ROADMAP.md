# ROADMAP
План поетапної реалізації K_Supervisor від базового каркаса до розширюваної мультиагентної платформи.

Version: 1.0
Status: ACTIVE

## 1. Purpose

This roadmap defines the implementation sequence for K_Supervisor.

The roadmap follows the approved architecture and keeps the first product workflow focused on one complete research and independent critique pipeline while preserving a generic multi-agent foundation.

## 2. Delivery Principles

- Build orchestration before domain complexity.
- Keep Supervisor independent from domain-specific research and critique logic.
- Use explicit validated contracts between components.
- Require user approval of CriticProfile before autonomous execution.
- Keep CriticAgent generic and dynamically configured per task.
- Preserve task_id and run_id across workflow stages.
- Keep agents independent from storage implementation.
- Preserve auditability and explicit failure states.
- Complete one end-to-end MVP before advanced platform expansion.
- Keep documentation compliant with PROJECT_FILE_STANDARD.md.

## 3. Phase 0 - Repository Bootstrap

Goal: establish a clean project foundation.

Scope:

- create repository structure;
- establish docs/, agents/, supervisor/, tools/, models/, config/, prompts/, tests/, scripts/, output/, and logs/;
- add project documentation;
- prepare `.env.example`, dependency definition, `.gitignore`, and local run instructions.

Exit criteria:

- repository structure is stable;
- required project documentation exists;
- secrets are excluded from Git;
- the project can be cloned and prepared for development.

Status: COMPLETE

## 4. Phase 1 - Core Domain Models and Contracts

Goal: define stable machine-readable contracts before workflow implementation.

Scope:

- Task;
- AgentRunRequest and AgentResult;
- CriticProfile;
- Claim and Source;
- CriticReview;
- WorkflowRun and StateTransition;
- Artifact metadata;
- common identifiers, statuses, errors, warnings, and metrics.

Primary documents:

```text
AGENT_INTERFACE.md
DATA_MODELS.md
```

Exit criteria:

- components exchange validated contracts rather than ad hoc dictionaries;
- invalid contract input is rejected;
- IDs and approval boundaries are explicit.

Status: COMPLETE

## 5. Phase 2 - Supervisor Foundation

Goal: implement the orchestration core without domain research logic.

Scope:

- TaskManager;
- StateMachine;
- WorkflowEngine;
- AgentRegistry;
- run tracking;
- explicit state transitions;
- iteration counters;
- failure and termination handling.

Core task states:

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

Exit criteria:

- mock workflow traverses the state machine;
- invalid transitions are rejected;
- state changes are auditable;
- Supervisor contains no research or critique logic.

Status: COMPLETE

## 6. Phase 3 - Domain Resolver and CriticProfile Workflow

Goal: implement dynamic critic configuration with mandatory user approval.

Scope:

- DomainResolver;
- primary and secondary domain detection;
- task type and risk level;
- source classes and verification criteria;
- CriticProfile draft generation;
- explicit user approve/edit/reject boundary;
- approved profile immutability;
- material amendment detection;
- multi-domain profiles.

Required interaction rule:

```text
Supervisor proposes.
User approves or edits.
Critic executes.
```

Exit criteria:

- autonomous Research-Critic execution cannot start without PROFILE_APPROVED;
- approved CriticProfile is immutable for normal execution;
- material amendments return to user approval.

Status: COMPLETE

## 7. Phase 4 - ResearchAgent MVP

Goal: produce evidence-backed draft research results.

Scope:

- generic ResearchAgent;
- task decomposition;
- search plan generation;
- source collection;
- Claim extraction;
- uncertainty and limitation tracking;
- draft report representation;
- structured revision input from CriticAgent.

Exit criteria:

- ResearchResult contains structured claims and sources;
- important claims reference source IDs;
- revision feedback can produce a new iteration.

Status: COMPLETE

## 8. Phase 5 - Tools and Evidence Layer

Goal: isolate external information access and evidence handling.

Scope:

- provider-neutral web_search and web_fetch boundaries;
- source metadata extraction;
- source normalization and deduplication;
- citation management;
- source reliability classification;
- Claim-Source linking;
- publication/access time handling.

Default reliability classes:

```text
A - primary or official
B - authoritative independent
C - secondary
D - weak or unverified
```

Exit criteria:

- agents use common tool boundaries;
- duplicate sources are normalized;
- evidence is auditable at claim level;
- reliability policy can be influenced by CriticProfile.

Status: COMPLETE

## 9. Phase 6 - CriticAgent MVP

Goal: provide independent profile-driven verification and critique.

Scope:

- generic CriticAgent;
- approved CriticProfile loading;
- independent verification research;
- source authority/freshness review;
- unsupported claim detection;
- contradiction detection;
- missing topic detection;
- conclusion/evidence consistency checks;
- machine-readable PASS or REVISE;
- structured improvement requests.

Initial critic result shape:

```json
{
  "decision": "PASS | REVISE",
  "reliability_score": 0.0,
  "critical_issues": [],
  "unsupported_claims": [],
  "weak_sources": [],
  "contradictions": [],
  "missing_topics": [],
  "recommended_changes": []
}
```

Exit criteria:

- behavior changes according to CriticProfile;
- one implementation supports literary, medical, technical, and multi-domain profiles;
- independent verification is performed;
- PASS/REVISE is machine-readable.

Status: COMPLETE

## 10. Phase 7 - Autonomous Research-Critic Loop

Goal: complete the main autonomous multi-agent workflow.

Scope:

- connect ResearchAgent and CriticAgent through Supervisor;
- pass CriticReview feedback to the next ResearchAgent iteration;
- version research results by iteration;
- enforce max_iterations;
- enforce reliability threshold;
- stop on accepted PASS;
- terminate explicitly on unrecoverable failure;
- support COMPLETED_WITH_LIMITATIONS.

Workflow:

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

Exit criteria:

- normal revision cycles require no user interaction;
- all iterations are auditable;
- loop termination is deterministic.

Status: COMPLETE

## 11. Phase 8 - ReportGenerator and Final Artifacts

Goal: produce final user-facing outputs.

Scope:

- ReportGenerator;
- `<TASK_ID>_FINAL_REPORT.md`;
- `<TASK_ID>_REVIEW_PROTOCOL.md`;
- UTF-8 work-result artifacts;
- source and uncertainty reporting;
- iteration/review/limitation summary;
- no hidden chain-of-thought/private reasoning in artifacts.

Exit criteria:

- both artifacts use the same task_id;
- artifact metadata records final state and checksum;
- reports are usable without internal runtime state.

Status: COMPLETE

## 12. Phase 9 - End-to-End MVP

Goal: deliver the first complete usable system.

Initial interface:

```text
CLI or equivalent local command
```

Scope:

- accept a user task;
- generate CriticProfile proposal;
- receive explicit user approval or edits;
- execute autonomous Research-Critic iterations;
- finalize accepted or limited results;
- generate both final artifacts;
- expose SUCCESS, LIMITATION, or FAILURE.

Required scenarios:

- literary analysis;
- medical knowledge research;
- geodesy/construction technical research;
- multi-domain task;
- max_iterations;
- tool failure;
- material CriticProfile amendment.

Exit criteria:

- primary workflows pass E2E tests;
- output is repeatable with deterministic local provider;
- failure paths are explicit;
- user interaction occurs only at defined approval boundaries.

MVP boundary: Phase 9.

Status: COMPLETE

## 12.1 Post-MVP Enhancement - Hybrid Domain Resolver

Goal: improve domain classification semantically while preserving deterministic safety and the existing approval boundary.

Scope:

- preserve RuleBasedResolver;
- add provider-neutral LLMSemanticResolver;
- implement HybridResolver merge/conflict policy;
- preserve deterministic risk floors;
- validate semantic output before merge;
- confidence and uncertainty handling;
- fallback and fail-closed modes;
- preserve CriticProfile user approval semantics.

Primary document:

```text
HYBRID_RESOLVER_PLAN.md
```

Exit criteria:

- semantic classification is schema validated;
- deterministic fallback remains available;
- deterministic matched risk cannot be silently lowered;
- material conflicts are auditable;
- DomainAssessment schema and approval boundary remain stable.

Status: COMPLETE

## 13. Phase 10 - Persistence and Audit

Goal: preserve execution history and enable restart-safe audit/recovery.

Scope:

- implement storage-neutral PersistenceStore protocol;
- implement SQLitePersistenceStore;
- persist Task;
- persist WorkflowRun and StateTransition;
- persist AgentResult;
- persist DomainAssessment;
- persist CriticProfile versions and UserApproval;
- persist ResearchResult, Claim, and Source;
- persist CriticReview;
- persist Artifact metadata;
- provide TaskAuditSnapshot;
- provide conservative restart recovery;
- add persisted-task audit CLI.

Initial SQLite tables:

```text
schema_meta
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

Safe automatic recovery checkpoints:

```text
PROFILE_REVIEW_REQUIRED
PROFILE_APPROVED
REVISE_REQUIRED
```

Automatic mid-step replay is intentionally not performed from `RESEARCHING`, `DRAFT_READY`, or `REVIEWING` because an unfinished external side effect may be ambiguous.

Primary document:

```text
PERSISTENCE.md
```

Exit criteria:

- completed tasks are auditable after process restart;
- approved CriticProfile reconstructs exactly;
- safe workflow checkpoints can be restored and continued;
- persistence writes are idempotent by stable ID;
- agent business logic has no direct SQLite dependency;
- full CI suite passes.

Implementation validation:

```text
Commit: 24377e5370b60efd92e86bae8229d200b72bedb3
GitHub Actions run: 31658626453
119 tests passed
```

Status: COMPLETE

## 14. Phase 11 - Configuration, Cost, and Quality Controls

Goal: make runtime behavior controlled, provider-configurable, and measurable.

Scope:

- central configuration loader and validation;
- use `config/settings.yaml` as tracked defaults;
- environment and secret loading;
- freeze effective task configuration snapshot;
- configure max_iterations and resource limits;
- configure reliability thresholds and source/search limits;
- configure timeouts and retries;
- configure model selection by role;
- add provider factories/adapters for configured model roles;
- wire a concrete semantic LLM provider without embedding vendor code in Supervisor;
- track token/API usage where providers expose it;
- record estimated cost;
- record quality metrics;
- implement logging policy and secret redaction.

Implementation steps:

```text
11.1 Configuration Core                       COMPLETE
11.2 Task Configuration Snapshot              COMPLETE
11.3 Provider / Model Factory                 COMPLETE
11.4 Runtime Controls                         COMPLETE
11.5 Usage, Cost, and Quality Metrics         NEXT
11.6 Logging / Secret Redaction / Finalization PLANNED
```

Implemented through 11.4:

- frozen typed settings and explicit configuration invariants;
- tracked defaults plus environment/secret loading;
- immutable secret-free task configuration snapshots created after CriticProfile approval;
- snapshot persistence through Task audit metadata and restart-safe reconstruction;
- profile-amendment snapshots preserve the original active task settings even after restart and global configuration changes;
- role-based domain resolver factory;
- concrete OpenAI semantic domain provider adapter behind the provider-neutral resolver boundary;
- semantic provider remains disabled in tracked defaults until provider/model/API key are explicitly configured;
- frozen research and critic limits are passed into agent execution;
- search/fetch enablement, call budgets, timeout, retry/backoff, runtime ceiling checks, and final artifact size limits are enforced.

Exit criteria:

- operational limits are configuration-driven;
- model/provider selection changes without editing agent business logic;
- effective task configuration is auditable and frozen;
- usage/cost/quality metrics are available per task/run where supported;
- concrete semantic resolver provider can be selected through configuration;
- full CI suite passes.

Interim validation through Step 11.4:

```text
Implementation commit: fc64e407a2f69179e69fe4df9d3b1562a725886e
Snapshot restart hardening: 5482ac0c5fe2aa294a94585aef8d147d08c19e62
GitHub Actions run: 31661584051
134 tests passed
```

Status: IN PROGRESS

## 15. Phase 12 - Test and CI Hardening

Goal: establish a hardened engineering workflow in GitHub.

Scope:

- broaden unit/contract/integration/E2E coverage;
- linting;
- type checks;
- coverage/reporting policy;
- GitHub Actions maintenance;
- branch/PR checks;
- dependency and CI-action maintenance.

Exit criteria:

- required checks run automatically;
- contract regressions are detected;
- critical workflow paths have automated coverage;
- CI configuration uses supported action/runtime versions.

Status: PLANNED

## 16. Phase 13 - Modular Agent Platform

Goal: evolve K_Supervisor beyond the first research workflow.

Scope:

- formalize capability discovery in AgentRegistry;
- select agents by capability;
- add generic agents through Agent Interface;
- support additional workflow definitions;
- support multiple critic instances where required;
- keep Supervisor independent from domain-specific agent code.

Possible future agents:

```text
FactCheckAgent
DataAnalysisAgent
TechnicalAgent
FinancialAgent
LegalAgent
PlanningAgent
```

Exit criteria:

- new agents register without redesigning Supervisor core;
- unrelated agents do not require modification;
- workflows reference capabilities rather than hard-coded classes.

Status: PLANNED

## 17. Deferred Capabilities

The following remain outside the current core platform scope until separate architectural decisions are approved:

```text
Web UI
distributed execution
complex parallel orchestration
vector database
complex long-term memory
automatic agent generation
large-scale workflow scheduling
```

## 18. Project Documents

Current canonical documents include:

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
```

`PROJECT_HISTORY.md` remains a planned historical consolidation document when required.

## 19. Current Implementation Order

Completed sequence:

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

Current implementation phase:

```text
Phase 11 - Configuration, Cost, and Quality Controls    IN PROGRESS
11.1-11.4                                               COMPLETE
11.5 Usage, Cost, and Quality Metrics                   NEXT
```

Later phases:

```text
Phase 12 - Test and CI Hardening
Phase 13 - Modular Agent Platform
```

## 20. Roadmap Decision Summary

- The first product workflow is a complete research and independent critique pipeline.
- CriticProfile approval is a mandatory user-controlled gate.
- CriticAgent remains generic and profile-driven.
- Supervisor owns workflow state, iteration limits, recovery, and finalization.
- ResearchAgent and CriticAgent operate autonomously after profile approval.
- MVP completion is defined at Phase 9 and is complete.
- Hybrid domain resolution is complete with deterministic fallback and unchanged approval semantics.
- Phase 10 durable SQLite persistence and restart-safe audit/recovery are complete.
- Phase 11 is in progress: configuration core, frozen task snapshots, provider/model wiring, concrete semantic provider selection, and runtime controls are complete through Step 11.4.
- Phase 11.5 will add usage, cost, and quality metrics; Phase 11.6 will finalize logging and secret redaction.
