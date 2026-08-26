# A10 Copy-Safe Claim Table Runtime Acceptance

Status: RUNTIME_ACCEPTED
Date: 2026-08-26
Scope: isolated owner-only `K-Research & Critic - MEDIA BETA` runtime.

## Acceptance target

Fresh private-GPT fact-check of:

`https://t.me/techcrimes/12107`

Mode: verify facts/claims.

The owner applied Builder package `0.9.1-beta-a10`, started a new chat, reached the normal CriticProfile gate and selected `1` to approve/run.

## Observed runtime evidence

The final report rendered `ПІДСУМОК ЗА ТВЕРДЖЕННЯМИ` as four distinct visible columns:

- `Твердження`;
- `Потрібно`;
- `Отримано незалежних`;
- `Виняток`.

The rendered table contained four material claims with the following accounting:

1. square-drive purpose: required `1`, achieved `3`, exception `NONE`;
2. larger socket implies larger drive: required `1`, achieved `2`, exception `NONE`;
3. pipe wrench as normal socket drive: required `1`, achieved `2`, exception `NONE`;
4. improvised construction is workable/safe: required `1`, achieved `0`, exception `SHORTFALL`.

The report preserved the real `0/1 - SHORTFALL` and ended `ЗАВЕРШЕНО З ОБМЕЖЕННЯМИ` rather than converting the shortfall into an unconditional PASS.

Media accounting shown in the report remained `53 s` media / `53 s` STT / `0` credits.

## Copy-safe runtime gate

The first A10 runtime attempt proved that ChatGPT can visually render the normal Markdown table correctly but whole-response Copy may serialize the rendered header incorrectly as a collapsed first cell.

The refined Builder package therefore requires a second representation immediately after the rendered table under:

`КОПІЯ ДЛЯ НАДІЙНОГО КОПІЮВАННЯ`

The fresh owner runtime produced the required fenced `text` block. Whole-response Copy preserved the literal pipe-delimited table exactly:

```text
| Твердження | Потрібно | Отримано незалежних | Виняток |
| --- | ---: | ---: | --- |
| 1. Призначення квадратного отвору головки | 1 | 3 | NONE |
| 2. Більша головка означає більший квадрат приводу | 1 | 2 | NONE |
| 3. Трубний ключ як штатний привод головки | 1 | 2 | NONE |
| 4. Саморобна конструкція є працездатною та безпечною | 1 | 0 | SHORTFALL |
```

The copy-safe rows and values match the visible rendered table.

## Acceptance decision

A10 runtime gate: **PASS**.

Accepted facts:

- refined Builder package is applied to the actual private GPT;
- CriticProfile gate remains correct;
- visible claim-summary table renders as four columns;
- copy-safe fenced table survives whole-response Copy with four literal pipe-delimited columns;
- rendered and copy-safe values are identical;
- claim-level required/achieved/exception semantics remain correct;
- a real SHORTFALL remains visible and qualifies final status;
- accepted A9 media routing, credit, privacy and fallback boundaries did not regress in this test;
- no Action/backend schema change was required.

## Remaining UI limitation

The ordinary rendered Markdown table may still be serialized incorrectly by ChatGPT's whole-response Copy function. This is treated as a UI serialization limitation, not a KRC claim-accounting or rendered-table failure, because the owner screenshot shows the normal table visually rendered with four distinct columns.

The required fenced copy-safe duplicate is the accepted mitigation.

## Release boundary

A10 acceptance does **not** authorize:

- merge to KRC `main`;
- production VoiceBridge deployment;
- external tester onboarding;
- public sharing or Store publication.

Those remain separately gated owner decisions.

Final marker:

`A10_COPY_SAFE_CLAIM_TABLE_RUNTIME_ACCEPTED`
