# GPT_STORE_PACKAGE
Документ визначає production-пакет K-Research & Critic, перевірки релізу та maintenance-gates для GPT Store.

Version: 1.9
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
no mandatory external backend
no Actions
no Apps
no pinned model
user-plan model policy
built-in ChatGPT capabilities for the core path
Ukrainian user-facing language by default
```

## 2. Package Files

```text
gpt_store/manifest.yaml
prompts/GPT_STORE_INSTRUCTIONS.md
gpt_store/checkpoint.py
gpt_store/checkpoint_example.json
scripts/validate_store_package.py
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
```

Disable for the public Core package:

```text
Image generation
Apps
Actions
```

No external backend is required by the current public Core.

## 4. Current Public Core Workflow

The accepted workflow is:

```text
request
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

No independent research starts before explicit approval.

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

## 8. Checkpoint and Fresh-Chat Recovery

Cross-chat continuation remains explicit-request only and uses the existing checkpoint contract marked:

```text
K_SUPERVISOR_CHECKPOINT
```

Schema version remains `1.0`. The runtime must never auto-create a checkpoint at a normal profile gate or final report.

## 9. Static Validation

Run after public Core package changes:

```text
python -m scripts.validate_store_package
python -m pytest
```

CI additionally validates repository policy, typed boundaries, lint correctness, dependency integrity and coverage.

## 10. Historical Launch Validation

Initial publication and launch smoke validation completed on 2026-08-14. Manifest retains:

```text
publication_state: published
published_at: 2026-08-14
production_smoke_test_passed: true
production_smoke_tested_at: 2026-08-14
```

These fields preserve the original launch record.

## 11. Current Core Runtime Regression

On 2026-08-23 the actual public `K-Research & Critic` Builder was manually synchronized with the hardened Core instructions and validated in NEW chats.

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
```

Current runtime markers recorded in `gpt_store/manifest.yaml`:

```text
criticprofile_two_stage_gate_runtime_accepted: true
cross_check_claim_level_runtime_accepted: true
cross_check_traceability_runtime_accepted: true
report_label_localization_runtime_accepted: true
repository_matches_current_public_builder: true
```

## 12. Maintenance Boundary

Any later Builder change is a product update and must be revalidated before being treated as the public baseline.

Allowed maintenance includes:

```text
bug/security fixes
OpenAI/ChatGPT compatibility changes
Store-package compatibility changes
regression fixes
small UX improvements
documentation corrections
narrow product analytics/observability improvements after privacy and architecture approval
```

The current public Core must remain independent of mandatory external services unless a separate product decision explicitly changes that invariant.
