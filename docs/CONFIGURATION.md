# CONFIGURATION
Документ визначає конфігурацію K_Supervisor для GPT Store-first продукту та optional standalone/API runtime.

Version: 1.1
Status: ACTIVE

## 1. Purpose

K_Supervisor configuration must support predictable runtime behavior, explicit approval boundaries, reproducibility, provider isolation, resource controls, and two deployment profiles without making the free GPT Store edition depend on developer secrets.

## 2. Configuration Principles

- Configuration is centralized and explicit.
- System invariants cannot be weakened by normal settings.
- User-approved CriticProfile values are authoritative for critique behavior.
- Active task configuration is frozen and auditable.
- Provider-specific settings remain outside agent business logic.
- Invalid configuration fails early.
- GPT Store Edition must not require a developer API key or mandatory external backend.
- Standalone/API provider secrets remain optional and untracked.
- No named ChatGPT model is a core workflow dependency.

## 3. Configuration Layers

```text
SYSTEM INVARIANTS
       |
       v
PRODUCT DISTRIBUTION POLICY
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
USER-APPROVED CRITIC PROFILE
       |
       v
EXECUTION SNAPSHOT
```

## 4. Product Distribution Policy

Tracked configuration includes a `distribution` section.

Primary defaults:

```yaml
distribution:
  primary_channel: chatgpt_store
  free_user_compatible: true
  developer_api_key_required: false
  model_policy: user_plan
  recommended_model: null
  allow_user_model_switch: true
  external_backend_required: false
```

For `primary_channel: chatgpt_store`, these values are treated as configuration invariants.

`recommended_model: null` means K_Supervisor does not pin a model identifier. ChatGPT supplies a model available to the current user, and users may switch when their plan exposes additional choices.

The detailed product policy is defined in `GPT_STORE_DEPLOYMENT.md`.

## 5. System Invariants

System invariants include:

- CriticAgent cannot start without an APPROVED CriticProfile;
- approved profile changes require a new version and user approval;
- workflow state transitions must validate;
- hidden chain-of-thought/private reasoning must not be persisted;
- task configuration is frozen before autonomous execution;
- secret values must not enter reports, snapshots, or logs;
- GPT Store Edition cannot require a developer API key;
- GPT Store Edition cannot require an external backend;
- GPT Store Edition uses `model_policy: user_plan`;
- GPT Store Edition allows user model switching when available;
- GPT Store Edition does not pin `recommended_model`.

## 6. Project Defaults

Tracked defaults live in:

```text
config/settings.yaml
```

Main sections:

```text
runtime
distribution
workflow
agents
models
resolver
tools
research
critic
reports
persistence
logging
retry
limits
```

## 7. Environments

Supported environments:

```text
development
test
production
```

The environment may be selected with:

```text
K_SUPERVISOR_ENV=development
```

Environment changes must not weaken system invariants.

## 8. Secrets

### GPT Store Edition

No developer-owned secret is required for the core public GPT Store experience.

The Store edition does not require:

```text
OPENAI_API_KEY
SEARCH_API_KEY
DATABASE_URL
```

### Standalone/API Edition

Optional standalone/server integrations may use `.env` or a platform secret manager.

Typical optional variables:

```text
OPENAI_API_KEY
SEARCH_API_KEY
DATABASE_URL
```

Rules:

- `.env` is untracked;
- secrets are never committed;
- secrets are never copied into TaskConfigurationSnapshot;
- secrets are never written to FINAL_REPORT or REVIEW_PROTOCOL;
- operational logs must redact secret-like values;
- a missing secret is an error only when a selected standalone provider explicitly requires it.

## 9. Configuration Precedence

For legally overridable runtime settings:

```text
1. System invariants
2. Explicit allowed execution override
3. Frozen task configuration
4. Environment configuration
5. Project defaults
6. Built-in fallback
```

CriticProfile is separate. A user-approved profile overrides generated draft values for that task only, and no configuration layer may silently modify it.

## 10. Task Configuration

Task-level operational settings may include language, output format, max_iterations, source/search limits, timeout, allowed tools, and report detail.

Task configuration does not replace CriticProfile.

## 11. CriticProfile Boundary

CriticProfile controls critique semantics for one task and includes domain, subdomains, task type, risk level, critic role, evaluation criteria, preferred source types, required cross-checks, standards, evidence level, freshness requirement, confidence threshold, and special user requirements.

Supervisor generates a draft. The user approves or edits it. Approved profile content is frozen.

## 12. Research Configuration

Current research settings include:

```text
max_queries
max_sources
max_sources_per_query
prefer_primary_sources
enable_cross_source_comparison
capture_publication_date
capture_access_time
deduplicate_sources
```

## 13. Critic Configuration

Current critic settings include:

```text
max_verification_queries
max_verification_sources_per_claim
require_independent_search
require_claim_level_review
default_minimum_cross_checks
default_confidence_threshold
stop_on_critical_issue
```

Domain-specific criteria belong in CriticProfile, not hard-coded global settings.

## 14. Workflow Configuration

Required workflow invariants remain:

```yaml
workflow:
  require_profile_approval: true
  freeze_task_configuration: true
  freeze_critic_profile: true
```

`max_iterations` and limitation policy are configuration-driven.

## 15. Model Configuration

### GPT Store Edition

The Store edition uses:

```text
model_policy: user_plan
recommended_model: null
```

This layer does not choose or call a model through a developer API. The ChatGPT runtime provides the model available to the user. Paid users may switch to additional models when the platform exposes them.

Workflow behavior must remain valid across supported model choices.

### Standalone/API Edition

The existing `models` role mapping remains available for optional external runtime use:

```text
supervisor
domain_resolver
research_agent
critic_agent
report_generator
```

A role may define provider, model, reasoning level, temperature, max output tokens, and timeout.

The provider factory translates these settings without changing Agent Interface contracts.

The OpenAI semantic adapter implemented in Phase 11.3 is an optional standalone/API adapter, not a dependency of GPT Store Edition.

## 16. Resolver Configuration

Resolver settings include:

```text
mode: rules | semantic | hybrid
semantic_enabled
minimum_semantic_confidence
require_agreement_for_high_risk
fallback_to_rules
```

The Python reference runtime currently requires provider/model configuration when its external semantic adapter is enabled.

GPT Store packaging must instead map semantic reasoning to the host ChatGPT runtime without requiring a developer secret.

## 17. Tool Configuration

Tools are configured independently from agents.

Current logical tools:

```text
web_search
web_fetch
source_validator
citation_manager
```

GPT Store Edition should use built-in ChatGPT capabilities where available. Standalone/API Edition may inject external tool providers.

## 18. Resource Limits

Current limits include:

```text
max_iterations
max_agent_runs
max_search_calls
max_fetch_calls
max_sources
max_runtime_seconds
max_output_size_bytes
```

Future standalone limits may include token and cost ceilings where provider metering exists.

A reached limit produces an explicit workflow outcome rather than silent termination.

## 19. Retry and Timeout Policy

Retry settings are centralized:

```text
max_attempts
initial_delay_seconds
max_delay_seconds
backoff_multiplier
```

Timeouts and call budgets are enforced by runtime controls in the Python reference runtime.

The Store edition cannot assume access to provider-level retry/token telemetry that ChatGPT does not expose to the GPT configuration itself.

## 20. Logging

Operational logs may include task_id, workflow_run_id, run_id, agent_id, and request_id where the runtime exposes them.

Logs must not contain secrets or hidden chain-of-thought.

Server-side file logging applies only to standalone/API execution. Store Edition relies on ChatGPT conversation/runtime behavior and explicit user-facing checkpoint artifacts rather than a private server log dependency.

## 21. Persistence

Standalone/API Edition currently supports:

```text
backend: sqlite
path: runtime/k_supervisor.db
```

Agents do not depend directly on SQLite.

GPT Store Edition has no mandatory server persistence. Baseline state is conversation-local. Cross-chat continuation must use explicit checkpoint/recovery artifacts until a separately approved backend design exists.

## 22. Report Configuration

Final research artifacts remain UTF-8:

```text
<TASK_ID>_FINAL_REPORT.md
<TASK_ID>_REVIEW_PROTOCOL.md
```

Standalone runtime writes files to the configured output directory. GPT Store Edition may present or generate equivalent user-facing artifacts using ChatGPT-native capabilities.

## 23. Freshness and Risk

Freshness requirements and risk levels may influence generated CriticProfile defaults, evidence thresholds, required cross-checks, and source hierarchy.

Risk does not replace domain-specific criteria.

## 24. Task Configuration Snapshot

Before autonomous execution in the Python reference runtime, Supervisor creates an immutable secret-free TaskConfigurationSnapshot containing effective settings, environment, schema version, approved profile identity/version, and a configuration fingerprint.

Global changes affect new tasks only. Profile amendments create a superseding snapshot without silently changing previously frozen task settings.

The `distribution` policy is included in the effective settings and therefore auditable.

## 25. GPT Store Snapshot Equivalent

The Store edition cannot depend on the Python SQLite snapshot implementation.

Its functional equivalent must preserve at least:

```text
task identity
approved CriticProfile
active workflow state
iteration number
current research result
current CriticReview
important limitations
configuration/distribution policy version
```

For cross-chat recovery, this state should be serialized into an explicit checkpoint artifact that the user can carry into a fresh conversation.

## 26. Validation

Configuration validation includes required fields, enums, numeric ranges, resource consistency, provider compatibility, tool availability, approval state, and distribution invariants.

For GPT Store defaults, validation rejects attempts to require a developer API key, pin a model, disable free-user compatibility, disable user model switching, or require an external backend.

## 27. Schema Version

Current tracked schema version:

```text
1.0
```

Breaking schema changes require explicit migration or compatibility handling.

## 28. Current settings.yaml Distribution Block

```yaml
distribution:
  primary_channel: chatgpt_store
  free_user_compatible: true
  developer_api_key_required: false
  model_policy: user_plan
  recommended_model: null
  allow_user_model_switch: true
  external_backend_required: false
```

## 29. .env.example Policy

`.env.example` may list optional standalone/API variable names but must state that the GPT Store Edition needs no developer-owned secret.

## 30. Audit Requirements

For each standalone task, audit should identify configuration schema version, environment, approved CriticProfile version, distribution policy, model role settings, tool limits, and workflow limits without exposing secrets.

For Store Edition, equivalent user-visible auditability is provided through workflow/report/checkpoint artifacts rather than mandatory private backend telemetry.

## 31. Phase 11 Metrics Boundary

Usage/cost/quality metrics must respect deployment capabilities.

```text
GPT Store Edition:
  - workflow quality metrics
  - iteration/review outcomes
  - source/claim coverage
  - no assumed provider token/cost telemetry

Standalone/API Edition:
  - all workflow quality metrics
  - provider API calls where exposed
  - input/output tokens where exposed
  - estimated cost where pricing data is configured
```

The free Store experience must not require developer-funded API usage for metrics collection.

## 32. Acceptance Criteria

Configuration is compliant when:

- tracked defaults validate;
- GPT Store is the primary channel;
- Store defaults require no developer secret or backend;
- no ChatGPT model identifier is pinned as a core dependency;
- users may switch models when their plan allows it;
- standalone provider/model adapters remain optional;
- approved CriticProfile remains authoritative;
- active standalone task settings are frozen and auditable;
- runtime limits are enforceable where the execution environment exposes them;
- secret values never enter tracked configuration, snapshots, reports, or logs.
