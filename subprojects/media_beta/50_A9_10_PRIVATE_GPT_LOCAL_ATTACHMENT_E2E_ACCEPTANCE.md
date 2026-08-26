# A9.10 Private GPT Local Attachment E2E Acceptance

Status: PRIVATE_GPT_E2E_ACCEPTED
Date: 2026-08-26
Scope: private owner-only MEDIA BETA only

## Acceptance result

A fresh private `K-Research & Critic - MEDIA BETA` conversation completed the full zero-client local attachment path with a real MP4 attachment of approximately 5 MB.

User request:

`Перевірити факти/твердження у прикріпленому відео.`

Observed end-to-end flow:

```text
local MP4 attachment
 -> startManagedAttachmentTranscription
 -> trusted OpenAI attachment transport
 -> AssemblyAI
 -> durable KRCM transcript/segments
 -> CriticProfile gate
 -> explicit owner approval with `1`
 -> Research
 -> Critic
 -> localized final report
```

The private GPT reached the canonical CriticProfile gate before independent research:

```text
Профіль збору і критики успішно створено.
1 - виконати аналіз одразу.
2 - переглянути і відредагувати профіль збору і критики.
3 - скасувати дослідження.
```

The owner selected `1`. Research/Critic then completed and returned a Ukrainian final fact-check report.

## Runtime transcription evidence

The final report recorded:
- source: local attachment;
- STT provider: AssemblyAI;
- detected language: Russian;
- language confidence: `0.9984`;
- media duration: `70.668 s`;
- STT accounting: `71 s`;
- retrieval/provider credits reported: `0`;
- durable transcript segment count: `2`;
- approximate segment recognition confidence: `0.861` and `0.869`.

The source transcript was explicitly treated as evidence of what the video said, not as proof that the claims were true.

## Research/Critic acceptance evidence

The final report contained all required major sections:
- `ФІНАЛЬНИЙ ЗВІТ`;
- `ПЕРЕВІРКА ТВЕРДЖЕНЬ`;
- `ПІДСУМОК ЗА ТВЕРДЖЕННЯМИ`;
- `ПРОТОКОЛ ПЕРЕВІРКИ`.

Seven material claims were evaluated with localized verdicts, visible confidence and claim-level cross-check accounting.

The report preserved a real evidence shortfall:
- claim 5, `10 хвилин = -1/3 підйому`;
- cross-check `0/1 - SHORTFALL`;
- the report did not represent this claim as verified.

The final report recorded:
- CriticProfile risk level `MEDIUM`;
- minimum cross-check requirement `1` per material claim;
- two Critic iterations;
- reliability score `88/100`;
- final status `COMPLETED_WITH_LIMITATIONS`.

This is consistent with the accepted claim-level shortfall and traceability contract.

## Privacy and UX boundary

PASS:
- no Helper was required;
- no local client or browser extension was required;
- no user beta code was requested;
- no platform login/cookies/session were requested;
- no KRCM Job ID was exposed in the user-visible report;
- no OpenAI file ID or signed attachment URL was exposed;
- no provider credential or backend secret was exposed;
- local attachment retrieval itself reported zero credits.

## Non-blocking presentation observation

The copied Markdown representation of the claim-summary table again showed a malformed header row in the first column, while the seven data rows and `required / achieved / exception` values remained readable and internally consistent.

This is a presentation defect only. It does not invalidate attachment transport, transcription, CriticProfile gating, Research/Critic execution or claim-level shortfall acceptance. Keep it as a later formatting hardening item rather than reopening A9.10 ingestion.

## Gate disposition

### Gate 1 - Action/Builder package
PASS.

`startManagedAttachmentTranscription` was present in the actual private GPT Action schema.

### Gate 2 - attachment transport
PASS.

Previously accepted by the real `openaiFileIdRefs` transport probe and recorded in `49_A9_10_ATTACHMENT_TRANSPORT_RUNTIME_ACCEPTANCE.md`.

### Gate 3 - full ingestion and durable transcription
PASS.

The real local MP4 reached AssemblyAI and produced durable transcript segments consumed by the private GPT workflow.

### Gate 4 - private GPT Research/Critic E2E
PASS.

The actual private GPT completed CriticProfile approval, Research/Critic and the localized final report.

## Decision

A9.10 local audio/video attachment ingress is accepted for the private owner-only MEDIA BETA.

Canonical state marker:

`A9_10_ATTACHMENT_PRIVATE_GPT_E2E_ACCEPTED`

This acceptance does not authorize public sharing, external tester rollout, production VoiceBridge promotion, repository `main` merge, paid Telegram retrieval, or paid Facebook fallback. Those boundaries remain unchanged until separately authorized.
