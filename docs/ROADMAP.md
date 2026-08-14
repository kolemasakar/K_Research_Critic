# ROADMAP
План завершеного розвитку K-Research & Critic та межі подальшого maintenance.

Version: 1.7
Status: MAINTENANCE

## 1. Purpose

This roadmap records the completed implementation path for K-Research & Critic.

K-Research & Critic is a finished GPT Store product. Its active product-development roadmap ends with Phase 12. Future work in this repository is limited to maintenance, compatibility, security, regression fixes, and narrowly scoped product improvements.

The previously planned Modular Agent Platform is no longer Phase 13 of this product. That direction is transferred to a separate new project and repository named `K_Supervisor`, which starts from a new Phase 0 roadmap.

## 2. Stable Product Invariants

- Supervisor coordinates but does not replace research or critique.
- CriticProfile approval is mandatory before autonomous execution.
- Approved profiles remain immutable unless a material amendment is approved.
- Research-Critic revision cycles are autonomous after approval.
- Contracts, task states, evidence, limitations, and failures remain explicit.
- The public Store workflow does not depend on a fixed model identifier or mandatory external service.
- Private chain-of-thought is never required for auditability.
- Cross-chat continuation uses the explicit checkpoint contract when requested.
- Maintenance changes must preserve the validated production workflow unless a separately approved product revision changes it.

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

MVP boundary: Phase 9.

The post-MVP Hybrid Domain Resolver enhancement is COMPLETE.

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

Delivered:

- validated frozen configuration;
- immutable task configuration snapshots and restart-safe reconstruction;
- role-based provider isolation for optional standalone execution;
- research and critic limits;
- tool call budgets, timeouts, retries, runtime ceilings, and output-size limits;
- GPT Store distribution invariants and user-plan model policy;
- usage and quality metrics;
- restart-safe metric reconstruction;
- structured operational logging and sensitive-data redaction;
- Store manifest, instructions, checkpoint contract, release validator, and operator documentation.

## 6. Phase 12 - Test and CI Hardening

Status: COMPLETE

Delivered:

- orchestration, profile, loop, report, failure, Store-package, and configuration regression coverage;
- deterministic offline reference benchmark;
- four reference domains: literary analysis, software engineering, medicine, and geodesy;
- Python 3.13 and Python 3.14 CI test matrix;
- dependency integrity gate;
- Ruff correctness gate;
- Mypy typed-boundary gate;
- repository policy validation;
- GPT Store package regression validation;
- blocking coverage floor;
- dependency maintenance automation;
- synchronized quality documentation.

Validated release baseline:

```text
Python 3.13 full suite: PASS
Python 3.14 full suite: PASS
Quality gates: PASS
Repository validation: PASS
GPT Store package validation: PASS
Production smoke test: PASS
```

## 7. Production Release Boundary

Canonical first production release:

```text
K-Research & Critic v1.0.0
Git tag: v1.0.0
```

Release characteristics:

```text
status: PRODUCTION / MAINTENANCE
GPT Store: published
Free-account validation: PASS
Paid-account validation: PASS
Model/runtime-switch validation: PASS
Store discoverability: PASS
Production Research -> Critic workflow: PASS
Production REVISE -> PASS cycle: PASS
```

The `v1.0.0` tag must point to the finalized maintenance-synchronization commit whose CI is fully green.

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
maintenance releases such as v1.0.1 and v1.0.2
```

Changes that turn the product into a general modular agent platform are out of scope here.

## 9. Modular Agent Platform Transfer

The former planned item:

```text
Phase 13 - Modular Agent Platform
```

is intentionally removed from the K-Research & Critic product roadmap.

Its goals are transferred to the separate `K_Supervisor` project:

```text
capability-oriented agent metadata
automatic agent discovery
executable agent registration
capability-based selection and routing
standard compatibility contracts
modular FactCheck/DataAnalysis/Technical/Financial/Legal/Planning agents
```

The new K_Supervisor project starts with its own Phase 0 and is not a continuation of this roadmap numbering.

## 10. Legacy Engineering Identifiers

Some stable internal identifiers retain the historical `K_Supervisor` name for compatibility, including the checkpoint marker and existing runtime/database conventions. These identifiers are not repository/product names and must not be renamed solely for cosmetic consistency if doing so would break compatibility.

Examples:

```text
K_SUPERVISOR_CHECKPOINT
runtime/k_supervisor.db
```

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

## 12. Final Implementation State

```text
Phase 0-10                               COMPLETE
Post-MVP Hybrid Domain Resolver         COMPLETE
GPT Store-first Product Decision        COMPLETE
Phase 11                                COMPLETE
Phase 12                                COMPLETE
GPT Store publication                   COMPLETE
Production smoke test                   COMPLETE
K-Research & Critic v1.0.0              RELEASE BASELINE
Future Modular Agent Platform           MOVED TO NEW K_Supervisor PROJECT
Current repository mode                 MAINTENANCE
```
