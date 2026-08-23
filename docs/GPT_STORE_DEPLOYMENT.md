# GPT_STORE_DEPLOYMENT
Документ визначає основну GPT Store-модель розгортання K-Research & Critic без обов'язкового developer API key.

Version: 1.5
Status: REQUEST-LOG DISABLEMENT PENDING MANUAL BUILDER SYNC
Updated: 2026-08-23

## 1. Decision

K-Research & Critic is GPT Store-first.

Target runtime policy:

```text
channel: chatgpt_store
model_policy: user_plan
developer_api_key_required: false
external_backend_required_for_research: false
recommended_model: null
allow_user_model_switch: true
apps: false
actions: false
```

The request-log Action is intentionally removed from the target public configuration because ChatGPT's external-Action consent screen interrupts the normal UX for new users.

## 2. Canonical Active Public Package

```text
gpt_store/manifest.yaml
prompts/GPT_STORE_INSTRUCTIONS.md
gpt_store/checkpoint.py
gpt_store/checkpoint_example.json
scripts/validate_store_package.py
docs/GPT_STORE_PACKAGE.md
```

The request-log implementation remains in the repository as a tested inactive prototype.

## 3. Target Builder Workflow

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

No automatic `logRequest` call occurs in the target public Builder.

## 4. Historical Request Log Prototype

Historical implementation:

```text
GPT Action `logRequest`
 -> Google Apps Script Web App
 -> Google Sheet `K-Research & Critic — Request Log`
```

It passed technical and NEW-chat runtime tests on 2026-08-23. The prototype is retained but disabled due to user-consent UX, not technical failure.

Retained resources:

```text
integrations/request_log/openapi.yaml
integrations/request_log/google_apps_script/Code.gs
prompts/GPT_STORE_REQUEST_LOG_ADDENDUM.md
docs/REQUEST_LOG_MVP.md
docs/PRIVACY_POLICY_REQUEST_LOG.md
docs/REQUEST_LOG_MVP_RUNTIME_ACCEPTANCE_2026-08-23.md
```

## 5. Evidence Contract

Risk floors:

```text
LOW >= 0
MEDIUM >= 1
HIGH >= 2
CRITICAL >= 3
```

Every material factual claim maintains required, achieved_independent and exception=NONE|SHORTFALL. Count independent evidence origins, not URLs. Every counted origin must remain visibly traceable to the relevant claim.

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

## 7. Current Manual Deployment Step

GitHub commits do not automatically update the Custom GPT.

Required manual Builder operations:

```text
1. remove the configured `logRequest` Action;
2. replace Builder Instructions with current `main/prompts/GPT_STORE_INSTRUCTIONS.md`;
3. save/update the public GPT;
4. open a NEW chat and verify that no script.google.com consent screen appears;
5. verify the normal CriticProfile gate appears directly;
6. only then mark repository/public Builder synchronization complete.
```

Until this is done:

```text
repository target actions=false
actual public Builder may still contain Action
repository_matches_current_public_builder=false
```

## 8. Validation

Static package validation:

```text
python -m scripts.validate_store_package
python -m pytest
```

## 9. Publication Boundary

The product remains published. Any future external Action must be separately approved with its user-consent UX treated as part of the product design.
