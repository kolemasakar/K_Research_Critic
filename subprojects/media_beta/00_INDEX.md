# MEDIA BETA Documentation Index

Canonical documentation index for K-Research & Critic media-input work.

Version: 3.5
Status: ACTIVE
Updated: 2026-08-26

## Purpose

This directory is the self-contained documentation root for MEDIA BETA and related K-Research & Critic workflow hardening on the isolated feature branches.

It covers:
- accepted browser-assisted A8 baseline;
- zero-client A9 managed ingestion;
- credit consent and durable managed jobs;
- private GPT Action integration and owner E2E acceptance;
- CriticProfile presentation/approval UX and runtime acceptance;
- claim-level cross-check enforcement and auditability;
- Core and MEDIA BETA evidence-origin traceability;
- report-label localization;
- Facebook Cobalt free retrieval acceptance;
- A9.7-I Facebook failure-policy hardening;
- later sustainable/free media architecture.

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
19. `38_REPORT_LANGUAGE_LABEL_LOCALIZATION_HARDENING.md` - visible-language hardening for both Core and MEDIA BETA.
20. `39_REPORT_LANGUAGE_AND_MEDIA_TRACEABILITY_RUNTIME_ACCEPTANCE.md` - dual-GPT localization PASS and MEDIA BETA traceability runtime acceptance.
21. `40_FACEBOOK_REMEDIATION_DEFERRED.md` - historical owner decision to defer the failed A9.6 Supadata route.
22. `41_A9_7_FACEBOOK_COBALT_LIVE_ACCEPTANCE.md` - live acceptance of the free Facebook Cobalt -> AssemblyAI -> durable KRCM path.
23. `42_A9_7_PRIVATE_GPT_BUILDER_UPDATE_PACKAGE.md` - historical Builder application record before the final A9.7-I failure-policy correction.
24. `43_A9_7_I_FACEBOOK_POLICY_FIX_BACKEND_HARDENING.md` - current A9.7-I policy-fix authority for Cobalt failure and paid-fallback suppression.

## Source-of-truth precedence

When documents disagree:
1. current code, current CI evidence and verified runtime evidence on active feature branches;
2. `03_CURRENT_STATE.md`;
3. `43_A9_7_I_FACEBOOK_POLICY_FIX_BACKEND_HARDENING.md` for the active Facebook Cobalt-failure policy;
4. `41_A9_7_FACEBOOK_COBALT_LIVE_ACCEPTANCE.md` for the accepted positive Cobalt path;
5. `39_REPORT_LANGUAGE_AND_MEDIA_TRACEABILITY_RUNTIME_ACCEPTANCE.md` for latest dual-GPT runtime acceptance;
6. `38_REPORT_LANGUAGE_LABEL_LOCALIZATION_HARDENING.md` for the visible-language contract;
7. `37_MEDIA_BETA_TRACEABILITY_ALIGNMENT.md` for the MEDIA BETA traceability contract;
8. `36_CORE_TRACEABILITY_RUNTIME_ACCEPTANCE.md` for accepted main Core traceability evidence;
9. `35_CORE_RUNTIME_TRACEABILITY_HARDENING.md`;
10. `34_CLAIM_LEVEL_CROSS_CHECK_RUNTIME_ACCEPTANCE.md`;
11. `33_CLAIM_LEVEL_CROSS_CHECK_ENFORCEMENT.md`;
12. `32_CRITICPROFILE_GATE_RUNTIME_ACCEPTANCE.md`;
13. `31_CRITICPROFILE_GATE_UX_UPDATE.md`;
14. `06_DECISION_LOG.md`;
15. roadmap/handoff/older phase records.

`42_A9_7_PRIVATE_GPT_BUILDER_UPDATE_PACKAGE.md` is a historical application record. Its prior paid-continuation description does not override the later A9.7-I policy correction.

Do not mark a phase complete from roadmap text alone.

## Current phase checkpoint

`A4_COMPLETE / A5_COMPLETE / A6_COMPLETE / A7_EXTERNAL_ROLLOUT_PAUSED / A8_BROWSER_ASSISTED_OWNER_BASELINE_COMPLETE / A9_1_COMPLETE / A9_2_DIRECT_YOUTUBE_BLOCKED / A9_2R_MANAGED_NATIVE_COMPLETE / A9_3_DURABLE_MANAGED_COMPLETE / A9_5_PRIVATE_GPT_ZERO_CLIENT_E2E_COMPLETE / A9_8_OWNER_ZERO_CLIENT_YOUTUBE_COMPLETE / A9_6_INSTAGRAM_MANAGED_COMPLETE / A9_6_FACEBOOK_SUPADATA_NOT_ACCEPTED / A9_7_FACEBOOK_COBALT_LIVE_ACCEPTED / A9_7_I_FACEBOOK_POLICY_BACKEND_HARDENED / A9_7_I_BUILDER_POLICY_REAPPLY_PENDING`

## Accepted Research/Critic contract

- two-stage CriticProfile gate runtime accepted;
- floors `LOW>=0`, `MEDIUM>=1`, `HIGH>=2`, `CRITICAL>=3`;
- each material factual claim has `required / achieved_independent / exception`;
- independence is based on underlying evidence, not URL count;
- shortfalls are visible and qualified;
- every counted evidence origin is visibly traceable to its claim;
- achieved cannot exceed visible independent origins;
- systematic-review derivative evidence is not double-counted;
- Critic checks each material claim before PASS.

## Report-language contract

Default report language is Ukrainian unless explicitly changed by the user. User-visible headings, table titles/columns, verdict labels and CriticProfile field labels follow the selected report language; canonical English keys remain internal.

Runtime acceptance details remain in records `38` and `39`.

## Runtime status

- `CORE_TRACEABILITY_HARDENING_RUNTIME = ACCEPTED`;
- `CORE_REPORT_LABEL_LOCALIZATION_RUNTIME = ACCEPTED`;
- `MEDIA_BETA_TRACEABILITY_LOGIC_RUNTIME = PASS`;
- `MEDIA_BETA_TRACEABILITY_HARDENING_RUNTIME = ACCEPTED`;
- `MEDIA_BETA_REPORT_LABEL_LOCALIZATION_RUNTIME = ACCEPTED`;
- `gpt_builder_private_update_required = false` is retained as a legacy compatibility marker;
- `builder_policy_fix_runtime_applied = false` is authoritative for the current A9.7-I reapply step;
- `a9_7_i_private_gpt_e2e_complete = false`.

## Current A9 security/UX boundaries

- live-accepted zero-client adapters: YouTube, Instagram Reel, and Facebook through the free Cobalt -> AssemblyAI path;
- active Facebook policy is Cobalt first and only for retrieval;
- if Cobalt/free retrieval fails, media retrieval is unavailable and media intake stops;
- active MEDIA BETA must not offer or call paid Facebook retrieval after Cobalt failure;
- ScrapeCreators remains reserve-only, unconfigured and not live accepted;
- historical paid-preflight/continuation schema operations are compatibility surface only and are forbidden by the active Builder routing policy;
- any future ScrapeCreators activation requires a separate owner decision and a new acceptance scope;
- public URL sources only;
- no platform login/password/cookies/session/account tokens;
- no user-facing beta code in owner flow;
- private Action bearer remains mandatory;
- Supadata native cap remains 1 approved credit;
- Instagram AI fallback requires separate quote and explicit consent;
- no automatic managed AI fallback;
- `credit_charge_uncertain=true` operations are never auto-retried;
- A8 Helper remains fallback evidence only.

## Related repositories and branches

KRC: `kolemasakar/K_Research_Critic`, branch `agent/video-url-research`, draft PR #8.
VoiceBridge: `kolemasakar/VoiceBridge`, branch `agent/krc-media-transcript`, draft PR #28.

Latest VoiceBridge policy-hardening commit: `1b46f15588840eda5b8f14f5206fd966b69c4887`.

## Next task

Reapply the corrected A9.7-I Builder instructions to the actual private owner GPT, then run one NEW-chat Facebook zero-client E2E. If Cobalt cannot retrieve the public media, the expected result is retrieval unavailable with no paid fallback offer or call.

## Non-negotiable boundary

Do not merge the media feature, resume external tester/public-sharing work, expose credentials, use private platform sessions, replay uncertain-charge operations, enable ScrapeCreators, or change repository `main` without a separate explicit owner decision.
