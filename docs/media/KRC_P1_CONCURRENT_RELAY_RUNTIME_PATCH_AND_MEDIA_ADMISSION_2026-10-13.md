# KRC P1 execution checkpoint — concurrent wake fix and media admission (2026-10-13)

## Scope
Owner approved P1 steps (1) concurrent cold wake remediation, (2) public Instagram/Facebook 480–720 s video discovery, (3) one permissible media start per verified candidate, (4) status/segments, accuracy, free-only and completeness checks. Execution stays gated by the established admission protocol and safeguards.

## 1. Concurrent cold wake — deployed minimally on krc-cobalt
Source GitHub branch `agent/krc-public-media-r3-integration` already contained `RateGate.begin_or_join()` with `Condition(Lock())`, 34 s join window and 90 s cooldown in `plugins/krc_migration_candidate/p0_wake_relay_server.py`. The actual krc-cobalt runtime `/home/krcops/krc-p0-wake/relay_server.py` was inspected and contained an older `RateGate.acquire()` returning immediate 429 on concurrent requests. This source/runtime difference explains observed concurrent `relay_rejected` from 2026-10-13 16:21 UTC; it does not prove exact request-level correlation.

With owner authorization under P1:
- Backed up exact original runtime script to `/home/krcops/krc-p0-wake/relay_server.py.bak-concurrent-20261013T175803Z`.
- Replaced the legacy cooldown-only gate with a bounded `begin_or_join` model matching current GitHub design, retaining safe diagnostic event logging, fixed upstream, no arbitrary URL, strict bearer auth, loopback binding, one owner wake and protected 0600 source mode.
- Parsed revised Python successfully; restarted existing unprivileged user service `krc-p0-wake-relay.service`, status ACTIVE.
- Offline concurrent unit simulation: one owner + second waiter, joined success returns `ready`; failed owner means second waiter returns `unavailable`, fresh attempt under cooldown returns `rate_limited`; `OFFLINE_CONCURRENCY_SELFTEST_PASS`.
- Local HTTP negative gate: GET fixed route = 405; unauthenticated POST = 403; service ACTIVE. These probes did NOT generate a VoiceBridge wake.
- **Not yet independently proven:** real simultaneous cold requests E1/E2 against deployed relay; this requires a separate controlled live concurrent probe window and must not be inferred from offline self-test.
- No Render code/deploy changes; no secret read/output; no provider call.

## 2. Long-video candidate search
Public web searches performed for Instagram reels/posts and Facebook videos/interviews. Facebook official material confirms platform permits long videos, and Instagram has long video/reel support, but neither fact identifies a test asset. Search results lacked independent exact stream duration 480–720s and checked speech/audio for an individual public canonical URL. No Instagram/Facebook URL passed admission. **BLOCKED_MISSING_VERIFIED_480_720S_MEDIA**.
Previously identified official TED editorial 654s YouTube comparator remains partial evidence, not a substitute for exact media-stream audio and duration verification; earlier YouTube start failed at readiness with `consequential_post_attempted=false`. Do not retry blindly.

## 3–4. MEDIA execution and quality validation
Under `docs/media/KRC_LONG_MEDIA_LIVE_TEST_PROTOCOL_2026-10-10.md`, consequential provider start must not occur until eligible public URL, independently verified 480–720s exact duration and speech, current FREE_ONLY preflight and credits evidence. No qualifying Instagram/Facebook inputs found, so real start deliberately NOT_RUN, status/segments and human three-point audio comparison NOT_RUN. Telegram remains BLOCKED. No provider jobs created or paid fallback used.

## Completion ledger
| Work item | Result |
|---|---|
| 1. source/runtime concurrent relay audit | PASS |
| 1. guarded deployed patch + backup + restart | PASS |
| 1. isolated concurrency test | PASS |
| 1. local unauthorized/method gates | PASS |
| 1. concurrent production cold E2E | OPEN |
| 2. public candidate discovery | attempted; qualifying Instagram/Facebook media NOT_VERIFIED |
| 3. FREE_ONLY long provider starts | NOT_RUN / ADMISSION BLOCK |
| 4. long transcripts, audio three checkpoints | NOT_RUN |

## Next actions
- Independently validate one Instagram and one Facebook public canonical video with exact 480–720s duration and speech using actual player metadata or lawful downloaded bytes and ffprobe. Search descriptions alone are insufficient.
- After verified candidates, one start per approved media source and immediate status/segments within configured TTL; no retry after unknown consequential outcome.
- Schedule a controlled concurrent cold R3C+E1/E2 readiness test to demonstrate the deployed relay join behavior without starting paid work, inspect Render and safe krc-cobalt event logs.
- Keep FREE_ONLY, fail-closed Telegram and separate R4 release acceptance.

## Live post-patch concurrent read-only recovery — 2026-10-13T18:00Z
- Historical Render VoiceBridge logs show `service_stopping` at 17:19:54Z and no later start before controlled test. After 40 min idle, two MCP `media_get_capabilities` requests were dispatched simultaneously to R3C and E1, both **PASS**.
- R3C response `request_id=61b03cf5-120f-482a-974c-c0312732c810`, `configured=true`, `automatic_paid_fallback=false`. E1 `request_id=420e043a-8765-4631-9b45-3610b0e0d022`, same configured/FREE_ONLY results.
- R3C log: 18:00:10.500Z cold readiness 429 CF-Ray `a4a03e050c89d2e7-FRA`; VoiceBridge startup 18:00:18.332Z; R3C `relay_success` 18:00:23.284Z and HTTP 200 at 18:00:27.445Z.
- Independent relay `krc-cobalt` journal confirms `wake_relay_success` at 18:00:23Z.
- This confirms real cold recovery while two read-only requests were issued concurrently, with both completing. It does **not** demonstrate that both POSTs arrived simultaneously at relay or that the join branch specifically executed: journal recorded a single `wake_relay_success` and no `wake_relay_join_success` in the inspected interval.
- No new MEDIA jobs, STT/retrieval provider starts or paid fallback.
- Update verdict: `CONCURRENT_READONLY_COLD_CAPABILITIES=PASS`; `CONCURRENT_RELAY_JOIN_BRANCH=OFFLINE_PASS_LIVE_NOT_OBSERVED`. Long-video candidate admission and consequential P1 media tests remain blocked by absent independently verified 480–720s speech-bearing Instagram/Facebook videos.
