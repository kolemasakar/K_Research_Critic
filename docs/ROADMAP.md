# ROADMAP
План завершеного розвитку K-Research & Critic та межі подальшого maintenance.

Version: 1.14
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
- Private chain-of-thought is never required for auditability.
- Cross-chat continuation uses the explicit checkpoint contract when requested.
- Non-essential telemetry must not degrade the normal public request UX.

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
Phase 11 Configuration, Cost and Quality Controls     COMPLETE
Phase 12 Test and CI Hardening                        COMPLETE
```

## 4. GPT Store-first Product Decision

Status: COMPLETE

```text
channel: chatgpt_store
public product: K-Research & Critic
free-user compatible: yes
model policy: user_plan
fixed model dependency: none
user model switching: allowed when available
publication state: published
```

## 5. Current Public Core Runtime Baseline

Status: ACCEPTED / SYNCHRONIZED

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
Actions                                     DISABLED
request logging in Builder instructions     DISABLED
script.google.com consent interruption      ABSENT
```

The repository and actual public Builder are synchronized for the no-Action public Core.

## 6. Maintenance Scope

Allowed future work:

```text
bug/security fixes
GPT Store/OpenAI compatibility updates
regression fixes
documentation corrections
narrow UX improvements
narrow analytics/observability improvements
maintenance releases
```

## 6.1 Request Accounting MVP

Status: `DISABLED_DUE_TO_USER_CONSENT_UX_RUNTIME_ACCEPTED`

Historical implementation:

```text
Public K-Research & Critic
  -> GPT Action `logRequest`
  -> Google Apps Script Web App
  -> Google Sheet
```

The implementation and runtime tests passed, including one substantive request -> one row and no extra row for standalone workflow reply `1`.

However, the public GPT presented a platform-controlled external-Action consent screen before sending the generalized topic to `script.google.com`. The owner decided that this is unacceptable UX for a non-essential request counter.

Final accepted decision:

```text
remove `logRequest` from active public Builder       COMPLETE
remove request logging from active Instructions      COMPLETE
save/update public GPT                                COMPLETE
NEW-chat post-disable smoke test                      PASS
script.google.com consent screen                      ABSENT
CriticProfile gate appears directly                  PASS
retain Apps Script/OpenAPI/Sheet prototype            YES
```

Canonical retained prototype resources:

```text
integrations/request_log/google_apps_script/Code.gs
integrations/request_log/openapi.yaml
prompts/GPT_STORE_REQUEST_LOG_ADDENDUM.md
docs/REQUEST_LOG_MVP.md
docs/PRIVACY_POLICY_REQUEST_LOG.md
docs/REQUEST_LOG_MVP_RUNTIME_ACCEPTANCE_2026-08-23.md
docs/REQUEST_LOG_DISABLEMENT_DECISION_2026-08-23.md
```

Do not re-enable the public Action unless the owner explicitly accepts the consent UX or a different telemetry architecture avoids it.

## 7. Current Activation Boundary

Current accepted Builder state:

```text
Actions: disabled
Apps: disabled
Web search: enabled
Code Interpreter & Data Analysis: enabled
REQUEST LOGGING instruction block: absent
privacy-policy URL required by active package: no
```

## 8. Modular Agent Platform Transfer

General modular platform work remains in separate `K_Supervisor`.

## 9. Legacy Engineering Identifiers

Stable compatibility identifiers may retain `K_Supervisor`, including `K_SUPERVISOR_CHECKPOINT` and `runtime/k_supervisor.db`.

## 10. Canonical Project Documents

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
REQUEST_LOG_MVP.md
PRIVACY_POLICY_REQUEST_LOG.md
REQUEST_LOG_MVP_RUNTIME_ACCEPTANCE_2026-08-23.md
REQUEST_LOG_DISABLEMENT_DECISION_2026-08-23.md
```

## 11. Current Implementation State

```text
Phase 0-12                                COMPLETE
GPT Store publication                    COMPLETE
2026-08-23 public Core runtime hardening ACCEPTED
Request-log prototype                    IMPLEMENTED / TESTED / RETAINED
Request-log public usage                 DISABLED_DUE_TO_USER_CONSENT_UX
Repository Instructions without logging COMPLETE
Repository actions=false                 COMPLETE
Public Builder Action removal            COMPLETE
Public Builder Instructions resync       COMPLETE
Post-disable NEW-chat smoke test         PASS
Repository / public Builder sync         COMPLETE
Current repository mode                 MAINTENANCE
```
