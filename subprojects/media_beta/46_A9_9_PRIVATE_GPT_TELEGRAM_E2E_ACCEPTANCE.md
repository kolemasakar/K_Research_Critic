# A9.9 Private GPT Telegram E2E Acceptance

Owner-only NEW-chat acceptance of the Telegram public-video zero-client path in the actual private `K-Research & Critic - MEDIA BETA` GPT.

Status: ACCEPTED
Date: 2026-08-26
Scope: actual private Custom GPT + isolated VoiceBridge MEDIA BETA runtime

## Acceptance target

Positive-path public Telegram post:

`https://t.me/techcrimes/12107`

Requested mode:

`Перевірити факти/твердження`

The test was performed in a fresh private-GPT conversation after Builder instructions and Action schema `0.5.0-a9.9` were applied.

## Observed private-GPT flow

The GPT reached the CriticProfile gate, proving that Telegram media intake/transcription succeeded sufficiently to construct the claim inventory and profile before research.

The owner then selected:

`1 - виконати аналіз одразу`

The GPT completed Research/Critic and returned a Ukrainian final fact-check report.

## Runtime evidence visible in final report

The final report disclosed the following safe operational summary:
- source: public Telegram post;
- STT provider: AssemblyAI;
- detected language: English;
- language confidence: `0.9927`;
- segment count: `1`;
- STT audio processed: `53 s`;
- average STT confidence: approximately `0.975`;
- charged credits: `0`.

These values match the independently accepted isolated backend positive-path evidence for the same target:
- `retrieval_provider=telegram_public_web`;
- `provider=assemblyai`;
- `provider_mode=telegram_public_retrieval_stt`;
- `retrieval_credits_charged=0`;
- `credits_charged=0`;
- `stt_seconds_charged=53`;
- `segment_count=1`;
- `transcript_characters=769`;
- provider data deleted;
- durable status/segments reread succeeded;
- duplicate start reused the same durable job.

Backend workflow run: `32969713110`.

## Research/Critic acceptance assertions

PASS:
- Telegram URL was handled through the managed Telegram route rather than being rejected as unsupported;
- media/transcription completed before the CriticProfile gate;
- no Telegram login, password, cookies, MTProto session, bot token, Helper, beta code or manual Job ID was requested;
- no paid Telegram retrieval fallback was offered or used;
- charged credits were `0`;
- explicit profile approval occurred before independent claim research;
- final report language was Ukrainian;
- final report included `ФІНАЛЬНИЙ ЗВІТ`, `ПЕРЕВІРКА ТВЕРДЖЕНЬ`, `ПІДСУМОК ЗА ТВЕРДЖЕННЯМИ`, and `ПРОТОКОЛ ПЕРЕВІРКИ`;
- material claims received localized verdicts;
- claim-level required/achieved/exception accounting was visible;
- real cross-check shortfalls remained explicit (`0/2 - SHORTFALL`) rather than being silently passed;
- source transcript was treated as source content, not proof of truth;
- no KRCM Job ID, backend credential or provider secret was exposed to the user;
- final status was `ЗАВЕРШЕНО З ОБМЕЖЕННЯМИ`, consistent with unresolved physical-fit claims.

## Non-blocking presentation observation

The copied Markdown representation of the claim-summary table showed a malformed header row where the four column labels were visually concatenated. The four-column data rows remained understandable and the required claim-level counts/shortfalls were still present.

Disposition: non-blocking UI/formatting defect. It does not invalidate Telegram intake, transcript, approval gating, Research/Critic execution, traceability or credit-safety acceptance. Track separately if table-rendering polish is prioritized.

## Negative/no-speech companion behavior

Earlier private-GPT test target:

`https://t.me/techcrimes/12101`

was handled by the Telegram route but returned no recognizable speech, with `0` credits and `0` STT seconds, then stopped without paid or authorization bypass. This remains useful negative/no-speech evidence and is not the canonical positive target.

## Acceptance decision

A9.9 private-GPT Telegram E2E: ACCEPTED.

Authoritative state after acceptance:
- `builder_runtime_applied = true`;
- `managed_telegram_builder_runtime_applied = true`;
- `managed_telegram_private_gpt_e2e_complete = true`;
- `a9_9_telegram_builder_runtime_applied = true`;
- `a9_9_telegram_private_gpt_e2e_complete = true`;
- `rollout_state = A9_9_TELEGRAM_PRIVATE_GPT_E2E_ACCEPTED`.

Telegram joins YouTube, Instagram and Facebook as an accepted owner-only public zero-client adapter in the isolated MEDIA BETA.

This acceptance does not authorize:
- external tester rollout;
- public GPT promotion;
- merge to repository `main`;
- production VoiceBridge changes;
- private/authenticated Telegram retrieval;
- Telegram login/session/cookie use;
- any paid Telegram fallback;
- local attachment ingestion.

## Next engineering boundary

The remaining not-accepted A9 ingress target is local audio/video attachment transport and ingestion. Its ChatGPT-to-backend transport boundary must be proven before implementation is represented as available.
