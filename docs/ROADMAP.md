# ROADMAP
План завершеного розвитку K-Research & Critic та межі подальшого maintenance.

Version: 1.12
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
- Request accounting is optional observability: it is best-effort and must never block Research/Critic execution.

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
publication state: published
production smoke test: passed
```

## 5. Phase 11 - Configuration, Cost, and Quality Controls

Status: COMPLETE

## 6. Phase 12 - Test and CI Hardening

Status: COMPLETE

Delivered:
- Python 3.13 and Python 3.14 CI matrix;
- dependency integrity, Ruff, mypy, repository policy, GPT Store package and coverage gates;
- deterministic reference and workflow regression coverage.

## 7. Current Public Core Runtime Baseline

Status: ACCEPTED / SYNCHRONIZED TO REPOSITORY MAIN

Accepted public behavior:

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
optional request-log Action                  PASS
```

The repository and current public Builder are synchronized for the accepted Public Core plus Request Log MVP.

## 8. Maintenance Scope

Allowed future work:

```text
bug/security fixes
GPT Store/OpenAI compatibility updates
regression fixes
documentation corrections
narrow UX improvements
narrow analytics/observability improvements
maintenance releases v1.0.x
```

## 8.1 Narrow Product Improvement - Request Accounting MVP

Status: RUNTIME_ACCEPTED

Accepted architecture:

```text
Public K-Research & Critic
  -> best-effort GPT Action `logRequest`
  -> Google Apps Script Web App
  -> Google Sheet
```

Google Sheet:

```text
K-Research & Critic — Request Log
spreadsheet_id: 1icDvAkPx43s7568iZkANBCriz8UaanB4kMITO-icLaU
sheet: Звернення
timezone: Europe/Kyiv
```

Columns:

```text
Номер звернення
Дата
Час
Ім'я користувача
Коротка узагальнена тема запиту
```

Accepted MVP decisions:
- authentication: none;
- `user_name`: `none` until a separately approved reliable identity mechanism exists;
- full prompts/conversations are not stored;
- only a generalized topic up to 160 characters is sent;
- Apps Script generates sequential number, date and time;
- Google Sheets is both storage and owner review interface;
- CSV/XLSX export comes from Google Sheets;
- logging failure or user denial is non-blocking and must not alter Research/Critic results;
- standalone `1/2/3` workflow replies are not new logged requests.

Canonical package:

```text
integrations/request_log/google_apps_script/Code.gs
integrations/request_log/openapi.yaml
prompts/GPT_STORE_REQUEST_LOG_ADDENDUM.md
prompts/GPT_STORE_INSTRUCTIONS.md
docs/REQUEST_LOG_MVP.md
docs/PRIVACY_POLICY_REQUEST_LOG.md
docs/REQUEST_LOG_MVP_RUNTIME_ACCEPTANCE_2026-08-23.md
```

Runtime acceptance on 2026-08-23:

```text
Builder OpenAPI validation                  PASS
Builder direct Action write                 PASS
NEW-chat substantive request logging        PASS
request_number=2 physical Sheet write       PASS
standalone `1` created no row 3             PASS
1 substantive request -> exactly 1 row      PASS
```

Important UX property: because this is an external Action, ChatGPT may require the user to authorize sharing the generalized topic with `script.google.com`. This consent behavior is platform-controlled.

## 9. Modular Agent Platform Transfer

General modular platform work remains in separate `K_Supervisor`.

## 10. Legacy Engineering Identifiers

Stable compatibility identifiers may retain `K_Supervisor`, including `K_SUPERVISOR_CHECKPOINT` and `runtime/k_supervisor.db`.

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
REQUEST_LOG_MVP.md
PRIVACY_POLICY_REQUEST_LOG.md
REQUEST_LOG_MVP_RUNTIME_ACCEPTANCE_2026-08-23.md
```

## 12. Current Implementation State

```text
Phase 0-12                                COMPLETE
GPT Store publication                    COMPLETE
2026-08-23 public Core runtime hardening ACCEPTED
GitHub main / public Builder Core sync   COMPLETE
Request-log Google Sheet                 CREATED
Request-log repository package           COMPLETE
Apps Script Web App deployment           COMPLETE
OpenAPI endpoint configuration           COMPLETE
Builder Action configuration/test        PASS
Google Sheet write test                  PASS
Public Builder Instructions sync         COMPLETE
Public GPT update                         COMPLETE
Request-log NEW-chat runtime acceptance  ACCEPTED
Future Modular Agent Platform            MOVED TO K_Supervisor
Current repository mode                  MAINTENANCE
```
