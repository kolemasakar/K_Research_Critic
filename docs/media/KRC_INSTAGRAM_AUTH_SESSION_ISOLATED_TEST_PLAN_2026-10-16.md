# Instagram authorized-session isolated test plan — 2026-10-16

## Purpose and current authority
Owner selected preparation of this plan, not credential use. No authentication session connected, cookie file created, login attempted, provider start or production mutation. Current anonymous diagnostic category: oEmbed and GraphQL401, login_required and temporary-wait markers; local Cobalt error.api.fetch.empty. This does not prove session authentication will resolve the failure.

## Primary implementation evidence
Exact upstream/production-reported commit a636575b09de1fc55d9b8cd98cac88f5f2f16b42 docs/examples/cookies.example.json uses an instagram array of cookie strings. Adapter reads getCookie('instagram') and may separately read instagram_bearer. COOKIE_PATH is configured for a cookie JSON file; manager validates per-service string arrays and may write updated cookies periodically. Therefore test must use a separate disposable writable copy, never the owner's original browser profile or production configuration.

References:
- https://github.com/imputnet/cobalt/blob/a636575b09de1fc55d9b8cd98cac88f5f2f16b42/docs/examples/cookies.example.json
- https://github.com/imputnet/cobalt/blob/a636575b09de1fc55d9b8cd98cac88f5f2f16b42/api/src/processing/cookie/manager.js
- https://github.com/imputnet/cobalt/blob/a636575b09de1fc55d9b8cd98cac88f5f2f16b42/api/src/processing/services/instagram.js

## Proposed approved scope
1. Owner separately authorizes one test with a lawfully controlled Instagram account/session. Prefer a dedicated test account if available. The owner handles login/MFA/challenge directly; no password or cookies in chat, GitHub, Library, shell history or logs. Use a protected file transfer or administrator placement on host; do not automatically extract a browser profile.
2. Capture exact current image/digest and installed adapter hash via bounded approved metadata before testing. Choose baseline first; do not mix adapter patch and authentication changes in one experiment.
3. Run a disposable isolated process/container from the pinned baseline, without production volumes, published ports, Docker socket, STT keys or persistent job database. Existing infrastructure only, no paid services/proxy/IP rotation. Reuse the existing network identity; no evasion of login/challenge restrictions. This isolation is not yet provisioned or verified.
4. Administrator places only Instagram session material required by the documented schema in a dedicated service-readable directory with restrictive permissions. A disposable copy is mounted only into the test process; COOKIE_PATH points there. Runtime identity/mount permissions must be reviewed; no broad permission grants to krcops. Do not assume all example fields are mandatory or collect unrelated-domain cookies. Session validity checked only as required by the one fixed public reel retrieval; no inbox/private-content/account browsing.
5. One bounded retrieval-only experiment on Dcea3BiPTBm, no STT/AssemblyAI/Gemini. Time/request limits, no automatic retry. Collect stage names, exact HTTP status, static error flags and media-presence/type/duration booleans only. Any resulting signed media URL remains in process memory and is never archived. A small bounded media-header validation may verify audio/video, without persisting content. Required anonymous baseline evidence already exists; do not rerun an anonymous baseline solely for symmetry while throttled.
6. If a stage raises login/challenge/checkpoint/throttling, stop; do not solve/bypass challenges, rotate identity or retry. If retrieval succeeds, do not promote to production or launch STT. Any further isolated patch comparison needs a distinct bounded plan after first result.
7. End test process/container; remove session file and disposable copies, temporary media and any runtime updates. Verify absence by file existence checks only. Owner revokes the test session from Instagram if no longer needed. Do not claim secure forensic erasure; removing files is not proof all physical remnants are erased. Log sanitized metadata only.

## Acceptance matrix
- Diagnostic authentication evidence: expected stage access improves and usable media asset returned, with no challenge; cookie presence alone is not success.
- Retrieval PASS: actual single video/audio resource, not JPEG cover, carousel picker, login HTML, zero-byte file or unsupported local-processing result. No STT call.
- FAIL/INCONCLUSIVE:401 persists, rate marker, challenge, unsupported media, unknown code, timeout or missing metadata. Stop after one experiment, preserve only sanitized facts.
- Successful experiment does not prove long-run reliability, account safety, transcript quality, FREE_ONLY billing or public-release readiness.

## Implementation gate
Existing helper v3 has no session-file input and intentionally lacks arbitrary execution. It must not be repurposed to accept secrets or paths from krcops. Any isolated test launcher must be root-owned, fixed source/image/options, no shell command injection and no broad Docker/sudo grant. This launcher, metadata read and protected credential placement need existing administrator execution. No production deploy permission is included.

## Owner decision required before execution
Explicit authorization to use the owner-selected Instagram session only for the one isolated retrieval experiment, with owner-controlled secure placement and cleanup. No credentials requested in chat. Until authorized and the protected session exists: AUTH_SESSION_TEST=PREPARED_NOT_STARTED; INSTAGRAM_RETRIEVAL=FAIL; FREE_ONLY; PUBLIC HOLD; Telegram LIVE BLOCKED.
