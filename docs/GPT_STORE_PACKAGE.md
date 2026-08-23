# GPT_STORE_PACKAGE
Документ визначає production-пакет K-Research & Critic, перевірки релізу та maintenance-gates для GPT Store.

Version: 2.0
Status: MAINTENANCE / CURRENT PUBLIC CORE SYNCED
Updated: 2026-08-23

## 1. Purpose

This document is the operator-facing packaging specification for the published K-Research & Critic Custom GPT.

Repository:

```text
kolemasakar/K_Research_Critic
```

The public Core follows these invariants:

```text
no developer API key
no mandatory external backend for Research/Critic
one optional request-log Action
no Apps
no pinned model
user-plan model policy
built-in ChatGPT capabilities for the core path
Ukrainian user-facing language by default
```

The request-log Action is optional observability and must remain non-blocking.

## 2. Package Files

```text
gpt_store/manifest.yaml
prompts/GPT_STORE_INSTRUCTIONS.md
gpt_store/checkpoint.py
gpt_store/checkpoint_example.json
scripts/validate_store_package.py
integrations/request_log/openapi.yaml
integrations/request_log/google_apps_script/Code.gs
docs/PRIVACY_POLICY_REQUEST_LOG.md
docs/REQUEST_LOG_MVP.md
docs/REQUEST_LOG_MVP_RUNTIME_ACCEPTANCE_2026-08-23.md
docs/GPT_STORE_PACKAGE.md
```

`prompts/GPT_STORE_INSTRUCTIONS.md` is the canonical repository copy of the currently accepted public Builder instructions. The manifest records the accepted runtime contract.

## 3. Builder Configuration

### Name

```text
K-Research & Critic
```

### Default language

```text
uk-UA
```

### Recommended model

Leave the recommended model unset. The workflow must not depend on a named model.

### Capabilities

Enable:

```text
Web search
Code Interpreter & Data Analysis
Actions: request-log `logRequest`
```

Disable:

```text
Image generation
Apps
```

The Action uses Authentication=None and the public privacy-policy URL in `docs/PRIVACY_POLICY_REQUEST_LOG.md`.

No external backend is mandatory for Research/Critic execution. If request logging is unavailable or denied, the normal workflow continues.

## 4. Current Public Core Workflow

The accepted workflow is:

```text
new substantive request
 -> best-effort generalized-topic logRequest
 -> CriticProfile created internally
 -> first gate: direct run / profile review-edit / cancel
 -> explicit profile approval
 -> Research
 -> Critic
 -> REVISE when required
 -> final report
 -> review protocol
```

The profile is NOT displayed automatically.

First gate:

```text
Профіль збору і критики успішно створено.
1 - виконати аналіз одразу.
2 - переглянути і відредагувати профіль збору і критики.
3 - скасувати дослідження.
```

If option `2` is selected, the complete profile is displayed with localized field labels, followed by:

```text
1 - прийняти профіль, виконати дослідження.
2 - редагувати профіль.
3 - скасувати дослідження.
```

No independent research starts before explicit approval. Standalone workflow replies such as `1`, `2`, `3` are not new request-log rows.

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

If achieved evidence is below the approved requirement, the report must expose `SHORTFALL`, explain the limitation, reduce confidence as appropriate, and qualify the conclusion.

## 6. Traceability and Critic Contract

Every evidence origin counted in `achieved_independent` must be visible and traceable to the relevant material claim in the final user-facing report.

A PASS count cannot exceed the number of visibly traceable independent evidence origins.

Critic checks claim-level ledgers, source authority, independence, freshness, support, contradictions, missing topics, evidence/conclusion consistency and traceability. Maximum revision loop: three iterations. Unresolved issues finish as `COMPLETED_WITH_LIMITATIONS`.

## 7. User-Visible Language Contract

The selected report language controls all user-visible headings, table titles/columns, CriticProfile field labels and verdict labels. Ukrainian is the default.

Required Ukrainian headings where applicable:

```text
ФІНАЛЬНИЙ ЗВІТ
ПЕРЕВІРКА ТВЕРДЖЕНЬ
ПРОТОКОЛ ПЕРЕВІРКИ
ПІДСУМОК ЗА ТВЕРДЖЕННЯМИ
```

Required claim-summary columns:

```text
Твердження | Потрібно | Отримано незалежних | Виняток
```

Canonical English/internal keys stay internal unless explicitly requested.

## 8. Request Log Contract

For each NEW substantive request, the GPT sends only a generalized topic up to 160 characters to `logRequest` exactly once before the CriticProfile gate.

The server writes:

```text
request number
date
time
user_name=none
generalized request topic
```

The full prompt, answer, CriticProfile and hidden reasoning are not intentionally stored. Logging is best-effort and non-blocking.

Runtime acceptance on 2026-08-23 verified:

```text
Builder direct Action write: PASS
Published NEW-chat write: PASS
request_number 2: PASS
standalone `1` -> no row 3: PASS
```

## 9. Checkpoint and Fresh-Chat Recovery

Cross-chat continuation remains explicit-request only and uses the existing checkpoint contract marked:

```text
K_SUPERVISOR_CHECKPOINT
```

Schema version remains `1.0`. The runtime must never auto-create a checkpoint at a normal profile gate or final report.

## 10. Static Validation

Run after public Core package changes:

```text
python -m scripts.validate_store_package
python -m pytest
```

CI additionally validates repository policy, typed boundaries, lint correctness, dependency integrity and coverage.

## 11. Historical Launch Validation

Initial publication and launch smoke validation completed on 2026-08-14. Manifest retains:

```text
publication_state: published
published_at: 2026-08-14
production_smoke_test_passed: true
production_smoke_tested_at: 2026-08-14
```

These fields preserve the original launch record.

## 12. Current Runtime Acceptance

On 2026-08-23 the actual public `K-Research & Critic` Builder was synchronized and validated in NEW chats.

Accepted behavior includes:

```text
two-stage CriticProfile gate: PASS
CRITICAL -> required_cross_checks >= 3: PASS
claim-level PASS/SHORTFALL: PASS
evidence-origin traceability: PASS
systematic-review double-counting protection: PASS
mandatory claim-level summary: PASS
Ukrainian headings/columns/profile labels: PASS
REVISE -> PASS Critic cycle: PASS
COMPLETED_WITH_LIMITATIONS when evidence remains insufficient: PASS
request-log Action: PASS
request-log one request -> one row: PASS
workflow-reply de-duplication: PASS
```

Current runtime markers recorded in `gpt_store/manifest.yaml`:

```text
criticprofile_two_stage_gate_runtime_accepted: true
cross_check_claim_level_runtime_accepted: true
cross_check_traceability_runtime_accepted: true
report_label_localization_runtime_accepted: true
request_log_runtime_accepted: true
repository_matches_current_public_builder: true
```

## 13. Maintenance Boundary

Any later Builder change is a product update and must be revalidated before being treated as the public baseline.

The Research/Critic core must remain independent of mandatory external services. The accepted request-log Action is optional observability only.
