# MEDIA BETA Chat Handoff
Канонічна інструкція відновлення K-Research & Critic - MEDIA BETA у новому чаті.

Version: 4.0
Status: ACTIVE_HANDOFF / RELEASE_HOLD_OWNER_TESTING / M3_ACTIVE
Checkpoint date: 2026-09-01

## Recovery Command

`recover KRC MEDIA BETA full state checkpoint 2026-09-01`

## Mandatory Recovery Order

1. `subprojects/media_beta/62_FULL_PROJECT_STATE_CHECKPOINT_2026_09_01.md`
2. `subprojects/media_beta/00_INDEX.md`
3. `subprojects/media_beta/61_VOICEBRIDGE_GEMINI_IMPACT_AUDIT_2026_09_01.md`
4. `subprojects/media_beta/60_PROJECT_DOCUMENTATION_AUDIT_AND_M3_ROADMAP_SYNC_2026_09_01.md`
5. `subprojects/media_beta/03_CURRENT_STATE.md`
6. `subprojects/media_beta/53_RELEASE_HOLD_OWNER_TESTING_CHECKPOINT.md`
7. `subprojects/media_beta/01_ARCHITECTURE.md`
8. `subprojects/media_beta/02_ROADMAP.md`
9. `subprojects/media_beta/06_DECISION_LOG.md`
10. `subprojects/media_beta/04_OPERATIONS_RUNBOOK.md` and `05_TEST_PLAN.md` as needed.

After reading the checkpoint, verify current GitHub heads and CI before any write.

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

## Snapshot Heads to Compare Against

The full-state checkpoint recorded these pre-write/current external heads:

```text
K_Research_Critic/main
17cb85361c2e5727e3de176a05b2a55660e5e2be
CI 33486314648 SUCCESS

K_Research_Critic/agent/video-url-research
pre-full-checkpoint head c29d8626df8bb799742cd0cc970e7e65d4fc254f
CI 33486527423 SUCCESS
PR #8: OPEN / DRAFT / UNMERGED / mergeable=false at snapshot

VoiceBridge/main
a426ae331721dd36291874e45380faf603d854cf
CI 33290771682 SUCCESS
Phase 2 COMPLETE

VoiceBridge/agent/krc-media-gemini-migration
7c2cac849d9322a8b532815ac3be44e87bd52e27
CI 33480804395 SUCCESS
PR #45: OPEN / DRAFT / UNMERGED / mergeable=true at snapshot
```

The KRC MEDIA BETA branch advances when checkpoint/index/handoff documentation is committed. Use the live branch head after recovery and inspect any delta from the checkpoint before modifying code.

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
FIRST_PUBLIC_SOURCE_TRANCHE_LOCKED
REAL_ASSET_BYTES_CAPTURED_FALSE
READY_FOR_AB_FALSE
M3_LIVE_PRERECORDED_AB_NOT_RUN
CURRENT_MILESTONE_M3_BYTE_CAPTURE_SHA256
RELEASE_HOLD_OWNER_TESTING
```

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
```

Do not infer authorization to change any gate from a request to fix/test the private beta or continue M3 engineering work.

## Exact Continuation Point

```text
M3 BYTE CAPTURE + SHA-256
```

Next valid technical operation:

```text
capture exact bytes for the locked public source tranche
 -> SHA-256 exact media bytes
 -> do not retain raw media as GitHub artifact
 -> delete temporary media after hashing
 -> do not call AssemblyAI/Gemini in byte-capture step
 -> prepare/review reference transcript evidence
 -> reference SHA-256
 -> READY_FOR_AB
 -> controlled same-asset prerecorded AssemblyAI/Gemini A/B
```

## Continuation Rule

During the hold, continue only owner testing, defect remediation, regression hardening, documentation maintenance, and explicitly authorized M3 evidence work. If any branch head differs from the checkpoint, inspect the delta before modifying code or declaring a new project state.

## Terminal Marker

`MEDIA_BETA_HANDOFF_V4_FULL_STATE_M3_BYTE_CAPTURE`
