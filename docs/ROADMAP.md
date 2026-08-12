# ROADMAP
План поетапної реалізації K_Supervisor від базового каркаса до розширюваної мультиагентної платформи.

Version: 1.0
Status: ACTIVE

## 1. Purpose

This roadmap defines the implementation sequence for K_Supervisor.

The roadmap follows the approved ARCHITECTURE.md and keeps the initial MVP focused on one complete autonomous research and critique workflow while preserving a generic multi-agent foundation.

## 2. Delivery Principles

- Build the orchestration core before adding domain complexity.
- Keep Supervisor independent from domain-specific research and critique logic.
- Use explicit contracts between components.
- Require user approval of CriticProfile before autonomous execution.
- Keep CriticAgent generic and dynamically configured per task.
- Preserve task_id and run_id across all workflow stages.
- Add persistence and auditability without coupling agents to storage implementation.
- Complete one end-to-end MVP before adding advanced parallel orchestration.
- Keep all project documentation compliant with PROJECT_FILE_STANDARD.md.

## 3. Phase 0 - Repository Bootstrap

Goal: establish a clean project foundation.

Scope:

- create and validate the repository structure;
- maintain docs/, agents/, supervisor/, tools/, models/, config/, prompts/, tests/, scripts/, output/, and logs/;
- maintain PROJECT_FILE_STANDARD.md;
- maintain ARCHITECTURE.md;
- add ROADMAP.md;
- prepare .env.example;
- prepare requirements.txt or equivalent dependency definition;
- verify .gitignore coverage;
- define minimal local run instructions.

Exit criteria:

- repository structure is stable;
- required project documentation exists;
- secrets are excluded from Git;
- the project can be cloned and prepared for development.

Status: IN_PROGRESS

## 4. Phase 1 - Core Domain Models and Contracts

Goal: define stable machine-readable contracts before workflow implementation.

Scope:

- define Task model;
- define AgentResult model;
- define CriticProfile model;
- define Claim model;
- define Source model;
- define ReviewResult model;
- define Artifact metadata model;
- define task_id and run_id generation rules;
- define common status and error structures.

Primary documents:

```text
AGENT_INTERFACE.md
DATA_MODELS.md
```

Exit criteria:

- all initial components can exchange structured data without ad hoc dictionaries;
- schemas have validation rules;
- contract tests cover required fields and invalid input.

## 5. Phase 2 - Supervisor Foundation

Goal: implement the orchestration core without domain research logic.

Scope:

- implement Task Manager;
- implement State Machine;
- implement Workflow Engine skeleton;
- implement Agent Registry;
- implement run tracking;
- implement explicit workflow transitions;
- implement iteration counters;
- implement failure states;
- implement termination handling.

Initial states:

```text
NEW
PROFILE_GENERATING
PROFILE_REVIEW_REQUIRED
PROFILE_APPROVED
RESEARCHING
DRAFT_READY
REVIEWING
APPROVED
FINALIZING
FINALIZED
FAILED
MAX_ITERATIONS_REACHED
COMPLETED_WITH_LIMITATIONS
```

Exit criteria:

- Supervisor can move a mock task through the complete state machine;
- invalid transitions are rejected;
- state changes are recorded;
- Supervisor does not contain research or critique logic.

## 6. Phase 3 - Domain Resolver and CriticProfile Workflow

Goal: implement dynamic critic configuration with mandatory user approval.

Scope:

- implement DomainResolver;
- detect primary and secondary domains;
- detect task type;
- estimate risk level;
- propose source classes and verification criteria;
- generate a draft CriticProfile;
- present the draft profile to the user;
- support user approval and editing;
- freeze the approved profile for the current task_id;
- detect material profile amendment requirements.

Required interaction rule:

```text
Supervisor proposes.
User approves or edits.
Critic executes.
```

Exit criteria:

- no autonomous Research-Critic workflow starts without PROFILE_APPROVED;
- approved CriticProfile is immutable for normal agent execution;
- material amendments return to user approval;
- multi-domain profiles are supported.

## 7. Phase 4 - ResearchAgent MVP

Goal: produce evidence-backed draft research results.

Scope:

- implement generic ResearchAgent;
- decompose the user task;
- generate a search plan;
- use tools layer for web research;
- collect sources;
- extract claims;
- record uncertainty;
- create a draft report representation;
- accept structured revision feedback from CriticAgent.

Exit criteria:

- ResearchAgent can complete a research task with structured claims and sources;
- every important claim can reference source_ids;
- the agent does not directly bypass the tools layer;
- revision input can produce a new draft version.

## 8. Phase 5 - Tools and Evidence Layer

Goal: isolate external information access and evidence handling.

Scope:

- implement web_search abstraction;
- implement web_fetch abstraction;
- implement source metadata extraction;
- implement source deduplication;
- implement citation management;
- implement source reliability classification support;
- implement claim-to-source linking;
- implement access time and publication date handling where available.

Default source classes:

```text
A - primary or official source
B - authoritative independent source
C - secondary source
D - weak or unverified source
```

Exit criteria:

- agents use common tools instead of embedded web logic;
- duplicate sources are normalized;
- claims can be audited against source records;
- source reliability rules can be overridden by CriticProfile.

## 9. Phase 6 - CriticAgent MVP

Goal: provide independent, profile-driven verification and critique.

Scope:

- implement generic CriticAgent;
- load the approved CriticProfile;
- independently verify key claims;
- perform separate web research where required;
- assess source authority and freshness;
- detect unsupported claims;
- detect contradictions;
- identify missing important topics;
- evaluate whether conclusions follow from evidence;
- return PASS or REVISE;
- return structured improvement requests.

Initial result contract:

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

- CriticAgent behavior changes according to CriticProfile;
- literary, medical, technical, and multi-domain test profiles can use the same agent implementation;
- CriticAgent performs independent verification rather than only text editing;
- PASS and REVISE decisions are machine-readable.

## 10. Phase 7 - Autonomous Research-Critic Loop

Goal: complete the main autonomous multi-agent workflow.

Scope:

- connect ResearchAgent and CriticAgent through Supervisor;
- pass structured review feedback to ResearchAgent;
- version draft results by iteration;
- enforce max_iterations;
- enforce minimum reliability threshold;
- stop on PASS when acceptance criteria are satisfied;
- terminate explicitly on unrecoverable failure;
- support COMPLETED_WITH_LIMITATIONS when useful output exists but full acceptance is not reached.

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

- no user interaction is required during normal revision cycles;
- all iterations are auditable;
- the loop stops deterministically;
- the final workflow state matches the acceptance result.

## 11. Phase 8 - ReportGenerator and Final Artifacts

Goal: produce final user-facing outputs.

Scope:

- implement ReportGenerator;
- generate <TASK_ID>_FINAL_REPORT.md;
- generate <TASK_ID>_REVIEW_PROTOCOL.md;
- use UTF-8 for work-result artifacts;
- include sources and uncertainty in FINAL_REPORT;
- include iteration summary, critic decisions, improvements, and limitations in REVIEW_PROTOCOL;
- exclude hidden chain-of-thought and private model reasoning.

Exit criteria:

- both required artifacts are created from the same task_id;
- artifact metadata records final task status;
- reports are readable without access to internal runtime state;
- limitations are explicit when acceptance criteria are not fully met.

## 12. Phase 9 - End-to-End MVP

Goal: deliver the first complete usable system.

Initial interface:

```text
CLI or equivalent local command
```

Scope:

- accept a user research task;
- generate CriticProfile proposal;
- receive user approval or edits;
- run autonomous Research-Critic iterations;
- finalize the task;
- generate both output documents;
- provide explicit success, limitation, or failure status.

Required test scenarios:

- literary analysis task;
- medical knowledge research task;
- geodesy or construction technical task;
- multi-domain task;
- forced max_iterations case;
- tool failure case;
- material CriticProfile amendment case.

Exit criteria:

- all primary workflows pass end-to-end tests;
- MVP produces repeatable outputs;
- failure paths do not terminate silently;
- user interaction occurs only at defined approval boundaries.

MVP boundary: Phase 9.

## 13. Phase 10 - Persistence and Audit

Goal: preserve full execution history and enable recovery.

Scope:

- implement persistence abstraction;
- add SQLite as the initial persistent store unless another decision supersedes it;
- store tasks;
- store workflow runs;
- store agent runs;
- store critic profiles and amendments;
- store claims and sources;
- store reviews;
- store artifact metadata;
- support restart and recovery where practical.

Candidate tables:

```text
tasks
workflow_runs
agent_runs
critic_profiles
claims
sources
reviews
artifacts
```

Exit criteria:

- a completed task can be audited after process restart;
- approved CriticProfile can be reconstructed exactly;
- agent business logic does not depend directly on SQLite APIs.

## 14. Phase 11 - Configuration, Cost, and Quality Controls

Goal: make runtime behavior controlled and measurable.

Scope:

- centralize settings in config/settings.yaml;
- configure max_iterations;
- configure reliability thresholds;
- configure source limits;
- configure search call limits;
- configure timeouts and retries;
- configure model selection by role;
- track token and API usage where supported;
- record quality metrics;
- add logging policy.

Exit criteria:

- operational limits are configuration-driven;
- model selection can change without modifying agent code;
- usage and quality metrics are available per task and run.

## 15. Phase 12 - Test and CI Hardening

Goal: establish a stable engineering workflow in GitHub.

Scope:

- unit tests;
- contract tests;
- state machine tests;
- profile approval tests;
- domain resolver tests;
- agent integration tests;
- end-to-end tests;
- linting;
- type checks;
- GitHub Actions CI;
- branch and pull request checks.

Exit criteria:

- required checks run automatically on changes;
- contract regressions are detected;
- critical workflow paths have automated coverage.

## 16. Phase 13 - Modular Agent Platform

Goal: evolve K_Supervisor beyond the initial research workflow.

Scope:

- formalize capability discovery in AgentRegistry;
- allow Supervisor to select agents by required capability;
- add new generic agents through the common Agent Interface;
- support additional workflow definitions;
- support multiple critic instances when required;
- support domain-specific profiles without domain-specific Supervisor code.

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

- a new agent can be registered without redesigning Supervisor core;
- unrelated agents do not require modification;
- workflow definitions can reference capabilities rather than hard-coded classes.

## 17. Deferred Capabilities

The following are intentionally deferred until the core platform is stable:

```text
Web UI
distributed execution
complex parallel orchestration
vector database
complex long-term memory
automatic agent generation
large-scale workflow scheduling
```

These items require separate architectural decisions before implementation.

## 18. Planned Project Documents

Documentation should be developed in this order unless implementation needs require adjustment:

```text
AGENT_INTERFACE.md
DATA_MODELS.md
RESEARCH_WORKFLOW.md
CONFIGURATION.md
TEST_PLAN.md
PROJECT_HISTORY.md
```

## 19. Current Implementation Order

Immediate development sequence:

```text
Phase 0 - Repository Bootstrap
Phase 1 - Core Domain Models and Contracts
Phase 2 - Supervisor Foundation
Phase 3 - Domain Resolver and CriticProfile Workflow
Phase 4 - ResearchAgent MVP
Phase 5 - Tools and Evidence Layer
Phase 6 - CriticAgent MVP
Phase 7 - Autonomous Research-Critic Loop
Phase 8 - ReportGenerator and Final Artifacts
Phase 9 - End-to-End MVP
```

After MVP:

```text
Phase 10 - Persistence and Audit
Phase 11 - Configuration, Cost, and Quality Controls
Phase 12 - Test and CI Hardening
Phase 13 - Modular Agent Platform
```

## 20. Roadmap Decision Summary

- The first product goal is one complete research and independent critique workflow.
- CriticProfile approval is a mandatory user-controlled gate before autonomous execution.
- CriticAgent remains generic and receives dynamic domain configuration.
- Supervisor owns workflow control, state, iteration limits, and finalization.
- ResearchAgent and CriticAgent operate autonomously after profile approval.
- MVP completion is defined at Phase 9.
- Persistence, cost controls, CI hardening, and broader agent expansion follow the working MVP.
