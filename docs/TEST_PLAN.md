# TEST_PLAN
План перевірки функціональності, надійності, якості та відтворюваності K_Supervisor.

Version: 1.0
Status: ACTIVE

## 1. Purpose

This document defines the canonical test strategy for K_Supervisor.

The plan verifies that the system:

- follows ARCHITECTURE.md;
- follows AGENT_INTERFACE.md;
- follows DATA_MODELS.md;
- follows RESEARCH_WORKFLOW.md;
- follows CONFIGURATION.md;
- follows PROJECT_FILE_STANDARD.md;
- preserves the mandatory user approval gate for CriticProfile;
- runs the ResearchAgent-CriticAgent loop autonomously after approval;
- produces reproducible and auditable final artifacts.

## 2. Test Objectives

The test program must prove that K_Supervisor can:

- accept a valid user task;
- resolve one or more task domains;
- generate a valid draft CriticProfile;
- stop before autonomous work until the user approves the profile;
- freeze the approved profile for the current task_id;
- launch ResearchAgent with valid structured context;
- launch CriticAgent with the approved profile;
- allow CriticAgent to perform independent verification;
- route PASS and REVISE decisions correctly;
- enforce max_iterations and other configured limits;
- handle recoverable and unrecoverable failures;
- produce FINAL_REPORT and REVIEW_PROTOCOL artifacts;
- preserve traceability through task_id, run_id, state transitions, and artifacts.

## 3. Test Levels

The project uses the following test levels.

### 3.1 Unit Tests

Unit tests validate isolated logic without real external providers where possible.

Initial targets:

```text
DomainResolver
ProfileManager
StateMachine
AgentRegistry
configuration validation
identifier generation
claim-source linking
reliability scoring helpers
artifact naming
serialization and deserialization
```

### 3.2 Contract Tests

Contract tests validate structures defined in AGENT_INTERFACE.md and DATA_MODELS.md.

Required contracts include:

```text
AgentRunRequest
AgentResult
CriticProfile
Task
Claim
Source
CriticReview
WorkflowRun
StateTransition
Artifact
```

Contract tests must reject:

- missing required fields;
- invalid status values;
- invalid identifiers;
- invalid profile state;
- malformed agent results;
- incompatible schema versions.

### 3.3 Integration Tests

Integration tests validate interaction between components.

Initial integration paths:

```text
Supervisor -> DomainResolver
Supervisor -> ProfileManager
Supervisor -> AgentRegistry
Supervisor -> ResearchAgent
Supervisor -> CriticAgent
ResearchAgent -> Tools Layer
CriticAgent -> Tools Layer
Supervisor -> ReportGenerator
Supervisor -> Persistence Layer
```

### 3.4 Workflow Tests

Workflow tests validate state transitions and orchestration behavior.

The primary success path is:

```text
NEW
-> PROFILE_GENERATING
-> PROFILE_REVIEW_REQUIRED
-> PROFILE_APPROVED
-> RESEARCHING
-> DRAFT_READY
-> REVIEWING
-> APPROVED
-> FINALIZING
-> FINALIZED
```

The primary revision path is:

```text
REVIEWING
-> REVISE
-> RESEARCHING
-> DRAFT_READY
-> REVIEWING
```

Exceptional terminal paths include:

```text
FAILED
MAX_ITERATIONS_REACHED
COMPLETED_WITH_LIMITATIONS
```

### 3.5 End-to-End Tests

End-to-end tests validate the complete user-visible workflow with real or staging providers.

A test is successful only when the full task can be traced from input through final artifacts.

## 4. Mandatory Profile Approval Tests

The CriticProfile approval boundary is a critical control and requires dedicated tests.

### TC-PROFILE-001 - Draft profile generation

Expected result:

- Supervisor generates a CriticProfile in DRAFT or REVIEW_REQUIRED state;
- the profile contains domain, evaluation criteria, source requirements, and confidence settings appropriate to the task.

### TC-PROFILE-002 - Execution blocked before approval

Expected result:

- ResearchAgent and CriticAgent autonomous workflow does not start while profile status is not APPROVED.

### TC-PROFILE-003 - User approval

Expected result:

- explicit user approval creates a UserApproval record;
- profile status becomes APPROVED;
- approved profile version is linked to task_id.

### TC-PROFILE-004 - User edit before approval

Expected result:

- user edits create a new profile revision or update the draft according to implementation policy;
- only the final approved profile becomes active.

### TC-PROFILE-005 - Profile freeze

Expected result:

- CriticAgent cannot silently modify the approved profile;
- task execution continues with the approved snapshot.

### TC-PROFILE-006 - Material amendment

Expected result:

- Supervisor detects a material domain or criteria change;
- autonomous execution pauses at a profile review gate;
- the amendment requires user approval before activation.

## 5. Domain Resolver Tests

DomainResolver must be tested with single-domain, multi-domain, and ambiguous tasks.

Required test classes:

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

The list is illustrative, not closed.

### TC-DOMAIN-001 - Single domain

Input example:

```text
Analyze a novel and compare two interpretations.
```

Expected result:

```text
primary_domain = literary_analysis
```

### TC-DOMAIN-002 - Multi-domain

Input example:

```text
Evaluate GNSS monitoring methods for structural deformation of a building.
```

Expected result includes:

```text
geodesy
structural_engineering
```

### TC-DOMAIN-003 - Unknown domain

Expected result:

- resolver does not fail because a predefined profile is absent;
- Supervisor may generate a temporary task-specific profile.

### TC-DOMAIN-004 - Ambiguous domain

Expected result:

- ambiguity is recorded;
- Supervisor chooses a safe resolution path or requests user clarification if internal resolution is not sufficient.

## 6. ResearchAgent Tests

ResearchAgent tests must verify:

- task decomposition;
- search strategy generation;
- source collection;
- duplicate source handling;
- claim extraction;
- claim-source linking;
- uncertainty capture;
- response to structured revision requests;
- output contract compliance.

ResearchAgent must not self-approve the final reliability of its result.

## 7. CriticAgent Tests

CriticAgent tests must verify:

- use of the approved CriticProfile;
- independent search capability;
- source quality assessment;
- freshness checks where required;
- identification of unsupported claims;
- contradiction detection;
- missing-topic detection;
- evidence-conclusion consistency;
- structured PASS or REVISE output;
- reliability score validation;
- no silent profile modification.

## 8. Evidence Tests

Evidence tests validate Claim and Source behavior.

Required checks:

- every key claim has a stable claim_id;
- source_ids reference existing Source entities;
- duplicate sources are normalized according to policy;
- broken source links are recorded explicitly;
- contradictory evidence can coexist without data loss;
- source reliability class is stored independently from prose;
- claim verification status can change across iterations without changing claim_id unless the claim itself changes materially.

## 9. Revision Loop Tests

### TC-LOOP-001 - PASS on first review

Expected result:

```text
REVIEWING -> APPROVED
```

### TC-LOOP-002 - One revision

Expected result:

```text
REVIEWING -> REVISE -> RESEARCHING -> REVIEWING -> APPROVED
```

### TC-LOOP-003 - Multiple revisions

Expected result:

- each revision has an iteration number;
- previous review records remain available;
- new research addresses structured critic feedback.

### TC-LOOP-004 - Max iterations reached

Expected result:

- the system stops further automatic revisions;
- the result is not reported as fully verified solely because the limit was reached;
- final status is MAX_ITERATIONS_REACHED or COMPLETED_WITH_LIMITATIONS according to policy.

## 10. State Machine Tests

Every valid state transition must have a positive test.

Every prohibited transition must have a negative test.

Examples of prohibited transitions:

```text
NEW -> REVIEWING
PROFILE_REVIEW_REQUIRED -> RESEARCHING without approval
FAILED -> FINALIZED without explicit recovery workflow
FINALIZED -> RESEARCHING
```

Each recorded transition must include:

```text
task_id
from_state
to_state
timestamp
reason or trigger
```

## 11. Configuration Tests

Configuration tests must verify:

- settings file parsing;
- environment overrides;
- secret separation;
- configuration precedence;
- invalid values fail early;
- task configuration snapshot creation;
- active task configuration does not change silently after global settings change;
- max_iterations is enforced;
- timeout and retry values are enforced;
- model and tool provider settings are isolated from domain logic.

## 12. Failure and Recovery Tests

The following failures require explicit test coverage:

```text
LLM timeout
web search timeout
web fetch failure
unavailable source
malformed agent output
invalid schema
provider exception
agent exception
duplicate request
persistence failure
artifact write failure
iteration limit exceeded
```

Expected behavior:

- recoverable failures follow configured retry policy;
- retries preserve request identity and audit information;
- unrecoverable failures produce FAILED or another explicit terminal state;
- no failure may silently disappear from the audit trail.

## 13. Idempotency Tests

The system must be safe against accidental duplicate execution where the contract marks an operation as idempotent.

Test cases must verify:

- repeated request_id does not create duplicate logical work when prohibited;
- repeated artifact generation does not create conflicting filenames;
- duplicate state transition requests do not corrupt workflow state;
- retry behavior creates a new run_id only when defined by policy while preserving correlation with the original request.

## 14. Artifact Tests

The initial required user-facing artifacts are:

```text
<TASK_ID>_FINAL_REPORT.md
<TASK_ID>_REVIEW_PROTOCOL.md
```

Tests must verify:

- filenames follow PROJECT_FILE_STANDARD.md;
- output encoding is UTF-8;
- FINAL_REPORT contains the consolidated result and limitations;
- REVIEW_PROTOCOL contains iteration and improvement history;
- review protocol does not expose private chain-of-thought;
- artifacts reference the correct task_id;
- final task status is represented consistently in both artifacts.

## 15. Documentation Compliance Tests

Documentation checks should verify:

- documentation filenames use ASCII;
- documentation body uses ASCII except for the single approved Ukrainian description line after the top-level title;
- reports and analyses use UTF-8 by default;
- no ambiguous version suffixes such as final2, new, latest, fixed, or copy are introduced;
- stable project documents rely on Git history instead of unnecessary filename versions.

A lightweight automated documentation linter is recommended after the MVP.

## 16. Security and Secret Tests

Tests must verify:

- API keys are not present in tracked files;
- .env is ignored by Git;
- logs do not expose secrets;
- error messages do not expose credentials;
- agent payloads contain only required secret-independent configuration;
- committed test fixtures contain fake credentials only.

## 17. Auditability Tests

For every completed or failed task, the system should be able to reconstruct:

```text
user task
approved CriticProfile
configuration snapshot
workflow states
agent runs
research iterations
critic reviews
claims and sources
final artifacts
errors and warnings
```

The audit trail must not require private chain-of-thought.

## 18. Determinism and Reproducibility

LLM and web research cannot be assumed to be fully deterministic.

Testing therefore separates:

- structural reproducibility;
- content reproducibility.

Structural reproducibility requires that the same valid inputs follow the same control rules, contracts, state boundaries, and artifact rules.

Content reproducibility may vary because external information, provider behavior, and model outputs can change.

Each task should preserve enough metadata to explain relevant runtime conditions.

## 19. Quality Evaluation

End-to-end quality tests should score at least:

```text
coverage
source quality
claim support
contradiction handling
freshness where relevant
critic usefulness
revision effectiveness
final report consistency
```

Quality thresholds may vary by CriticProfile and task risk level.

A high-risk profile may require stronger evidence rules than a low-risk literary interpretation task.

## 20. Initial End-to-End Scenario Set

Before the MVP is accepted, at least three substantially different domains must be tested.

Recommended initial scenario set:

```text
Scenario A - literary analysis
Scenario B - technical geodesy or construction research
Scenario C - high-evidence medical knowledge review
```

At least one scenario must trigger REVISE before PASS.

At least one scenario must exercise a multi-domain CriticProfile.

At least one scenario must exercise a failure or limitation path.

## 21. MVP Acceptance Criteria

The MVP is accepted only when all critical requirements below are demonstrated:

- repository bootstrap is complete;
- core contracts validate;
- state machine valid and invalid transitions are tested;
- CriticProfile generation works;
- user approval is mandatory and enforced;
- approved profile is frozen for the task;
- ResearchAgent completes a structured research run;
- CriticAgent independently reviews the result;
- PASS path works;
- REVISE path works;
- max_iterations path works;
- final artifacts are generated correctly;
- errors are recorded explicitly;
- secrets are excluded from tracked content;
- three end-to-end domain scenarios pass the defined acceptance conditions.

## 22. Test Automation

The preferred automation sequence is:

```text
unit tests
-> contract tests
-> integration tests
-> workflow tests
-> selected end-to-end tests
```

Fast deterministic tests should run on every relevant commit.

Provider-dependent or cost-bearing end-to-end tests may run separately according to CI policy.

## 23. Test Data Rules

Test data must:

- avoid real secrets;
- avoid unnecessary personal data;
- identify synthetic fixtures clearly;
- preserve stable IDs where deterministic fixtures are required;
- separate expected valid and invalid cases;
- allow provider-independent testing through mocks or stubs where practical.

## 24. Regression Policy

Every confirmed defect should result in a regression test when technically practical.

A regression test should reproduce the failed behavior before the fix and remain in the suite after the fix.

Changes to ARCHITECTURE.md, AGENT_INTERFACE.md, DATA_MODELS.md, RESEARCH_WORKFLOW.md, or CONFIGURATION.md must trigger a review of affected tests.

## 25. Test Status Classification

Recommended result values:

```text
PASS
FAIL
SKIPPED
BLOCKED
EXPECTED_FAILURE
```

Production readiness must not count SKIPPED or BLOCKED critical tests as PASS.

## 26. Traceability

Critical requirements should be traceable to one or more test cases.

Recommended naming:

```text
TC-<AREA>-<NUMBER>
```

Examples:

```text
TC-PROFILE-001
TC-DOMAIN-002
TC-LOOP-004
TC-CONFIG-003
TC-ARTIFACT-002
```

Future implementation may maintain a machine-readable requirements-to-tests matrix.

## 27. Planned Test Structure

Recommended repository layout:

```text
tests/
|-- unit/
|-- contracts/
|-- integration/
|-- workflow/
|-- e2e/
|-- fixtures/
`-- conftest.py
```

The exact Python test framework is an implementation decision, but pytest is the default candidate unless a later project decision changes it.

## 28. Exit Rule

A development phase may be marked complete only when:

- its defined tests exist;
- critical tests pass;
- known limitations are documented;
- no unresolved critical defect is hidden by retries, skips, or manual intervention.

MVP completion additionally requires the end-to-end acceptance criteria in this document.