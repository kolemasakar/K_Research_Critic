# MEDIA BETA Chat Handoff
Канонічна інструкція відновлення K-Research & Critic - MEDIA BETA у новому чаті.

Version: 4.1
Status: ACTIVE_HANDOFF / RELEASE_HOLD_OWNER_TESTING / M3_ACTIVE
Checkpoint date: 2026-09-01

## Recovery Command

`recover KRC MEDIA BETA M3 reference review checkpoint 2026-09-01`

## Mandatory Recovery Order

1. `subprojects/media_beta/63_M3_REFERENCE_REVIEW_CHECKPOINT_2026_09_01.md`
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

## Latest Validated Engineering Evidence

```text
K_Research_Critic/agent/video-url-research roadmap evidence head
fe6c56aae6208527bba0cddfdeac5a55ff3ef357
CI 33521649491 SUCCESS
Python 3.13 PASS
Python 3.14 PASS
quality gates PASS

VoiceBridge/agent/krc-media-gemini-migration
c98c77521c919611b735971451e72366dedd2750
CI 33521717978 SUCCESS
cloud 224/224 PASS
browser-extension PASS
repository-docs PASS
PR #45 OPEN / DRAFT / UNMERGED
```

KRC checkpoint/index/handoff documentation commits may advance the branch after the validated roadmap head. They are documentation-only, but their exact-head CI must still be checked during recovery.

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
REAL_ASSET_BYTES_CAPTURED_TRUE
ASSET_SHA256_ACCEPTED_3_OF_3
REFERENCE_SOURCE_CANDIDATES_LOCKED_3_OF_3
REFERENCE_ARTIFACT_CANDIDATE_SHA256_CREATED_3_OF_3
REFERENCE_AUDIO_RECONCILIATION_COMPLETE_FALSE
REFERENCE_SHA256_ACCEPTED_FALSE
READY_FOR_AB_FALSE
M3_LIVE_PRERECORDED_AB_NOT_RUN
CURRENT_MILESTONE_M3_INDEPENDENT_LISTENING_REVIEW
RELEASE_HOLD_OWNER_TESTING
```

## Accepted M3 Clean-Public Evidence

```text
ua-clean-public-001
asset SHA-256: 98e29c2276533699c67454de16b713d9846f668b6cc32b7591a0b2eb8a275a8c
candidate reference SHA-256: d9a6dbf5f2d0d1f8c200b11736982f3c9b2c02741d2303c96a359fe30015e461

ru-clean-public-001
asset SHA-256: d066239503c4e7406ebeb47423334b5109aa6b30d62046d0338a04e41b4c52f5
candidate reference SHA-256: 1c7ac3953951270a56bf5927c86a26d28281ca9b958981c9ab56776837faaadf

en-clean-public-001
asset SHA-256: 63a4b1e4c1dc655ac70961ffbf518acd249df237e5a0152faae9a4a836949715
candidate reference SHA-256: 044267656cd78db47edd50fead3ae70f8f7240f3c1f3523cc53b94594de5ecfa
```

The three candidate reference hashes are not final accepted reference digests until actual independent listening review is complete.

## Accepted Owner Inputs

```text
YouTube
Instagram Reel
Facebook Video/Reel via free Cobalt
supported public Telegram video post
one current-conversation local audio/video attachment
```

## Critical Policy Recovery

- Facebook: Cobalt fail -> unavailable; no automatic/offerable paid fallback.
- Telegram: public-only, zero retrieval credits, no login/session/bot-token/paid fallback.
- Local attachment: `openaiFileIdRefs`, trusted OpenAI delivery, max 32 MiB, zero retrieval credits.
- AssemblyAI `universal-2` remains the active KRC prerecorded STT provider.
- Gemini `gemini-3.5-transcribe` is implemented/tested but inactive for normal KRC jobs.
- VoiceBridge live `gemini-3.5-transcribe-live` acceptance does not activate KRC prerecorded Gemini.
- no normal-flow Helper or user beta code;
- no KRCM/file/signed-URL exposure;
- CriticProfile gate before Research;
- per-claim independent cross-check accounting;
- A10 fenced copy-safe summary remains mandatory.

## Current Package

```text
Builder package: 0.9.1-beta-a10
Action schema: 0.6.0-a9.10
Builder already applied: yes
```

Do not ask the owner to re-apply Builder content unless the package itself has changed and needs a new runtime acceptance.

## Current Release Decision

```text
R1 merge selected MEDIA BETA work toward main = HOLD
R2 backend/production promotion = HOLD
R3 external testers = HOLD
R4 public rollout = HOLD
M4 canary = NOT_STARTED
M5 cutover = NOT_AUTHORIZED
```

Do not infer authorization to change any gate from a request to fix/test the private beta or continue M3 engineering work.

## Exact Continuation Point

```text
M3 INDEPENDENT LISTENING REVIEW + FINAL REFERENCE SHA-256
```

Next valid operation:

```text
listen to each exact accepted audio asset end-to-end
 -> reconcile candidate transcript against actual speech
 -> correct only actual mismatches/clipping boundaries
 -> keep UTF-8 + LF + exactly one terminal newline
 -> recompute SHA-256 after any change
 -> mark independent_reviewed only after real review
 -> READY_FOR_AB
 -> controlled same-asset prerecorded AssemblyAI/Gemini A/B
```

Do not use AssemblyAI, Gemini, another STT provider, or upstream annotation alone as a substitute for the independent listening review.

## Continuation Rule

During the hold, continue only owner testing, defect remediation, regression hardening, documentation maintenance, and explicitly authorized M3 evidence work. If any branch head differs from the checkpoint, inspect the delta before modifying code or declaring a new project state.

## Terminal Marker

`MEDIA_BETA_HANDOFF_V4_1_M3_REFERENCE_LISTENING_REVIEW`
