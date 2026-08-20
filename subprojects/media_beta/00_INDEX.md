# MEDIA BETA Documentation Index
Канонічний індекс документації підпроєкту закритого та майбутнього безкоштовного медіарежиму K-Research & Critic.

Version: 1.4
Status: ACTIVE
Updated: 2026-08-20

## Purpose

This directory is the self-contained documentation root for the K-Research & Critic media-input work.

It covers two related tracks:

- CLOSED MEDIA BETA: first-priority controlled YouTube claim-analysis beta for the owner and up to three testers;
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
11. `10_A4_2_CAPTIONS_ACCEPTANCE.md` - live captions-first owner acceptance and 227/227 GPT-facing pagination evidence.
12. `11_A4_3_AUDIO_FALLBACK_ACCEPTANCE.md` - live browser-audio/AssemblyAI fallback acceptance, duration accounting, provider cleanup, and restart-durability finding.
13. `12_A4_4_DURABILITY_ACCEPTANCE.md` - durable Postgres restart/resume acceptance and immutable `created_at` continuity.
14. `13_A4_5_GUARD_MATRIX_ACCEPTANCE.md` - live negative-path guard matrix for access, source, duration, concurrency, and STT quota.
15. `14_A4_LANGUAGE_SOURCE_MATRIX_ACCEPTANCE.md` - completed UK/RU/EN/AUTO-IT language/source matrix and large-payload persistence remediation evidence.
16. `15_A4_QUOTA_LEDGER_RESTART_ACCEPTANCE.md` - live real-STT-charge persistence and runtime quota restoration after isolated restart.
17. `16_A4_ACTIVE_AUDIO_PROCESS_REPLACEMENT_ACCEPTANCE.md` - forced active-audio process-loss, retry-safe failure, and no-duplicate-quota acceptance.
18. `17_A4_STT_TEXT_QUALITY_DISPOSITION.md` - `U+FFFD` replacement-character investigation and non-reproducible quality-anomaly disposition.

## Source-of-truth order

When documents disagree, use this precedence:

1. current code and CI state on the active feature branches;
2. `03_CURRENT_STATE.md`;
3. `06_DECISION_LOG.md`;
4. `02_ROADMAP.md`;
5. other documents in this directory.

A new chat must not infer completed work from roadmap items alone. Only `03_CURRENT_STATE.md`, live repository state, and actual CI/deployment evidence may mark work as completed.

## Current phase checkpoint

`A4_COMPLETE / A5_READY`

A4 live transcript validation is closed. The next implementation block is A5: separate GPT Builder beta.

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

Do not merge or publish the media feature merely because code CI passes. Live Render, transcription, privacy, GPT Action, and Free-plan validation gates remain mandatory.
