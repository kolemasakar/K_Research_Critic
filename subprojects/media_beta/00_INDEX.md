# MEDIA BETA Documentation Index

Canonical documentation index for the closed and future sustainable-free media mode of K-Research & Critic.

Version: 1.8
Status: ACTIVE
Updated: 2026-08-20

## Purpose

This directory is the self-contained documentation root for K-Research & Critic media-input work.

It covers:
- CLOSED MEDIA BETA: controlled YouTube claim-analysis beta for the owner and up to three testers;
- SUSTAINABLE FREE MEDIA: later architecture intended to remove permanent dependence on exhaustible paid STT credits.

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
11. `10_A4_2_CAPTIONS_ACCEPTANCE.md` - live captions-first acceptance and 227/227 GPT-facing pagination evidence.
12. `11_A4_3_AUDIO_FALLBACK_ACCEPTANCE.md` - live browser-audio/AssemblyAI fallback acceptance, duration accounting, and provider cleanup.
13. `12_A4_4_DURABILITY_ACCEPTANCE.md` - durable Postgres restart/resume acceptance and immutable `created_at` continuity.
14. `13_A4_5_GUARD_MATRIX_ACCEPTANCE.md` - negative-path guard matrix for access, source, duration, concurrency, and STT quota.
15. `14_A4_LANGUAGE_SOURCE_MATRIX_ACCEPTANCE.md` - UK/RU/EN/AUTO-IT language/source matrix and large-payload persistence remediation.
16. `15_A4_QUOTA_LEDGER_RESTART_ACCEPTANCE.md` - real-STT-charge persistence and runtime quota restoration after isolated restart.
17. `16_A4_ACTIVE_AUDIO_PROCESS_REPLACEMENT_ACCEPTANCE.md` - forced active-audio process loss, retry-safe failure, and no-duplicate-quota acceptance.
18. `17_A4_STT_TEXT_QUALITY_DISPOSITION.md` - U+FFFD investigation and non-reproducible quality-anomaly disposition.
19. `18_A5_A6_GPT_BUILDER_E2E_ACCEPTANCE.md` - separate GPT Builder configuration, captions-first CriticProfile gate, and first owner-operated Research/Critic end-to-end acceptance.
20. `19_A7_CONTROLLED_TESTER_ROLLOUT.md` - external tester onboarding, failure reporting, monitoring, and rollout rules.
21. `20_A7_EU_AUDIO_PRIVACY_GATE_ACCEPTANCE.md` - isolated AssemblyAI EU Audio fallback deployment, live completion, quota, and provider-cleanup acceptance.
22. `21_CREDENTIAL_ATTRIBUTION_CORRECTION.md` - canonical correction that prior owner-operated live tests used the credential designated for Tester 1, while the owner-designated credential remains separately untested.

## Source-of-truth order

When documents disagree, use this precedence:
1. current code and CI state on the active feature branches;
2. `03_CURRENT_STATE.md`;
3. `06_DECISION_LOG.md`;
4. `02_ROADMAP.md`;
5. other documents in this directory.

A new chat must not infer completed work from roadmap items alone. Only `03_CURRENT_STATE.md`, live repository state, and actual acceptance evidence may mark work complete.

## Current phase checkpoint

`A4_COMPLETE / A5_COMPLETE / A6_COMPLETE / A7_READY_FOR_TESTER1`

A4 live transcript validation, A5 separate GPT Builder beta, and the first owner-operated A6 end-to-end Research/Critic flow are accepted. Those prior live tests were performed by the owner/operator using the Tester 1 credential. The A7 AssemblyAI EU/no-training Audio fallback gate is accepted. The next block remains the first independent external Tester 1 run.

## Related repositories and branches

K-Research & Critic:
- repository: `kolemasakar/K_Research_Critic`
- production branch: `main`
- media feature branch: `agent/video-url-research`
- media PR: `#8`

VoiceBridge backend dependency:
- repository: `kolemasakar/VoiceBridge`
- production branch: `main`
- media feature branch: `agent/krc-media-transcript`
- media PR: `#28`

## Non-negotiable boundary

Do not merge or publish the media feature merely because implementation or owner/operator beta acceptance passes. Controlled tester rollout, runtime-plan compatibility, and explicit promotion approval remain separate gates.
