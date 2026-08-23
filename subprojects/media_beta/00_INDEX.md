# MEDIA BETA Documentation Index

Canonical documentation index for K-Research & Critic media-input work.

Version: 2.6
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
- claim-level required cross-check enforcement/auditability;
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
11. `10_A4_2_CAPTIONS_ACCEPTANCE.md` through `30_A9_5_PRIVATE_GPT_ZERO_CLIENT_E2E_ACCEPTANCE.md` - phase acceptance records.
12. `31_CRITICPROFILE_GATE_UX_UPDATE.md` - two-stage CriticProfile UX contract.
13. `32_CRITICPROFILE_GATE_RUNTIME_ACCEPTANCE.md` - actual private GPT runtime acceptance of the gate.
14. `33_CLAIM_LEVEL_CROSS_CHECK_ENFORCEMENT.md` - claim-level required/achieved/exception enforcement contract.

## Source-of-truth precedence

When documents disagree:
1. current code, live isolated runtime evidence and CI on active feature branches;
2. `03_CURRENT_STATE.md`;
3. `33_CLAIM_LEVEL_CROSS_CHECK_ENFORCEMENT.md` for current cross-check behavior;
4. `32_CRITICPROFILE_GATE_RUNTIME_ACCEPTANCE.md` for actual gate runtime evidence;
5. `31_CRITICPROFILE_GATE_UX_UPDATE.md` for CriticProfile UX behavior;
6. `06_DECISION_LOG.md`;
7. roadmap/handoff/phase records.

Do not mark a phase complete from roadmap text alone.

## Current phase checkpoint

`A4_COMPLETE / A5_COMPLETE / A6_COMPLETE / A7_EXTERNAL_ROLLOUT_PAUSED / A8_BROWSER_ASSISTED_OWNER_BASELINE_COMPLETE / A9_1_COMPLETE / A9_2_DIRECT_YOUTUBE_BLOCKED / A9_2R_MANAGED_NATIVE_COMPLETE / A9_3_DURABLE_MANAGED_COMPLETE / A9_5_PRIVATE_GPT_ZERO_CLIENT_E2E_COMPLETE / A9_8_OWNER_ZERO_CLIENT_YOUTUBE_COMPLETE / A9_6_INSTAGRAM_MANAGED_COMPLETE / A9_6_FACEBOOK_IN_PROGRESS`

## Current CriticProfile UX

- CriticProfile is mandatory before independent research;
- it is created internally but not displayed automatically;
- first menu offers direct analysis, profile review/edit, or cancel;
- option `1` explicitly approves the current profile before research;
- option `2` displays the profile and enters the review/edit menu;
- option `3` cancels without research;
- recovered `PROFILE_REVIEW_REQUIRED` checkpoints use the same gate;
- actual private-GPT gate runtime acceptance passed on 2026-08-23.

## Required cross-check contract

- floors: `LOW>=0`, `MEDIUM>=1`, `HIGH>=2`, `CRITICAL>=3`;
- each material factual claim has its own `required / achieved_independent / exception` ledger;
- independence is based on underlying evidence, not number of URLs/articles;
- duplicates, syndication, repeated reporting of one study/source, and source media/transcript do not count separately;
- `achieved_independent < required` must be visible as `SHORTFALL`, with reason, confidence adjustment and qualified conclusion;
- Critic verifies the ledger claim-by-claim;
- unconditional PASS is forbidden for hidden or unqualified material shortfalls;
- fact-check output exposes `Cross-check: achieved/required - PASS|SHORTFALL`;
- claim-level runtime acceptance remains pending after Builder resynchronization.

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
- A8 Helper 0.2.2 remains fallback evidence, not normal A9 UX.

## Related repositories and branches

KRC: `kolemasakar/K_Research_Critic`, branch `agent/video-url-research`, draft PR #8.
VoiceBridge: `kolemasakar/VoiceBridge`, branch `agent/krc-media-transcript`, draft PR #28.

## Non-negotiable boundary

Do not merge or publish the media feature, resume external tester/public-sharing work, expose credentials, bypass any provider credit-consent gate, use private platform sessions, or modify production merely because owner-only YouTube/Instagram paths passed. Those require separate explicit decisions and acceptance gates.
