# K-Research & Critic
Базовий опис завершеного production-продукту K-Research & Critic для дослідження та незалежної перевірки.

Version: 1.4
Status: PRODUCTION / MAINTENANCE
Updated: 2026-08-23

## Overview

K-Research & Critic is a published GPT Store product for structured research, independent critique, autonomous revision, and sourced final reporting.

Repository:

```text
kolemasakar/K_Research_Critic
```

Public product:

```text
K-Research & Critic
```

## Current Public Core Status

Accepted Core behavior:

```text
Two-stage CriticProfile gate                        PASS
Risk-based cross-check floors                       PASS
Claim-level required/achieved/exception             PASS
Visible SHORTFALL                                   PASS
Evidence-origin traceability                        PASS
Systematic-review double-counting protection        PASS
Critic REVISE -> PASS loop                          PASS
Ukrainian headings/table/profile-field localization PASS
```

A previously accepted request-log Action is now being removed from the public product because ChatGPT's external Action consent screen interrupts the normal UX for new users.

Target public state:

```text
Actions                                             DISABLED
automatic request logging                           DISABLED
Apps                                                DISABLED
```

The repository already contains the target no-Action Instructions. Manual Builder synchronization is still required before repository/public Builder sync can be marked complete.

## Public Workflow

```text
User request
   |
   v
CriticProfile created internally
   |
   v
1 - run now / 2 - review-edit / 3 - cancel
   |
   +-- 2 --> localized CriticProfile --> approve/edit/cancel gate
   |
   v
Explicit approval
   |
   v
Research
   |
   v
Critic
   |
   +---- REVISE ----> Research
   |
   +---- PASS ------> Final report + Review protocol
```

No request-log Action belongs in the target public workflow.

Risk floors:

```text
LOW >= 0
MEDIUM >= 1
HIGH >= 2
CRITICAL >= 3
```

Each material factual claim is audited independently. Evidence counted in `achieved_independent` must be visibly traceable to that claim; derivative reporting of the same underlying evidence is not double-counted.

## Language Contract

Ukrainian is the default user-facing report language unless the user explicitly requests another language.

Required Ukrainian labels include, where applicable:

```text
ФІНАЛЬНИЙ ЗВІТ
ПЕРЕВІРКА ТВЕРДЖЕНЬ
ПРОТОКОЛ ПЕРЕВІРКИ
ПІДСУМОК ЗА ТВЕРДЖЕННЯМИ
Твердження | Потрібно | Отримано незалежних | Виняток
```

## Product Boundary

```text
GPT Store Edition
  - public ChatGPT product
  - no developer-owned API key required
  - no mandatory external backend
  - Apps disabled
  - Actions disabled in target public configuration
  - no pinned model identifier
  - user-plan model policy
```

## Request Log Prototype

The Request Log MVP was implemented and runtime-tested successfully on 2026-08-23.

Historical implementation:

```text
Public GPT
 -> logRequest Action
 -> Google Apps Script
 -> Google Sheet `K-Research & Critic — Request Log`
```

It is now classified as:

```text
IMPLEMENTED / TESTED / DISABLED_DUE_TO_USER_CONSENT_UX
```

The implementation remains in the repository for reference and possible future reuse outside the public Action-consent path. It is not part of the target active Builder configuration.

## GPT Store Package

Active target package files:

```text
gpt_store/manifest.yaml
prompts/GPT_STORE_INSTRUCTIONS.md
gpt_store/checkpoint.py
gpt_store/checkpoint_example.json
scripts/validate_store_package.py
docs/GPT_STORE_DEPLOYMENT.md
docs/GPT_STORE_PACKAGE.md
```

Retained request-log prototype documentation/resources:

```text
integrations/request_log/openapi.yaml
integrations/request_log/google_apps_script/Code.gs
prompts/GPT_STORE_REQUEST_LOG_ADDENDUM.md
docs/REQUEST_LOG_MVP.md
docs/PRIVACY_POLICY_REQUEST_LOG.md
docs/REQUEST_LOG_MVP_RUNTIME_ACCEPTANCE_2026-08-23.md
```

## Current Synchronization State

```text
repository target actions=false                 COMPLETE
request logging removed from repo Instructions COMPLETE
public Builder Action removal                  PENDING MANUAL STEP
public Builder Instructions resync             PENDING MANUAL STEP
post-disable NEW-chat smoke test               PENDING
repository_matches_current_public_builder      false until completion
```

## Checkpoint and Recovery

Cross-chat continuity uses the explicit user-controlled checkpoint marker:

```text
K_SUPERVISOR_CHECKPOINT
```

Checkpoint creation is explicit-request only.

## Quality Baseline

CI is configured for push and pull requests and includes Python 3.13/3.14 tests, dependency integrity, Ruff, mypy, repository policy, Store package validation and coverage.

## User Guide

[Open the Ukrainian user guide](docs/K_RESEARCH_CRITIC_USER_GUIDE_UK.pdf)

## Maintenance Policy

Allowed work here:

```text
bug fixes
security fixes
GPT Store/OpenAI compatibility updates
regression fixes
documentation corrections
narrow UX improvements
maintenance releases
```

General modular multi-agent platform development belongs to the separate `K_Supervisor` project.
