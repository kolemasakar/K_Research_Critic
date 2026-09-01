# MEDIA BETA Chat Handoff
Канонічна інструкція відновлення K-Research & Critic - MEDIA BETA у новому чаті.

Version: 4.2
Status: ACTIVE_HANDOFF / RELEASE_HOLD_OWNER_TESTING / M3_READY_FOR_AB
Checkpoint date: 2026-09-01

## Recovery Command

`recover KRC MEDIA BETA M3 READY_FOR_AB checkpoint 2026-09-01`

## Mandatory Recovery Order

1. `subprojects/media_beta/64_M3_READY_FOR_AB_CHECKPOINT_2026_09_01.md`
2. `subprojects/media_beta/62_FULL_PROJECT_STATE_CHECKPOINT_2026_09_01.md`
3. `subprojects/media_beta/00_INDEX.md`
4. `subprojects/media_beta/61_VOICEBRIDGE_GEMINI_IMPACT_AUDIT_2026_09_01.md`
5. `subprojects/media_beta/60_PROJECT_DOCUMENTATION_AUDIT_AND_M3_ROADMAP_SYNC_2026_09_01.md`
6. `subprojects/media_beta/03_CURRENT_STATE.md`
7. `subprojects/media_beta/53_RELEASE_HOLD_OWNER_TESTING_CHECKPOINT.md`
8. `subprojects/media_beta/01_ARCHITECTURE.md`
9. `subprojects/media_beta/02_ROADMAP.md`
10. `subprojects/media_beta/06_DECISION_LOG.md`
11. `subprojects/media_beta/04_OPERATIONS_RUNBOOK.md` and `05_TEST_PLAN.md` as needed.

After reading the checkpoints, verify current GitHub heads and CI before any write or provider-consuming operation.

## Product / Repository Context

```text
K-Research & Critic
 -> public Core
    repo: kolemasakar/K_Research_Critic
    branch: main
    state: published / maintenance

 -> K-Research & Critic - MEDIA BETA
    role: closed-beta module of K-Research & Critic
    product/roadmap authority: K_Research_Critic
    branch: agent/video-url-research
    PR: #8 draft/open/unmerged
    release state: RELEASE_HOLD_OWNER_TESTING

VoiceBridge
 -> technology/backend implementation source
 -> main: accepted VoiceBridge project baseline
 -> agent/krc-media-gemini-migration: active KRC prerecorded forward-port / PR #45
 -> agent/krc-media-transcript: historical accepted KRC runtime lineage
```

VoiceBridge is not the parent product and cannot authorize KRC release gates.

## Latest Validated M3 Evidence

```text
VoiceBridge/agent/krc-media-gemini-migration
head: 90ca4f354a466f7f5ffdba20de246eb033b369a8
Validate run: 33527873644 SUCCESS
PR #45: OPEN / DRAFT / UNMERGED

K_Research_Critic/agent/video-url-research
roadmap READY_FOR_AB commit: 499d79f29eaf0aeffe6845d6dde476c4a78582ae
Tests run: 33528028454
```

Later checkpoint/index/handoff documentation commits may advance the KRC branch. Verify exact-head CI during recovery.

## Current Functional Checkpoint

```text
A9_OWNER_ZERO_CLIENT_MEDIA_INPUT_ACCEPTED
A9_10_LOCAL_ATTACHMENT_ACCEPTED
A10_COPY_SAFE_CLAIM_TABLE_RUNTIME_ACCEPTED
VOICEBRIDGE_LIVE_GEMINI_DEFAULT_ACCEPTED
VOICEBRIDGE_PHASE_2_COMPLETE
KRC_PRERECORDED_ASSEMBLYAI_ACTIVE
KRC_GEMINI_PRERECORDED_IMPLEMENTED_INACTIVE
KRC_MEDIA_GEMINI_M0_COMPLETE
KRC_MEDIA_GEMINI_M1_PASS
KRC_MEDIA_GEMINI_M2_PASS_INACTIVE
KRC_MEDIA_GEMINI_M3_ACTIVE
M3_BYTE_CAPTURE_ACCEPTED
ASSET_SHA256_ACCEPTED_3_OF_3
REFERENCE_LISTENING_REVIEW_COMPLETED_3_OF_3
FINAL_REFERENCE_SHA256_ACCEPTED_3_OF_3
REFERENCE_REVIEW_STATE_INDEPENDENT_REVIEWED_3_OF_3
READY_FOR_AB_TRUE_3_OF_3
M3_PROVIDER_AB_NOT_RUN
CURRENT_MILESTONE_M3_READY_FOR_AB_PROVIDER_AUTHORIZATION
RELEASE_HOLD_OWNER_TESTING
```

## Accepted M3 Clean-Public Evidence

```text
ua-clean-public-001
asset SHA-256: 98e29c2276533699c67454de16b713d9846f668b6cc32b7591a0b2eb8a275a8c
final reference SHA-256: 2ec614c71321a8747b6bb50fb57a7c341bcad9150a09c5cb2a1825ebfc0f828e
state: READY_FOR_AB

ru-clean-public-001
asset SHA-256: d066239503c4e7406ebeb47423334b5109aa6b30d62046d0338a04e41b4c52f5
final reference SHA-256: 1c7ac3953951270a56bf5927c86a26d28281ca9b958981c9ab56776837faaadf
state: READY_FOR_AB

en-clean-public-001
asset SHA-256: 63a4b1e4c1dc655ac70961ffbf518acd249df237e5a0152faae9a4a836949715
final reference SHA-256: 044267656cd78db47edd50fead3ae70f8f7240f3c1f3523cc53b94594de5ecfa
state: READY_FOR_AB
```

The Ukrainian upstream candidate reference was rejected after manual listening revealed a material lexical mismatch. A corrected reference artifact was created outside GitHub, hashed under the accepted byte convention, and accepted as `independent_reviewed`.

## Critical Policy Recovery

- Facebook: Cobalt fail -> unavailable; no automatic/offerable paid fallback.
- Telegram: public-only, zero retrieval credits, no login/session/bot-token/paid fallback.
- Local attachment: `openaiFileIdRefs`, trusted OpenAI delivery, max 32 MiB, zero retrieval credits.
- AssemblyAI `universal-2` remains the active KRC prerecorded STT provider.
- Gemini `gemini-3.5-transcribe` is implemented/tested but inactive for normal KRC jobs.
- VoiceBridge live `gemini-3.5-transcribe-live` acceptance does not activate KRC prerecorded Gemini.
- CriticProfile gate remains before Research.
- per-claim independent cross-check accounting remains mandatory.
- A10 fenced copy-safe summary remains mandatory.

## Current Package

```text
Builder package: 0.9.1-beta-a10
Action schema: 0.6.0-a9.10
Builder already applied: yes
```

## Current Release Decision

```text
R1 merge selected MEDIA BETA work toward main = HOLD
R2 backend/production promotion = HOLD
R3 external testers = HOLD
R4 public rollout = HOLD
M4 canary = NOT_STARTED
M5 cutover = NOT_AUTHORIZED
```

## Exact Continuation Point

```text
M3 READY_FOR_AB / PROVIDER-CONSUMING A/B AUTHORIZATION GATE
```

Next valid operation after explicit provider-consuming authorization:

```text
same exact accepted asset -> AssemblyAI universal-2
same exact accepted asset -> Gemini gemini-3.5-transcribe
 -> capture outputs and execution metadata
 -> deterministic comparison against final reference
 -> manual factual/hallucination review
 -> M3 closure decision
```

Do not infer provider-spend authorization merely from READY_FOR_AB. Do not activate Gemini for normal KRC jobs as part of the A/B test.

## Continuation Rule

During release hold, continue only owner testing, defect remediation, regression hardening, documentation maintenance, and explicitly authorized M3 evidence work. Re-check branch deltas before any M4, merge, deployment, or provider activation decision.

## Terminal Marker

`MEDIA_BETA_HANDOFF_V4_2_M3_READY_FOR_AB_PROVIDER_AUTHORIZATION`
