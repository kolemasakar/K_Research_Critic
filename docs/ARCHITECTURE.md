# ARCHITECTURE
Короткий опис архітектури K_Supervisor, основних компонентів та принципів їх взаємодії.

Version: 1.0
Status: ACTIVE

## 1. Purpose

K_Supervisor is a reusable multi-agent orchestration system.

Its core responsibility is to accept a user task, configure the required agent roles, coordinate autonomous agent interaction, control quality gates, and produce final artifacts.

The initial workflow focuses on research and independent critique, but the architecture must support adding new agent types without redesigning the Supervisor core.

## 2. Core Principles

- Supervisor coordinates work but does not perform domain research or critique itself.
- Each agent has one clear primary responsibility.
- Agents communicate through explicit structured contracts.
- Every task has a stable task_id.
- Every agent execution has a stable run_id.
- Workflow state transitions must be explicit and auditable.
- Agent behavior is configured dynamically for the current task.
- The system must support adding agents without changing unrelated agents.
- User participation is required for critic profile approval before autonomous execution begins.
- After profile approval, the Research-Critic loop runs without additional user involvement unless the approved profile must materially change.

## 3. High-Level Architecture

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

## 4. Supervisor Responsibilities

Supervisor is responsible for:

- receiving a user task;
- creating task_id;
- analyzing the task domain and task type;
- generating a draft critic profile;
- presenting the critic profile to the user for approval or editing;
- freezing the approved critic profile for the current task;
- selecting and launching agents;
- passing structured context and results between agents;
- controlling workflow state;
- controlling iteration limits;
- handling recoverable and unrecoverable failures;
- applying termination criteria;
- triggering final artifact generation.

Supervisor must not perform domain research, fact checking, or domain critique directly.

## 5. Dynamic Agent Configuration

A core architectural rule is:

```text
Agent = generic capability + dynamically assigned task/domain profile
```

The system should avoid creating hard-coded agents such as:

```text
MedicalCriticAgent
GeodesyCriticAgent
LiteraryCriticAgent
ConstructionCriticAgent
```

Instead, one generic CriticAgent receives a task-specific profile before execution.

The same principle may later be applied to ResearchAgent and other reusable agents.

## 6. Domain Resolver

DomainResolver analyzes the user task and identifies:

- primary domain;
- secondary domains;
- task type;
- likely risk level;
- relevant standards or source classes;
- whether the task is multi-domain.

Examples of domains include:

```text
literary_analysis
medicine
geodesy
construction
military
finance
law
software_engineering
```

The domain list is not closed and must be extensible.

## 7. Critic Profile Generation and User Approval

Before the autonomous workflow starts, Supervisor must generate a draft CriticProfile and present it to the user.

The user may:

- approve it unchanged;
- add evaluation criteria;
- remove evaluation criteria;
- modify source requirements;
- modify strictness or risk level;
- add task-specific requirements.

Only an approved profile may be used by CriticAgent.

The required interaction rule is:

```text
Supervisor proposes.
User approves or edits.
Critic executes.
```

## 8. CriticProfile Model

The profile should support at least the following fields:

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

Recommended profile states:

```text
DRAFT
REVIEW_REQUIRED
APPROVED
REJECTED
```

## 9. Profile Freeze Rule

After user approval, the CriticProfile is frozen for the current task_id.

CriticAgent must not independently change:

- assigned domain;
- evaluation criteria;
- evidence thresholds;
- source hierarchy;
- standards;
- confidence threshold.

If research reveals a materially new domain or requirement, Supervisor may generate a proposed profile amendment.

A material amendment requires user approval before it becomes active.

## 10. Multi-Domain Profiles

A task may require more than one domain.

Example:

```text
Geodetic monitoring of structural deformation
```

Possible profile:

```text
domains:
- geodesy
- structural_engineering
```

Evaluation criteria may be grouped by domain while still being executed by one CriticAgent.

If future complexity requires it, Supervisor may assign multiple specialized critic instances through the same Agent Interface.

## 11. Agent Registry

Supervisor must not hard-code all agent implementations into workflow logic.

An AgentRegistry provides discoverable agent capabilities.

Initial registry:

```text
AgentRegistry
|
+-- ResearchAgent
+-- CriticAgent
+-- ReportGenerator
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

Adding a new agent should not require changes to unrelated agents.

## 12. Agent Interface

All executable agents should follow a common logical contract.

Minimum execution context:

```text
agent_id
agent_type
task_id
run_id
input
context
profile
status
result
errors
metadata
```

Logical operation:

```text
run(task, context, profile) -> AgentResult
```

The detailed contract will be specified in AGENT_INTERFACE.md.

## 13. ResearchAgent Responsibilities

ResearchAgent is responsible for:

- decomposing the task;
- building a search strategy;
- collecting information;
- collecting sources;
- extracting claims;
- identifying uncertainty;
- creating a draft report;
- revising the report in response to structured CriticAgent feedback.

ResearchAgent is not the final authority on the reliability of its own conclusions.

## 14. CriticAgent Responsibilities

CriticAgent is responsible for independent verification and critique according to the approved CriticProfile.

It must be able to:

- perform independent web research;
- verify important claims;
- assess source quality;
- check freshness where relevant;
- detect unsupported claims;
- detect contradictions;
- identify missing important topics;
- assess whether conclusions follow from evidence;
- return PASS or REVISE with structured feedback.

CriticAgent must not be limited to editing ResearchAgent wording.

## 15. Evidence Layer

Claims and sources should be represented separately from the final prose report.

Suggested Claim model:

```text
claim_id
text
source_ids[]
confidence
verification_status
```

Suggested Source model:

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

This allows the system to verify evidence at claim level instead of only reviewing finished prose.

## 16. Source Reliability Classes

A default source hierarchy may use:

```text
A - primary or official source
B - authoritative independent source
C - secondary source
D - weak or unverified source
```

The CriticProfile may override or refine this hierarchy for a specific domain.

## 17. Research-Critic Workflow

The approved initial workflow is:

```text
NEW
 |
 v
PROFILE_GENERATING
 |
 v
PROFILE_REVIEW_REQUIRED
 |
 +-- user edit --> PROFILE_GENERATING
 |
 +-- user approval --> PROFILE_APPROVED
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
         RESEARCHING             APPROVED
                                    |
                                    v
                               FINALIZING
                                    |
                                    v
                                FINALIZED
```

Additional terminal or exceptional states:

```text
FAILED
MAX_ITERATIONS_REACHED
COMPLETED_WITH_LIMITATIONS
```

## 18. Autonomous Interaction Boundary

User interaction is required before PROFILE_APPROVED.

After PROFILE_APPROVED, ResearchAgent and CriticAgent interact autonomously under Supervisor control.

Normal revision cycles must not require user intervention.

User interaction is required again only if:

- the task scope materially changes;
- the required critic domain materially changes;
- Supervisor proposes a material amendment to the approved profile;
- an unrecoverable ambiguity cannot be resolved internally.

## 19. Critic Result Contract

CriticAgent should return a structured result similar to:

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

The exact schema will be finalized in DATA_MODELS.md or AGENT_INTERFACE.md.

## 20. Termination Rules

The Research-Critic loop may terminate when:

- CriticAgent returns PASS;
- no critical issues remain;
- the configured reliability threshold is met;
- max_iterations is reached;
- an unrecoverable failure occurs.

Reaching max_iterations must not automatically imply successful verification.

If useful output exists but acceptance criteria are not fully met, the task may end as:

```text
COMPLETED_WITH_LIMITATIONS
```

## 21. ReportGenerator

ReportGenerator creates final user-facing artifacts from approved or explicitly limited results.

Initial artifacts:

```text
<TASK_ID>_FINAL_REPORT.md
<TASK_ID>_REVIEW_PROTOCOL.md
```

Both are work-result files and use UTF-8 by default according to PROJECT_FILE_STANDARD.md.

FINAL_REPORT should contain the consolidated result, evidence references, uncertainty, and conclusions.

REVIEW_PROTOCOL should contain a concise audit of:

- iteration count;
- critic decisions and scores;
- significant issues found;
- changes applied;
- unresolved limitations;
- final status.

It must not contain private chain-of-thought or hidden model reasoning.

## 22. Tools Layer

External capabilities should be exposed through a tools layer instead of being implemented directly inside agents.

Examples:

```text
tools/
|
+-- web_search
+-- web_fetch
+-- source_validator
+-- citation_manager
```

This allows tools to be replaced, tested, limited, or extended independently from agent logic.

## 23. Configuration

Project runtime configuration should be centralized.

Initial location:

```text
config/settings.yaml
```

Typical settings:

```text
max_iterations
minimum_reliability_score
max_sources
max_search_calls
timeouts
models
logging
```

Secrets must be stored outside tracked configuration, typically in .env or a secret manager.

Secrets must not be committed to Git.

## 24. Persistence

The architecture must isolate persistence behind a dedicated layer.

MVP may initially use structured files or JSON where appropriate.

A later persistent store may use SQLite with entities such as:

```text
tasks
agent_runs
workflow_runs
critic_profiles
claims
sources
reviews
artifacts
```

Changing the persistence implementation should not require changing agent business logic.

## 25. Failure Handling

Supervisor must handle at least:

- LLM timeout;
- web tool failure;
- malformed agent output;
- unavailable source;
- duplicate or repeated results;
- iteration limit exceeded;
- tool exception;
- agent exception.

Recoverable failures should be retried or routed according to policy.

Unrecoverable failures must produce an explicit task status instead of silent termination.

## 26. Extensibility

A new agent should become available by:

```text
New Agent
   |
   v
implements Agent Interface
   |
   v
registered in Agent Registry
   |
   v
available to Supervisor
```

Adding a new agent must not require modifying ResearchAgent or CriticAgent unless their explicit contract changes.

## 27. MVP Boundary

Initial MVP includes:

```text
Supervisor
Task Manager
Domain Resolver
Profile Manager
State Machine
Agent Registry
Workflow Engine
ResearchAgent
CriticAgent
Tools Layer
Evidence Model
ReportGenerator
CLI
```

Initial MVP excludes:

```text
Web UI
distributed agent execution
complex parallel orchestration
vector database
automatic agent generation
complex long-term memory
```

## 28. Planned Architecture Documents

The following project documents are expected after this architecture is accepted:

```text
ROADMAP.md
AGENT_INTERFACE.md
DATA_MODELS.md
RESEARCH_WORKFLOW.md
CONFIGURATION.md
TEST_PLAN.md
```

## 29. Architecture Decision Summary

The approved foundational decisions are:

- K_Supervisor is a generic multi-agent orchestration platform.
- Supervisor controls workflow but does not replace domain agents.
- CriticAgent is generic and dynamically configured per task.
- Supervisor generates a draft CriticProfile from the task domain.
- User approval or editing of CriticProfile is mandatory before autonomous execution.
- The approved profile is frozen for the task unless a material amendment is separately approved.
- Multi-domain critic profiles are supported.
- Research-Critic interaction becomes autonomous after profile approval.
- Final output includes a consolidated report and a concise review protocol.
- The architecture must remain extensible for future agents and workflows.
