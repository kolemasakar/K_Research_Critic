# VoiceBridge Gemini Migration Impact Audit - 2026-09-01
Аудит впливу завершеної VoiceBridge міграції на Gemini на K-Research & Critic - MEDIA BETA.

Version: 1.0
Status: AUDIT_APPLIED / RELEASE_HOLD_OWNER_TESTING / KRC_M3_ACTIVE
Date: 2026-09-01

## Scope

This audit answers one specific cross-project question:

```text
VoiceBridge has migrated its real-time STT to Gemini.
What changes, if anything, does that imply for K-Research & Critic - MEDIA BETA?
```

The audit reads the current VoiceBridge main provider decision and Phase 2 closure together with the active KRC prerecorded forward-port branch.

No Builder, Action schema, provider selection, Render environment, Neon state, credential, quota, deployment, or release gate is changed by this audit.

## VoiceBridge Accepted State

Current VoiceBridge main:

```text
commit: a426ae331721dd36291874e45380faf603d854cf
Validate run: 33290771682 SUCCESS
Phase 1: COMPLETE
Phase 2 Universal Cloud Audio: COMPLETE
next VoiceBridge functional phase: Phase 3 Cloud Service Hardening
```

Accepted VoiceBridge real-time STT provider state:

```text
STT_PROVIDER=gemini
GEMINI_STT_MODEL=gemini-3.5-transcribe-live
AssemblyAI universal-streaming-english = explicit rollback
```

Canonical VoiceBridge evidence:

```text
docs/adr/ADR-009_GEMINI_3_5_TRANSCRIBE_DEFAULT_STT.md
docs/history/2026-08-29_GEMINI_3_5_TRANSCRIBE_STT_ACCEPTED.md
docs/planning/03_ROADMAP.md
docs/architecture/05_TECHNOLOGY_STACK.md
```

The VoiceBridge live migration was accepted after automated tests, live WebSocket validation, end-to-end STT/translation/TTS/playback validation, and a controlled same-duration AssemblyAI/Gemini comparison. The accepted migration introduced no automatic paid fallback and retained AssemblyAI as configuration-only rollback.

## Critical Domain Separation

VoiceBridge live speech recognition and KRC prerecorded evidence transcription are separate provider domains.

```text
VOICEBRIDGE LIVE
 input: browser PCM stream
 provider interface: SttProvider
 selector: STT_PROVIDER
 default: gemini
 model: gemini-3.5-transcribe-live
 state: ACCEPTED DEFAULT

KRC MEDIA BETA PRERECORDED
 input: retrieved/uploaded media asset
 provider interface: MediaTranscriptionProvider
 selector: KRC_MEDIA_STT_PROVIDER
 active provider: assemblyai
 active model: universal-2
 Gemini candidate: gemini-3.5-transcribe
 state: ASSEMBLYAI ACTIVE / GEMINI INACTIVE
```

The completed VoiceBridge live migration therefore does not constitute a KRC prerecorded cutover.

## Code-Level Verification of Separation

In the current KRC forward-port branch:

```text
VoiceBridge branch: agent/krc-media-gemini-migration
head: 7c2cac849d9322a8b532815ac3be44e87bd52e27
PR: #45 draft/open
Validate run: 33480804395 SUCCESS
cloud tests: 224/224 PASS
```

The configuration contract defines the normal KRC prerecorded provider type as AssemblyAI-only at the current gate.

Equivalent effective state:

```text
KRC_MEDIA_STT_PROVIDER allowed normal value = assemblyai
```

The provider factory fails closed if another normal provider is selected before activation.

The Gemini prerecorded implementation is constructed through a separate candidate path for controlled testing and is not the provider returned to normal managed-media routes.

Therefore:

```text
VoiceBridge live Gemini active                  TRUE
KRC normal Gemini prerecorded active           FALSE
KRC AssemblyAI normal prerecorded active       TRUE
implicit inheritance from STT_PROVIDER         FALSE
```

## Impact on Current MEDIA BETA Runtime

Direct runtime impact of the completed VoiceBridge live migration:

```text
private GPT behavior                            NO CHANGE
Builder package 0.9.1-beta-a10                  NO CHANGE
Action schema 0.6.0-a9.10                       NO CHANGE
isolated beta endpoint                          NO CHANGE
Neon PostgreSQL durable state                   NO CHANGE
Facebook Cobalt-only policy                     NO CHANGE
Telegram zero-credit public policy              NO CHANGE
local attachment boundary                       NO CHANGE
active prerecorded provider                     NO CHANGE / AssemblyAI universal-2
release state                                   NO CHANGE / HOLD
```

The accepted owner MEDIA BETA runtime continues to operate on its existing isolated contour until an explicit later infrastructure/provider transition is approved.

## Positive Engineering Impact

The VoiceBridge migration materially improves the technical basis for KRC future work without activating it automatically.

Relevant benefits:

```text
provider-neutral STT precedent                  VALIDATED
Gemini credential/runtime integration           VALIDATED IN VOICEBRIDGE LIVE DOMAIN
Gemini operational failure handling             IMPROVED BASELINE
rollback discipline                             VALIDATED
no automatic paid fallback policy               CONSISTENT
current VoiceBridge cloud baseline              PHASE 2 COMPLETE
KRC prerecorded Gemini adapter                  IMPLEMENTED / TESTED / INACTIVE
```

The completed VoiceBridge migration reduces uncertainty about shared infrastructure and provider integration patterns, but it does not remove KRC-specific evidence requirements.

## Why VoiceBridge Live Acceptance Cannot Close KRC M3

KRC prerecorded transcription is an evidence-producing subsystem. Its acceptance standard is different from real-time speech translation.

The VoiceBridge live comparison cannot replace KRC prerecorded validation because at least these dimensions differ:

```text
model: gemini-3.5-transcribe-live vs gemini-3.5-transcribe
input: streaming PCM vs prerecorded media/file
session/transport semantics: WebSocket live vs file/request processing
duration limits: different provider feature constraints
timestamps/diarization: KRC evidence-sensitive requirements
cleanup/retention: KRC provider-file lifecycle requirement
corpus: KRC multilingual/evidence corpus differs from VoiceBridge live sample
quality criterion: KRC factual fidelity outweighs fluent cleanup
persistence: KRC durable KRCM contract vs VoiceBridge transient live state
```

Therefore a separate same-asset AssemblyAI/Gemini prerecorded A/B remains mandatory before KRC Gemini activation.

## VoiceBridge Main vs KRC Migration Branch Drift

KRC forward-port base:

```text
eba77183bee29621aa6c7cb859737a10edb6e4d4
```

Current VoiceBridge main:

```text
a426ae331721dd36291874e45380faf603d854cf
```

Comparison result:

```text
KRC migration branch vs current main: DIVERGED
migration branch ahead: 32 commits
migration branch behind: 13 commits
```

The 13 commits added to VoiceBridge main after the KRC branch base modify only documentation/Phase 2 closure files:

```text
README.md
docs/architecture/*
docs/bootstrap/*
docs/history/*
docs/phases/*
docs/planning/03_ROADMAP.md
```

No additional runtime source file appears in that post-base main delta.

Impact:

```text
immediate KRC runtime re-port required solely for this drift: NO
VoiceBridge documentation baseline needs synchronization awareness: YES
re-check/rebase before later integration or M4 productionization: RECOMMENDED
```

This conclusion applies to the currently observed 13-commit delta only; later VoiceBridge main changes must be re-evaluated at the time of M4/rebase.

## KRC Current Roadmap Position After Impact Review

The current KRC prerecorded track remains unchanged:

```text
M0 preflight                                COMPLETE
M1 provider abstraction                     PASS
M2 Gemini prerecorded adapter               PASS / INACTIVE
M3 offline evaluator/contracts              PASS
first public source tranche                 LOCKED
REAL_ASSET_BYTES_CAPTURED                   FALSE
ASSET_SHA256                                NOT_CREATED
REFERENCE_TRANSCRIPT_SHA256                 NOT_CREATED
READY_FOR_AB                                FALSE
M3 prerecorded provider A/B                 NOT_RUN
CURRENT                                     M3 BYTE CAPTURE + SHA-256
M4 canary                                   NOT_STARTED
M5 KRC cutover                              NOT_AUTHORIZED
```

The correct roadmap interpretation is therefore:

```text
VOICEBRIDGE LIVE GEMINI MIGRATION            COMPLETE
KRC PRERECORDED GEMINI MIGRATION             IN PROGRESS / M3
```

These two statements are simultaneously true and must not be collapsed into one project state.

## M4 Impact

VoiceBridge Phase 2 completion is positive evidence that the target VoiceBridge cloud platform is mature enough to remain the forward-port target.

However, before KRC M4 canary the deployment image/runtime still requires a KRC-specific parity audit for:

```text
media retrieval dependencies
media probing/transcoding
managed KRC HTTP routes
Neon/PostgreSQL tooling and durable persistence
quota ledger
KRC retention/cleanup rules
Facebook/Telegram/attachment route isolation
privacy/log-redaction guards
```

VoiceBridge live runtime acceptance does not implicitly validate those KRC-specific dependencies.

## Release Impact

No KRC release gate changes because of the completed VoiceBridge migration.

```text
R1 merge toward KRC main               HOLD
R2 backend/production promotion         HOLD
R3 external testers                     HOLD
R4 public sharing/Store rollout         HOLD
```

A later KRC provider switch also requires a separate explicit owner approval even if M3 quality evidence favors Gemini.

## Documentation Corrections Applied

Updated to make the live/prerecorded distinction explicit:

```text
K_Research_Critic/main/docs/ROADMAP.md
K_Research_Critic/agent/video-url-research/docs/ROADMAP.md
K_Research_Critic/agent/video-url-research/subprojects/media_beta/01_ARCHITECTURE.md
K_Research_Critic/agent/video-url-research/subprojects/media_beta/02_ROADMAP.md
K_Research_Critic/agent/video-url-research/subprojects/media_beta/00_INDEX.md
```

The existing `03_CURRENT_STATE.md` remains the accepted isolated-runtime baseline through the 2026-08-29 hardening state. This audit and the roadmap/architecture updates are the newer provider/infrastructure interpretation overlay.

## Final State

```text
VOICEBRIDGE_LIVE_GEMINI_DEFAULT              ACCEPTED
VOICEBRIDGE_PHASE_2                          COMPLETE
VOICEBRIDGE_MAIN                             a426ae331721dd36291874e45380faf603d854cf
KRC_MEDIA_ACCEPTED_RUNTIME_PROVIDER          AssemblyAI universal-2
KRC_GEMINI_PRERECORDED_ADAPTER               IMPLEMENTED / INACTIVE
KRC_M3                                       ACTIVE
KRC_CURRENT_MILESTONE                        M3 BYTE CAPTURE + SHA-256
KRC_RELEASE_HOLD                             PRESERVED
PUBLIC_CORE_IMPACT                           NONE
```

## Audit Marker

`KRC_MEDIA_VOICEBRIDGE_GEMINI_IMPACT_2026_09_01_APPLIED`
