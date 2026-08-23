# GPT_STORE_PACKAGE
Документ визначає production-пакет K-Research & Critic, перевірки релізу та maintenance-gates для GPT Store.

Version: 2.1
Status: MAINTENANCE / REQUEST-LOG DISABLEMENT PENDING BUILDER SYNC
Updated: 2026-08-23

## 1. Purpose

This document is the operator-facing packaging specification for the published K-Research & Critic Custom GPT.

Repository:

```text
kolemasakar/K_Research_Critic
```

Target public Core invariants:

```text
no developer API key
no mandatory external backend
no active Actions
no Apps
no pinned model
user-plan model policy
built-in ChatGPT capabilities for the core path
Ukrainian user-facing language by default
```

The previously accepted request-log Action is intentionally disabled because the platform-controlled external Action consent screen interrupts the normal public UX.

## 2. Active Package Files

```text
gpt_store/manifest.yaml
prompts/GPT_STORE_INSTRUCTIONS.md
gpt_store/checkpoint.py
gpt_store/checkpoint_example.json
scripts/validate_store_package.py
docs/GPT_STORE_PACKAGE.md
```

Retained historical request-log prototype resources:

```text
integrations/request_log/openapi.yaml
integrations/request_log/google_apps_script/Code.gs
prompts/GPT_STORE_REQUEST_LOG_ADDENDUM.md
docs/PRIVACY_POLICY_REQUEST_LOG.md
docs/REQUEST_LOG_MVP.md
docs/REQUEST_LOG_MVP_RUNTIME_ACCEPTANCE_2026-08-23.md
```

These retained resources are not part of the active target Builder configuration.

## 3. Target Builder Configuration

### Name

```text
K-Research & Critic
```

### Default language

```text
uk-UA
```

### Capabilities

Enable:

```text
Web search
Code Interpreter & Data Analysis
```

Disable:

```text
Image generation
Apps
Actions
```

No external backend or privacy-policy URL is required by the target active public package.

## 4. Target Public Workflow

```text
new substantive request
 -> CriticProfile created internally
 -> first gate: direct run / profile review-edit / cancel
 -> explicit profile approval
 -> Research
 -> Critic
 -> REVISE when required
 -> final report
 -> review protocol
```

The request-log call is no longer part of the target public workflow.

## 5. Risk and Claim-Level Cross-Check Contract

Risk floors:

```text
LOW >= 0
MEDIUM >= 1
HIGH >= 2
CRITICAL >= 3
```

For every material factual claim the runtime maintains:

```text
required
achieved_independent
exception = NONE | SHORTFALL
```

Independence is based on underlying evidence origins, not URL count. Duplicate/derivative reporting does not increase `achieved_independent`. A systematic review/meta-analysis counts as one evidence origin unless specific underlying studies were independently inspected and cited.

## 6. Traceability and Critic Contract

Every evidence origin counted in `achieved_independent` must be visible and traceable to the relevant material claim. A PASS count cannot exceed the number of visibly traceable independent evidence origins.

Critic checks claim-level ledgers, source authority, independence, freshness, support, contradictions, missing topics, evidence/conclusion consistency and traceability. Maximum revision loop: three iterations. Unresolved issues finish as `COMPLETED_WITH_LIMITATIONS`.

## 7. User-Visible Language Contract

Ukrainian is the default. Required labels where applicable:

```text
ФІНАЛЬНИЙ ЗВІТ
ПЕРЕВІРКА ТВЕРДЖЕНЬ
ПРОТОКОЛ ПЕРЕВІРКИ
ПІДСУМОК ЗА ТВЕРДЖЕННЯМИ
Твердження | Потрібно | Отримано незалежних | Виняток
```

## 8. Historical Request Log Result

The Request Log MVP was implemented and runtime-accepted on 2026-08-23. The implementation itself worked correctly, including one substantive request -> one row and workflow-reply de-duplication.

It is now disabled for product UX reasons, not because of a technical failure.

Current markers:

```text
historical request-log runtime acceptance: PRESERVED
public request-log target: DISABLED
prototype resources: RETAINED
```

## 9. Static Validation

```text
python -m scripts.validate_store_package
python -m pytest
```

## 10. Current Synchronization State

Repository target:

```text
actions: false
REQUEST LOGGING removed from Builder instructions
privacy-policy URL not required by active package
```

Current public Builder still requires manual synchronization. Until the owner removes the Action and replaces Instructions, the manifest intentionally records:

```text
repository_matches_current_public_builder: false
```

After manual Builder sync, run one NEW-chat smoke test confirming that no `script.google.com` consent screen appears before the CriticProfile gate.

## 11. Maintenance Boundary

Any later Builder change is a product update and must be revalidated before being treated as the public baseline.
