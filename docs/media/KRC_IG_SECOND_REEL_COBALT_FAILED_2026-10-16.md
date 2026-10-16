# KRC — Instagram Cobalt second-source diagnostic, 2026-10-16

## Result
One additional free-only Instagram E2 job, on a different historically successful short reel, confirms the Cobalt retrieval failure is not confined to earlier URL Dcea3BiPTBm. New media processing was initiated only once for the second URL; there were no paid fallbacks, no Telegram starts and no repeated post-failure starts.

## Evidence
- Source: https://www.instagram.com/reel/DF1CIrPSVmf/
- Historical KRC docs report an earlier `COMPLETED` result on this reel; current E2 preflight `request_id=41aa4687-bbbd-4966-a945-3549319d3148`, `can_continue=true`, estimated Cobalt credits 0, automatic_paid_fallback=false.
- Before start, lookup returned HTTP 404, `request_id=a8865d3f-d233-469e-ba9c-e2a1b533b3ed` (no currently reusable job).
- Start request `064a3fc6-d89c-49f0-9c1b-30997356792e`, new job `KRCM_90bc5a30-4d34-4288-9bca-04ff1170cc75`, created 2026-10-16T08:43:09.269Z, `reused=false`. Terminal `FAILED`, `error.code=COBALT_PUBLIC_MEDIA_FAILED`, `retryable=false`; 0 transcript chars, 0 segments, 0 STT seconds, 0 reported credits.
- Readback E2 status **PASS** `request_id=a4a75a9c-6ba0-492d-8632-022b6e6b8d05`; E2 segments **PASS** `request_id=0e64ab08-e17f-4bca-b854-b067bacf0e75`, empty segments as expected for FAILED.
- Neon independent aggregate read showed **2 unexpired FAILED jobs**, consistent with this and the earlier reel's failed attempt, no COMPLETED job.
- Diagnostic VoiceBridge release `38a30cac8e33194cefba04ea2771e91c99531f17` was live before this start. It only converts known upstream authentication rejects to `COBALT_PUBLIC_MEDIA_AUTH_MISSING` or `COBALT_PUBLIC_MEDIA_AUTH_REJECTED`; observed error remained generic `COBALT_PUBLIC_MEDIA_FAILED`. Thus this does not support the specific known auth error categories. Other upstream rejection is still possible.
- Local and public Cobalt health endpoint HTTP 200; v11.7.1 advertises Instagram. Earlier deliberate unauthenticated direct Cobalt POST gave `error.api.auth.key.missing`, as expected. Neither health nor this deliberate 400 demonstrates authorized retrieval of Instagram.
- Render logs query for 08:40–08:47Z yielded zero visible logs; hence upstream HTTP status and specific failure cause cannot yet be determined.

## Acceptance and boundaries
E2 read of real stored FAILED jobs and PostgreSQL persistence PASS. Instagram retrieval of **two distinct URLs** FAIL. Full real COMPLETED transcript with nonempty segments NOT VERIFIED. No further start should be attempted until scoped safe observability or authenticated local diagnostics can distinguish Cobalt's actual upstream failure (e.g. HTTP 4xx category, unsupported reel, upstream Instagram response).

## Next safe technical step
Review only bounded redacted Cobalt logs on authorized host via a separately approved privileged diagnostic channel, or augment backend to emit a strict status/category allowlist. Do not reveal API keys, bearer tokens, media URLs, transcript contents, raw response bodies or cookies. Do not change credentials blind. Maintain FREE_ONLY, E4 Telegram LIVE blocked, public R4 HOLD.
