# MEDIA BETA Architecture
Архітектура прийнятого owner-only zero-client MEDIA BETA контуру та ізольованого provider-migration треку.

Version: 2.1
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

## Isolation and Engineering Branches

Accepted KRC beta product/documentation branch:

```text
K_Research_Critic: agent/video-url-research
```

Legacy/accepted VoiceBridge KRC-media runtime lineage:

```text
VoiceBridge: agent/krc-media-transcript
```

Active provider-migration forward-port:

```text
VoiceBridge: agent/krc-media-gemini-migration
Draft PR: #45
```

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

VoiceBridge live STT provider selection is independent from the KRC prerecorded provider selection.

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
live AssemblyAI/Gemini corpus A/B       NOT_RUN
```

The current valid transition is exact media-byte capture and SHA-256 hashing, followed by independent reference preparation/review. Raw media must not be retained as a GitHub artifact by that capture step.

## Transcript/Evidence Boundary

Media acquisition may occur before the CriticProfile. Independent factual verification may not. Transcript content is source evidence for what was said and does not count as an independent truth cross-check.

## Critic Contract

Risk floors are `LOW>=0`, `MEDIUM>=1`, `HIGH>=2`, `CRITICAL>=3`. Every material factual claim tracks `required`, `achieved_independent`, and `exception`. Shortfalls remain visible and qualify the result.

## Presentation Contract

A10 requires the normal four-column claim summary plus an identical fenced copy-safe table. The second form mitigates an external ChatGPT whole-response Copy serialization defect.

## Release Boundary

Current state is `RELEASE_HOLD_OWNER_TESTING`. Merge, backend/production promotion, external testers, and public rollout are separate future owner decisions. Completion of M3 does not itself approve any of those gates.
