# MEDIA BETA Documentation Index

Canonical documentation index for K-Research & Critic media-input work.

Version: 3.1
Status: ACTIVE
Updated: 2026-08-23

## Purpose

This directory is the self-contained documentation root for MEDIA BETA and related K-Research & Critic workflow hardening performed on the isolated feature branch.

It covers:
- accepted browser-assisted A8 baseline;
- zero-client A9 managed ingestion;
- credit consent and durable managed jobs;
- private GPT Action integration and owner E2E acceptance;
- CriticProfile presentation/approval UX and runtime acceptance;
- claim-level cross-check enforcement/auditability;
- Core and MEDIA BETA evidence-origin traceability;
- report-language label localization across both Builder variants;
- additional public platform adapters and later sustainable/free media architecture.

The published K-Research & Critic product and repository `main` remain separate production baselines and must not be changed implicitly by this subproject.

## Canonical reading order

1. `README.md` - scope and orientation.
2. `01_ARCHITECTURE.md` - components, data flow, trust boundaries and isolation.
3. `02_ROADMAP.md` - phased implementation and release gates.
4. `03_CURRENT_STATE.md` - exact latest implementation checkpoint.
5. `04_OPERATIONS_RUNBOOK.md` - deployment and operational procedures.
6. `05_TEST_PLAN.md` - automated/live acceptance plan.
7. `06_DECISION_LOG.md` - approved architecture/product decisions.
8. `07_FREE_MODE_TARGET.md` - later sustainable/free architecture direction.
9. `08_CHAT_HANDOFF.md` - recovery/cross-chat continuation.
10. `09_WORK_LOG.md` - chronological implementation evidence.
11. `10_A4_2_CAPTIONS_ACCEPTANCE.md` through `30_A9_5_PRIVATE_GPT_ZERO_CLIENT_E2E_ACCEPTANCE.md` - phase acceptance records.
12. `31_CRITICPROFILE_GATE_UX_UPDATE.md` - two-stage CriticProfile UX contract.
13. `32_CRITICPROFILE_GATE_RUNTIME_ACCEPTANCE.md` - actual private GPT runtime acceptance of the gate.
14. `33_CLAIM_LEVEL_CROSS_CHECK_ENFORCEMENT.md` - claim-level required/achieved/exception enforcement contract.
15. `34_CLAIM_LEVEL_CROSS_CHECK_RUNTIME_ACCEPTANCE.md` - private MEDIA BETA runtime acceptance before traceability alignment.
16. `35_CORE_RUNTIME_TRACEABILITY_HARDENING.md` - Core traceability/protocol-table hardening.
17. `36_CORE_TRACEABILITY_RUNTIME_ACCEPTANCE.md` - final Core traceability NEW-chat PASS.
18. `37_MEDIA_BETA_TRACEABILITY_ALIGNMENT.md` - MEDIA BETA alignment to the accepted Core traceability contract.
19. `38_REPORT_LANGUAGE_LABEL_LOCALIZATION_HARDENING.md` - Ukrainian-default visible heading/table/field-label hardening for both Core and MEDIA BETA.

## Source-of-truth precedence

When documents disagree:
1. current code, live runtime evidence and CI on active feature branches;
2. `03_CURRENT_STATE.md`;
3. `38_REPORT_LANGUAGE_LABEL_LOCALIZATION_HARDENING.md` for current visible-language requirements and pending runtime gate;
4. `37_MEDIA_BETA_TRACEABILITY_ALIGNMENT.md` for MEDIA BETA traceability contract;
5. `36_CORE_TRACEABILITY_RUNTIME_ACCEPTANCE.md` for accepted main Core traceability evidence;
6. `35_CORE_RUNTIME_TRACEABILITY_HARDENING.md`;
7. `34_CLAIM_LEVEL_CROSS_CHECK_RUNTIME_ACCEPTANCE.md`;
8. `33_CLAIM_LEVEL_CROSS_CHECK_ENFORCEMENT.md`;
9. `32_CRITICPROFILE_GATE_RUNTIME_ACCEPTANCE.md`;
10. `31_CRITICPROFILE_GATE_UX_UPDATE.md`;
11. `06_DECISION_LOG.md`;
12. roadmap/handoff/phase records.

Do not mark a phase complete from roadmap text alone.

## Current phase checkpoint

`A4_COMPLETE / A5_COMPLETE / A6_COMPLETE / A7_EXTERNAL_ROLLOUT_PAUSED / A8_BROWSER_ASSISTED_OWNER_BASELINE_COMPLETE / A9_1_COMPLETE / A9_2_DIRECT_YOUTUBE_BLOCKED / A9_2R_MANAGED_NATIVE_COMPLETE / A9_3_DURABLE_MANAGED_COMPLETE / A9_5_PRIVATE_GPT_ZERO_CLIENT_E2E_COMPLETE / A9_8_OWNER_ZERO_CLIENT_YOUTUBE_COMPLETE / A9_6_INSTAGRAM_MANAGED_COMPLETE / A9_6_FACEBOOK_IN_PROGRESS`

## Required cross-check / traceability contract

- floors: `LOW>=0`, `MEDIUM>=1`, `HIGH>=2`, `CRITICAL>=3`;
- each material factual claim has `required / achieved_independent / exception`;
- independence is based on underlying evidence, not URLs;
- shortfalls are visible and qualified;
- every counted evidence origin must be visibly traceable to its claim;
- achieved cannot exceed visible independent origins;
- a systematic review/meta-analysis is one origin unless underlying studies were separately inspected and cited;
- Critic checks the ledger and traceability claim-by-claim.

## Report-language label contract

Default report language is Ukrainian unless the user explicitly requests another language. All user-visible headings, table titles/columns and CriticProfile field labels follow the selected report language; canonical English keys remain internal.

For Ukrainian reports use:
- `ФІНАЛЬНИЙ ЗВІТ`;
- `ПЕРЕВІРКА ТВЕРДЖЕНЬ`;
- `ПРОТОКОЛ ПЕРЕВІРКИ`;
- `ПІДСУМОК ЗА ТВЕРДЖЕННЯМИ`;
- claim-level columns `Твердження | Потрібно | Отримано незалежних | Виняток`.

Do not expose `Claim-level summary`, `Claim`, `Required`, `Achieved independent`, `Exception` or raw CriticProfile keys as Ukrainian user-visible labels unless explicitly requested.

## Runtime status

Main Core evidence-origin traceability remains accepted.

The latest MEDIA BETA regression demonstrated traceability logic and the four-column summary correctly, but exposed English visible labels. That run is not final acceptance of the complete updated language contract.

Current markers:
- `CORE_TRACEABILITY_HARDENING_RUNTIME = ACCEPTED`;
- `MEDIA_BETA_TRACEABILITY_LOGIC_RUNTIME = PASS`;
- `MEDIA_BETA_REPORT_LABEL_LOCALIZATION_CODE = IMPLEMENTED`;
- `MEDIA_BETA_REPORT_LABEL_LOCALIZATION_RUNTIME = PENDING`;
- `MEDIA_BETA_TRACEABILITY_HARDENING_RUNTIME = PENDING_FINAL_LANGUAGE_REGRESSION`.

Both actual Custom GPT Builder instruction sets require manual resynchronization with their latest branch Builder files before the localization runtime gate.

## Current A9 security/UX boundaries

- live-accepted zero-client adapters: YouTube and Instagram Reel;
- Facebook remains in progress/not accepted;
- public URL sources only;
- no platform login/password/cookies/session/account tokens;
- no user-facing beta code in owner flow;
- private Action bearer remains mandatory;
- Supadata native cap remains 1 approved credit;
- Instagram AI fallback requires separate quote and explicit consent;
- no automatic managed AI fallback;
- A8 Helper remains fallback evidence only.

## Related repositories and branches

KRC: `kolemasakar/K_Research_Critic`, branch `agent/video-url-research`, draft PR #8.
VoiceBridge: `kolemasakar/VoiceBridge`, branch `agent/krc-media-transcript`, draft PR #28.

## Non-negotiable boundary

Do not merge the media feature, resume external tester/public-sharing work, expose credentials, bypass credit consent, use private platform sessions, or change repository `main` without a separate explicit decision.
