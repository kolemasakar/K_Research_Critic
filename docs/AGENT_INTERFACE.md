# AGENT_INTERFACE
Універсальний контракт взаємодії Supervisor з агентами та правила їх виконання в K_Supervisor.

Version: 1.0
Status: ACTIVE

## 1. Purpose

This document defines the common logical interface used by Supervisor to discover, configure, execute, monitor, and receive results from agents.

The interface is domain-neutral. Domain behavior is supplied through task context and approved profiles instead of hard-coded domain agent classes.

## 2. Core Rule

All executable agents must follow one common contract:

```text
run(request) -> AgentResult
```

The logical model is:

```text
Agent = generic capability + task context + approved profile
```

An agent must not depend on direct knowledge of Supervisor internals.

## 3. Scope

This interface applies to executable components registered in AgentRegistry, including initially:

```text
ResearchAgent
CriticAgent
ReportGenerator
```

Future agents may include:

```text
FactCheckAgent
DataAnalysisAgent
TechnicalAgent
FinancialAgent
LegalAgent
PlanningAgent
```

A component may use a specialized internal implementation as long as its external contract remains compatible.

## 4. Agent Identity

Every registered agent must expose stable identity metadata:

```text
agent_id
agent_type
agent_version
capabilities[]
status
```

Rules:

- agent_id uniquely identifies the registered implementation;
- agent_type identifies its logical role;
- agent_version identifies interface-relevant implementation version;
- capabilities declares functions available to Supervisor;
- status indicates whether the agent may currently accept work.

Example:

```json
{
  "agent_id": "critic.default",
  "agent_type": "CRITIC",
  "agent_version": "1.0",
  "capabilities": ["independent_review", "web_verification", "source_assessment"],
  "status": "AVAILABLE"
}
```

## 5. Agent Registry Contract

AgentRegistry must allow Supervisor to:

```text
register(agent)
get(agent_id)
find_by_type(agent_type)
find_by_capability(capability)
list_available()
```

Workflow logic should select agents by declared type or capability rather than importing concrete implementations directly.

## 6. AgentRunRequest

Supervisor invokes an agent through a structured request envelope.

Required fields:

```text
request_id
task_id
run_id
agent_id
agent_type
operation
input
context
profile
limits
metadata
```

Recommended logical schema:

```json
{
  "request_id": "REQ_000001",
  "task_id": "TASK_000001",
  "run_id": "RUN_000001",
  "agent_id": "critic.default",
  "agent_type": "CRITIC",
  "operation": "review",
  "input": {},
  "context": {},
  "profile": {},
  "limits": {},
  "metadata": {}
}
```

## 7. Identifier Rules

The following identifiers must remain stable within one execution record:

```text
task_id
run_id
request_id
```

Definitions:

- task_id identifies the user task across the complete workflow;
- run_id identifies one agent execution attempt;
- request_id identifies one invocation request.

A retry must receive a new run_id unless the retry mechanism explicitly guarantees idempotent continuation of the same run.

## 8. Input

The `input` object contains data that the agent is expected to process directly.

Examples:

ResearchAgent:

```text
topic
requirements
previous_review
```

CriticAgent:

```text
draft_report
claims
sources
previous_reviews
```

ReportGenerator:

```text
approved_findings
claims
sources
review_history
final_status
```

The interface must not require all agents to share the same input fields.

## 9. Context

The `context` object contains workflow information that may influence execution but is not the primary work payload.

Typical fields:

```text
iteration
workflow_state
language
created_at
prior_run_ids[]
related_artifacts[]
```

Agents must treat context as read-only unless their contract explicitly defines an output that proposes context changes.

## 10. Profile

The `profile` object dynamically configures task or domain behavior.

For CriticAgent, the profile must be the user-approved CriticProfile for the current task.

CriticAgent must not modify approved profile fields during execution.

Typical CriticProfile fields:

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

If no profile is required for an agent or operation, `profile` may be an empty object.

## 11. Profile Approval Boundary

The following rule is mandatory for CriticAgent:

```text
CriticProfile.status == APPROVED
```

Supervisor must not invoke normal CriticAgent review when the profile is still:

```text
DRAFT
REVIEW_REQUIRED
REJECTED
```

If a material profile amendment is required, execution returns to the profile approval workflow before critique continues.

## 12. Limits

Supervisor may provide execution limits such as:

```text
max_tool_calls
max_sources
timeout_seconds
max_tokens
max_retries
```

Agents must respect supplied hard limits.

If a limit prevents completion, the agent must return an explicit limitation or error instead of silently ignoring the limit.

## 13. Tool Access

Agents must use capabilities supplied through the Tools Layer.

An agent should request tools by logical capability, for example:

```text
web_search
web_fetch
source_validator
citation_manager
```

Agents should not embed provider-specific external API calls directly into domain logic when a project tool abstraction exists.

Tool failures must be represented in the AgentResult or error details when they materially affect the result.

## 14. AgentResult

Every execution returns a structured result envelope.

Required fields:

```text
run_id
task_id
agent_id
status
result
errors
warnings
metrics
metadata
```

Recommended logical schema:

```json
{
  "run_id": "RUN_000001",
  "task_id": "TASK_000001",
  "agent_id": "critic.default",
  "status": "SUCCEEDED",
  "result": {},
  "errors": [],
  "warnings": [],
  "metrics": {},
  "metadata": {}
}
```

## 15. Execution Status

Common execution states:

```text
PENDING
RUNNING
SUCCEEDED
FAILED
PARTIAL
CANCELLED
```

Meaning:

- SUCCEEDED: contractually complete result was produced;
- FAILED: usable contract result could not be produced;
- PARTIAL: some useful result exists but execution was incomplete;
- CANCELLED: Supervisor or policy ended execution before completion.

Workflow decisions such as PASS or REVISE belong inside the domain result, not in the generic execution status.

Example:

```text
status: SUCCEEDED
result.decision: REVISE
```

## 16. CriticAgent Result

CriticAgent must return at least:

```text
decision
reliability_score
critical_issues[]
unsupported_claims[]
weak_sources[]
contradictions[]
missing_topics[]
recommended_changes[]
```

Example:

```json
{
  "decision": "REVISE",
  "reliability_score": 0.82,
  "critical_issues": [],
  "unsupported_claims": [],
  "weak_sources": [],
  "contradictions": [],
  "missing_topics": [],
  "recommended_changes": []
}
```

Allowed decisions for the initial workflow:

```text
PASS
REVISE
```

A failed execution must use generic status FAILED rather than inventing a third review decision.

## 17. ResearchAgent Result

ResearchAgent should return structured research output instead of only final prose.

Minimum logical fields:

```text
summary
findings[]
claims[]
sources[]
uncertainties[]
draft_report
changes_applied[]
```

On revision cycles, `changes_applied` should identify how the previous CriticAgent recommendations were addressed.

## 18. ReportGenerator Result

ReportGenerator should return artifact metadata:

```text
artifacts[]
final_status
```

Each artifact record should include:

```text
artifact_type
path
encoding
created_at
```

Initial artifact types:

```text
FINAL_REPORT
REVIEW_PROTOCOL
```

## 19. Errors

Errors must be structured and machine-readable.

Recommended fields:

```text
code
message
retryable
source
context
```

Example:

```json
{
  "code": "TOOL_TIMEOUT",
  "message": "Web search did not complete within the configured timeout.",
  "retryable": true,
  "source": "web_search",
  "context": {}
}
```

Do not encode normal review findings as generic errors.

## 20. Warnings

Warnings represent non-fatal limitations such as:

```text
insufficient_source_diversity
stale_source_detected
partial_tool_failure
confidence_below_target
```

Warnings must not change execution status to FAILED unless the agent cannot satisfy its required contract.

## 21. Metrics

Agents should expose execution metrics where available.

Typical fields:

```text
duration_ms
model_calls
tool_calls
sources_used
tokens_input
tokens_output
estimated_cost
```

Metrics are operational data and must not be mixed into the substantive research or critique result.

## 22. Deterministic Validation

Before Supervisor accepts an AgentResult, it should validate:

- required envelope fields exist;
- task_id matches the active task;
- run_id matches the expected run;
- agent_id matches the invoked agent;
- status uses an allowed value;
- required role-specific result fields exist;
- CriticProfile is approved where required;
- result is structurally parseable.

Malformed results must not be treated as successful workflow decisions.

## 23. Retry Rules

Retry behavior is controlled by Supervisor policy.

An agent may indicate whether an error is retryable, but it must not independently create uncontrolled retry loops.

Supervisor decides:

```text
retry
route_to_alternative_agent
continue_with_limitation
fail_task
```

Retries must remain auditable through run_id and metadata.

## 24. Idempotency

Agents should avoid duplicate side effects when the same logical request is retried.

Any agent that writes artifacts or external state must support one of:

```text
idempotent operation by request_id
explicit duplicate detection
Supervisor-controlled unique output path
```

Duplicate artifacts must not be silently created during retries.

## 25. User Interaction Rule

Agents do not directly ask the user for routine workflow decisions.

User interaction is mediated by Supervisor.

Critic profile approval is handled by Supervisor before CriticAgent execution.

If an agent detects an ambiguity that cannot be resolved internally, it returns a structured request for Supervisor action rather than addressing the user directly.

## 26. Security and Secrets

Agents must not expose secrets in results, logs, reports, or errors.

Secrets must not be passed inside normal profile or task text when a secure configuration mechanism is available.

Tool credentials belong to configuration or secret management, not agent-generated artifacts.

## 27. Logging and Audit

Every agent run should be traceable by:

```text
task_id
run_id
agent_id
operation
start_time
end_time
status
```

Audit records should store decisions and structured outputs needed to reconstruct workflow progress.

Private chain-of-thought or hidden model reasoning must not be persisted as an audit requirement.

## 28. Backward Compatibility

Changes that modify required request or response fields are interface changes.

Compatible additions may extend optional fields without changing the major interface version.

Breaking changes require an explicit interface version decision and migration plan.

## 29. Initial Python Shape

The initial Python implementation may follow this logical shape:

```python
class Agent:
    agent_id: str
    agent_type: str
    agent_version: str
    capabilities: list[str]

    def run(self, request: AgentRunRequest) -> AgentResult:
        raise NotImplementedError
```

Concrete agents implement the same boundary:

```text
ResearchAgent(Agent)
CriticAgent(Agent)
ReportGenerator(Agent)
```

The exact Python classes and validation library may be selected during implementation without changing this logical contract.

## 30. Acceptance Criteria

An agent implementation complies with AGENT_INTERFACE when:

- it is discoverable through AgentRegistry;
- it declares stable identity and capabilities;
- it accepts a structured AgentRunRequest;
- it returns a structured AgentResult;
- it preserves task_id and run_id correctly;
- it respects profiles and execution limits;
- it exposes failures explicitly;
- it does not create uncontrolled retries;
- it does not directly bypass the Supervisor interaction boundary;
- it can be replaced by another compatible implementation without changing unrelated workflow components.

## 31. Decision Summary

The approved interface foundation is:

- one common logical execution contract for all agents;
- dynamic task/domain profiles instead of domain-specific hard-coded agent classes;
- Supervisor-controlled invocation, retries, user interaction, and workflow decisions;
- structured request and result envelopes;
- role-specific result payloads inside a generic execution envelope;
- mandatory approved CriticProfile for CriticAgent review;
- tool access through the Tools Layer;
- explicit errors, warnings, metrics, and audit identifiers;
- extensibility without coupling Supervisor to concrete agent implementations.
