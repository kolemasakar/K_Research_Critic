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

## Follow-up cold-429 reproduction — 2026-10-10 12:17+ UTC
- Attempted one additional public Facebook source via approved E3 route: https://www.facebook.com/spaceappschallenge/videos/2414369805425544/. Tool failed before returning a MEDIA job: voicebridge_http_error, http_status=429, retryable=true. Do not assert provider work occurred or that none occurred without a confirmed lookup; do not repeat POST.
- VoiceBridge Render app logs show service_stopping SIGTERM at 2026-10-10T12:17:02.683696919Z (instance srv-da1kic5bedkc73d6fk60-7fvz8), preceding the 429 observation. This is temporal evidence only; it does not attribute HTTP 429 to a specific proxy/application component.
- External health-only GET from krc-cobalt returned HTTP 200 / JSON status=ok in 13.33 s, Content-Type application/json; charset=utf-8; Server cloudflare; x-render-origin-server Render; x-request-id 1e3983ef-1c08-449a-8157-18f3b39abc86; CF-RAY a485948edda8d246-FRA. Those are headers of the SUCCESSFUL health request, NOT headers of the failing 429 request.
- Needed attribution measurement remains response headers/content-type/request-id directly from failed cold KRC→VoiceBridge health GET; correlate with Render edge/request log and app starts. Current R3C _wait_for_voicebridge_health catches HTTPError but discards sanitized metadata, including status details. A bounded read-only instrumentation change may capture per-attempt safe metadata, but requires separate code change and test/deploy before it can confirm the cause.
- Telegram invocation blocked in prior check by platform safety. No bypass or retry performed. Long test gate still PARTIAL; no unverified video durations accepted.

## Cold readiness HTTP instrumentation — 2026-10-10 (next continuation)
- Source updated: plugins/krc_migration_candidate/mcp_canary/r3c.py. First HTTPError per _wait_for_voicebridge_health run now logs HTTP code, attempt number and safe_http_error_metadata allowlist only. No raw response body, arbitrary headers, auth tokens, or URL. It preserves readiness retry count/budget and does not send a consequential POST when not ready.
- Regression added: tests/test_media_execution_readiness.py::test_cold_health_429_logs_only_allowlisted_diagnostics.
- GitHub commits: instrumentation 9658f9b287f84d4353fa1c32be714d9c6684244f; regression e4aa0c9cf52d7d71d87822201d2f44f0e38e8aa9.
- Remote krc-cobalt local smoke using mocked HTTPError 429, Content-Type HTML, Retry-After 11, secret header and body: PASS, exactly one log entry over two attempts, no secret leakage. Python compileall PASS. Existing unittest diagnostics: 7/7 PASS.
- Full pytest regression NOT RUN because available Python environment has no pytest module. The new pytest case itself has not been run under pytest. Therefore acceptance/deploy gate is NOT PASS and Render deployment was NOT triggered.
- Important limitation: new sanitized log is emitted in MCP app server, but when no MCP instance exists yet or Render edge blocks request before MCP process runs, application logs cannot capture this event. Further confirmation requires a real cold condition after tests.
- FREE_ONLY remains unchanged. VoiceBridge repository/production not modified during this instrumentation step; no job starts, provider work, keepalive, paid fallback or changes to main.

## Full regression + Render instrumentation deployment — 2026-10-10 12:35 UTC
- Test environment: existing krc-cobalt workspace /tmp/krc_all_routes_integration_20261004; Python 3.12 with Python dependencies installed to isolated /tmp/krc_pytest_deps_20261010 via pip --target, no sudo/system Python changes. Targeted diagnostics/readiness: 21 passed. Full `PYTHONPATH=/tmp/krc_pytest_deps_20261010:. python3 -m pytest -q tests`: **480 passed, 17 skipped, 0 failed; exit 0, 19.18 seconds**. Skipped tests were not exercised.
- The local workspace source included the same bounded readiness-429 patch and regression previously committed to KRC. Prior lack of pydantic/dotenv dependencies was remedied in temporary isolated test directory.
- With test gate passed, explicitly triggered Render deployment for R3C only: service srv-dale3r942hec73c5t9hg, deploy dep-db531knlk1mc738ie850, deployed branch source commit c577ba9f4d891817ca54d186ce3e0159d179472b, status **live**, finished 2026-10-10T12:35:07.214879Z. VoiceBridge was NOT redeployed or modified.
- External read-only GET from krc-cobalt: R3C /healthz HTTP 200 in 3.19 s; VoiceBridge /api/v1/health HTTP 200 in 0.18 s. Read-only R3C media_get_capabilities succeeded, request_id fc546c2a-0d77-46a2-b844-8e65e1c27efa; configured=true, automatic_paid_fallback=false, durable_store=postgres.
- **Cold-429 root cause remains OPEN**. VoiceBridge was already warm in this check, so no new cold 429 with the enhanced logs was observed. The instrumentation is active on R3C, but sufficient cold response provenance is not available yet. Do not claim that the defect has been resolved.
- No provider jobs started, no paid fallback, no Telegram retry, no keepalive, and no public/main changes in this step. Long live checks remain PARTIAL.

## Continuation: reproduced cold 429 and Facebook three-minute live test — 2026-10-10
### Cold health failure after deployed diagnostics
- R3C live diagnostic log at 2026-10-10T12:59:29.654511209Z: `voicebridge_readiness_http_error status=429 attempt=1 diagnostics={}`.
- Subsequent R3C read-only media_get_capabilities failed with `voicebridge_http_error`, HTTP 429, `readonly_health_attempts=22`, `readonly_health_ready=false`. R3C POST /mcp HTTP 200 appears at 13:00:14.566538705Z; 429 was returned in the tool result, not as MCP transport status.
- VoiceBridge log: service_stopping SIGTERM at 12:50:23.345302381Z; next service_started at 13:00:46.664863556Z, after the unsuccessful internal R3C cold readiness cycle.
- External krc-cobalt health-only GET later returned HTTP 200/status=ok, elapsed 13.372 s; headers from this SUCCESSFUL response included Content-Type application/json; Server cloudflare; x-render-origin-server Render; x-request-id 8d395bfc-8273-45e6-86b3-cd844d72c579; CF-RAY a485cf155ff71e33-FRA.
- Evidence excludes normal MEDIA POST admission control for GET /health and confirms cold failure before application startup. However the exact layer producing 429 (Render routing vs other edge proxy) remains unproven; diagnostics={} indicates no allowlisted application code, response format, retry-after, or request ID was extracted. Do not declare solved.

### Facebook live, recovered start and segments
- Public URL: https://www.facebook.com/FriendsOfNASA/videos/1515673112768756/
- Job KRCM_c7547bbc-cb9b-4f20-b18d-079991116343; start request_id e0df5c75-8c51-4d61-9378-f700e62710ba, recovered PROCESSING, reused=true, start_response_recovered=true. No second start was sent.
- Status subsequently COMPLETED, request_id f5ea615b-c588-47ad-a4e2-d1b9b20c8fb9. Media duration 180.302938 s; 3 transcript segments, 2984 characters; STT charged seconds 181, credits charged 0, charge uncertain=false, provider_data_deleted=true, cobalt retrieval + assemblyai STT.
- Segment read request_id 8d794b04-ab56-4597-b65b-c5fe8581c944, indices 0,1,2, cursor=0, next_cursor=null; segment ends 59920 / 119620 / 171500 ms. Audio transcription was not independently validated against original media.
- This confirms a ~3 minute Facebook route but NOT the planned 8–12 minute gate. Prior Facebook failed audio-normalization sample remains separate. Instagram long sample not executed without a verified suitable URL; Telegram invocation previously blocked by platform safety and not repeated. FREE_ONLY unchanged.

### Remaining scope
- Cold-429 attribution requires correlatable failed-response edge diagnostics (safe header/server/trace ID capture on FAILED health, Render support/edge logs); do not infer cause from timestamps alone.
- Additional verified 8–12 minute IG/FB audiovisual examples are required to close long-test gate. Do not reuse FAILED jobs or start undocumented speculative media. Telegram safety gate remains respected.

## Continuation: Render edge-provenance instrumentation — 2026-10-10
- R3C `plugins/krc_migration_candidate/mcp_canary/voicebridge_http_diagnostics.py` now extracts only tightly allowlisted error-response proxy provenance: `Server` enum cloudflare/render, `X-Render-Origin-Server` literal Render flag, bounded Cloudflare Ray format, UUID `X-Request-Id`; pre-existing JSON/HTML and Retry-After handling retained. Arbitrary header values, bearer tokens, body content, and unvalidated IDs are not logged.
- Additional tests in `tests/test_voicebridge_http_diagnostics.py` verify the allowed fields and malicious/untrusted values. Local krc-cobalt tests: targeted **23 passed**; full suite **482 passed, 17 skipped, 0 failed** (19.43 seconds). Full test environment was isolated in /tmp; no OS-wide dependencies changed.
- KRC commits: code `74dc423b9ca19e4f1005dedf0c936f7ab97031b7`; tests `7087ad33ccfc4e431e0e95143195241553196e3a`. Only KRC service was redeployed on Render: service `srv-dale3r942hec73c5t9hg`, deploy `dep-db53l5nlk1mc738kh4ig`, commit `7087ad33ccfc4e431e0e95143195241553196e3a`, status **LIVE** 2026-10-10T13:16:57.320023Z. VoiceBridge was not redeployed.
- Read-only `media_get_capabilities` after deployment succeeded, request_id `20de767c-5c61-4c20-ad8b-a9618179291c`, configured=true, durable_store=postgres, paid fallback false. R3C application log POST /mcp HTTP 200 at 13:17:05.227751558Z. **No new cold 429 occurred after this deployment** and no root-cause attribution can yet be claimed. Earlier observed cold 429 with diagnostics={} remains authoritative as prior observation.
- The last source-candidate web search did NOT identify a demonstrably public, 8–12-minute Instagram/Facebook clip with verified duration and usable audio; thus no speculative long-media POST was sent. Telegram remains blocked by the platform safety gate and was not retried.
- Next safe gate: observe a real cold read-only GET failure and correlate its allowlisted provenance with Render logs. If no trace ID is returned on the failing response, Render edge-level instrumentation/support is required to attribute 429 conclusively. Keep FREE_ONLY; no keepalive or paid fallback.
