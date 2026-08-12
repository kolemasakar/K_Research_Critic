# DATA_MODELS
Моделі даних K_Supervisor для задач, профілів агентів, доказів, перевірок, станів workflow та артефактів.

Version: 1.0
Status: ACTIVE

## 1. Purpose

This document defines the canonical logical data models used by K_Supervisor.

The models are storage-neutral and transport-neutral. They define the information that must exist regardless of whether the implementation uses Python objects, JSON files, SQLite, or another persistence layer.

## 2. General Rules

- Every persistent entity must have a stable identifier.
- All timestamps use ISO 8601 in UTC unless a task explicitly requires local time metadata.
- IDs are immutable after creation.
- Agent outputs must be serializable to JSON-compatible structures.
- Domain-specific payloads may extend generic models but must not remove required fields.
- Missing optional values must be represented explicitly as null or omitted according to the implementation schema.
- User-approved configuration must be distinguishable from generated draft configuration.
- Final user-facing reports are UTF-8 artifacts according to PROJECT_FILE_STANDARD.md.

## 3. Identifier Conventions

Recommended logical prefixes:

```text
TASK_000001
RUN_000001
WF_000001
PROFILE_000001
CLAIM_000001
SOURCE_000001
REVIEW_000001
ARTIFACT_000001
```

Identifiers may later use UUIDs internally, but external representation should remain stable and human-traceable where practical.

## 4. Task Model

Task is the root entity for one user request.

Required fields:

```text
task_id
created_at
updated_at
status
user_request
task_type
primary_domain
secondary_domains[]
risk_level
active_profile_id
current_workflow_run_id
metadata
```

Suggested task statuses:

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

Rules:

- task_id is created once by Supervisor.
- user_request preserves the original user instruction.
- status is controlled only by Supervisor or the state machine.
- active_profile_id is null until a CriticProfile is approved.
- task status must never imply PASS when acceptance criteria were not met.

## 5. DomainAssessment Model

DomainAssessment stores Supervisor analysis used to propose a critic profile.

Required fields:

```text
assessment_id
task_id
primary_domain
secondary_domains[]
task_type
risk_level
identified_standards[]
recommended_source_types[]
recommended_evaluation_criteria[]
uncertainties[]
created_at
```

This entity is advisory. It does not authorize CriticAgent execution.

## 6. CriticProfile Model

CriticProfile defines how CriticAgent must evaluate the task.

Required fields:

```text
profile_id
task_id
version
status
domain[]
subdomains[]
task_type
risk_level
critic_role
evaluation_criteria[]
preferred_source_types[]
required_cross_checks[]
standards[]
minimum_evidence_level
freshness_requirement
confidence_threshold
special_user_requirements[]
created_at
approved_at
approved_by
supersedes_profile_id
```

Allowed profile statuses:

```text
DRAFT
REVIEW_REQUIRED
APPROVED
REJECTED
SUPERSEDED
```

Rules:

- CriticAgent may execute only with status APPROVED.
- approved_by must identify the user approval boundary.
- approved_at is immutable after approval.
- an approved profile is frozen for its task.
- a material change creates a new profile version instead of mutating the approved record.
- supersedes_profile_id links an approved amendment to the previous profile.

## 7. AgentDefinition Model

AgentDefinition describes a registered agent capability.

Required fields:

```text
agent_id
agent_type
name
version
capabilities[]
accepted_input_types[]
produced_output_types[]
supports_profile
status
metadata
```

Suggested agent statuses:

```text
ACTIVE
DISABLED
DEPRECATED
```

Initial agent types:

```text
RESEARCH
CRITIC
REPORT_GENERATOR
```

The registry may later contain additional agent types without changing the common contract.

## 8. AgentRunRequest Model

AgentRunRequest is the canonical Supervisor-to-agent execution envelope.

Required fields:

```text
request_id
task_id
workflow_run_id
run_id
agent_id
agent_type
iteration
input
context
profile
constraints
created_at
```

Rules:

- run_id identifies one execution attempt.
- request_id supports idempotency and retry control.
- profile may be null for agents that do not require one.
- CriticAgent requires the full approved CriticProfile or an immutable reference to it.
- context should contain only information required for the current execution.

## 9. AgentResult Model

AgentResult is the canonical agent-to-Supervisor response envelope.

Required fields:

```text
run_id
request_id
task_id
agent_id
agent_type
status
result_type
payload
warnings[]
errors[]
metrics
started_at
completed_at
```

Allowed generic execution statuses:

```text
SUCCEEDED
PARTIAL
FAILED
```

AgentResult status describes execution success, not domain acceptance.

For example, CriticAgent may return:

```text
status: SUCCEEDED
decision: REVISE
```

## 10. ResearchResult Model

ResearchResult is the main payload produced by ResearchAgent.

Required fields:

```text
research_result_id
task_id
run_id
iteration
summary
findings[]
claim_ids[]
source_ids[]
uncertainties[]
limitations[]
draft_report
change_log[]
created_at
```

Rules:

- findings should reference claims where practical.
- claims and sources must be stored separately from prose.
- change_log is required for revision iterations after the first draft.

## 11. Claim Model

Claim is a discrete factual or analytical assertion that may require verification.

Required fields:

```text
claim_id
task_id
text
claim_type
importance
source_ids[]
confidence
verification_status
created_by_run_id
created_at
updated_at
```

Suggested claim types:

```text
FACT
INTERPRETATION
INFERENCE
ESTIMATE
RECOMMENDATION
```

Suggested importance levels:

```text
LOW
MEDIUM
HIGH
CRITICAL
```

Suggested verification statuses:

```text
UNVERIFIED
PARTIALLY_VERIFIED
VERIFIED
CONTRADICTED
INSUFFICIENT_EVIDENCE
NOT_APPLICABLE
```

Rules:

- an inference must not be represented as a verified fact.
- critical claims should receive stricter evidence requirements defined by CriticProfile.
- one claim may reference multiple independent sources.

## 12. Source Model

Source represents one external or provided information source.

Required fields:

```text
source_id
task_id
url
title
publisher
author
publication_date
accessed_at
source_type
reliability_class
primary_source
independence_group
supports_claim_ids[]
contradicts_claim_ids[]
notes
```

Default reliability classes:

```text
A - primary or official source
B - authoritative independent source
C - secondary source
D - weak or unverified source
```

Suggested source types:

```text
OFFICIAL
PRIMARY_DOCUMENT
STANDARD
PEER_REVIEWED
ACADEMIC
GOVERNMENT
MANUFACTURER
NEWS
PROFESSIONAL_PUBLICATION
REFERENCE
USER_PROVIDED
OTHER
```

Rules:

- reliability_class is contextual and may be overridden by the approved CriticProfile.
- independence_group helps prevent counting syndicated or copied material as independent confirmation.
- accessed_at is required for web sources.

## 13. CriticReview Model

CriticReview is the structured domain review produced by CriticAgent.

Required fields:

```text
review_id
task_id
run_id
profile_id
iteration
decision
reliability_score
critical_issues[]
unsupported_claim_ids[]
weak_source_ids[]
contradictions[]
missing_topics[]
recommended_changes[]
verified_claim_ids[]
unresolved_claim_ids[]
created_at
```

Allowed decisions:

```text
PASS
REVISE
```

Rules:

- PASS is a domain decision, not merely successful agent execution.
- reliability_score must be in the range 0.0 to 1.0.
- PASS must satisfy the approved CriticProfile and workflow acceptance rules.
- CriticReview must reference concrete claims and sources where possible.

## 14. Contradiction Model

Contradiction records conflicting evidence or incompatible claims.

Required fields:

```text
contradiction_id
task_id
claim_ids[]
source_ids[]
description
severity
resolution_status
resolution_note
```

Suggested severities:

```text
LOW
MEDIUM
HIGH
CRITICAL
```

Suggested resolution statuses:

```text
OPEN
RESOLVED
UNRESOLVED
ACCEPTED_UNCERTAINTY
```

## 15. WorkflowRun Model

WorkflowRun tracks one orchestration execution for a task.

Required fields:

```text
workflow_run_id
task_id
workflow_type
status
current_state
iteration
max_iterations
started_at
completed_at
agent_run_ids[]
transition_ids[]
final_decision
metadata
```

Initial workflow type:

```text
RESEARCH_CRITIC
```

Suggested workflow statuses:

```text
RUNNING
WAITING_FOR_USER
SUCCEEDED
FAILED
COMPLETED_WITH_LIMITATIONS
```

## 16. StateTransition Model

StateTransition provides an auditable state machine history.

Required fields:

```text
transition_id
task_id
workflow_run_id
from_state
to_state
trigger
reason
actor_type
actor_id
created_at
```

Suggested actor types:

```text
USER
SUPERVISOR
AGENT
SYSTEM
```

Rules:

- every task state change should produce one StateTransition record.
- invalid transitions must be rejected by the state machine.

## 17. Artifact Model

Artifact represents a generated file or final output.

Required fields:

```text
artifact_id
task_id
workflow_run_id
artifact_type
path
encoding
status
created_by_run_id
created_at
checksum
metadata
```

Initial artifact types:

```text
DRAFT_REPORT
FINAL_REPORT
REVIEW_PROTOCOL
```

Suggested artifact statuses:

```text
GENERATED
APPROVED
SUPERSEDED
FAILED
```

Initial final filenames:

```text
<TASK_ID>_FINAL_REPORT.md
<TASK_ID>_REVIEW_PROTOCOL.md
```

Final reports and review protocols use UTF-8 by default.

## 18. ErrorRecord Model

ErrorRecord provides structured error handling.

Required fields:

```text
error_code
error_type
message
recoverable
component
run_id
retry_count
details
created_at
```

Suggested error types:

```text
VALIDATION_ERROR
TOOL_ERROR
LLM_ERROR
TIMEOUT
SOURCE_ERROR
CONTRACT_ERROR
STATE_ERROR
INTERNAL_ERROR
```

Sensitive secrets must never be copied into error details.

## 19. WarningRecord Model

WarningRecord represents non-fatal issues.

Required fields:

```text
warning_code
message
component
run_id
details
created_at
```

Warnings must not silently replace errors when the contract cannot be satisfied.

## 20. Metrics Model

Agent and workflow metrics should support cost and quality controls.

Suggested fields:

```text
duration_ms
llm_calls
search_calls
fetch_calls
input_tokens
output_tokens
estimated_cost
sources_examined
claims_created
claims_verified
retry_count
```

Metrics fields may be null when a provider does not expose the value.

## 21. Revision Model

Revision records changes made in response to CriticAgent feedback.

Required fields:

```text
revision_id
task_id
iteration
research_run_id
review_id
addressed_issue_ids[]
unresolved_issue_ids[]
changes[]
created_at
```

This model supports the concise REVIEW_PROTOCOL without exposing private model reasoning.

## 22. UserApproval Model

UserApproval records explicit approval of a profile or material amendment.

Required fields:

```text
approval_id
task_id
approval_type
target_id
decision
user_changes
created_at
```

Initial approval types:

```text
CRITIC_PROFILE
CRITIC_PROFILE_AMENDMENT
```

Initial decisions:

```text
APPROVED
REJECTED
EDITED_AND_APPROVED
```

Rules:

- CriticProfile approval must be explicit.
- autonomous agent execution begins only after the active profile has an approval record.

## 23. Data Relationships

Canonical relationships:

```text
Task
 |
 +-- DomainAssessment
 +-- CriticProfile[]
 +-- UserApproval[]
 +-- WorkflowRun[]
 |     |
 |     +-- AgentRunRequest[]
 |     +-- AgentResult[]
 |     +-- StateTransition[]
 |
 +-- Claim[]
 +-- Source[]
 +-- CriticReview[]
 +-- Revision[]
 +-- Artifact[]
```

A task may have multiple profile versions and workflow runs, but only one active approved CriticProfile at a time.

## 24. Serialization Rules

For JSON-compatible serialization:

- timestamps are ISO 8601 strings;
- enums are represented as uppercase strings;
- absent optional arrays should normally serialize as empty arrays;
- object references use stable IDs rather than embedded duplicated records unless a transport contract requires embedding;
- numeric confidence and score values use range 0.0 to 1.0;
- unknown values must not be invented to satisfy required fields.

## 25. Validation Rules

At minimum, schema validation must reject:

- missing required identifiers;
- invalid enum values;
- reliability_score outside 0.0 to 1.0;
- confidence_threshold outside 0.0 to 1.0;
- CriticAgent execution with an unapproved profile;
- task state transitions not allowed by the state machine;
- PASS without a valid CriticReview;
- final artifact generation without an accepted terminal workflow state;
- duplicate immutable identifiers.

## 26. Persistence Mapping

The logical models should support later persistence tables such as:

```text
tasks
domain_assessments
critic_profiles
user_approvals
agent_definitions
agent_runs
workflow_runs
state_transitions
research_results
claims
sources
critic_reviews
contradictions
revisions
artifacts
errors
warnings
metrics
```

The first MVP may use JSON files or in-memory objects, but the field semantics defined here must remain stable.

## 27. Compatibility Rules

- Adding optional fields is backward-compatible.
- Removing or changing required fields requires a contract version change.
- Changing enum meaning requires explicit migration planning.
- Persisted approved CriticProfiles must remain readable after application upgrades.
- Historical reviews and artifacts must retain their original task and profile references.

## 28. Security and Privacy

Data models must not intentionally persist:

```text
API keys
access tokens
passwords
private chain-of-thought
hidden model reasoning
```

If sensitive user data becomes part of a future task type, its storage policy must be defined explicitly before persistence is enabled for that data.

## 29. MVP Required Models

The minimum models required before the first end-to-end workflow are:

```text
Task
DomainAssessment
CriticProfile
UserApproval
AgentDefinition
AgentRunRequest
AgentResult
ResearchResult
Claim
Source
CriticReview
WorkflowRun
StateTransition
Revision
Artifact
ErrorRecord
```

Other models may be implemented when first required.

## 30. Acceptance Criteria

DATA_MODELS v1.0 is satisfied when:

- every core workflow object maps to a defined model;
- ResearchAgent and CriticAgent exchange only contract-compatible structures;
- Supervisor can reconstruct task state from stored entities;
- claims and sources are independently addressable;
- profile approval is auditable;
- revision history can generate REVIEW_PROTOCOL without private reasoning;
- final artifacts are traceable to task_id, workflow_run_id, and source agent runs;
- models can be serialized to JSON without loss of required information.
