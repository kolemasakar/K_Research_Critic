# ARCHITECTURE
Короткий опис зафіксованої production-архітектури K-Research & Critic та її maintenance-меж.

Version: 1.2
Status: MAINTENANCE

## 1. Purpose

K-Research & Critic is a completed GPT Store-first research and independent-critique product.

Its production architecture accepts a user task, resolves the task domain and risk, proposes a CriticProfile for explicit user approval, performs research, executes an independent critique/revision loop, and produces a sourced final report plus review protocol.

The repository `K_Research_Critic` is now maintained as a stable product. General modular-agent-platform evolution is transferred to the separate new `K_Supervisor` project.

## 2. Core Principles

- Supervisor coordinates work but does not replace research or critique.
- Agents/components communicate through explicit validated contracts.
- Workflow transitions are explicit and auditable.
- CriticAgent is generic and receives a task-specific CriticProfile.
- User approval of CriticProfile is mandatory before autonomous execution.
- Approved profiles are immutable unless a material amendment is separately approved.
- Research-Critic revision cycles are autonomous after approval.
- Evidence, uncertainty, limitations, and final status remain explicit.
- Execution status, critic decision, task state, and workflow state remain separate concepts.
- Hidden chain-of-thought/private reasoning is never persisted as an artifact.
- Maintenance changes must preserve production behavior unless an explicitly approved product revision changes it.

## 3. Product Identity

```text
Public product: K-Research & Critic
Repository: kolemasakar/K_Research_Critic
Distribution: GPT Store
Release line: v1.0.x
Repository mode: PRODUCTION / MAINTENANCE
```

Stable legacy engineering identifiers intentionally remain where compatibility matters:

```text
K_SUPERVISOR_CHECKPOINT
runtime/k_supervisor.db
```

These are compatibility identifiers, not the current repository/product name.

## 4. Product Distribution Decision

The primary public edition is a Custom GPT distributed through ChatGPT.

```text
channel: chatgpt_store
free_user_compatible: true
developer_api_key_required: false
model_policy: user_plan
recommended_model: null
allow_user_model_switch: true
external_backend_required: false
publication_state: published
production_smoke_test_passed: true
```

The public product is designed to work without a developer-owned API key, without a mandatory external backend, and without a pinned model identifier.

The optional Python/SQLite/provider runtime remains an engineering reference and standalone execution path. It is not a dependency of the GPT Store product.

## 5. High-Level Logical Architecture

```text
USER
  |
  v
SUPERVISOR
  |
  +-- Domain Resolver
  +-- Profile Manager
  +-- Workflow / State Control
  |
  +-----------------------------+
  |                             |
  v                             v
ResearchAgent               CriticAgent
  |                             |
  +---------- Tools / Evidence -+
  |
  v
Evidence / Sources
  |
  v
ReportGenerator
  |
  +-- FINAL REPORT
  +-- REVIEW PROTOCOL
```

In the GPT Store Edition these are separated logical roles/passes inside one ChatGPT runtime rather than independent agent processes.

## 6. Supervisor Responsibilities

Supervisor is responsible for:

- receiving the user task;
- resolving task domain/type/risk;
- generating a draft CriticProfile;
- presenting the profile for explicit user approval/edit/reject;
- freezing the approved profile;
- controlling workflow state and iteration limits;
- passing structured context/results between logical roles;
- handling recoverable and unrecoverable failures;
- triggering final output generation.

Supervisor must not silently bypass the approval gate or replace independent critique with self-approval.

## 7. Domain Resolution

Domain resolution identifies:

```text
primary domain
secondary domains
task type
risk level
relevant source classes / standards
multi-domain requirements
```

The engineering reference implementation includes deterministic RuleBasedResolver plus semantic and HybridResolver paths with conservative fallback and risk floors.

The GPT Store Edition uses ChatGPT-native reasoning/capabilities where available and must not require a developer API secret.

## 8. CriticProfile and User Approval

Before autonomous execution, Supervisor generates a CriticProfile draft.

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

Interaction rule:

```text
Supervisor proposes.
User approves or edits.
Critic executes.
```

Only an APPROVED profile may be used for normal autonomous research/review execution.

## 9. Profile Freeze Rule

After approval, CriticProfile is frozen for the task.

If research reveals a materially new requirement, Supervisor may propose an amended profile. The amendment becomes active only after explicit user approval.

Ordinary Research-Critic revisions do not reopen the approval gate.

## 10. ResearchAgent

ResearchAgent/logical Research stage:

- decomposes the task;
- builds a search/research strategy;
- collects sources and evidence;
- extracts and evaluates claims;
- records uncertainty and limitations;
- creates a draft report;
- revises output from structured critic feedback.

Research is not the final verifier of its own conclusions.

## 11. CriticAgent

CriticAgent/logical Critic stage performs an independent verification pass under the approved CriticProfile.

It evaluates:

```text
source authority
source freshness
unsupported claims
contradictions
missing topics
conclusion/evidence consistency
approved thresholds
```

The result is PASS or REVISE with reliability score and structured recommendations.

## 12. Research-Critic Workflow

```text
NEW
 |
 v
PROFILE_REVIEW_REQUIRED
 |
 +-- EDIT ------> PROFILE_REVIEW_REQUIRED
 |
 +-- REJECT ----> STOP
 |
 +-- APPROVE ---> PROFILE_APPROVED
                    |
                    v
                RESEARCHING
                    |
                    v
                 REVIEWING
                    |
             +------+------+
             |             |
          REVISE          PASS
             |             |
             v             v
        RESEARCHING     FINALIZED
```

Additional outcomes:

```text
FAILED
COMPLETED_WITH_LIMITATIONS
```

The Store instructions define the exact public state semantics and checkpoint-safe states.

## 13. Evidence Model

Claims and sources are represented separately from prose in the engineering reference model.

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

The public report must distinguish evidence-backed claims, uncertainty, inference, and limitations.

## 14. Termination Rules

The review loop stops when:

- PASS meets the approved reliability threshold;
- maximum permitted iterations are reached;
- an unrecoverable failure occurs.

Failure to reach PASS is not silently presented as verified success. Useful output may finish as `COMPLETED_WITH_LIMITATIONS` when appropriate.

## 15. Final Output

The final user-facing result contains:

```text
FINAL REPORT
REVIEW PROTOCOL
```

It includes evidence references, uncertainty, significant review issues, applied changes, unresolved limitations, reliability information, and final status.

It must not contain hidden chain-of-thought/private reasoning or internal citation/tool placeholders.

## 16. Tools and Capabilities

Public Store execution primarily uses built-in ChatGPT capabilities where available, including web research and data analysis when exposed to the current runtime.

Optional standalone adapters remain isolated behind provider-neutral boundaries.

Capability absence must be surfaced explicitly when it materially limits freshness or verification.

## 17. Persistence and Recovery

Standalone/reference persistence remains isolated behind a dedicated boundary and may use:

```text
runtime/k_supervisor.db
```

GPT Store Edition does not depend on private server-side SQLite.

Cross-chat continuation uses the explicit user-controlled checkpoint contract:

```text
K_SUPERVISOR_CHECKPOINT
```

Checkpoint generation is explicit-request only in the public Store workflow.

## 18. Configuration, Limits, and Audit

The completed architecture includes:

```text
validated configuration
frozen task configuration snapshots
runtime limits
timeouts and retries
usage/quality metrics
structured logging
sensitive-data redaction
audit/recovery support
GPT Store package validation
```

The free Store path has no mandatory developer secret or backend dependency.

## 19. Quality Boundary

The production baseline is protected by:

```text
Python 3.13 tests
Python 3.14 tests
dependency integrity
Ruff correctness checks
Mypy typed-boundary checks
repository policy validation
GPT Store package validation
coverage gate
deterministic reference benchmark
manual Free/paid Store validation
production smoke test
```

Repository CI validates what can be proven offline. Live ChatGPT UI/account behavior remains a manual release/maintenance verification boundary.

## 20. Maintenance Architecture Boundary

This repository may evolve only within the K-Research & Critic product boundary unless a new major product decision explicitly reopens architecture scope.

Normal maintenance includes:

```text
bug fixes
security fixes
Store/platform compatibility changes
regression fixes
small UX improvements
documentation corrections
v1.0.x maintenance releases
```

The following are intentionally NOT developed here as the next architecture generation:

```text
capability-based general agent platform
automatic agent discovery
executable plugin registry for arbitrary new agents
general capability router
large catalog of domain agents
complex parallel/distributed orchestration
automatic agent generation
```

## 21. Successor Platform Decision

The previously planned Phase 13 Modular Agent Platform is transferred to a separate new project:

```text
K_Supervisor
```

The new project starts from Phase 0 with clean platform-level requirements and may selectively extract reusable concepts from K-Research & Critic.

Migration principle:

```text
extract -> generalize -> import
```

not:

```text
clone -> modify
```

K-Research & Critic therefore remains a stable production reference product rather than becoming the experimental development branch of the future platform.

## 22. Architecture Decision Summary

- K-Research & Critic is the completed production research/critique product.
- Repository name is `K_Research_Critic`.
- GPT Store Edition is the primary public distribution target.
- Supervisor/Profile/Research/Critic/Report boundaries remain stable.
- CriticProfile approval is mandatory and approved profiles are frozen.
- Research-Critic interaction is autonomous after approval.
- Final output contains a consolidated report and review protocol.
- GPT Store Edition requires no developer API key and no mandatory backend.
- Model selection follows the user's available ChatGPT runtime/plan rather than a pinned model identifier.
- The Python/SQLite/provider stack remains an optional engineering/reference runtime.
- Legacy compatibility identifiers such as `K_SUPERVISOR_CHECKPOINT` remain unchanged in v1.0.x.
- The general modular agent platform is developed separately as the new `K_Supervisor` project with a new roadmap beginning at Phase 0.
