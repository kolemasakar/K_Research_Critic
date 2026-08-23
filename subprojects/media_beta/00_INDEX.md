# MEDIA BETA Documentation Index

Canonical documentation index for K-Research & Critic media-input work.

Version: 2.5
Status: ACTIVE
Updated: 2026-08-23

## Purpose

This directory is the self-contained documentation root for MEDIA BETA and owner-only zero-client media ingestion work.

It covers:
- accepted browser-assisted A8 baseline;
- zero-client A9 managed ingestion;
- credit consent and durable managed jobs;
- private GPT Action integration and owner E2E acceptance;
- CriticProfile presentation/approval UX and runtime acceptance;
- required cross-check enforcement/auditability;
- additional public platform adapters and local upload;
- later sustainable/free media architecture.

The published K-Research & Critic product remains a separate production baseline and must not be changed implicitly by this subproject.

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
11. `10_A4_2_CAPTIONS_ACCEPTANCE.md` - captions-first A4 acceptance.
12. `11_A4_3_AUDIO_FALLBACK_ACCEPTANCE.md` - Audio fallback acceptance.
13. `12_A4_4_DURABILITY_ACCEPTANCE.md` - browser-assisted durability.
14. `13_A4_5_GUARD_MATRIX_ACCEPTANCE.md` - negative guards.
15. `14_A4_LANGUAGE_SOURCE_MATRIX_ACCEPTANCE.md` - language/source matrix.
16. `15_A4_QUOTA_LEDGER_RESTART_ACCEPTANCE.md` - durable quota restoration.
17. `16_A4_ACTIVE_AUDIO_PROCESS_REPLACEMENT_ACCEPTANCE.md` - process-loss acceptance.
18. `17_A4_STT_TEXT_QUALITY_DISPOSITION.md` - STT text-quality disposition.
19. `18_A5_A6_GPT_BUILDER_E2E_ACCEPTANCE.md` - Builder/A6 Research-Critic acceptance.
20. `19_A7_CONTROLLED_TESTER_ROLLOUT.md` - external tester rollout plan, paused.
21. `20_A7_EU_AUDIO_PRIVACY_GATE_ACCEPTANCE.md` - AssemblyAI EU Audio acceptance.
22. `21_CREDENTIAL_ATTRIBUTION_CORRECTION.md` - historical credential correction.
23. `22_OWNER_ONLY_COMPLETION_PLAN.md` - A8 completion plan, baseline-complete.
24. `23_A8_OWNER_ONLY_BROWSER_ASSISTED_ACCEPTANCE.md` - accepted browser-assisted owner baseline.
25. `24_A9_ZERO_CLIENT_INGESTION_PLAN.md` - A9 zero-client plan/state sequence.
26. `25_A9_CHAT_TRANSITION_BOOTSTRAP.md` - A9 transition bootstrap.
27. `26_A9_MANAGED_PROVIDER_ACCEPTANCE.md` - Supadata native managed acceptance.
28. `27_A9_DURABLE_MANAGED_ACCEPTANCE.md` - durable KRCM/idempotency acceptance.
29. `28_A9_5_PRIVATE_GPT_ACTION_INTEGRATION.md` - A9.5 package/backend preflight checkpoint.
30. `29_A9_5_BUILDER_UPDATE_RUNBOOK.md` - private GPT Builder switch and Preview procedure.
31. `30_A9_5_PRIVATE_GPT_ZERO_CLIENT_E2E_ACCEPTANCE.md` - actual private GPT zero-client YouTube E2E acceptance.
32. `31_CRITICPROFILE_GATE_UX_UPDATE.md` - two-stage CriticProfile direct-run/review/edit UX contract and cross-check enforcement.
33. `32_CRITICPROFILE_GATE_RUNTIME_ACCEPTANCE.md` - actual private GPT runtime acceptance of the new gate.

## Source-of-truth precedence

When documents disagree:
1. current code, live isolated runtime evidence and CI on active feature branches;
2. `03_CURRENT_STATE.md`;
3. `32_CRITICPROFILE_GATE_RUNTIME_ACCEPTANCE.md` for actual gate runtime evidence;
4. `31_CRITICPROFILE_GATE_UX_UPDATE.md` for CriticProfile UX and cross-check contract;
5. `06_DECISION_LOG.md`;
6. `24_A9_ZERO_CLIENT_INGESTION_PLAN.md`;
7. `02_ROADMAP.md`;
8. `08_CHAT_HANDOFF.md`;
9. phase acceptance records and other documents.

Do not mark a phase complete from roadmap text alone.

## Current phase checkpoint

`A4_COMPLETE / A5_COMPLETE / A6_COMPLETE / A7_EXTERNAL_ROLLOUT_PAUSED / A8_BROWSER_ASSISTED_OWNER_BASELINE_COMPLETE / A9_1_COMPLETE / A9_2_DIRECT_YOUTUBE_BLOCKED / A9_2R_MANAGED_NATIVE_COMPLETE / A9_3_DURABLE_MANAGED_COMPLETE / A9_5_PRIVATE_GPT_ZERO_CLIENT_E2E_COMPLETE / A9_8_OWNER_ZERO_CLIENT_YOUTUBE_COMPLETE / A9_6_INSTAGRAM_MANAGED_COMPLETE / A9_6_FACEBOOK_IN_PROGRESS`

Current next media task:

`Complete Facebook isolated remediation and acceptance while preserving YouTube and Instagram as regression baselines.`

## Current CriticProfile UX

- CriticProfile is mandatory before independent research;
- it is created internally but not displayed automatically;
- first menu offers direct analysis, profile review/edit, or cancel;
- option `1` explicitly approves the current profile before research;
- option `2` displays the profile and enters the review/edit menu;
- option `3` cancels without research;
- recovered `PROFILE_REVIEW_REQUIRED` checkpoints use the same gate;
- actual private-GPT runtime acceptance passed on 2026-08-23.

## Required cross-check contract

- default floors: `LOW>=0`, `MEDIUM>=1`, `HIGH>=2`, `CRITICAL>=3`;
- approved `required_cross_checks` is mandatory for material factual conclusions;
- independence is based on underlying evidence, not number of URLs/articles;
- duplicates, syndication, repeated reporting of one study/source, and source media/transcript do not count separately;
- evidence scarcity must be explicit, confidence adjusted, and the limitation recorded;
- Critic verifies compliance before PASS;
- review protocol reports required/achieved cross-checks and exceptions.

## Current A9 security/UX boundaries

- live-accepted zero-client public adapters: YouTube and Instagram Reel;
- Facebook remains in progress and is not user-facing accepted;
- public URL sources only unless `local_upload` is later separately accepted;
- no platform login/password/cookies/authenticated sessions/account tokens;
- no user-facing beta access code in the private owner zero-client flow;
- private Action bearer remains mandatory;
- owner beta admission is injected server-side only after bearer authentication;
- Supadata native cost hard cap is one approved credit;
- Instagram AI fallback requires a separate quote and separate explicit consent;
- no automatic managed AI fallback;
- ChatGPT may show its own consequential-Action confirmation before a billable external call;
- A8 Helper 0.2.2 remains fallback evidence, not normal A9 UX.

## Related repositories and branches

KRC:
- `kolemasakar/K_Research_Critic`;
- branch `agent/video-url-research`;
- draft PR #8.

VoiceBridge:
- `kolemasakar/VoiceBridge`;
- branch `agent/krc-media-transcript`;
- draft PR #28.

## Non-negotiable boundary

Do not merge or publish the media feature, resume external tester/public-sharing work, expose credentials, bypass any provider credit-consent gate, use private platform sessions, or modify production merely because owner-only YouTube/Instagram paths passed. Those require separate explicit decisions and acceptance gates.
