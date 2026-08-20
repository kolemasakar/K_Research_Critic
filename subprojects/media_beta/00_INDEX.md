# MEDIA BETA Documentation Index

Canonical documentation index for K-Research & Critic media-input work.

Version: 2.0
Status: ACTIVE
Updated: 2026-08-20

## Purpose

This directory is the self-contained documentation root for the MEDIA BETA and future zero-client media ingestion work.

It covers:
- the accepted private browser-assisted baseline;
- the planned zero-client `MediaSourceRouter`;
- public media URL adapters;
- local video/audio upload direction;
- later sustainable/free media architecture.

The published text-only K-Research & Critic product remains a separate production baseline and must not be changed implicitly by this subproject.

## Canonical reading order

1. `README.md` - scope, goals, boundaries, and quick orientation.
2. `01_ARCHITECTURE.md` - system components, data flow, trust boundaries, and production isolation.
3. `02_ROADMAP.md` - phased implementation and release gates.
4. `03_CURRENT_STATE.md` - exact implementation state at the latest checkpoint.
5. `04_OPERATIONS_RUNBOOK.md` - Render, secrets, GPT Builder, deployment, rollback, and operational procedures.
6. `05_TEST_PLAN.md` - automated and live acceptance tests.
7. `06_DECISION_LOG.md` - approved architecture and product decisions.
8. `07_FREE_MODE_TARGET.md` - post-beta sustainable free architecture options and target design.
9. `08_CHAT_HANDOFF.md` - canonical recovery and cross-chat continuation document.
10. `09_WORK_LOG.md` - chronological implementation evidence.
11. `10_A4_2_CAPTIONS_ACCEPTANCE.md` - live captions-first acceptance.
12. `11_A4_3_AUDIO_FALLBACK_ACCEPTANCE.md` - live Audio fallback acceptance.
13. `12_A4_4_DURABILITY_ACCEPTANCE.md` - durable restart/resume acceptance.
14. `13_A4_5_GUARD_MATRIX_ACCEPTANCE.md` - negative-path guard matrix.
15. `14_A4_LANGUAGE_SOURCE_MATRIX_ACCEPTANCE.md` - language/source matrix.
16. `15_A4_QUOTA_LEDGER_RESTART_ACCEPTANCE.md` - durable STT quota restoration.
17. `16_A4_ACTIVE_AUDIO_PROCESS_REPLACEMENT_ACCEPTANCE.md` - forced process-loss acceptance.
18. `17_A4_STT_TEXT_QUALITY_DISPOSITION.md` - STT text-quality disposition.
19. `18_A5_A6_GPT_BUILDER_E2E_ACCEPTANCE.md` - Builder and first Research/Critic E2E acceptance.
20. `19_A7_CONTROLLED_TESTER_ROLLOUT.md` - external tester rollout plan, currently paused.
21. `20_A7_EU_AUDIO_PRIVACY_GATE_ACCEPTANCE.md` - AssemblyAI EU Audio fallback acceptance.
22. `21_CREDENTIAL_ATTRIBUTION_CORRECTION.md` - historical credential attribution correction.
23. `22_OWNER_ONLY_COMPLETION_PLAN.md` - A8 completion plan, now baseline-complete and superseded by A9 final target.
24. `23_A8_OWNER_ONLY_BROWSER_ASSISTED_ACCEPTANCE.md` - accepted private browser-assisted owner baseline.
25. `24_A9_ZERO_CLIENT_INGESTION_PLAN.md` - zero-client public-media/local-upload target plan.
26. `25_A9_CHAT_TRANSITION_BOOTSTRAP.md` - current new-chat recovery bootstrap.

## Source-of-truth order

When documents disagree, use this precedence:
1. current code and CI state on the active feature branches;
2. `03_CURRENT_STATE.md`;
3. `06_DECISION_LOG.md`;
4. `02_ROADMAP.md`;
5. `08_CHAT_HANDOFF.md`;
6. phase acceptance records and other documents.

A new chat must not infer completed work from roadmap items alone. Only current repository/CI state, `03_CURRENT_STATE.md`, and actual acceptance evidence may mark work complete.

## Current phase checkpoint

`A4_COMPLETE / A5_COMPLETE / A6_COMPLETE / A7_EXTERNAL_ROLLOUT_PAUSED / A8_BROWSER_ASSISTED_OWNER_BASELINE_COMPLETE / A9_ZERO_CLIENT_MEDIA_ROUTER_PLANNED / A9_IMPLEMENTATION_NOT_STARTED`

A8 proves the private GPT works end-to-end with Helper 0.2.2. The final desired normal UX is A9 zero-client ingestion, so the whole media project is not yet complete.

Approved A9 ingress directions:
- public media URLs through `MediaSourceRouter`;
- initial public adapters: YouTube, Instagram, Facebook, Telegram;
- public-only policy with no user logins/cookies/sessions/tokens;
- local video/audio upload through future `local_upload` ingress.

## New-chat recovery

Use:

`recover MEDIA BETA A9`

Then read:
`subprojects/media_beta/25_A9_CHAT_TRANSITION_BOOTSTRAP.md`

## Related repositories and branches

K-Research & Critic:
- repository `kolemasakar/K_Research_Critic`;
- production branch `main`;
- media feature branch `agent/video-url-research`;
- draft PR #8.

VoiceBridge backend dependency:
- repository `kolemasakar/VoiceBridge`;
- production branch `main`;
- media feature branch `agent/krc-media-transcript`;
- draft PR #28.

## Non-negotiable boundary

Do not merge or publish the media feature, resume external tester/public-sharing work, use user platform credentials, or modify production merely because the private browser-assisted baseline passed. Those require separate explicit owner decisions.
