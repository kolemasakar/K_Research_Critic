# ARCHITECTURE
Короткий опис архітектури K_Supervisor, основних компонентів, workflow та моделей розгортання.

Version: 1.1
Status: ACTIVE

## 1. Purpose

K_Supervisor is a reusable multi-agent orchestration system.

Its core responsibility is to accept a user task, configure the required agent roles, coordinate autonomous agent interaction, control quality gates, and produce final artifacts.

The initial product workflow is research plus independent critique. The architecture remains extensible for additional agents and workflows.

## 2. Core Principles

- Supervisor coordinates work but does not perform domain research or critique itself.
- Agents communicate through explicit validated contracts.
- Every task has a stable task_id and every agent execution has a stable run_id.
- Workflow transitions are explicit and auditable.
- CriticAgent is generic and receives a task-specific CriticProfile.
- User approval of CriticProfile is mandatory before autonomous execution.
- Approved profiles are immutable unless a material amendment is separately approved.
- Research-Critic revision cycles are autonomous after approval.
- Evidence, uncertainty, limitations, and final status remain explicit.
- Execution status, critic decision, task state, and workflow state remain separate concepts.
- Hidden chain-of-thought/private reasoning is never persisted as an artifact.

## 3. Product Distribution Decision

K_Supervisor is GPT Store-first.

The primary public edition is a Custom GPT distributed through ChatGPT. It is designed to work without a developer-owned OpenAI API key, without a mandatory external backend, and without a pinned model identifier.

Primary policy:

```text
channel: chatgpt_store
free_user_compatible: true
developer_api_key_required: false
model_policy: user_plan
recommended_model: null
allow_user_model_switch: true
external_backend_required: false
```

The platform supplies the model available to the user. Users with additional model choices may switch to another model exposed by their ChatGPT plan. K_Supervisor workflow semantics must not depend on a specific named ChatGPT model.

The canonical deployment policy is specified in `GPT_STORE_DEPLOYMENT.md`.

## 4. Deployment Profiles

K_Supervisor has two deployment profiles built around the same logical workflow contracts.

```text
K_Supervisor Core
  |
  +-- GPT Store Edition       PRIMARY
  |     - runs inside ChatGPT
  |     - ChatGPT-managed model
  |     - no developer API key
  |     - no mandatory backend
  |     - built-in ChatGPT capabilities where available
  |
  +-- Standalone/API Edition  OPTIONAL
        - Python runtime
        - SQLite persistence
        - provider/model factory
        - provider secrets only when a selected provider requires them
```

The optional standalone/API edition exists for local engineering, automated tests, server integrations, and future products. It must not become a dependency of the free GPT Store core experience.

## 5. High-Level Logical Architecture

```text
USER
  |
  v
SUPERVISOR
  |
  +-- Task Manager
  +-- Domain Resolver
  +-- Profile Manager
  +-- Agent Registry
  +-- Workflow Engine
  +-- State Machine
  |
  +-----------------------------+
  |                             |
  v                             v
ResearchAgent               CriticAgent
  |                             |
  +---------- Tools Layer ------+
  |
  v
Evidence / Sources
  |
  v
ReportGenerator
  |
  +-- FINAL_REPORT
  +-- REVIEW_PROTOCOL
```

Deployment infrastructure may differ, but these logical roles and boundaries remain stable.

## 6. Supervisor Responsibilities

Supervisor is responsible for:

- receiving the user task;
- creating task_id;
- analyzing task domain/type;
- generating a draft CriticProfile;
- presenting the profile for explicit user approval/edit/reject;
- freezing the approved profile;
- selecting and launching agents;
- passing structured context/results between agents;
- controlling workflow state and iteration limits;
- enforcing configured limits and termination rules;
- handling recoverable and unrecoverable failures;
- triggering final artifact generation.

Supervisor must not perform domain research, fact checking, or domain critique directly.

## 7. Dynamic Agent Configuration

Core rule:

```text
Agent = generic capability + dynamically assigned task/domain profile
```

The system avoids hard-coded domain critic classes such as `MedicalCriticAgent` or `GeodesyCriticAgent`. One generic CriticAgent receives the approved task-specific CriticProfile.

## 8. Domain Resolution

Domain resolution identifies:

- primary domain;
- secondary domains;
- task type;
- risk level;
- relevant source classes/standards;
- multi-domain requirements.

Current implementation supports deterministic RuleBasedResolver plus provider-neutral LLMSemanticResolver and HybridResolver.

HybridResolver preserves deterministic fallback and risk floors, validates semantic results, and surfaces material disagreement for user review.

In the GPT Store edition, semantic reasoning is supplied by the ChatGPT runtime and must not require a developer API secret. The existing OpenAI API adapter remains optional for standalone/API execution.

## 9. CriticProfile and User Approval

Before autonomous execution, Supervisor generates a CriticProfile draft and presents it to the user.

The user may approve, edit, or reject it.

The profile includes at least:

```text
profile_id
domain
subdomains
task_type
risk_level
critic_role
evaluation_criteria
preferred_source_types
required_cross_checks
standards
minimum_evidence_level
freshness_requirement
confidence_threshold
special_user_requirements
status
```

Required interaction rule:

```text
Supervisor proposes.
User approves or edits.
Critic executes.
```

Only an APPROVED profile may be used by CriticAgent.

## 10. Profile Freeze Rule

After approval, CriticProfile is frozen for the current task.

CriticAgent must not independently change assigned domain, evaluation criteria, evidence thresholds, source hierarchy, standards, or confidence threshold.

If research reveals a materially new requirement, Supervisor may propose an amended profile. The amendment becomes active only after explicit user approval.

## 11. Multi-Domain Support

A task may require multiple domains, for example geodetic monitoring of structural deformation.

One CriticProfile may contain multiple domains and grouped criteria. Future workflows may assign multiple critic instances through the same Agent Interface without redesigning Supervisor.

## 12. Agent Registry and Interface

Initial registry:

```text
ResearchAgent
CriticAgent
ReportGenerator
```

Future examples:

```text
FactCheckAgent
DataAnalysisAgent
TechnicalAgent
FinancialAgent
LegalAgent
PlanningAgent
```

Logical execution contract:

```text
run(request) -> AgentResult
```

Detailed contracts are defined in `AGENT_INTERFACE.md` and `DATA_MODELS.md`.

## 13. ResearchAgent

ResearchAgent:

- decomposes the task;
- builds a search strategy;
- collects sources and evidence;
- extracts claims;
- records uncertainty/limitations;
- creates a draft report;
- revises output from structured CriticAgent feedback.

ResearchAgent is not the final verifier of its own conclusions.

## 14. CriticAgent

CriticAgent performs independent verification under the approved CriticProfile.

It evaluates source authority/freshness, unsupported claims, contradictions, missing topics, conclusion/evidence consistency, and returns a machine-readable PASS or REVISE decision with structured recommendations.

CriticAgent is not limited to wording edits.

## 15. Evidence Layer

Claims and sources are represented separately from prose.

Claim baseline:

```text
claim_id
text
source_ids[]
confidence
verification_status
```

Source baseline:

```text
source_id
url
title
publisher
publication_date
accessed_at
source_type
reliability_class
```

Default reliability classes:

```text
A - primary or official
B - authoritative independent
C - secondary
D - weak or unverified
```

CriticProfile may strengthen or refine evidence requirements.

## 16. Research-Critic Workflow

```text
NEW
 |
 v
PROFILE_GENERATING
 |
 v
PROFILE_REVIEW_REQUIRED
 |
 +-- user edit/reject --> PROFILE_GENERATING
 |
 +-- user approval ----> PROFILE_APPROVED
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
                +----------+----------+
                |                     |
             REVISE                  PASS
                |                     |
                v                     v
          REVISE_REQUIRED          APPROVED
                |                     |
                v                     v
           RESEARCHING            FINALIZING
                                      |
                                      v
                                  FINALIZED
```

Additional terminal/exception states:

```text
FAILED
MAX_ITERATIONS_REACHED
COMPLETED_WITH_LIMITATIONS
```

## 17. Autonomous Interaction Boundary

User interaction is required before PROFILE_APPROVED and again only for material profile amendments or unrecoverable ambiguity that cannot be resolved internally.

Normal Research-Critic revision cycles require no user intervention.

## 18. Critic Result Contract

Baseline review result:

```json
{
  "decision": "PASS | REVISE",
  "reliability_score": 0.0,
  "critical_issues": [],
  "unsupported_claim_ids": [],
  "weak_source_ids": [],
  "contradictions": [],
  "missing_topics": [],
  "recommended_changes": []
}
```

AgentResult.status remains separate from CriticReview.decision.

## 19. Termination Rules

The loop stops when:

- accepted PASS meets the approved reliability threshold;
- max_iterations is reached;
- an unrecoverable failure occurs.

Reaching max_iterations is not successful verification. If useful output exists but full acceptance is not reached, Supervisor may finish as `COMPLETED_WITH_LIMITATIONS`.

## 20. ReportGenerator

ReportGenerator creates:

```text
<TASK_ID>_FINAL_REPORT.md
<TASK_ID>_REVIEW_PROTOCOL.md
```

Reports include evidence references, uncertainty, significant review issues, applied changes, unresolved limitations, and final status. They must not contain hidden chain-of-thought/private reasoning.

## 21. Tools Layer

External capabilities are isolated behind provider-neutral boundaries, including:

```text
web_search
web_fetch
source_validator
citation_manager
```

GPT Store Edition should prefer built-in ChatGPT capabilities where available. Standalone/API Edition may use injected provider adapters.

## 22. Configuration

Tracked defaults live in:

```text
config/settings.yaml
```

Configuration includes workflow, distribution policy, models, tools, research, critic, reports, persistence, logging, retry, and limits.

The GPT Store distribution policy is a system invariant in tracked defaults: no required developer API key, no required external backend, user-plan model selection, and no pinned model identifier.

Provider secrets remain optional standalone/API configuration and are never part of persisted task configuration snapshots.

## 23. Persistence

Persistence is isolated behind a dedicated boundary.

Standalone/API Edition currently provides SQLite persistence for tasks, workflows, profiles, claims, sources, reviews, agent results, and artifacts.

GPT Store Edition cannot depend on that server-side SQLite runtime. Its baseline continuity model is conversation-local state plus explicit checkpoint/recovery artifacts for cross-chat continuation.

## 24. Failure Handling

Supervisor handles at least model/tool timeout, malformed output, unavailable source, repeated results, resource limit, tool exception, agent exception, and unrecoverable ambiguity.

Recoverable failures follow retry policy. Unrecoverable failures produce explicit task status.

## 25. Extensibility

New agents implement the Agent Interface, register through AgentRegistry, and become available to workflow definitions without requiring unrelated agents to change.

## 26. MVP and Product Boundary

The completed Python MVP includes Supervisor, Task Manager, Domain Resolver, Profile Manager, State Machine, Agent Registry, Workflow Engine, ResearchAgent, CriticAgent, Tools Layer, Evidence Model, ReportGenerator, CLI, and SQLite persistence.

The primary public product target is now the GPT Store Edition. Packaging/publication work must preserve the completed core workflow while adapting execution state, tools, and model selection to ChatGPT-native capabilities.

## 27. Deferred Capabilities

Deferred until separate architectural decisions:

```text
custom Web UI
distributed execution
complex parallel orchestration
vector database
complex long-term memory
automatic agent generation
large-scale workflow scheduling
mandatory external backend for Store Edition
```

## 28. Architecture Decision Summary

- K_Supervisor remains a generic multi-agent orchestration platform.
- Supervisor coordinates but does not replace domain agents.
- CriticAgent remains generic and profile-driven.
- CriticProfile approval is mandatory and approved profiles are frozen.
- Multi-domain profiles are supported.
- Research-Critic interaction is autonomous after approval.
- Final output contains a consolidated report and review protocol.
- GPT Store Edition is the primary public distribution target.
- GPT Store Edition requires no developer API key and no mandatory backend.
- GPT Store Edition uses the model available to the user's ChatGPT plan; paid users may select additional available models.
- No concrete ChatGPT model identifier is a core architectural dependency.
- The existing Python/SQLite/provider stack is retained as an optional standalone/API edition and engineering reference runtime.
