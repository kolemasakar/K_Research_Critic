# A10 Stabilization and Release Boundary

Status: IN_PROGRESS / COPY_SAFE_RUNTIME_RETEST_PENDING
Date: 2026-08-26
Scope: isolated `K-Research & Critic - MEDIA BETA` feature branch only.

## Starting point

A9 owner zero-client ingress is accepted for YouTube, Instagram, Facebook, Telegram and one local audio/video attachment. The accepted runtime/security boundaries remain authoritative and are not reopened by this phase.

## Stabilization findings

### S1. Claim-summary Markdown header defect

Actual A9.9/A9.10 owner reports showed that copied Markdown could collapse the four expected table headings into the first cell:

`ТвердженняПотрібноОтримано незалежнихВиняток`

Rows and cross-check values remained readable, so this was non-blocking for A9 acceptance, but it is a repeatable presentation defect worth hardening before any wider rollout.

### S2. Canonical managed-instruction drift

The compact Builder package had already gained Telegram and local-attachment routing, while `prompts/GPT_STORE_MEDIA_MANAGED_BETA_INSTRUCTIONS.md` still described the earlier A9.7-I state and omitted those accepted ingress paths. A10 aligns the canonical reference to the accepted A9.10 state.

## A10 changes

- harden the private MEDIA BETA Builder prompt to require a literal four-column Markdown table;
- require exact Ukrainian header and separator rows:

`| Твердження | Потрібно | Отримано незалежних | Виняток |`
`| --- | ---: | ---: | --- |`

- explicitly forbid merging/concatenating the four header labels;
- preserve claim-level `required / achieved_independent / exception` semantics and traceability;
- align the canonical managed reference with YouTube/Instagram/Facebook/Telegram/local-attachment accepted routing;
- keep Action schema `0.6.0-a9.10` unchanged;
- keep all A9 accepted transport, credit, replay, privacy and fallback boundaries unchanged;
- stage Builder package `0.9.1-beta-a10` for private owner runtime application.

## Runtime attempt 1

The owner applied the A10 Builder instructions and ran a fresh Telegram fact-check against `https://t.me/techcrimes/12107`.

Observed:
- CriticProfile gate appeared correctly;
- final report rendered `ПІДСУМОК ЗА ТВЕРДЖЕННЯМИ` visually as four distinct columns;
- cross-check values remained coherent in the rendered table;
- however, copying the whole response still serialized the header as a collapsed first cell:
  `| ТвердженняПотрібноОтримано незалежнихВиняток |   |   |      |`.

Conclusion:
- visual table-rendering gate: PASS;
- whole-response copied-Markdown gate: FAIL;
- A10 is not yet runtime accepted.

The evidence indicates a ChatGPT UI copy/serialization issue rather than a model table-rendering failure: a malformed source Markdown table would not have rendered as the correct four-column table shown in the owner screenshot.

## Copy-safe refinement

To make the report robust to the UI serializer, the same A10 Builder package is refined so every Ukrainian fact-check report must output both:
1. the normal rendered four-column Markdown table; and
2. immediately after it, `КОПІЯ ДЛЯ НАДІЙНОГО КОПІЮВАННЯ` containing the same complete table inside one fenced `text` code block.

The fenced block must preserve literal `|` delimiters and exactly match the rendered table values. This does not change claim accounting, media routing, credits, backend behavior or Action schema.

## Runtime gate

Repository/CI success is necessary but not sufficient to close A10.

The actual private GPT must receive the refined Builder instructions and a fresh owner test must confirm:
- the visual `ПІДСУМОК ЗА ТВЕРДЖЕННЯМИ` still renders as four distinct columns;
- the immediately following copy-safe fenced block contains four explicit pipe-delimited columns and survives whole-response copy;
- the two representations contain identical claim rows and cross-check values.

Until that runtime retest:
- `builder_runtime_applied = false` for the current A10 package state;
- `gpt_builder_private_update_required = true`;
- `a10_claim_summary_table_runtime_accepted = false`.

This does not revoke the already accepted A9.10 media ingestion E2E.

## Release boundary

No automatic promotion follows from A10 stabilization.

Remain paused unless the owner separately authorizes:
- merge to repository `main`;
- production VoiceBridge deployment;
- external tester onboarding;
- public sharing/store rollout.

Facebook remains Cobalt-only in the active path after failure, ScrapeCreators remains reserve-only/unconfigured/inactive, Telegram remains public-web/no-paid-fallback, and uncertain-charge operations remain non-replayable.

## Exit criteria

A10 can be marked COMPLETE only when:
1. repository validators/tests are green on the final stabilization commit;
2. the refined Builder instructions are applied to the actual private GPT;
3. a fresh report demonstrates a valid four-column rendered claim-summary table;
4. the copy-safe fenced table preserves the same four columns and values when the whole response is copied;
5. no accepted A9 routing/security/credit invariant regresses;
6. public/production boundaries remain unchanged unless separately approved.
