# ROADMAP
План завершеного розвитку K-Research & Critic та межі подальшого maintenance.

Version: 1.8
Status: MAINTENANCE
Updated: 2026-08-23

## 1. Purpose

This roadmap records the completed implementation path for K-Research & Critic and narrowly scoped future product improvements.

K-Research & Critic is a finished GPT Store product. Its active product-development roadmap ends with Phase 12. Future work in this repository is limited to maintenance, compatibility, security, regression fixes, and separately approved narrow product improvements.

The previously planned Modular Agent Platform is no longer Phase 13 of this product. That direction is transferred to the separate `K_Supervisor` project.

## 2. Stable Product Invariants

- Supervisor coordinates but does not replace research or critique.
- CriticProfile approval is mandatory before autonomous independent research.
- The current public UX uses the accepted two-stage direct-run / review-edit / cancel gate.
- Approved profiles remain immutable unless a material amendment is approved.
- Research-Critic revision cycles are autonomous after approval.
- Risk floors control minimum independent cross-check requirements.
- Every material factual claim has its own required/achieved/exception cross-check ledger.
- Evidence counted as independent must be traceable to visible evidence origins.
- Derivative reporting of the same underlying evidence is not double-counted.
- Ukrainian is the default user-facing report language; headings, table columns and CriticProfile labels follow the selected report language.
- Contracts, task states, evidence, limitations, and failures remain explicit.
- The public Store workflow does not depend on a fixed model identifier or mandatory external service.
- Private chain-of-thought is never required for auditability.
- Cross-chat continuation uses the explicit checkpoint contract when requested.
- Maintenance changes must preserve the validated public workflow unless a separately approved product revision changes it.

## 3. Completed Core

```text
Phase 0  Repository Bootstrap                         COMPLETE
Phase 1  Core Domain Models and Contracts             COMPLETE
Phase 2  Supervisor Foundation                        COMPLETE
Phase 3  Domain Resolver and CriticProfile Workflow   COMPLETE
Phase 4  ResearchAgent MVP                            COMPLETE
Phase 5  Tools and Evidence Layer                     COMPLETE
Phase 6  CriticAgent MVP                              COMPLETE
Phase 7  Autonomous Research-Critic Loop              COMPLETE
Phase 8  ReportGenerator and Final Artifacts          COMPLETE
Phase 9  End-to-End MVP                               COMPLETE
Phase 10 Persistence and Audit                        COMPLETE
```

MVP boundary: Phase 9. The post-MVP Hybrid Domain Resolver enhancement is COMPLETE.

## 4. GPT Store-first Product Decision

Status: COMPLETE

```text
channel: chatgpt_store
public product: K-Research & Critic
free-user compatible: yes
model policy: user_plan
fixed model dependency: none
user model switching: allowed when available
mandatory external backend: no
publication state: published
production smoke test: passed
```

The Python/provider runtime remains an engineering and optional standalone reference implementation. It is not required by the public GPT Store execution path.

## 5. Phase 11 - Configuration, Cost, and Quality Controls

Status: COMPLETE

```text
11.1 Configuration Core                          COMPLETE
11.2 Task Configuration Snapshot                 COMPLETE
11.3 Provider / Model Factory                    COMPLETE
11.4 Runtime Controls                            COMPLETE
11.4A GPT Store-first Distribution Policy        COMPLETE
11.5 Usage, Cost, and Quality Metrics            COMPLETE
11.6 Logging / Sensitive-data Redaction          COMPLETE
11.7 GPT Store Packaging / Publication Readiness COMPLETE
```

## 6. Phase 12 - Test and CI Hardening

Status: COMPLETE

Delivered:

- orchestration, profile, loop, report, failure, Store-package, and configuration regression coverage;
- deterministic offline reference benchmark;
- Python 3.13 and Python 3.14 CI test matrix;
- dependency integrity gate;
- Ruff correctness gate;
- Mypy typed-boundary gate;
- repository policy validation;
- GPT Store package regression validation;
- blocking coverage floor;
- dependency maintenance automation.

## 7. Current Public Core Runtime Baseline

Status: ACCEPTED / SYNCHRONIZED TO REPOSITORY MAIN

The current public Builder runtime was revalidated on 2026-08-23 and the accepted Core contract is now mirrored in `main`.

Accepted runtime behavior:

```text
two-stage CriticProfile gate                 PASS
CRITICAL -> required_cross_checks >= 3       PASS
claim-level required/achieved/exception      PASS
visible SHORTFALL                            PASS
evidence-origin traceability                 PASS
systematic-review double-counting protection PASS
Critic REVISE -> PASS loop                   PASS
Ukrainian report/profile/table localization  PASS
COMPLETED_WITH_LIMITATIONS when required     PASS
```

Canonical repository files:

```text
prompts/GPT_STORE_INSTRUCTIONS.md
gpt_store/manifest.yaml
scripts/validate_store_package.py
tests/test_gpt_store_package.py
docs/GPT_STORE_PACKAGE.md
```

## 8. Maintenance Scope

Allowed future work in this repository:

```text
bug fixes
security fixes
GPT Store compatibility updates
OpenAI platform compatibility updates
regression fixes
documentation corrections
narrow UX improvements
narrow analytics/observability improvements after privacy and architecture approval
maintenance releases such as v1.0.1 and v1.0.2
```

Changes that turn the product into a general modular agent platform are out of scope here.

## 8.1 Planned Narrow Product Improvement - Request Accounting

Status: PLANNED / ARCHITECTURE AND PRIVACY DECISION REQUIRED

Goal: create a persistent owner-visible register of user requests to the public K-Research & Critic product without changing the Research/Critic semantics.

Target table fields:

| Field | Requirement |
|---|---|
| `request_number` | sequential request number |
| `date` | request date |
| `time` | request time |
| `user_name` | reliable user name when actually available; otherwise `none` |
| `request_topic` | short generalized topic of the request |

Data-minimization rules:

- never infer a user's identity from message content;
- if the platform does not reliably expose an authenticated user name to the product, store `none`;
- store a short generalized topic, not the full prompt, by default;
- do not store hidden reasoning, credentials, sensitive tool metadata, or unrelated personal data;
- define the canonical timestamp/time-zone rule before implementation.

Required design tasks before implementation:

1. Verify what user/account identity metadata, if any, is actually available to the published Custom GPT runtime.
2. Select the persistence mechanism for the request table.
3. Select the owner review mechanism for browsing, filtering and exporting requests.
4. Define owner authentication/access control for the review interface.
5. Define retention/deletion policy and privacy notice requirements.
6. Confirm whether implementation requires an Action/external backend; if so, treat that as a separate product architecture decision because the current public Core has `actions=false` and no mandatory backend.
7. Implement only after the storage/review/privacy design is explicitly approved.

Mechanisms to compare for owner review:

```text
A. private admin web table/dashboard
B. protected spreadsheet-style owner view
C. database admin view with CSV/export capability
```

Selection criteria:

```text
privacy and access control
reliability
implementation complexity
operating cost
mobile/desktop usability
filter/search capability
export/backup capability
impact on current public GPT UX
```

No review mechanism is selected yet; mechanism selection is an explicit planned task.

## 9. Modular Agent Platform Transfer

The former planned `Phase 13 - Modular Agent Platform` is intentionally removed from the K-Research & Critic product roadmap.

Its goals are transferred to the separate `K_Supervisor` project, which starts with its own Phase 0.

## 10. Legacy Engineering Identifiers

Some stable internal identifiers retain the historical `K_Supervisor` name for compatibility, including:

```text
K_SUPERVISOR_CHECKPOINT
runtime/k_supervisor.db
```

These identifiers are not repository/product names and should not be renamed solely for cosmetic consistency if doing so would break compatibility.

## 11. Canonical Project Documents

```text
PROJECT_FILE_STANDARD.md
ARCHITECTURE.md
ROADMAP.md
AGENT_INTERFACE.md
DATA_MODELS.md
RESEARCH_WORKFLOW.md
CONFIGURATION.md
TEST_PLAN.md
CI_QUALITY.md
HYBRID_RESOLVER_PLAN.md
PERSISTENCE.md
GPT_STORE_DEPLOYMENT.md
GPT_STORE_PACKAGE.md
LOGGING.md
```

## 12. Current Implementation State

```text
Phase 0-10                               COMPLETE
Post-MVP Hybrid Domain Resolver         COMPLETE
GPT Store-first Product Decision        COMPLETE
Phase 11                                COMPLETE
Phase 12                                COMPLETE
GPT Store publication                   COMPLETE
Original production smoke test          COMPLETE
2026-08-23 public Core runtime hardening ACCEPTED
GitHub main / public Builder Core sync   COMPLETE
Request accounting                      PLANNED
Future Modular Agent Platform           MOVED TO K_Supervisor
Current repository mode                 MAINTENANCE
```
