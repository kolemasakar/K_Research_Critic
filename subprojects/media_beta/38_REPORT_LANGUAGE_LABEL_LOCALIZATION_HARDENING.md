# Report Language Label Localization Hardening

Version: 1.0
Date: 2026-08-23
Status: IMPLEMENTED_IN_BRANCH_PENDING_BUILDER_RESYNC_RUNTIME

## Trigger

A NEW-chat MEDIA BETA regression after traceability alignment showed that the Research/Critic logic was functioning, but some user-visible labels remained English despite the Ukrainian default report language.

Observed mixed-language output included:
- `Claim-level summary`;
- `Claim`;
- `Required`;
- `Achieved independent`;
- `Exception`;
- raw CriticProfile field keys such as `profile_id`, `risk_level`, `required_cross_checks`, and `approved_at` shown as visible table labels.

The same class of mixed-language labels had also appeared in the main Core regression output. Therefore the fix applies to BOTH Builder instruction sets.

## Required invariant

The selected report language controls ALL user-visible labels, including:
- section headings;
- table titles;
- table column names;
- CriticProfile field labels;
- verdict labels;
- final report and review protocol labels.

Canonical English/internal keys remain internal unless the user explicitly requests them.

For Ukrainian reports use, as applicable:
- `ФІНАЛЬНИЙ ЗВІТ`;
- `ПЕРЕВІРКА ТВЕРДЖЕНЬ`;
- `ПРОТОКОЛ ПЕРЕВІРКИ`;
- `ПІДСУМОК ЗА ТВЕРДЖЕННЯМИ`.

The mandatory claim-level protocol table uses exactly:

```text
Твердження | Потрібно | Отримано незалежних | Виняток
```

Do not expose `Claim-level summary`, `Claim`, `Required`, `Achieved independent`, `Exception`, or raw CriticProfile field keys as Ukrainian user-visible labels.

## Files changed

Main Core:
- `prompts/GPT_STORE_CORE_BUILDER_INSTRUCTIONS.md`;
- `tests/test_core_builder_instructions.py`.

MEDIA BETA:
- `prompts/GPT_STORE_MEDIA_BETA_BUILDER_INSTRUCTIONS.md`;
- `prompts/GPT_STORE_MEDIA_MANAGED_BETA_INSTRUCTIONS.md` version `0.3.6-a9.6`;
- `gpt_store/media_beta_manifest.yaml`;
- `tests/test_claim_level_cross_check_enforcement.py`;
- `tests/test_media_beta_managed_package.py`.

## Runtime disposition

The latest MEDIA BETA regression demonstrated:
- claim-level traceability logic: PASS;
- visible independent-origin counting: PASS;
- systematic-review double-counting protection: PASS;
- mandatory four-column claim-level summary: present;
- default-language label localization: FAIL / REQUIRED_FIX.

Therefore do not treat that run as final acceptance of the complete updated MEDIA BETA contract.

Current markers:

`MEDIA_BETA_TRACEABILITY_LOGIC_RUNTIME = PASS`

`MEDIA_BETA_REPORT_LABEL_LOCALIZATION_CODE = IMPLEMENTED`

`MEDIA_BETA_REPORT_LABEL_LOCALIZATION_RUNTIME = PENDING`

`MEDIA_BETA_TRACEABILITY_HARDENING_RUNTIME = PENDING_FINAL_LANGUAGE_REGRESSION`

For the main Core, previous evidence-origin traceability acceptance remains valid, but the newly hardened label-localization behavior also requires a fresh Builder synchronization and NEW-chat visual regression before its localization runtime marker can be accepted.

## Unchanged boundaries

This hardening does not change:
- media ingestion;
- Supadata pricing or credit gates;
- Action/OpenAPI/authentication;
- YouTube/Instagram acceptance;
- Facebook state;
- repository `main`;
- production VoiceBridge;
- external tester rollout.

No merge is authorized by this change.
