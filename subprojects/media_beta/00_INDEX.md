# MEDIA BETA Documentation Index

Canonical documentation index for K-Research & Critic media-input work.

Version: 3.0
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
- claim-level required cross-check enforcement/auditability;
- clean Core Builder extraction, traceability hardening, and final runtime acceptance;
- MEDIA BETA alignment to the accepted Core traceability contract;
- additional public platform adapters and local upload;
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
15. `34_CLAIM_LEVEL_CROSS_CHECK_RUNTIME_ACCEPTANCE.md` - actual private MEDIA BETA runtime PASS of claim-level enforcement.
16. `35_CORE_RUNTIME_TRACEABILITY_HARDENING.md` - main Core auditability finding and traceability/protocol-table hardening.
17. `36_CORE_TRACEABILITY_RUNTIME_ACCEPTANCE.md` - final NEW-chat runtime PASS of the hardened main Core workflow.
18. `37_MEDIA_BETA_TRACEABILITY_ALIGNMENT.md` - MEDIA BETA alignment to the accepted Core evidence-origin traceability and mandatory protocol-table contract.

## Source-of-truth precedence

When documents disagree:
1. current code, live runtime evidence and CI on active feature branches;
2. `03_CURRENT_STATE.md`;
3. `37_MEDIA_BETA_TRACEABILITY_ALIGNMENT.md` for the current MEDIA BETA traceability contract and pending runtime gate;
4. `36_CORE_TRACEABILITY_RUNTIME_ACCEPTANCE.md` for final main Core runtime evidence;
5. `35_CORE_RUNTIME_TRACEABILITY_HARDENING.md` for the Core traceability contract and implementation history;
6. `34_CLAIM_LEVEL_CROSS_CHECK_RUNTIME_ACCEPTANCE.md` for MEDIA BETA claim-level runtime evidence before traceability alignment;
7. `33_CLAIM_LEVEL_CROSS_CHECK_ENFORCEMENT.md` for claim-level cross-check behavior;
8. `32_CRITICPROFILE_GATE_RUNTIME_ACCEPTANCE.md` for gate runtime evidence;
9. `31_CRITICPROFILE_GATE_UX_UPDATE.md` for CriticProfile UX behavior;
10. `06_DECISION_LOG.md`;
11. roadmap/handoff/phase records.

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

## Required cross-check / traceability contract

- floors: `LOW>=0`, `MEDIUM>=1`, `HIGH>=2`, `CRITICAL>=3`;
- each material factual claim has its own `required / achieved_independent / exception` ledger;
- independence is based on underlying evidence, not number of URLs/articles;
- `achieved_independent < required` is visible as `SHORTFALL`, with reason, confidence adjustment and qualified conclusion;
- Critic verifies the ledger claim-by-claim;
- unconditional PASS is forbidden for hidden/unqualified material shortfalls;
- every counted evidence origin must be visibly traceable to the claim;
- achieved count cannot exceed visibly traceable independent evidence origins;
- a systematic review/meta-analysis counts as one origin unless specific underlying studies were independently inspected and cited;
- review protocol must contain `Claim | Required | Achieved independent | Exception` for every material factual claim.

## Core runtime status

The main `K-Research & Critic` has been manually synchronized with the hardened clean Core Builder and passed the final NEW-chat regression.

Accepted runtime evidence includes:
- `CRITICAL -> required_cross_checks=3`;
- traceable `3/3 PASS` claims with three named/cited evidence origins;
- real `1/3 SHORTFALL` without double-counting derivative review evidence;
- mandatory claim-level protocol summary;
- `REVISE -> PASS` Critic cycle;
- `CORE_TRACEABILITY_HARDENING_RUNTIME = ACCEPTED`.

## MEDIA BETA traceability status

The same traceability contract is now implemented in the MEDIA BETA branch Builder/canonical instructions, manifest and tests.

Current markers:
- `MEDIA_BETA_CLAIM_LEVEL_RUNTIME = ACCEPTED` for the earlier claim-level contract;
- `MEDIA_BETA_TRACEABILITY_HARDENING_CODE = IMPLEMENTED`;
- `MEDIA_BETA_TRACEABILITY_HARDENING_RUNTIME = PENDING`;
- private MEDIA BETA Builder resynchronization required before the runtime gate.

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

Do not merge the media feature, resume external tester/public-sharing work, expose credentials, bypass any provider credit-consent gate, use private platform sessions, or change repository `main` without a separate explicit decision.
