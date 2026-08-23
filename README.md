# K-Research & Critic
Базовий опис завершеного production-продукту K-Research & Critic для дослідження та незалежної перевірки.

Version: 1.2
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

Stable legacy engineering identifiers intentionally retained for compatibility include:

```text
Checkpoint marker: K_SUPERVISOR_CHECKPOINT
Standalone database: runtime/k_supervisor.db
```

## Current Public Core Status

The actual public Builder runtime was revalidated on 2026-08-23 and the accepted Core instructions are synchronized to repository `main`.

```text
Two-stage CriticProfile gate                       PASS
Risk-based cross-check floors                      PASS
Claim-level required/achieved/exception            PASS
Visible SHORTFALL                                  PASS
Evidence-origin traceability                       PASS
Systematic-review double-counting protection       PASS
Critic REVISE -> PASS loop                         PASS
Ukrainian headings/table/profile-field localization PASS
Repository main / public Builder Core sync         COMPLETE
```

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

The profile is not displayed automatically before the first gate. No independent research starts before explicit approval.

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

CriticProfile field labels are also localized. Canonical internal keys remain internal unless explicitly requested.

## Product Boundary

```text
GPT Store Edition
  - public ChatGPT product
  - no developer-owned API key required
  - no mandatory external backend
  - Apps disabled
  - Actions disabled
  - no pinned model identifier
  - user-plan model policy
```

The Python/SQLite/provider implementation remains available as an optional standalone engineering reference runtime. It is not a dependency of the public Store path.

## GPT Store Package

Canonical package files:

```text
gpt_store/manifest.yaml
prompts/GPT_STORE_INSTRUCTIONS.md
gpt_store/checkpoint.py
gpt_store/checkpoint_example.json
scripts/validate_store_package.py
docs/GPT_STORE_DEPLOYMENT.md
docs/GPT_STORE_PACKAGE.md
```

Production package state includes:

```text
publication_state: published
production_smoke_test_passed: true
latest_core_runtime_regression_passed_at: 2026-08-23
repository_matches_current_public_builder: true
```

## Checkpoint and Recovery

Cross-chat continuity uses the explicit user-controlled checkpoint marker:

```text
K_SUPERVISOR_CHECKPOINT
```

Checkpoint creation is explicit-request only. The normal profile gate and final report do not auto-create checkpoints.

## Quality Baseline

CI is configured for push and pull requests and includes:

```text
Python 3.13 full pytest suite
Python 3.14 full pytest suite
python -m pip check
python -m ruff check . --select E9,F63,F7,F82
python -m mypy models config gpt_store
python -m scripts.validate_repository
python -m scripts.validate_store_package
coverage gate
```

## User Guide

Ukrainian quick-start guide for first-time users:

[Open the Ukrainian user guide](docs/K_RESEARCH_CRITIC_USER_GUIDE_UK.pdf)

## Optional Local / Standalone Setup

```text
git clone https://github.com/kolemasakar/K_Research_Critic.git
cd K_Research_Critic
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m pytest
```

## Maintenance Policy

Allowed work here:

```text
bug fixes
security fixes
GPT Store compatibility updates
OpenAI platform compatibility updates
regression fixes
documentation corrections
narrow UX improvements
narrow analytics/observability improvements after privacy and architecture approval
maintenance releases v1.0.1, v1.0.2, ...
```

The planned request-accounting improvement is documented in `docs/ROADMAP.md` and is not implemented yet.

General modular multi-agent platform development belongs to the separate `K_Supervisor` project.

## Canonical Documentation

```text
docs/PROJECT_FILE_STANDARD.md
docs/ARCHITECTURE.md
docs/ROADMAP.md
docs/AGENT_INTERFACE.md
docs/DATA_MODELS.md
docs/RESEARCH_WORKFLOW.md
docs/CONFIGURATION.md
docs/TEST_PLAN.md
docs/CI_QUALITY.md
docs/HYBRID_RESOLVER_PLAN.md
docs/PERSISTENCE.md
docs/GPT_STORE_DEPLOYMENT.md
docs/GPT_STORE_PACKAGE.md
docs/LOGGING.md
```
