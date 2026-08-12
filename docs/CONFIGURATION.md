# CONFIGURATION
Документ визначає правила конфігурації K_Supervisor, пріоритети параметрів, секрети, ліміти та відтворюваність запусків.

Version: 1.0
Status: ACTIVE

## 1. Purpose

This document defines the configuration model for K_Supervisor.

Configuration must support:

- predictable runtime behavior;
- environment separation;
- task-level customization;
- dynamic agent profiles;
- resource and cost controls;
- reproducible workflow runs;
- secure secret handling;
- future provider replacement without redesigning agent logic.

## 2. Configuration Principles

- Configuration is centralized and explicit.
- Secrets are never stored in tracked project files.
- Runtime defaults must be separated from task-specific behavior.
- User-approved CriticProfile values are authoritative for critique behavior within the current task.
- Configuration used by an active task is frozen as a task configuration snapshot.
- Changes to configuration must not silently alter an already running task.
- Agents receive only the configuration fields required for their execution.
- Provider-specific settings must be isolated from domain logic.
- Invalid configuration must fail early with a clear error.

## 3. Configuration Layers

K_Supervisor uses the following logical configuration layers:

```text
SYSTEM INVARIANTS
       |
       v
PROJECT DEFAULTS
       |
       v
ENVIRONMENT CONFIGURATION
       |
       v
TASK CONFIGURATION
       |
       v
USER-APPROVED AGENT PROFILE
       |
       v
EXECUTION SNAPSHOT
```

The layers have different responsibilities and must not be merged into one unrestricted settings object.

## 4. System Invariants

System invariants are mandatory rules that normal configuration cannot override.

Examples:

- required identifiers must be present;
- secrets must not be written to reports or logs;
- CriticAgent cannot start without an APPROVED CriticProfile;
- approved profile changes require a new profile version and user approval;
- private chain-of-thought must not be persisted in review artifacts;
- invalid state transitions are rejected;
- configuration schemas must validate before execution.

System invariants are implemented in code and documented in project specifications.

## 5. Project Defaults

The main tracked runtime configuration file is:

```text
config/settings.yaml
```

It contains non-secret defaults for the project.

Typical sections:

```text
runtime
workflow
agents
models
tools
research
critic
reports
persistence
logging
retry
limits
```

The repository should also provide a safe reference configuration when useful:

```text
config/settings.example.yaml
```

## 6. Environment Configuration

Environment-specific values must not require editing project source code.

Supported environments should initially include:

```text
development
test
production
```

The active environment may be selected through an environment variable or explicit startup parameter.

Example:

```text
K_SUPERVISOR_ENV=development
```

Environment selection may affect:

- log level;
- persistence location;
- provider endpoints;
- test mocks;
- resource limits;
- model configuration;
- debug behavior.

It must not silently weaken system invariants.

## 7. Secrets

Secrets must be stored outside tracked configuration.

Local development may use:

```text
.env
```

The repository may contain only:

```text
.env.example
```

Typical secret variables may include:

```text
OPENAI_API_KEY
SEARCH_API_KEY
DATABASE_URL
```

Actual provider names may vary as tools are added.

Rules:

- `.env` must be excluded by `.gitignore`;
- secret values must never be committed;
- secret values must never be written to FINAL_REPORT or REVIEW_PROTOCOL;
- logs must redact secret-like values;
- missing required secrets must produce an explicit startup or tool error;
- production deployments should use the hosting platform secret manager where available.

## 8. Configuration Precedence

For normal overridable runtime settings, precedence is:

```text
1. System invariants
2. Explicit allowed execution override
3. Task-specific configuration
4. Environment-specific configuration
5. Project defaults
6. Built-in fallback
```

Higher levels override lower levels only when the field is defined as overridable.

CriticProfile is handled separately:

```text
User-approved CriticProfile
    overrides generated CriticProfile draft
    for the current task only.
```

No configuration layer may silently modify an APPROVED CriticProfile.

## 9. Task Configuration

Each task may define operational requirements separate from the user request text.

Suggested TaskConfiguration fields:

```text
language
output_format
max_iterations
max_sources
max_search_calls
timeout_seconds
research_depth
report_detail_level
freshness_requirement
allowed_tools
```

Task configuration is validated before the workflow starts.

Task configuration does not replace CriticProfile.

## 10. CriticProfile Configuration Boundary

CriticProfile controls critique semantics for one task.

It may contain:

```text
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
```

Supervisor generates a DRAFT profile.

The user approves or edits it.

After approval:

```text
profile.status = APPROVED
```

The approved profile is frozen for the current task.

Configuration files may define profile generation defaults, but they must not replace user approval.

## 11. Research Configuration

ResearchAgent defaults may include:

```text
research:
  max_queries
  max_sources
  max_sources_per_query
  prefer_primary_sources
  enable_cross_source_comparison
  capture_publication_date
  capture_access_time
  deduplicate_sources
```

Research configuration controls execution strategy, not factual conclusions.

## 12. Critic Configuration

Global CriticAgent execution defaults may include:

```text
critic:
  max_verification_queries
  require_independent_search
  require_claim_level_review
  default_minimum_cross_checks
  default_confidence_threshold
  stop_on_critical_issue
```

Domain-specific critique criteria belong in CriticProfile rather than hard-coded global configuration.

## 13. Workflow Configuration

Initial workflow settings may include:

```text
workflow:
  max_iterations
  allow_completed_with_limitations
  require_profile_approval
  freeze_task_configuration
  freeze_critic_profile
```

Required MVP defaults should preserve:

```text
require_profile_approval: true
freeze_task_configuration: true
freeze_critic_profile: true
```

## 14. Model Configuration

Model selection must be configurable by role rather than embedded directly in agent source code.

Suggested logical mapping:

```text
models:
  supervisor
  domain_resolver
  research_agent
  critic_agent
  report_generator
```

Each role configuration may include:

```text
provider
model
reasoning_level
temperature
max_output_tokens
timeout_seconds
```

Only supported fields for the selected provider should be passed to the provider adapter.

Model replacement must not change the Agent Interface.

## 15. Tool Configuration

Tools must be configurable independently from agents.

Suggested structure:

```text
tools:
  web_search
  web_fetch
  source_validator
  citation_manager
```

Per-tool configuration may include:

```text
enabled
provider
timeout_seconds
max_calls
retry_policy
rate_limit
```

Agents must not bypass tool limits defined by Supervisor.

## 16. Resource Limits

The system must support explicit limits to prevent uncontrolled execution.

Initial configurable limits should include:

```text
max_iterations
max_agent_runs
max_search_calls
max_fetch_calls
max_sources
max_runtime_seconds
max_output_size
```

Future versions may add:

```text
max_tokens
max_cost_per_task
max_parallel_agents
```

When a limit is reached, Supervisor must create an explicit workflow event and decide whether the task becomes:

```text
COMPLETED_WITH_LIMITATIONS
FAILED
```

according to workflow rules.

## 17. Retry Configuration

Retry behavior must be centralized.

Suggested fields:

```text
retry:
  max_attempts
  initial_delay_seconds
  max_delay_seconds
  backoff_multiplier
  retryable_error_types
```

Retries are appropriate for transient failures such as:

- temporary provider errors;
- network timeouts;
- temporary tool unavailability;
- rate limiting where retry is permitted.

Retries must not hide deterministic validation failures.

## 18. Timeout Configuration

Timeouts should be defined separately for:

```text
agent_execution
web_search
web_fetch
model_request
workflow_total
```

A timeout must produce a structured ErrorRecord.

Timeout handling must not leave the workflow in an undefined state.

## 19. Logging Configuration

Suggested logging settings:

```text
logging:
  level
  format
  directory
  console_enabled
  file_enabled
  include_task_id
  include_run_id
  redact_secrets
```

Required identifiers in operational logs should include when available:

```text
task_id
workflow_run_id
run_id
agent_id
request_id
```

Logs are operational artifacts and must not contain private chain-of-thought.

## 20. Persistence Configuration

Persistence must be selected through configuration rather than agent logic.

Initial options may include:

```text
persistence:
  backend: file
  path: runtime/
```

Later:

```text
persistence:
  backend: sqlite
  path: runtime/k_supervisor.db
```

Agents must not require knowledge of the selected persistence backend.

## 21. Artifact Configuration

Final artifact behavior may be configured through:

```text
reports:
  output_directory
  final_report_enabled
  review_protocol_enabled
  include_sources
  include_limitations
  encoding
```

For research workflow outputs:

```text
encoding: UTF-8
```

File naming must follow PROJECT_FILE_STANDARD.md.

Typical outputs:

```text
<TASK_ID>_FINAL_REPORT.md
<TASK_ID>_REVIEW_PROTOCOL.md
```

## 22. Language Configuration

The user-facing output language may be defined per task.

Example:

```text
language: uk
```

The research source language may differ from the final output language.

The system should not restrict research only to sources written in the output language unless the task explicitly requires it.

## 23. Freshness Configuration

Freshness requirements may be task-specific and domain-specific.

Possible values may include:

```text
ANY
CURRENT_WHERE_RELEVANT
RECENT
STRICT_DATE_RANGE
```

A strict date range should include explicit start and end values.

CriticProfile may strengthen freshness requirements for the current task.

## 24. Risk Level Configuration

Suggested generic risk levels:

```text
LOW
MEDIUM
HIGH
CRITICAL
```

Risk level may influence generated profile defaults such as:

- evidence threshold;
- preferred source hierarchy;
- required cross-check count;
- tolerance for unresolved contradictions;
- freshness strictness.

Risk level must not substitute for domain-specific review criteria.

## 25. Configuration Snapshot

Before autonomous execution starts, Supervisor must create a task configuration snapshot.

The snapshot should include references or resolved values for:

```text
task_id
workflow configuration
agent role configuration
tool limits
model role configuration
approved CriticProfile version
active environment
configuration schema version
created_at
```

Secret values must not be copied into the persisted snapshot.

The snapshot must remain immutable for the active task.

This rule supports reproducibility and auditability.

## 26. Runtime Configuration Changes

Changes to global configuration affect new tasks only by default.

An active task continues using its frozen configuration snapshot.

A running task may receive an explicit amendment only through Supervisor and only for fields that are legally mutable.

A material CriticProfile amendment requires user approval.

## 27. Configuration Validation

Configuration must be validated before use.

Validation includes:

- required fields;
- allowed enum values;
- numeric ranges;
- path validity;
- provider configuration compatibility;
- tool availability;
- positive resource limits;
- profile approval state;
- incompatible setting combinations.

Invalid configuration must fail before launching the affected agent where possible.

## 28. Configuration Schema Version

Configuration must carry a schema version.

Example:

```text
configuration_schema_version: 1
```

Schema changes that break compatibility require an explicit migration or compatibility layer.

## 29. Example settings.yaml Skeleton

```yaml
configuration_schema_version: 1

environment: development

workflow:
  max_iterations: 3
  allow_completed_with_limitations: true
  require_profile_approval: true
  freeze_task_configuration: true
  freeze_critic_profile: true

research:
  max_queries: 10
  max_sources: 30
  prefer_primary_sources: true
  enable_cross_source_comparison: true
  deduplicate_sources: true

critic:
  require_independent_search: true
  require_claim_level_review: true
  default_minimum_cross_checks: 2
  default_confidence_threshold: 0.85

limits:
  max_agent_runs: 20
  max_search_calls: 30
  max_fetch_calls: 60
  max_runtime_seconds: 1800

logging:
  level: INFO
  console_enabled: true
  file_enabled: true
  redact_secrets: true

persistence:
  backend: file
  path: runtime/

reports:
  output_directory: output/
  final_report_enabled: true
  review_protocol_enabled: true
  include_sources: true
  include_limitations: true
  encoding: UTF-8
```

Values in this example are initial defaults only and may be revised during implementation and testing.

## 30. .env.example Skeleton

The tracked `.env.example` should contain variable names only.

Example:

```text
OPENAI_API_KEY=
SEARCH_API_KEY=
K_SUPERVISOR_ENV=development
```

No real credentials are allowed.

## 31. Ownership of Configuration

Supervisor owns resolved workflow configuration.

ProfileManager owns lifecycle management of agent profiles.

Provider adapters own provider-specific parameter translation.

Agents consume validated configuration but do not own global configuration state.

## 32. Audit Requirements

For each task, the system should be able to determine:

- which configuration schema version was used;
- which environment was active;
- which CriticProfile version was approved;
- which model roles were selected;
- which tool limits were active;
- which workflow limits were active.

Audit data must not expose secret values.

## 33. MVP Configuration Boundary

The MVP configuration implementation must support at minimum:

```text
config/settings.yaml
.env
.env.example
environment selection
workflow limits
research limits
critic execution defaults
model role configuration
tool limits
logging configuration
artifact output configuration
configuration validation
immutable task configuration snapshot
```

Advanced centralized configuration services and remote configuration are outside the MVP.

## 34. Acceptance Criteria

CONFIGURATION implementation is compliant when:

- project defaults load from a tracked configuration file;
- secrets load from an untracked source;
- invalid configuration is rejected explicitly;
- user-approved CriticProfile remains authoritative for critique semantics;
- configuration used by an active task is frozen;
- active tasks are not silently changed by later global edits;
- agents receive validated role-specific configuration;
- tool and workflow resource limits are enforceable;
- audit records identify the effective configuration without storing secrets;
- configuration changes do not require rewriting agent business logic.
