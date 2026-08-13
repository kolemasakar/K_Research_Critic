# PERSISTENCE
Документ описує реалізацію Phase 10 для збереження, аудиту та безпечного відновлення стану K_Supervisor.

Version: 1.0
Status: ACTIVE

## 1. Purpose

This document defines the implemented persistence and audit boundary introduced in Phase 10.

The design goals are:

- preserve complete task execution history across process restarts;
- reconstruct approved CriticProfiles exactly;
- keep agent business logic storage-neutral;
- provide deterministic audit access;
- support safe recovery where execution state is unambiguous;
- avoid automatic replay when an external side effect may be uncertain.

## 2. Architecture

Persistence is owned by orchestration components, not by agents.

```text
Agents
  |
  v
Supervisor / workflow boundaries
  |
  v
PersistenceStore protocol
  |
  +-- SQLitePersistenceStore
```

The common storage boundary is defined in:

```text
persistence/base.py
```

The initial implementation is:

```text
persistence/sqlite_store.py
```

Agent source code does not require SQLite APIs.

## 3. Default Storage

The tracked default is:

```yaml
persistence:
  backend: sqlite
  path: runtime/k_supervisor.db
  schema_version: "1"
```

The runtime directory and local database files are excluded from Git.

SQLite uses WAL mode for the local persistence database.

## 4. Persisted Entities

The implementation persists the following validated contracts:

```text
Task
WorkflowRun
StateTransition
AgentResult
DomainAssessment
CriticProfile
UserApproval
ResearchResult
Claim
Source
CriticReview
Artifact
```

The initial SQLite tables are:

```text
schema_meta
tasks
workflow_runs
state_transitions
agent_runs
domain_assessments
critic_profiles
user_approvals
research_results
claims
sources
reviews
artifacts
```

Each model is stored as a validated JSON snapshot together with selected indexed columns used for lookup and ordering.

## 5. Write-Through Boundaries

Persistence occurs at Supervisor-owned boundaries.

TaskManager persists:

- task creation;
- active profile changes;
- workflow attachment;
- applied DomainAssessment state;
- task status changes triggered by WorkflowEngine.

WorkflowEngine persists:

- WorkflowRun creation and updates;
- iteration changes;
- agent run references;
- StateTransition records;
- terminal workflow status.

ProfileManager persists:

- DomainAssessment;
- CriticProfile lifecycle states;
- CriticProfile amendments;
- UserApproval records.

ResearchCriticLoop persists:

- ResearchAgent and CriticAgent AgentResult records;
- ResearchResult;
- embedded Claim and Source records;
- CriticReview.

ReportWorkflow persists:

- ReportGenerator AgentResult;
- final Artifact metadata.

## 6. Idempotency

Stable entity identifiers are primary keys.

Persistence writes use upsert semantics so repeating the same save operation does not create duplicate records.

This supports safe write-through calls from orchestration code and reduces duplicate audit records after normal retries.

## 7. TaskAuditSnapshot

`TaskAuditSnapshot` is the storage-neutral aggregate used to reconstruct one task history.

It contains:

```text
task
workflow_run
transitions[]
domain_assessments[]
critic_profiles[]
user_approvals[]
agent_results[]
research_results[]
claims[]
sources[]
reviews[]
artifacts[]
```

A completed task can therefore be inspected after the original application process has ended.

## 8. CriticProfile Reconstruction

CriticProfile is persisted as the validated model snapshot, including:

```text
profile_id
version
status
approved_at
approved_by
supersedes_profile_id
all evaluation fields
```

An approved profile is reconstructed through the original model validation contract. The persisted approved profile is not regenerated from DomainAssessment.

This preserves the exact user-approved critic boundary.

## 9. Recovery

`RuntimeRecoveryService` restores persisted orchestration state into a fresh runtime.

Automatic continuation is supported only from explicit safe checkpoints:

```text
PROFILE_REVIEW_REQUIRED
PROFILE_APPROVED
REVISE_REQUIRED
```

These states have a clear next action and do not require guessing whether an unfinished external side effect completed.

Terminal states are not resumed:

```text
FINALIZED
FAILED
COMPLETED_WITH_LIMITATIONS
```

They remain fully auditable.

## 10. Ambiguous Mid-Step States

The following states are not automatically replayed:

```text
RESEARCHING
DRAFT_READY
REVIEWING
```

Reason: after an unexpected process stop, Supervisor may not know whether the last agent or external tool operation completed but failed to persist its result.

Automatic replay could therefore duplicate an external action or create inconsistent evidence history.

Phase 10 chooses conservative recovery instead of silent replay. More advanced checkpointing or execution leases require a separate design decision.

## 11. Application API

When a persistence store is configured, `KSupervisorApplication` exposes:

```text
recover_task(task_id)
audit_task(task_id)
```

`recover_task` restores runtime state and returns a `RecoveryOutcome` containing the task, workflow, audit snapshot, resumability flag, and a human-readable recovery reason.

`audit_task` returns the persisted `TaskAuditSnapshot` without requiring recovery.

## 12. CLI

The research CLI now accepts:

```text
--database runtime/k_supervisor.db
```

The default database is:

```text
runtime/k_supervisor.db
```

The audit CLI is:

```text
python -m scripts.audit_task --task-id TASK_EXAMPLE --database runtime/k_supervisor.db
```

It reports persisted task/workflow status and entity counts without exposing private reasoning.

## 13. Security and Privacy

The persistence layer stores contract data produced by the workflow.

It must not intentionally store:

```text
API keys
access tokens
passwords
private chain-of-thought
hidden model reasoning
```

Secret configuration remains external to tracked project files and must not be copied into persistence snapshots.

## 14. Phase 10 Validation

Phase 10 tests verify:

- SQLite schema initialization;
- schema version recording;
- exact approved CriticProfile round-trip after restart;
- completed-task audit reconstruction;
- restart recovery from PROFILE_REVIEW_REQUIRED;
- restart recovery from PROFILE_APPROVED;
- idempotent persistence writes;
- audit CLI access after restart;
- absence of SQLite coupling in agent business logic.

Implementation validation:

```text
Commit: 24377e5370b60efd92e86bae8229d200b72bedb3
GitHub Actions run: 31658626453
Tests: 119 passed
```

## 15. Exit Criteria

Phase 10 is complete because:

- a storage-neutral persistence abstraction exists;
- SQLite is the initial durable backend;
- core workflow and evidence entities are persisted;
- a completed task is auditable after process restart;
- approved CriticProfiles reconstruct exactly;
- safe checkpoint recovery works across restart;
- ambiguous mid-step execution is not silently replayed;
- agent business logic remains independent of SQLite;
- the complete automated test suite passes.

## 16. Next Phase

The next roadmap phase is:

```text
Phase 11 - Configuration, Cost, and Quality Controls
```

Phase 11 will centralize configuration loading/validation, model selection by role, provider wiring, resource and cost controls, and quality metrics on top of the durable Phase 10 audit layer.
