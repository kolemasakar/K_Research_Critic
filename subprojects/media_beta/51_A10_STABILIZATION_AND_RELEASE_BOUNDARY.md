# A10 Stabilization and Release Boundary

Status: IN_PROGRESS / PACKAGE_READY_RUNTIME_PENDING
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

## Runtime gate

Repository/CI success is necessary but not sufficient to close A10.

The actual private GPT must receive the new Builder instructions and a fresh owner test must confirm that `ПІДСУМОК ЗА ТВЕРДЖЕННЯМИ` renders/copies as four distinct Markdown columns while preserving the same cross-check values.

Until that manual Builder update/runtime test:

- `builder_runtime_applied = false` for package `0.9.1-beta-a10`;
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
2. Builder package `0.9.1-beta-a10` is applied to the actual private GPT;
3. a fresh report demonstrates a valid four-column claim-summary table;
4. no accepted A9 routing/security/credit invariant regresses;
5. public/production boundaries remain unchanged unless separately approved.
