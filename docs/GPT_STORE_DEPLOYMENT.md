# GPT_STORE_DEPLOYMENT
Документ визначає основну GPT Store-модель розгортання K-Research & Critic без обов'язкового developer API key.

Version: 1.3
Status: ACTIVE / PUBLIC CORE SYNCHRONIZED
Updated: 2026-08-23

## 1. Decision

K-Research & Critic is GPT Store-first.

Primary runtime policy:

```text
channel: chatgpt_store
model_policy: user_plan
developer_api_key_required: false
external_backend_required: false
recommended_model: null
allow_user_model_switch: true
apps: false
actions: false
```

The public Core must not depend on a developer-owned API key, mandatory external backend, or pinned model identifier.

## 2. Canonical Public Package

```text
gpt_store/manifest.yaml
prompts/GPT_STORE_INSTRUCTIONS.md
gpt_store/checkpoint.py
gpt_store/checkpoint_example.json
scripts/validate_store_package.py
docs/GPT_STORE_PACKAGE.md
```

`prompts/GPT_STORE_INSTRUCTIONS.md` is the repository copy of the current accepted public Builder instructions.

## 3. Current Builder Workflow

```text
request
 -> CriticProfile created internally
 -> first gate: 1 direct run / 2 review-edit / 3 cancel
 -> explicit approval
 -> Research
 -> Critic
 -> revision when needed
 -> final report
 -> review protocol
```

The first gate is:

```text
Профіль збору і критики успішно створено.
1 - виконати аналіз одразу.
2 - переглянути і відредагувати профіль збору і критики.
3 - скасувати дослідження.
```

Option `2` displays the complete localized profile and enters the approve/edit/cancel review gate. No independent research begins before explicit approval.

## 4. Current Evidence Contract

Risk floors:

```text
LOW >= 0
MEDIUM >= 1
HIGH >= 2
CRITICAL >= 3
```

Every material factual claim maintains:

```text
required
achieved_independent
exception = NONE | SHORTFALL
```

Independence is based on underlying evidence origins, not URL count. Duplicate and derivative reporting do not increase the count. A systematic review/meta-analysis counts as one origin unless specific underlying studies were independently inspected and cited.

Every counted evidence origin must be visible and traceable to the relevant claim. A PASS count may not exceed visibly traceable independent evidence origins.

## 5. Critic and Revision Contract

Critic audits:

```text
source authority
independence
freshness
claim support
contradictions
missing topics
evidence/conclusion consistency
claim-level cross-check compliance
evidence-origin traceability
```

Maximum revision loop: three iterations. Unresolved problems finish as `COMPLETED_WITH_LIMITATIONS`.

## 6. Language Contract

Default user-facing language is Ukrainian unless explicitly changed by the user.

For Ukrainian reports use, where applicable:

```text
ФІНАЛЬНИЙ ЗВІТ
ПЕРЕВІРКА ТВЕРДЖЕНЬ
ПРОТОКОЛ ПЕРЕВІРКИ
ПІДСУМОК ЗА ТВЕРДЖЕННЯМИ
Твердження | Потрібно | Отримано незалежних | Виняток
```

CriticProfile field labels also follow the selected report language. Raw canonical keys remain internal unless explicitly requested.

## 7. Persistence and Memory Boundary

The public Core uses conversation-local workflow state plus explicit checkpoint/recovery artifacts when requested.

Checkpoint marker:

```text
K_SUPERVISOR_CHECKPOINT
```

Schema version remains `1.0`.

Checkpoint creation is explicit-request only. Normal profile gates and final reports do not auto-create checkpoints.

The SQLite persistence layer remains part of the optional standalone engineering runtime and is not required by the public GPT Store path.

## 8. Public Core Runtime Acceptance

The actual public Builder was manually synchronized and revalidated in NEW chats on 2026-08-23.

Accepted runtime results:

```text
two-stage CriticProfile gate                 PASS
CRITICAL -> minimum 3 independent checks     PASS
claim-level PASS / SHORTFALL                  PASS
evidence-origin traceability                 PASS
derivative double-counting protection        PASS
Critic REVISE -> PASS                        PASS
Ukrainian headings/table/profile labels      PASS
```

Manifest records:

```text
latest_core_runtime_regression_passed_at: 2026-08-23
criticprofile_two_stage_gate_runtime_accepted: true
cross_check_claim_level_runtime_accepted: true
cross_check_traceability_runtime_accepted: true
report_label_localization_runtime_accepted: true
repository_matches_current_public_builder: true
```

## 9. Validation

Static package validation:

```text
python -m scripts.validate_store_package
python -m pytest
```

Repository CI is configured on both push and pull_request and also runs dependency integrity, Ruff correctness, Mypy typed-boundary checks, repository policy validation and coverage.

## 10. Publication Boundary

The product remains published. Manual Builder synchronization is the actual deployment step for instruction changes; GitHub commits do not automatically update the Custom GPT.

Any future public Builder change must be:

```text
implemented in repository
statically validated
manually synchronized to Builder
validated in a NEW chat
recorded as the new public baseline
```

The public Core currently has no Actions or mandatory external backend. Any future request-accounting feature that requires either is a separate architecture/privacy decision and must not be introduced implicitly.

## 11. Optional Standalone Runtime

The Python/provider runtime remains an optional engineering/reference implementation with stable legacy identifiers. It does not define the public Builder behavior unless explicitly synchronized through the public package contract.
