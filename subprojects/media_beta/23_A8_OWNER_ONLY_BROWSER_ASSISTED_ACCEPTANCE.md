# A8 Owner-Only Browser-Assisted Acceptance

Version: 1.0
Status: PASS / BASELINE ACCEPTED
Accepted: 2026-08-20

## Scope

This record closes the private owner-operated browser-assisted baseline. It does NOT declare the final zero-client product complete.

## Accepted live path

```text
private K-Research & Critic - MEDIA BETA GPT
 -> public YouTube URL
 -> owner-designated beta credential
 -> Builder Action
 -> KRCC job
 -> Helper 0.2.2
 -> YouTube captions-first intake
 -> GPT status + complete transcript retrieval
 -> DRAFT CriticProfile
 -> owner APPROVE
 -> independent Research
 -> Critic/revision
 -> final user-facing report
```

## Live evidence

Accepted owner-only run included:
- private GPT access mode `Only me`;
- owner-designated credential accepted by the backend;
- KRCC job creation through the actual private GPT, not Builder Preview;
- Helper 0.2.2 captions-first completion;
- Russian auto-generated YouTube captions accepted while the GPT response language remained Ukrainian;
- CriticProfile approval gate respected;
- independent web research only after owner approval;
- final claim-verification output completed.

## UX regressions accepted after the live run

The following instruction defects were identified and corrected on the active KRC branch:
- Ukrainian is now mandatory by default unless the user explicitly requests another response language;
- source/video/transcript language must not switch the response language;
- user-facing verdict labels are localized to the report language;
- Ukrainian verdict labels include `ПІДТВЕРДЖЕНО`, `ЧАСТКОВО ПІДТВЕРДЖЕНО`, `НЕ ПІДТВЕРДЖЕНО`, `СУПЕРЕЧИТЬ ДЖЕРЕЛАМ`, `ВВОДИТЬ В ОМАНУ`, `НЕМОЖЛИВО ПЕРЕВІРИТИ`, `ДУМКА`;
- each material claim must receive exactly one canonical verdict;
- displayed final-report section headings are localized (`ФІНАЛЬНИЙ ЗВІТ`, `ПЕРЕВІРКА ТВЕРДЖЕНЬ`, `ПРОТОКОЛ ПЕРЕВІРКИ`);
- Builder instructions were re-compacted below the Builder character limit and CI remained green.

## Product interpretation

A8 proves that the current private product works end-to-end when browser-assisted intake is available.

It does not meet the owner's final UX target because the user must still open the same YouTube video and run Helper 0.2.2.

Therefore the final private-product completion gate moves to A9 Zero-Client YouTube Ingestion.

## Acceptance marker

`A8_OWNER_ONLY_BROWSER_ASSISTED_BASELINE_PASS`
