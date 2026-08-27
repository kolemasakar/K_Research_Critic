# MEDIA BETA Documentation Index

Canonical documentation index for K-Research & Critic media-input work.

Version: 4.1
Status: ACTIVE
Updated: 2026-08-27

## Purpose

This directory is the self-contained documentation root for the isolated private `K-Research & Critic - MEDIA BETA` work.

It covers:
- accepted browser-assisted A8 baseline evidence;
- A9 owner zero-client managed ingestion;
- durable managed jobs and credit/replay boundaries;
- private GPT Action integration;
- CriticProfile approval UX;
- claim-level cross-check and evidence-origin traceability;
- report-label localization;
- accepted YouTube, Instagram, Facebook, Telegram and local audio/video attachment ingress;
- completed A10 copy-safe claim-summary stabilization;
- current release-hold owner-testing state;
- later optional external/public rollout boundaries.

Repository `main`, production VoiceBridge and public sharing remain separate and are not implicitly authorized by this subproject.

## Canonical reading order

1. `README.md` - scope and orientation.
2. `01_ARCHITECTURE.md` - components, flow, trust boundaries and isolation.
3. `02_ROADMAP.md` - phased implementation and release gates.
4. `03_CURRENT_STATE.md` - exact latest implementation checkpoint.
5. `04_OPERATIONS_RUNBOOK.md` - deployment and operations.
6. `05_TEST_PLAN.md` - automated/live acceptance plan.
7. `06_DECISION_LOG.md` - architecture/product decisions.
8. `07_FREE_MODE_TARGET.md` - later sustainable/free direction.
9. `08_CHAT_HANDOFF.md` - recovery/cross-chat continuation.
10. `09_WORK_LOG.md` - chronological evidence.
11. `10_A4_2_CAPTIONS_ACCEPTANCE.md` through `30_A9_5_PRIVATE_GPT_ZERO_CLIENT_E2E_ACCEPTANCE.md` - earlier phase records.
12. `31_CRITICPROFILE_GATE_UX_UPDATE.md`.
13. `32_CRITICPROFILE_GATE_RUNTIME_ACCEPTANCE.md`.
14. `33_CLAIM_LEVEL_CROSS_CHECK_ENFORCEMENT.md`.
15. `34_CLAIM_LEVEL_CROSS_CHECK_RUNTIME_ACCEPTANCE.md`.
16. `35_CORE_RUNTIME_TRACEABILITY_HARDENING.md`.
17. `36_CORE_TRACEABILITY_RUNTIME_ACCEPTANCE.md`.
18. `37_MEDIA_BETA_TRACEABILITY_ALIGNMENT.md`.
19. `38_REPORT_LANGUAGE_LABEL_LOCALIZATION_HARDENING.md`.
20. `39_REPORT_LANGUAGE_AND_MEDIA_TRACEABILITY_RUNTIME_ACCEPTANCE.md`.
21. `40_FACEBOOK_REMEDIATION_DEFERRED.md`.
22. `41_A9_7_FACEBOOK_COBALT_LIVE_ACCEPTANCE.md`.
23. `42_A9_7_PRIVATE_GPT_BUILDER_UPDATE_PACKAGE.md` - historical Builder record.
24. `43_A9_7_I_FACEBOOK_POLICY_FIX_BACKEND_HARDENING.md`.
25. `44_A9_7_I_PRIVATE_GPT_FACEBOOK_POLICY_E2E_ACCEPTANCE.md`.
26. `45_A9_9_TELEGRAM_PUBLIC_ADAPTER_AUDIT.md`.
27. `46_A9_9_PRIVATE_GPT_TELEGRAM_E2E_ACCEPTANCE.md`.
28. `47_A9_10_LOCAL_UPLOAD_TRANSPORT_AUDIT.md` - OpenAI attachment transport contract and security design.
29. `49_A9_10_ATTACHMENT_TRANSPORT_RUNTIME_ACCEPTANCE.md` - actual `openaiFileIdRefs` transport probe acceptance.
30. `50_A9_10_PRIVATE_GPT_LOCAL_ATTACHMENT_E2E_ACCEPTANCE.md` - actual owner local-attachment ingestion, CriticProfile and Research/Critic E2E acceptance.
31. `51_A10_STABILIZATION_AND_RELEASE_BOUNDARY.md` - A10 stabilization design, runtime attempts and release boundary.
32. `52_A10_SAFE_TABLE_RUNTIME_ACCEPTANCE.md` - accepted owner runtime evidence for the copy-safe claim table.
33. `53_RELEASE_HOLD_OWNER_TESTING_CHECKPOINT.md` - frozen owner-testing release-hold checkpoint and resume contract.

## Source-of-truth precedence

When documents disagree:
1. current code, current CI evidence and verified runtime evidence on active feature branches;
2. `03_CURRENT_STATE.md`;
3. `53_RELEASE_HOLD_OWNER_TESTING_CHECKPOINT.md` for the active release-hold decision and resume boundary;
4. `52_A10_SAFE_TABLE_RUNTIME_ACCEPTANCE.md` for A10 runtime acceptance;
5. `51_A10_STABILIZATION_AND_RELEASE_BOUNDARY.md` for A10 design/release boundary;
6. `50_A9_10_PRIVATE_GPT_LOCAL_ATTACHMENT_E2E_ACCEPTANCE.md` for accepted local attachment E2E;
7. `49_A9_10_ATTACHMENT_TRANSPORT_RUNTIME_ACCEPTANCE.md` for attachment transport;
8. `46_A9_9_PRIVATE_GPT_TELEGRAM_E2E_ACCEPTANCE.md` for Telegram E2E;
9. `44_A9_7_I_PRIVATE_GPT_FACEBOOK_POLICY_E2E_ACCEPTANCE.md` for Facebook failure policy;
10. older phase records and decision logs.

Historical documents do not override later acceptance records.

## Current phase checkpoint

`A4_COMPLETE / A5_COMPLETE / A6_COMPLETE / A7_EXTERNAL_ROLLOUT_PAUSED / A8_BROWSER_ASSISTED_OWNER_BASELINE_COMPLETE / A9_OWNER_ZERO_CLIENT_MEDIA_INPUT_ACCEPTED / YOUTUBE_ACCEPTED / INSTAGRAM_ACCEPTED / FACEBOOK_COBALT_ACCEPTED / FACEBOOK_FAILURE_POLICY_E2E_ACCEPTED / TELEGRAM_ACCEPTED / LOCAL_ATTACHMENT_ACCEPTED / A10_COPY_SAFE_CLAIM_TABLE_RUNTIME_ACCEPTED / RELEASE_HOLD_OWNER_TESTING`

## Accepted Research/Critic contract

- two-stage CriticProfile gate runtime accepted;
- floors `LOW>=0`, `MEDIUM>=1`, `HIGH>=2`, `CRITICAL>=3`;
- every material factual claim has `required / achieved_independent / exception`;
- independence is based on underlying evidence, not URL count;
- shortfalls are visible and qualified;
- every counted origin is traceable to the claim;
- achieved cannot exceed visible independent origins;
- Critic checks each material claim before PASS.

## A10 accepted stabilization

Builder package: `0.9.1-beta-a10`.

Action schema remains unchanged: `0.6.0-a9.10`.

The normal Ukrainian summary table still uses:

`| Твердження | Потрібно | Отримано незалежних | Виняток |`

`| --- | ---: | ---: | --- |`

A ChatGPT whole-response Copy serialization defect can corrupt the rendered-table header even when the visible table is correct. A10 therefore also requires `КОПІЯ ДЛЯ НАДІЙНОГО КОПІЮВАННЯ` followed by an identical fenced `text` table with literal pipe delimiters.

Fresh owner runtime proved:
- visible four-column table: PASS;
- fenced copy-safe whole-response Copy: PASS;
- identical values between the two forms: PASS;
- real `0/1 SHORTFALL` preserved: PASS.

Markers:
- `builder_runtime_applied = true`;
- `a10_claim_summary_table_runtime_accepted = true`;
- `a10_copy_safe_claim_table_runtime_accepted = true`;
- `gpt_builder_private_update_required = false`.

## Accepted owner media ingress

- prerecorded YouTube;
- Instagram Reel;
- Facebook Video/Reel via free Cobalt retrieval then AssemblyAI;
- supported public Telegram video posts via public Telegram web/embed retrieval then AssemblyAI;
- one local audio/video attachment from the current ChatGPT conversation via `openaiFileIdRefs` then AssemblyAI.

Local attachment boundary:
- `startManagedAttachmentTranscription`;
- retrieval provider `openai_attachment`;
- retrieval credits `0`;
- maximum attachment size `32 MiB`;
- trusted OpenAI attachment delivery only;
- no Helper, beta code, file ID, signed URL or provider credential exposed.

## Security/UX boundaries

- Facebook active retrieval is Cobalt-only; Cobalt failure means unavailable and STOP;
- ScrapeCreators remains reserve-only, unconfigured and not offerable in active flow;
- Telegram is public-web only, zero retrieval credits, no login/cookies/session/bot token and no paid fallback;
- local attachment flow accepts only the current-conversation attachment transport boundary;
- no platform credentials or imported sessions;
- private Action bearer remains mandatory;
- Supadata native and Instagram AI credit operations retain explicit consent gates;
- uncertain-charge operations are never auto-retried;
- A8 Helper remains fallback evidence only, not normal owner UX.

## Related repositories and branches

KRC: `kolemasakar/K_Research_Critic`, branch `agent/video-url-research`, draft PR #8.

VoiceBridge: `kolemasakar/VoiceBridge`, branch `agent/krc-media-transcript`, draft PR #28.

## Current operating mode

`RELEASE_HOLD_OWNER_TESTING`

The owner will continue private testing before making any release decision.

Current release gates:
- merge to `main`: HOLD;
- production promotion: HOLD;
- external testers: HOLD;
- public sharing / Store rollout: HOLD.

Defects found during this period stay isolated to the feature branches and are revalidated there unless the owner explicitly changes the release decision.

## Next task

Continue owner-only MEDIA BETA testing. No A10 remediation or release transition is pending by default.

When the owner is ready, revisit each release gate independently rather than treating release as one combined action.

## Non-negotiable boundary

Do not merge the media feature, resume external tester/public-sharing work, change repository `main`, deploy production VoiceBridge, expose credentials, enable ScrapeCreators, introduce paid Telegram retrieval, or replay uncertain-charge operations without a separate explicit owner decision.
