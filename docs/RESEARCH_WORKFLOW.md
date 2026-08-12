# RESEARCH_WORKFLOW
Опис повного циклу дослідження, погодження профілю критика, автономної перевірки та фіналізації результатів у K_Supervisor.

Version: 1.0
Status: ACTIVE

## 1. Purpose

This document defines the canonical end-to-end research workflow for K_Supervisor.

The workflow begins when a user submits a research task and ends when Supervisor produces the final report and review protocol.

The workflow is designed around one mandatory human control point: approval of the task-specific CriticProfile before autonomous ResearchAgent and CriticAgent execution begins.

## 2. Core Workflow Rule

The required control model is:

```text
User defines the task.
Supervisor analyzes the task.
Supervisor proposes the CriticProfile.
User approves or edits the CriticProfile.
Supervisor freezes the approved profile.
ResearchAgent performs research.
CriticAgent independently verifies and critiques.
Supervisor controls revision cycles.
ReportGenerator produces final artifacts.
```

After CriticProfile approval, normal ResearchAgent and CriticAgent interaction is autonomous.

## 3. Primary Actors

The initial workflow uses:

```text
User
Supervisor
DomainResolver
ProfileManager
ResearchAgent
CriticAgent
Tools Layer
Evidence Layer
ReportGenerator
```

Each component must follow ARCHITECTURE.md, AGENT_INTERFACE.md, and DATA_MODELS.md.

## 4. Workflow State Model

The canonical workflow states are:

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
COMPLETED_WITH_LIMITATIONS
FAILED
MAX_ITERATIONS_REACHED
```

All state changes must be recorded as StateTransition entities.

## 5. Stage 1 - Task Intake

Input:

```text
user_task
optional_constraints
optional_output_requirements
optional_user_domain_requirements
```

Supervisor must:

- create task_id;
- preserve the original user request unchanged;
- normalize task metadata without silently changing task meaning;
- identify missing information that can be resolved internally;
- avoid asking the user for information unless the task cannot be interpreted reliably without it;
- transition the task from NEW to PROFILE_GENERATING.

The original user task remains the authoritative task source throughout the workflow.

## 6. Stage 2 - Domain Assessment

DomainResolver analyzes the task before research begins.

The DomainAssessment should identify:

```text
primary_domain
secondary_domains[]
task_type
risk_level
likely_source_classes[]
likely_standards[]
freshness_requirement
special_verification_needs[]
```

Examples of supported domains may include:

```text
literary_analysis
medicine
geodesy
construction
military
finance
law
software_engineering
science
history
```

The domain list is open and must not be hard-coded as a closed enumeration.

Multi-domain classification is allowed and expected when required by the task.

## 7. Stage 3 - CriticProfile Generation

ProfileManager generates a draft CriticProfile from:

```text
user_task
DomainAssessment
system defaults
project configuration
user-provided requirements
```

The draft profile must define at least:

```text
profile_id
profile_version
domain
subdomains
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
status
```

The generated profile status must be REVIEW_REQUIRED before user approval.

## 8. Stage 4 - Mandatory User Profile Review

Supervisor presents the draft CriticProfile to the user before research begins.

The user may:

- approve the profile unchanged;
- add evaluation criteria;
- remove evaluation criteria;
- modify evaluation criteria;
- add or remove domains or subdomains;
- modify source hierarchy;
- specify standards or normative documents;
- modify freshness requirements;
- modify evidence requirements;
- modify confidence threshold;
- modify risk level;
- add special requirements.

Supervisor must not start autonomous research before an approval record exists.

The approved control rule is:

```text
Supervisor proposes.
User approves or edits.
Critic executes.
```

## 9. Stage 5 - Profile Approval and Freeze

When the user approves the profile, Supervisor must:

- create a UserApproval record;
- set CriticProfile status to APPROVED;
- preserve the approved profile version;
- bind the profile to task_id;
- prevent CriticAgent from modifying the profile;
- transition the task to PROFILE_APPROVED.

The approved profile is immutable for the active task unless a formal amendment is approved.

## 10. Material Profile Amendment

A material amendment may be required if research reveals that the approved critic scope is insufficient.

Examples:

- a new major domain becomes central to the task;
- a mandatory standard becomes relevant;
- the risk level materially changes;
- evidence requirements must change;
- the original profile would produce a misleading review.

In such a case Supervisor must:

```text
1. stop normal autonomous progression;
2. create a new draft profile version;
3. explain the proposed amendment to the user;
4. request user approval;
5. preserve the previous approved version;
6. activate the new version only after approval.
```

CriticAgent must not make this change independently.

Non-material operational changes, such as retrying a failed web request, do not require profile amendment.

## 11. Stage 6 - Research Planning

After PROFILE_APPROVED, Supervisor launches ResearchAgent.

ResearchAgent creates a research plan based on:

```text
user_task
approved CriticProfile
DomainAssessment
available tools
resource limits
previous revision feedback if any
```

The plan should include:

- task decomposition;
- search questions;
- source priorities;
- expected evidence types;
- known uncertainty areas;
- domain-specific research constraints.

ResearchAgent should prioritize authoritative evidence appropriate to the domain.

## 12. Stage 7 - Source Discovery and Collection

ResearchAgent uses the Tools Layer to discover and retrieve evidence.

ResearchAgent must:

- record each relevant source as a Source entity;
- preserve source URL or equivalent stable locator;
- capture publisher or authority when available;
- capture publication date when relevant;
- capture access time;
- classify source type;
- avoid duplicate sources;
- distinguish primary and secondary sources;
- flag inaccessible or incomplete sources;
- respect freshness requirements from CriticProfile.

Search results alone are not evidence unless the underlying source content supports the claim.

## 13. Stage 8 - Claim Extraction

ResearchAgent must separate factual or evaluative claims from final prose.

Each significant claim should include:

```text
claim_id
claim_text
source_ids[]
confidence
verification_status
notes
```

Important claims should be linked to evidence before the draft is considered complete.

Unsupported claims may exist temporarily during research but must be explicitly marked.

## 14. Stage 9 - Draft Research Result

ResearchAgent produces a ResearchResult containing at least:

```text
summary
key_findings[]
claims[]
sources[]
uncertainties[]
conflicting_evidence[]
limitations[]
draft_report
```

The output must follow AGENT_INTERFACE.md.

When ResearchAgent finishes successfully, Supervisor transitions:

```text
RESEARCHING -> DRAFT_READY
```

## 15. Stage 10 - Independent Critic Review

Supervisor launches CriticAgent with:

```text
original user task
approved CriticProfile
ResearchResult
claim set
source set
current iteration number
relevant workflow context
```

CriticAgent must perform independent verification rather than only reviewing wording.

Depending on the approved profile, CriticAgent should verify:

- factual correctness;
- source authority;
- primary source availability;
- source freshness;
- cross-source agreement;
- unsupported claims;
- contradictions;
- methodological validity;
- completeness;
- domain standards;
- uncertainty handling;
- whether conclusions follow from evidence.

CriticAgent may use the Tools Layer independently from ResearchAgent.

## 16. Critic Decision

CriticAgent returns a CriticReview containing at least:

```text
decision
reliability_score
critical_issues[]
unsupported_claims[]
weak_sources[]
contradictions[]
missing_topics[]
recommended_changes[]
unresolved_uncertainties[]
```

Decision values:

```text
PASS
REVISE
```

PASS means the result satisfies the approved CriticProfile and configured acceptance criteria.

REVISE means one or more required corrections remain.

## 17. Revision Loop

For REVISE, Supervisor must create a Revision record and return structured feedback to ResearchAgent.

The revision request should contain only actionable review outputs needed for correction.

ResearchAgent must:

- address each critical issue;
- improve or replace weak evidence where possible;
- resolve unsupported claims;
- investigate contradictions;
- add missing required topics;
- preserve unresolved uncertainty when evidence is insufficient;
- record the changes made.

The canonical loop is:

```text
RESEARCHING
   |
   v
DRAFT_READY
   |
   v
REVIEWING
   |
   +-- PASS --> APPROVED
   |
   +-- REVISE --> REVISE_REQUIRED
                     |
                     v
                 RESEARCHING
```

Normal revision loops must not require user involvement.

## 18. Iteration Control

Supervisor controls the iteration number.

Configuration should define:

```text
max_iterations
minimum_reliability_score
```

Each review cycle must increment the iteration counter exactly once.

Supervisor must prevent uncontrolled loops.

Repeated CriticAgent feedback with no material improvement should be detected and recorded.

## 19. Acceptance Rules

A task may reach APPROVED only when all configured acceptance criteria are satisfied.

Typical criteria:

- CriticAgent decision is PASS;
- no unresolved critical issue remains;
- reliability_score meets or exceeds the configured threshold;
- required evidence is present;
- approved profile requirements are satisfied;
- required source cross-checks are complete;
- important contradictions are resolved or explicitly documented.

Domain-specific rules from CriticProfile take precedence over generic defaults where they are stricter.

## 20. Maximum Iteration Handling

If max_iterations is reached before PASS, Supervisor must not silently treat the task as approved.

The task enters:

```text
MAX_ITERATIONS_REACHED
```

Supervisor then evaluates whether useful output exists.

If a usable result exists but important limitations remain, final status may become:

```text
COMPLETED_WITH_LIMITATIONS
```

The final report must clearly identify unresolved limitations.

If no reliable usable result exists, the task must end as FAILED.

## 21. High-Risk Domain Behavior

CriticProfile may classify a task as HIGH risk.

Examples may include medical, legal, financial, structural safety, or other domains where incorrect information may cause material harm.

For HIGH risk tasks, the profile should normally require stricter evidence and verification rules, such as:

- stronger source hierarchy;
- current authoritative sources;
- explicit uncertainty reporting;
- additional independent cross-checks;
- higher confidence threshold;
- stronger treatment of conflicting evidence.

The exact rules remain task-specific and are subject to user approval through CriticProfile.

## 22. Conflicting Evidence

Conflicting evidence must not be hidden by ResearchAgent or CriticAgent.

When credible sources disagree, the workflow should:

- identify the conflicting claims;
- record the relevant sources;
- compare source authority and recency;
- identify whether the conflict can be resolved;
- preserve unresolved disagreement in the final result;
- prevent false certainty.

CriticAgent should explicitly evaluate significant unresolved conflicts.

## 23. Uncertainty Handling

The system must distinguish:

```text
verified information
probable information
uncertain information
unsupported information
conflicting information
```

A lack of evidence must not be converted into a confident conclusion.

Final artifacts should preserve material uncertainty discovered during the workflow.

## 24. Stage 11 - Finalization

When the task reaches APPROVED or COMPLETED_WITH_LIMITATIONS, Supervisor launches ReportGenerator.

ReportGenerator receives:

```text
original user task
approved CriticProfile
final ResearchResult
final CriticReview
revision history
source set
claim set
final task status
```

ReportGenerator must not independently change verified conclusions without generating a new review requirement.

## 25. Final Artifacts

The initial workflow produces two user-facing UTF-8 artifacts:

```text
<TASK_ID>_FINAL_REPORT.md
<TASK_ID>_REVIEW_PROTOCOL.md
```

FINAL_REPORT should include:

- executive summary;
- scope;
- key findings;
- detailed analysis;
- important evidence;
- conflicting evidence where relevant;
- uncertainties and limitations;
- conclusions;
- source references.

REVIEW_PROTOCOL should include:

- task_id;
- approved critic profile summary;
- iteration count;
- critic decision history;
- significant issues found;
- significant improvements made;
- unresolved limitations;
- final reliability score;
- final status.

The protocol must not include private chain-of-thought or hidden model reasoning.

## 26. Failure Handling

Supervisor must classify failures as recoverable or unrecoverable.

Recoverable examples:

```text
temporary web failure
LLM timeout
rate limit
single unavailable source
malformed retryable tool response
```

Unrecoverable examples may include:

```text
invalid task state
persistent contract violation
missing mandatory approved profile
irrecoverable agent failure
insufficient evidence for any useful result
```

Recoverable failures should follow configured retry policy.

Unrecoverable failures must transition the task to FAILED and create an ErrorRecord.

## 27. Retry and Idempotency

Retries must not create duplicate logical work products.

Supervisor should preserve:

```text
task_id
request_id
iteration
agent identity
```

A retry may receive a new run_id but must remain linked to the same logical request.

Duplicate claims, sources, reviews, and artifacts should be detected where practical.

## 28. Audit Requirements

The workflow must preserve enough structured information to reconstruct what happened without exposing private chain-of-thought.

Minimum audit data:

```text
task metadata
DomainAssessment
CriticProfile versions
UserApproval records
agent runs
state transitions
claims
sources
critic reviews
revision records
errors
warnings
final artifacts
```

## 29. Autonomous Boundary

User interaction is mandatory for initial CriticProfile approval.

After approval, the workflow is autonomous until one of the following occurs:

```text
finalization
material profile amendment request
unrecoverable ambiguity
explicit user cancellation
```

Supervisor must not request user confirmation for routine internal Research-Critic iterations.

## 30. Cancellation

A future implementation may support explicit user cancellation.

Cancellation should:

- stop new agent execution;
- preserve completed audit records;
- avoid producing an artifact labeled as approved;
- record a terminal cancellation state if implemented.

A cancellation state is not required for the initial MVP unless explicitly added to the state model.

## 31. Resource Controls

Supervisor should enforce configured limits for:

```text
max_iterations
max_sources
max_search_calls
max_agent_calls
timeouts
cost limits
```

Resource limits must not silently convert incomplete work into PASS.

If a resource limit prevents completion, the limitation must be recorded.

## 32. Minimal MVP Sequence

The minimum end-to-end MVP sequence is:

```text
1. receive task;
2. create task_id;
3. resolve domain;
4. generate CriticProfile;
5. obtain user approval;
6. freeze profile;
7. run ResearchAgent;
8. run CriticAgent;
9. revise until PASS or limit;
10. generate FINAL_REPORT;
11. generate REVIEW_PROTOCOL;
12. finalize task status.
```

## 33. Acceptance Criteria for Workflow Implementation

The workflow implementation is compliant when:

- research cannot start before approved CriticProfile exists;
- user edits to CriticProfile are preserved;
- approved profile versions are immutable;
- ResearchAgent and CriticAgent can operate autonomously after approval;
- CriticAgent can use independent evidence collection;
- each significant claim can reference evidence;
- REVISE feedback can be routed back to ResearchAgent;
- iteration limits are enforced;
- PASS cannot bypass configured acceptance criteria;
- maximum iteration handling does not imply false approval;
- final report and review protocol can be generated;
- state transitions and agent runs are auditable;
- private chain-of-thought is not stored in the review protocol.

## 34. Related Documents

```text
PROJECT_FILE_STANDARD.md
ARCHITECTURE.md
ROADMAP.md
AGENT_INTERFACE.md
DATA_MODELS.md
CONFIGURATION.md
TEST_PLAN.md
```
