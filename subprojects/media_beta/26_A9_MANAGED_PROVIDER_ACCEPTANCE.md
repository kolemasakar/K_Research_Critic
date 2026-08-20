# A9 Managed Provider Acceptance

Version: 1.0
Status: PASS / LIVE_ACCEPTED
Accepted: 2026-08-20

## Scope

This record accepts the owner-only zero-client managed transcript path used to replace direct Render-to-YouTube acquisition when YouTube blocks datacenter IPs.

Production and `main` were not modified.

## Direct cloud blocker

A normal prerecorded public YouTube probe using the isolated Render service failed before metadata/captions with a YouTube bot/login challenge.

The failed direct-cloud probe charged zero STT seconds.

Disposition:

`DIRECT_RENDER_YOUTUBE = BLOCKED_BY_DATACENTER_ANTIBOT`

The project does not continue blind yt-dlp client permutation as the primary A9 strategy.

## A9.1 server-side STT privacy parity

VoiceBridge server-side AssemblyAI requests now use the configurable base URL contract:

`KRC_MEDIA_ASSEMBLYAI_BASE_URL`

The isolated beta runtime remains configured for:

`https://api.eu.assemblyai.com`

A9.1 code/CI acceptance: PASS.

## Managed provider choice

Primary owner-beta provider:

`Supadata`

Initial mode:

`native`

The initial managed mode requests existing/native transcript data only. Automatic AI transcript fallback is disabled.

## Credit consent gate

A billable managed transcript operation must not start automatically after a media URL is pasted.

Required sequence:

```text
media URL
 -> managed credit preflight
 -> show current credits
 -> show estimated credit cost
 -> show estimated balance after
 -> explicit user choice
      1 = approve
      2 = reject
 -> only after 1, start provider operation with hard credit cap
```

For Supadata native mode the approved operation cap is exactly:

`credit_consent.max_credits = 1`

If native captions are unavailable, the job must stop at:

`AWAITING_AI_CONSENT`

AI generation requires a separate future preflight and separate explicit user approval.

## Live preflight acceptance

Test source:

`https://www.youtube.com/watch?v=IzYyKRx7Qwg`

Preflight result:

```text
plan: Free (100/mo)
credits_available: 100
estimated_native_cost: 1
estimated_remaining: 99
can_continue: true
```

No transcript request was started during preflight.

## Live native acceptance after explicit owner consent

The owner explicitly selected `1` to approve a maximum one-credit native transcript request.

Result:

```text
job_id: KRCM_705fe6a2-5ff4-47de-b6e5-b6c9bf90caa4
status: COMPLETED
provider: supadata
provider_mode: native
detected_language: ru
segment_count: 277
credits_charged: 1
balance_before: 100
balance_after: 99
ai_fallback_authorized: false
```

Timestamped segment validation passed.

Transcript text and credentials were not written into the GitHub acceptance report.

## Accepted backend contract

Managed endpoint family:

```text
POST /api/v1/media/managed/preflight
POST /api/v1/media/managed/transcriptions
GET  /api/v1/media/managed/transcriptions/{job_id}
GET  /api/v1/media/managed/transcriptions/{job_id}/segments
```

The transcript start endpoint rejects missing/invalid one-credit consent before the provider transcript call.

## Acceptance conclusion

`A9_1_SERVER_STT_PRIVACY_PARITY = COMPLETE`

`A9_2_DIRECT_RENDER_YOUTUBE = BLOCKED`

`A9_2R_MANAGED_PROVIDER_NATIVE = COMPLETE`

`CREDIT_CONSENT_GATE = COMPLETE`

`ZERO_CLIENT_GPT_INTEGRATION = NOT_YET_COMPLETE`

## Next engineering target

Proceed to durable zero-client managed job persistence, then connect the managed preflight/consent/transcript contract to the private GPT Action so the owner can complete the entire flow in one ChatGPT conversation without Helper or manual Job ID handling.
