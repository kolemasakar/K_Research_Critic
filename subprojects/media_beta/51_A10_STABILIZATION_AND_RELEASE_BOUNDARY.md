# A10 Stabilization and Release Boundary

Status: COMPLETE / COPY_SAFE_RUNTIME_ACCEPTED
Date: 2026-08-26
Scope: isolated `K-Research & Critic - MEDIA BETA` feature branch only.

## Starting point

A9 owner zero-client ingress is accepted for YouTube, Instagram, Facebook, Telegram and one local audio/video attachment. Those transport, privacy, credit and fallback boundaries remain authoritative and were not reopened by A10.

## Stabilization finding

Actual owner reports showed a ChatGPT whole-response Copy serialization defect: a correctly rendered four-column Markdown table could be copied with its header collapsed to:

`ТвердженняПотрібноОтримано незалежнихВиняток`

The visible table itself rendered correctly. The problem therefore required a copy-safe presentation mitigation rather than a media/backend change.

## A10 package

Builder package `0.9.1-beta-a10` requires:

- the normal localized four-column `ПІДСУМОК ЗА ТВЕРДЖЕННЯМИ` table;
- exact header and separator rows:

`| Твердження | Потрібно | Отримано незалежних | Виняток |`
`| --- | ---: | ---: | --- |`

- no merged/concatenated header labels;
- immediately afterward `КОПІЯ ДЛЯ НАДІЙНОГО КОПІЮВАННЯ`;
- the same complete table inside one fenced `text` code block preserving literal `|` delimiters;
- identical values between rendered and copy-safe representations.

Action schema remains `0.6.0-a9.10`. No VoiceBridge/backend change was required.

## Runtime attempt 1

Fresh owner private-GPT Telegram fact-check of `https://t.me/techcrimes/12107`:

- CriticProfile gate: PASS;
- visible four-column claim summary: PASS;
- whole-response Copy of the rendered table: FAIL because the UI serializer collapsed the header.

This established the remaining defect as a ChatGPT UI copy/serialization limitation.

## Runtime attempt 2 - accepted

The owner applied the refined Builder package and repeated the same fresh Telegram fact-check.

Observed:

- CriticProfile gate appeared normally and owner selected `1`;
- visible `ПІДСУМОК ЗА ТВЕРДЖЕННЯМИ` rendered as four distinct columns;
- claim accounting was `3/1 NONE`, `2/1 NONE`, `2/1 NONE`, and `0/1 SHORTFALL`;
- final status remained `ЗАВЕРШЕНО З ОБМЕЖЕННЯМИ` because the unsupported safety/workability claim retained its SHORTFALL;
- media/STT accounting remained `53 s / 53 s`, with `0` credits;
- the ordinary rendered table header still became collapsed when the entire response was copied;
- the required fenced `text` duplicate survived the same whole-response Copy with all four literal pipe-delimited columns intact;
- all four copied rows and values matched the visible table exactly.

Therefore the copy-safe mitigation meets the A10 acceptance objective even though the external ChatGPT UI serialization limitation remains.

Canonical runtime evidence:
`52_A10_SAFE_TABLE_RUNTIME_ACCEPTANCE.md`.

## Accepted state

A10 runtime gate: **ACCEPTED**.

Authoritative markers:

- `builder_runtime_applied = true`;
- `claim_summary_table_hardening_package_ready = true`;
- `claim_summary_table_hardening_runtime_applied = true`;
- `a10_claim_summary_table_runtime_accepted = true`;
- `a10_copy_safe_claim_table_runtime_accepted = true`;
- `gpt_builder_private_update_required = false`;
- `stabilization_state = A10_COPY_SAFE_CLAIM_TABLE_RUNTIME_ACCEPTED`.

The accepted workaround is the fenced copy-safe table. The ordinary rendered-table Copy defect is recorded as an external UI limitation and is not treated as a KRC claim-accounting failure.

## Preserved A9 boundaries

- Facebook active retrieval remains free Cobalt only; Cobalt failure -> unavailable -> STOP; no paid fallback offer/call.
- ScrapeCreators remains reserve-only, unconfigured and inactive.
- Telegram remains public-web retrieval, zero retrieval credits, no login/session and no paid fallback.
- Local attachment remains one current-conversation audio/video file through trusted OpenAI attachment delivery, retrieval credits `0`.
- uncertain-charge operations remain non-replayable.
- no user-facing beta code, provider credential, media Job ID, file ID or signed URL is exposed.

## Release boundary

A10 completion does **not** authorize:

- merge to repository `main`;
- production VoiceBridge deployment;
- external tester onboarding;
- public sharing or Store publication.

Those remain separate explicit owner decisions.

Final marker:

`A10_COPY_SAFE_CLAIM_TABLE_RUNTIME_ACCEPTED`
