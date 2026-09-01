# ROADMAP
План завершеного розвитку K-Research & Critic, поточного закритого MEDIA BETA модуля та меж подальшого maintenance.

Version: 1.15
Status: CORE_MAINTENANCE / MEDIA_BETA_CLOSED_BETA
Updated: 2026-09-01

## 1. Purpose

This roadmap records the completed implementation path for the published K-Research & Critic Core and the separately isolated closed-beta MEDIA BETA extension.

The public K-Research & Critic Core is a finished GPT Store product. Its active Core product-development roadmap ends with Phase 12. Future Core work is limited to maintenance, compatibility, security, regression fixes, and separately approved narrow product improvements.

K-Research & Critic - MEDIA BETA is an additive closed-beta module of K-Research & Critic. It is developed and validated separately so that MEDIA work does not silently alter the published Core. The module uses technology and backend implementation work developed in VoiceBridge, but VoiceBridge is a technology source/implementation repository rather than the parent product or product-roadmap authority.

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
- Closed-beta MEDIA work must remain isolated from the published Core until a separate explicit release decision.

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

Allowed future Core work:

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

## 6.2 K-Research & Critic - MEDIA BETA

Status: `CLOSED_BETA / RELEASE_HOLD_OWNER_TESTING`

Product hierarchy:

```text
K-Research & Critic
  -> public Core: K_Research_Critic/main
  -> closed beta module: K-Research & Critic - MEDIA BETA
       -> product documentation/state authority: K_Research_Critic
       -> media/backend technology and validation source: VoiceBridge
```

The accepted private MEDIA BETA runtime already covers the A9/A9.10/A10 zero-client media path for supported YouTube, Instagram, Facebook, Telegram, and one current-conversation local audio/video attachment. These accepted beta capabilities do not imply public Core activation or merge.

The currently active engineering track is the prerecorded STT/provider forward migration on VoiceBridge. The current verified position is:

```text
A9/A9.10/A10 private runtime baseline          ACCEPTED
release hold                                  ACTIVE
M0 migration preflight                        COMPLETE
M1 provider abstraction                       PASS
M2 Gemini prerecorded adapter                 PASS / INACTIVE
M3 offline evaluator/contracts/preparation    PASS
first public corpus source tranche            LOCKED
exact real media bytes captured               FALSE
asset SHA-256 evidence                        NOT_CREATED
reference transcript SHA-256                  NOT_CREATED
READY_FOR_AB                                  FALSE
M3 live AssemblyAI/Gemini A/B                 NOT_RUN
CURRENT MILESTONE                             M3 BYTE CAPTURE + SHA-256
M4 new-infrastructure canary                  NOT_STARTED
M5 provider/new-infrastructure cutover        NOT_AUTHORIZED
```

Current M3 transition:

```text
SOURCE_LOCKED_PENDING_BYTE_CAPTURE
 -> capture exact public media bytes
 -> compute byte-exact asset SHA-256
 -> delete temporary raw media / do not retain raw media as CI artifact
 -> prepare and independently review reference transcript evidence
 -> compute reference transcript SHA-256
 -> READY_FOR_AB
 -> same-asset AssemblyAI vs Gemini A/B
 -> manual factual/hallucination review
```

No AssemblyAI/Gemini corpus provider call is authorized merely by this documentation state. Gemini prerecorded remains an inactive candidate until later evidence gates and explicit owner decisions pass.

## 7. Current Activation Boundary

Current accepted public Builder state:

```text
Actions: disabled
Apps: disabled
Web search: enabled
Code Interpreter & Data Analysis: enabled
REQUEST LOGGING instruction block: absent
privacy-policy URL required by active public package: no
```

MEDIA BETA has its own isolated closed-beta Action/backend contour. Its existence does not change the public Builder boundary above.

## 8. MEDIA BETA Release Gates

The beta release gates remain independent and on hold:

```text
R1 - merge KRC MEDIA BETA feature work toward main        HOLD
R2 - promote/replace beta backend infrastructure          HOLD
R3 - enable controlled external testers                   HOLD
R4 - public sharing / Store rollout                       HOLD
```

Approval of one gate does not authorize another. The active M3 provider-evaluation work is a technical evidence track, not approval of any release gate.

## 9. Modular Agent Platform Transfer

General modular platform work remains in separate `K_Supervisor`.

## 10. Legacy Engineering Identifiers

Stable compatibility identifiers may retain `K_Supervisor`, including `K_SUPERVISOR_CHECKPOINT` and `runtime/k_supervisor.db`.

## 11. Canonical Project Documents

Public/Core documents:

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

Closed-beta MEDIA documentation is maintained in the MEDIA BETA feature/subproject documentation and synchronized by explicit audit/checkpoint records. VoiceBridge KRC-media history files provide implementation and validation evidence but do not replace KRC product-roadmap authority.

## 12. Current Implementation State

```text
Public Core Phase 0-12                       COMPLETE
GPT Store Core publication                   COMPLETE
2026-08-23 public Core runtime hardening     ACCEPTED
Request-log prototype                        IMPLEMENTED / TESTED / RETAINED
Request-log public usage                     DISABLED_DUE_TO_USER_CONSENT_UX
Public repository / Builder sync             COMPLETE
Public Core repository mode                  MAINTENANCE
K-Research & Critic - MEDIA BETA             CLOSED_BETA
MEDIA BETA accepted runtime baseline         A9/A9.10/A10 ACCEPTED
MEDIA BETA release state                     RELEASE_HOLD_OWNER_TESTING
Gemini prerecorded migration                 M3 ACTIVE
Current MEDIA BETA engineering milestone     M3 BYTE CAPTURE + SHA-256
M3 live A/B                                  NOT_RUN
Public Core changed by current beta work     NO
```
