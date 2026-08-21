# MEDIA BETA Documentation Index

Canonical documentation index for K-Research & Critic media-input work.

Version: 2.3
Status: ACTIVE
Updated: 2026-08-21

## Purpose

This directory is the self-contained documentation root for MEDIA BETA and owner-only zero-client media ingestion work.

It covers:
- accepted browser-assisted A8 baseline;
- zero-client A9 managed ingestion;
- credit consent and durable managed jobs;
- private GPT Action integration and owner E2E acceptance;
- future public platform adapters and local upload;
- later sustainable/free media architecture.

The published text-only K-Research & Critic product remains a separate production baseline and must not be changed implicitly by this subproject.

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

## Source-of-truth precedence

When documents disagree:
1. current code, live isolated runtime evidence and CI on active feature branches;
2. `03_CURRENT_STATE.md`;
3. `06_DECISION_LOG.md`;
4. `24_A9_ZERO_CLIENT_INGESTION_PLAN.md`;
5. `02_ROADMAP.md`;
6. `08_CHAT_HANDOFF.md`;
7. phase acceptance records and other documents.

Do not mark a phase complete from roadmap text alone.

## Current phase checkpoint

`A4_COMPLETE / A5_COMPLETE / A6_COMPLETE / A7_EXTERNAL_ROLLOUT_PAUSED / A8_BROWSER_ASSISTED_OWNER_BASELINE_COMPLETE / A9_1_COMPLETE / A9_2_DIRECT_YOUTUBE_BLOCKED / A9_2R_MANAGED_NATIVE_COMPLETE / A9_3_DURABLE_MANAGED_COMPLETE / A9_5_PRIVATE_GPT_ZERO_CLIENT_E2E_COMPLETE / A9_8_OWNER_ZERO_CLIENT_YOUTUBE_COMPLETE / A9_6_MULTI_PLATFORM_NEXT`

Current next task:

`Validate additional public source adapters independently, beginning with A9.6, while keeping the accepted YouTube path as the regression baseline.`

## Current A9 security/UX boundaries

- current live-accepted zero-client public adapter: YouTube;
- public URL sources only unless `local_upload` is later separately accepted;
- no platform login/password/cookies/authenticated sessions/account tokens;
- no user-facing beta access code in the private owner zero-client flow;
- private Action bearer remains mandatory;
- owner beta admission is injected server-side only after bearer authentication;
- Supadata native cost hard cap is one approved credit;
- no automatic managed AI fallback;
- ChatGPT may show its own consequential-Action confirmation before the billable external call;
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

Do not merge or publish the media feature, resume external tester/public-sharing work, expose credentials, bypass the credit-consent gate, use private platform sessions, or modify production merely because owner-only YouTube E2E passed. Those require separate explicit decisions and acceptance gates.
