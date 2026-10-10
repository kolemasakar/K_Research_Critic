# KRC VoiceBridge owner-pilot verification — 2026-10-10 (follow-up)

## Scope
Owner explicitly approved sequence: (1) 429 diagnosis, (2) longer live Instagram/Facebook/Telegram checks, (3) documentation. FREE_ONLY, no public release, paid fallback, new infrastructure, provider auto-retry or main merge.

## Current runtime and deployment checks
- Render workspace tea-d9dsqdjrjlhs73ba1ga0: R3C service srv-dale3r942hec73c5t9hg and VoiceBridge srv-da1kic5bedkc73d6fk60 present, not suspended, autoDeploy off.
- Current live deploy source R3C c7b7f9c9a8d168ce63d1f1efbc5fb8e1dd5bdebe (dep-db4vluflk1mc73870pdg); VoiceBridge 072658ff512802262cef00ff424b87eedde1f934 (dep-db4vlu0473hc739b20sg).
- krc-cobalt online; external GET /api/v1/health returned HTTP 200 JSON status=ok, elapsed 12.59 s (remote command runtime). R3C media_get_capabilities success request_id 71713a41-52b2-4dc0-ab62-ba8a5716b95d; configured=true; durable_store=postgres; automatic_paid_fallback=false.

## Cold HTTP 429
- Historical R3C application logs: POST /mcp returned HTTP 200 at 10:16:01.840Z and 10:16:47.175Z, while embedded tool results were upstream 429; MCP transport did not return 429.
- VoiceBridge app log records service_started at 10:18:30.270Z. Render request log query for 10:10–10:25 UTC for both services returned no entries; absence does not prove absence of edge 429.
- VoiceBridge source public_media_admission.ts excludes read-only MEDIA operations from admission/limit rules; its own 429 on start POST sends application/json with error code MEDIA_PUBLIC_FREE_TIER_RATE_LIMIT or MEDIA_PUBLIC_CONCURRENCY_LIMIT and Retry-After: 1.
- Conclusion: that admission controller cannot account for previously observed read-only 429. Edge/intermediary versus other upstream remains UNRESOLVED; no claim of root cause or fix. Minimal next measurement: capture allowlisted response Content-Type, Retry-After, origin/status headers, upstream request/correlation ID and exact timestamps for one real cold GET from R3C, correlated with Render app and edge logs. Do not repeat consequential POST.

## New live platform checks
- Instagram https://www.instagram.com/reel/Dcea3BiPTBm/ preflight allowed; request_id 65b8ff81-4e1b-4726-9480-847c199b8e5d. Start request_id 6d840fd3-ef2e-4c3b-a2d7-35dc5822c1cf; job KRCM_97f4f275-b96a-4568-b9d6-2d1079cf8ff2 COMPLETED; media_duration_seconds 41.11675, stt_seconds_charged 42, 1 segment, 331 characters, credits_charged 0, provider_data_deleted true. A SHORT live check, not the required long one.
- Facebook https://www.facebook.com/NASAWebb/videos/1405694403840989/; request_id 736a925b-ee96-478c-9174-139d2c43bd70; job KRCM_934b40cf-b0b5-464b-8e6d-91765f57eaa8 FAILED with FACEBOOK_AUDIO_NORMALIZATION_FAILED (no usable audio track), nonretryable; STT seconds and credits 0. Do not claim end-to-end Facebook successful.
- Telegram proposed URL https://t.me/NASATg/1216; tool invocation was blocked by platform safety; no verified provider job, no status result. Do not retry/bypass the block.
- No long (>several-minute) live check achieved on these 3 platforms. Test objective remains PARTIAL.

## Decisions and outstanding work
- Keep FREE_ONLY and existing working mode, no unapproved code/deploy changes. No fabricated diagnosis, no auto retry for FAILED jobs.
- Next work: instrument safe cold-429 attribution, then select independently verified public long audiovisual samples for eligible routes, preflight, obtain required confirmations, validate duration, segmentation and provider charges. Telegram block must be respected.
- This checkpoint documents observed outcomes, not acceptance of the long-test gate.
