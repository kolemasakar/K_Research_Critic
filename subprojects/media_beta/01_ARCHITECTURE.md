# MEDIA BETA Architecture
Архітектура прийнятого owner-only zero-client MEDIA BETA контуру та ізольованого prerecorded provider-migration треку.

Version: 2.2
Status: ACCEPTED_PRIVATE_ARCHITECTURE / RELEASE_HOLD / M3_ACTIVE
Updated: 2026-09-01

## Product Hierarchy

```text
K-Research & Critic
 -> public Core: K_Research_Critic/main
 -> closed-beta module: K-Research & Critic - MEDIA BETA
      -> KRC product state/roadmap authority: K_Research_Critic
      -> media/backend technology and implementation evidence: VoiceBridge
```

VoiceBridge is a technology and backend implementation source. It is not the parent KRC product and cannot independently authorize a KRC release gate.

## Accepted Runtime Topology

```text
OWNER
 -> K-Research & Critic - MEDIA BETA
 -> private Action bearer
 -> isolated VoiceBridge MEDIA BETA runtime
 -> source router
    -> YouTube/Instagram managed transcript
    -> Facebook Cobalt -> AssemblyAI
    -> Telegram public web/embed -> trusted CDN -> AssemblyAI
    -> local openaiFileIdRefs -> trusted OpenAI delivery -> AssemblyAI
 -> durable Postgres KRCM job/segments
 -> CriticProfile
 -> owner approval
 -> Research
 -> Critic
 -> final report
```

## VoiceBridge Shared Technology Baseline

VoiceBridge itself has completed the real-time STT provider transition to Gemini and closed Phase 2 Universal Cloud Audio.

```text
VoiceBridge main                               a426ae331721dd36291874e45380faf603d854cf
streaming STT default                          Gemini gemini-3.5-transcribe-live
streaming STT rollback                         AssemblyAI universal-streaming-english
Phase 2 Universal Cloud Audio                  COMPLETE
```

This is an accepted technology baseline for future KRC forward-port work. It is not the active KRC prerecorded-media provider state.

## Two Independent STT Domains

The architecture intentionally separates VoiceBridge live speech recognition from KRC prerecorded evidence transcription.

```text
DOMAIN A - VoiceBridge real-time streaming
 browser PCM/WebSocket
 -> SttProvider
    -> Gemini Live          DEFAULT
    -> AssemblyAI streaming ROLLBACK

 configuration:
 STT_PROVIDER=gemini
 GEMINI_STT_MODEL=gemini-3.5-transcribe-live

DOMAIN B - KRC MEDIA BETA prerecorded media
 retrieved/uploaded media file
 -> MediaTranscriptionProvider
    -> AssemblyAI universal-2      ACTIVE
    -> Gemini prerecorded adapter  IMPLEMENTED / INACTIVE

 configuration:
 KRC_MEDIA_STT_PROVIDER=assemblyai
 KRC_MEDIA_TRANSCRIBE_MODEL=gemini-3.5-transcribe
```

A change in Domain A must not implicitly change Domain B.

The current forward-port implementation makes this separation fail-closed: the normal KRC provider selector accepts only `assemblyai` until the explicit Gemini activation gate, and the Gemini prerecorded adapter is constructed through a separate controlled candidate path.

Consequences:

```text
VoiceBridge live Gemini migration complete      YES
KRC prerecorded Gemini migration complete       NO
normal KRC provider changed                     NO
KRC Gemini adapter implemented                  YES
KRC Gemini adapter active                       NO
separate KRC same-asset A/B required            YES
```

The VoiceBridge live A/B cannot be treated as KRC prerecorded acceptance evidence because the models, transport/file semantics, corpus, duration/timestamp constraints, and evidence-fidelity requirements are different.

## Isolation and Engineering Branches

Accepted KRC beta product/documentation branch:

```text
K_Research_Critic: agent/video-url-research
```

Legacy/accepted VoiceBridge KRC-media runtime lineage:

```text
VoiceBridge: agent/krc-media-transcript
```

Active KRC prerecorded provider-migration forward-port:

```text
VoiceBridge: agent/krc-media-gemini-migration
Draft PR: #45
Head: 7c2cac849d9322a8b532815ac3be44e87bd52e27
Exact-head Validate: 33480804395 SUCCESS
```

The forward-port branch was created from VoiceBridge main at `eba77183bee29621aa6c7cb859737a10edb6e4d4`. Current VoiceBridge main is 13 commits ahead of that base. The compared post-base delta is documentation/Phase 2 closure synchronization, not a new runtime-code delta. Therefore it does not by itself invalidate the KRC forward-port implementation.

Dedicated beta backend remains `voicebridge-krc-media-beta-kolemasakar` until a separately approved infrastructure transition. Public KRC Core and production/backend promotion are not implicit targets during the current release hold.

## Prerecorded STT Provider Boundary

Current accepted runtime provider:

```text
KRC prerecorded STT -> AssemblyAI universal-2
```

Active migration architecture under validation:

```text
KRC prerecorded STT
 -> MediaTranscriptionProvider
      -> AssemblyAI adapter          ACTIVE/ROLLBACK
      -> Gemini prerecorded adapter  IMPLEMENTED / INACTIVE
```

Current migration checkpoint:

```text
M0 COMPLETE
M1 PASS
M2 PASS / GEMINI INACTIVE
M3 ACTIVE
CURRENT: M3 BYTE CAPTURE + SHA-256
READY_FOR_AB: FALSE
M3_LIVE_AB: NOT_RUN
```

No current M3 evidence-preparation step activates Gemini for normal MEDIA BETA jobs.

## Authentication

The GPT-facing Action uses bearer authentication. Owner admission and provider credentials remain server-side. The normal owner flow does not request a beta code, platform credentials, cookies/session, Helper, file ID, signed URL, or KRCM Job ID.

## Durable Job Contract

Managed jobs use `KRCM_` identifiers internally and durable Postgres state. Completed state and timestamped segments survive backend replacement. Duplicate request reuse is supported where defined. Uncertain-charge operations are never automatically replayed.

## Source Adapters

### YouTube / Instagram

Managed provider route. Billable operations require preflight and explicit consent. Instagram AI fallback requires a separate quote and new consent.

### Facebook

Active route is free Cobalt retrieval only. Successful retrieval may proceed to AssemblyAI and durable KRCM. Cobalt failure is terminal unavailable. ScrapeCreators remains reserved compatibility code only.

### Telegram

Only supported public post forms are accepted. Retrieval is public web/embed based, follows trusted Telegram media delivery, uses zero retrieval credits, and never requires Telegram authentication or paid fallback.

### Local Attachment

Exactly one supported current-conversation audio/video attachment may be supplied through ChatGPT `openaiFileIdRefs`. Backend acceptance is limited to trusted OpenAI HTTPS media delivery, bounded size/type/duration, no redirects to arbitrary hosts, and no user-visible file token. Current max attachment size is 32 MiB.

## M3 Evidence Boundary

The first three public corpus source candidates are locked, but no case is yet `READY_FOR_AB`.

```text
exact media bytes captured             FALSE
asset SHA-256                           NOT_CREATED
reference transcript SHA-256            NOT_CREATED
live AssemblyAI/Gemini prerecorded A/B  NOT_RUN
```

The current valid transition is exact media-byte capture and SHA-256 hashing, followed by independent reference preparation/review. Raw media must not be retained as a GitHub artifact by that capture step.

## M4 Infrastructure Boundary

VoiceBridge Phase 2 completion strengthens the target cloud-platform baseline, but does not prove KRC-specific deployment parity.

Before M4 canary, independently verify the target image/runtime contains every KRC dependency and contract required for:

```text
managed media retrieval
media probing/transcoding
KRC Action HTTP routes
Neon/PostgreSQL durable persistence
quota ledger
provider cleanup
privacy/log-redaction behavior
source-specific Facebook/Telegram/attachment boundaries
```

## Transcript/Evidence Boundary

Media acquisition may occur before the CriticProfile. Independent factual verification may not. Transcript content is source evidence for what was said and does not count as an independent truth cross-check.

## Critic Contract

Risk floors are `LOW>=0`, `MEDIUM>=1`, `HIGH>=2`, `CRITICAL>=3`. Every material factual claim tracks `required`, `achieved_independent`, and `exception`. Shortfalls remain visible and qualify the result.

## Presentation Contract

A10 requires the normal four-column claim summary plus an identical fenced copy-safe table. The second form mitigates an external ChatGPT whole-response Copy serialization defect.

## Release Boundary

Current state is `RELEASE_HOLD_OWNER_TESTING`. Merge, backend/production promotion, external testers, and public rollout are separate future owner decisions. Completion of VoiceBridge Phase 2 or KRC M3 does not itself approve any of those gates.
