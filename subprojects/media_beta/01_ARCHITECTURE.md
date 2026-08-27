# MEDIA BETA Architecture
Архітектура прийнятого owner-only zero-client MEDIA BETA контуру.

Version: 2.0
Status: ACCEPTED_PRIVATE_ARCHITECTURE / RELEASE_HOLD
Updated: 2026-08-27

## Topology

```text
OWNER
 -> K-Research & Critic - MEDIA BETA
 -> private Action bearer
 -> isolated VoiceBridge MEDIA BETA
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

## Isolation

KRC feature branch: `agent/video-url-research`, draft PR #8.
VoiceBridge feature branch: `agent/krc-media-transcript`, draft PR #28.
Dedicated backend: `voicebridge-krc-media-beta-kolemasakar`.

Public KRC `main` and production VoiceBridge are not deployment targets during the current release hold.

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

## Transcript/Evidence Boundary

Media acquisition may occur before the CriticProfile. Independent factual verification may not. Transcript content is source evidence for what was said and does not count as an independent truth cross-check.

## Critic Contract

Risk floors are `LOW>=0`, `MEDIUM>=1`, `HIGH>=2`, `CRITICAL>=3`. Every material factual claim tracks `required`, `achieved_independent`, and `exception`. Shortfalls remain visible and qualify the result.

## Presentation Contract

A10 requires the normal four-column claim summary plus an identical fenced copy-safe table. The second form mitigates an external ChatGPT whole-response Copy serialization defect.

## Release Boundary

Current state is `RELEASE_HOLD_OWNER_TESTING`. Merge, production promotion, external testers, and public rollout are separate future owner decisions.
