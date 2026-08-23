# GPT_STORE_DEPLOYMENT
Документ визначає основну GPT Store-модель розгортання K-Research & Critic без обов'язкового developer API key.

Version: 1.4
Status: ACTIVE / PUBLIC CORE SYNCHRONIZED
Updated: 2026-08-23

## 1. Decision

K-Research & Critic is GPT Store-first.

Primary runtime policy:

```text
channel: chatgpt_store
model_policy: user_plan
developer_api_key_required: false
external_backend_required_for_research: false
recommended_model: null
allow_user_model_switch: true
apps: false
actions: true
```

The public Core must not depend on a developer-owned API key, mandatory external backend for Research/Critic, or pinned model identifier.

The accepted public package includes one optional best-effort request-log Action. Failure or denial of that Action must not block research.

## 2. Canonical Public Package

```text
gpt_store/manifest.yaml
prompts/GPT_STORE_INSTRUCTIONS.md
gpt_store/checkpoint.py
gpt_store/checkpoint_example.json
scripts/validate_store_package.py
integrations/request_log/openapi.yaml
integrations/request_log/google_apps_script/Code.gs
docs/REQUEST_LOG_MVP.md
docs/PRIVACY_POLICY_REQUEST_LOG.md
docs/REQUEST_LOG_MVP_RUNTIME_ACCEPTANCE_2026-08-23.md
docs/GPT_STORE_PACKAGE.md
```

`prompts/GPT_STORE_INSTRUCTIONS.md` is the repository copy of the current accepted public Builder instructions.

## 3. Current Builder Workflow

```text
new substantive request
 -> best-effort `logRequest`
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

Standalone workflow replies such as `1`, `2`, `3` do not trigger a new `logRequest` row.

## 4. Request Log Deployment

Accepted implementation:

```text
GPT Action `logRequest`
 -> Google Apps Script Web App
 -> Google Sheet `K-Research & Critic — Request Log`
```

Builder configuration:

```text
Authentication: None
OpenAPI: integrations/request_log/openapi.yaml
Privacy Policy: docs/PRIVACY_POLICY_REQUEST_LOG.md
```

The GPT sends only a generalized topic up to 160 characters. The server records sequential number, Kyiv date/time, `user_name=none`, and generalized topic.

The full prompt, response and CriticProfile are not intentionally logged.

## 5. Current Evidence Contract

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

## 6. Critic and Revision Contract

Critic audits source authority, independence, freshness, claim support, contradictions, missing topics, evidence/conclusion consistency, claim-level cross-check compliance and evidence-origin traceability.

Maximum revision loop: three iterations. Unresolved problems finish as `COMPLETED_WITH_LIMITATIONS`.

## 7. Language Contract

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

## 8. Persistence and Memory Boundary

The public Core uses conversation-local workflow state plus explicit checkpoint/recovery artifacts when requested.

Checkpoint marker:

```text
K_SUPERVISOR_CHECKPOINT
```

Schema version remains `1.0`.

Checkpoint creation is explicit-request only. Normal profile gates and final reports do not auto-create checkpoints.

The Google Sheet request log is separate optional observability and is not conversation memory.

## 9. Public Runtime Acceptance

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
request-log Builder Action                   PASS
NEW-chat request -> one Sheet row            PASS
standalone `1` -> no extra row               PASS
```

Manifest records:

```text
latest_core_runtime_regression_passed_at: 2026-08-23
criticprofile_two_stage_gate_runtime_accepted: true
cross_check_claim_level_runtime_accepted: true
cross_check_traceability_runtime_accepted: true
report_label_localization_runtime_accepted: true
request_log_runtime_accepted: true
repository_matches_current_public_builder: true
```

## 10. Validation

Static package validation:

```text
python -m scripts.validate_store_package
python -m pytest
```

Repository CI is configured on both push and pull_request and also runs dependency integrity, Ruff correctness, Mypy typed-boundary checks, repository policy validation and coverage.

## 11. Publication Boundary

The product remains published. Manual Builder synchronization is the actual deployment step for instruction/Action changes; GitHub commits do not automatically update the Custom GPT.

Any future public Builder change must be:

```text
implemented in repository
statically validated
manually synchronized to Builder
validated in a NEW chat
recorded as the new public baseline
```

## 12. Optional Standalone Runtime

The Python/provider runtime remains an optional engineering/reference implementation with stable legacy identifiers. It does not define the public Builder behavior unless explicitly synchronized through the public package contract.
