# LOGGING
Документ визначає структуроване журналювання та правила редагування чутливих даних у K_Supervisor.

Version: 1.0
Status: ACTIVE

## 1. Purpose

This document defines the Phase 11.6 operational logging boundary for K_Supervisor.

The standalone/API reference runtime may write structured JSONL operational events. The GPT Store Edition does not depend on a private server log and instead exposes user-visible workflow state, review artifacts, quality metrics, and checkpoint artifacts.

## 2. Invariants

- Secret redaction is mandatory.
- Configured secret values must never be written to logs.
- Secret-like fields must be redacted even when the value was not loaded through RuntimeSecrets.
- Hidden chain-of-thought, scratchpad content, and private reasoning must never be persisted.
- User research text and report content are not required for operational logging and should not be logged by default.
- task_id, workflow_run_id, run_id, agent_id, and request_id are the preferred correlation identifiers.
- Logging must not change ResearchAgent, CriticAgent, or ReportGenerator business contracts.

## 3. Standalone Log Format

Default file:

```text
logs/k_supervisor.jsonl
```

Each line is one UTF-8 JSON object.

Typical fields:

```text
timestamp
level
event
message
task_id
workflow_run_id
run_id
agent_id
request_id
details
```

Identifier fields are included only when they exist in the current runtime context.

## 4. Logged Events

The reference CLI emits structured lifecycle events including:

```text
runtime_initialized
task_prepared
profile_approved
profile_gate_stopped
configuration_snapshot_frozen
autonomous_execution_started
agent_run_completed
workflow_completed
```

Failure paths emit explicit error events without requiring raw request or report payloads.

## 5. Redaction

SensitiveDataRedactor applies recursive redaction to mappings and sequences and also filters sensitive-looking text.

Sensitive field classes include:

```text
api_key
authorization
cookie
credential
database_url
password
private_key
secret
token
access_token
refresh_token
auth_token
```

Configured RuntimeSecrets values are replaced wherever they appear in a logged string.

Text filtering also covers common Bearer credentials, OpenAI-style secret keys, JWT-like values, URI user/password credentials, and secret assignments.

## 6. Private Reasoning Boundary

The logger explicitly removes fields such as:

```text
chain_of_thought
hidden_reasoning
private_reasoning
reasoning_trace
scratchpad
```

Operational logs may record decisions, statuses, metrics, errors, and auditable workflow outcomes. They must not record private reasoning traces.

## 7. Configuration

Tracked configuration remains:

```yaml
logging:
  level: INFO
  directory: logs
  console_enabled: true
  file_enabled: true
  include_task_id: true
  include_run_id: true
  redact_secrets: true
```

`logging.redact_secrets: true` is a system invariant and cannot be disabled by a normal settings file.

The default JSONL filename is `k_supervisor.jsonl` inside the configured logging directory.

## 8. Console Output

When console logging is enabled, the same sanitized JSON event is written to stderr.

User-facing CLI output remains on stdout.

## 9. Failure Handling

If configured file logging cannot initialize, the standalone CLI fails explicitly rather than silently pretending that operational logging is active.

Log records do not contain full source documents, report bodies, task text, or CriticProfile edit payloads by default.

## 10. GPT Store Edition Equivalent

The GPT Store Edition has no mandatory private log backend.

Its user-visible audit equivalent is composed from:

```text
explicit CriticProfile approval state
current workflow state
Research-Critic iteration outcome
PASS/REVISE history
TaskQualityMetrics
FINAL_REPORT
REVIEW_PROTOCOL
explicit limitations/failure status
checkpoint artifact for cross-chat continuation
```

The checkpoint artifact is a user-controlled continuity mechanism, not a hidden telemetry channel. Detailed packaging and fresh-chat recovery behavior are finalized in Phase 11.7.

## 11. Store Privacy Boundary

The Store edition must not add an Action or external logging backend merely to collect operational telemetry for the free core workflow.

Quality/audit information should be derived from the workflow state already available to the conversation and exposed to the user when useful.

## 12. Validation

Phase 11.6 validation covers:

- recursive configured-secret redaction;
- secret-like field redaction;
- free-text credential pattern redaction;
- private-reasoning field removal;
- log-level filtering;
- JSONL event output;
- stable correlation identifiers on agent-run events;
- end-to-end CLI log generation;
- rejection of configuration that disables mandatory redaction.
