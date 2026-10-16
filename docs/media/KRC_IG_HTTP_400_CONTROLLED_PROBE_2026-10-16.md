# KRC Instagram controlled HTTP diagnostic — 2026-10-16

## Scope
Owner continued from restored checkpoint 10818b14. One new Instagram start only; FREE_ONLY retained, no paid fallback, no Telegram execution, no deployment or privilege changes.

## Readiness and source
- R3C capabilities request 20b6ea3b-8c93-48c2-9fae-80a4251df1c2: configured=true, durable_store=postgres, duplicate_start_reuses_job=true, all paid fallbacks=false.
- Distinct source https://www.instagram.com/reel/DdIKGSaRILW/; publicly indexed speech-bearing reel. Exact duration could not be independently established before start, so this is a retrieval diagnostic, not verified short-duration acceptance or transcript-quality validation.
- E2 preflight cd9d0d40-165a-45c7-8627-2c9c90ca26b7: can_continue=true, estimated retrieval credits=0, consent_required=false, Cobalt/AssemblyAI.
- Pre-start lookup 616328d7-da90-42bb-b429-6b2ce6407184: HTTP 404, no reusable durable job.

## Single start and persistent readback
- Start request ca43698a-a927-4502-828d-cd445c753d5f.
- Job KRCM_e3e37765-cc0d-4240-a668-4ae5aefaa910, reused=false.
- Created 2026-10-16T09:38:34.374Z; terminal update 09:38:36.357Z.
- FAILED; error/free_retrieval_error_code COBALT_PUBLIC_MEDIA_HTTP_400; retryable=false.
- STT seconds 0, credits 0, transcript characters 0, segments 0, credit_charge_uncertain=false. These are reported counters, not independent billing audit.
- E2 status request d0365793-324a-47ad-8f60-6dc85f16d8c0 confirmed same persisted failure.
- E2 segments request e32ad5da-8e7d-4175-a0c8-f87bb10a8c5c: empty array, next_cursor=null, FAILED.

## Interpretation and next gate
New bounded HTTP classifier is exercised live and identifies a Cobalt HTTP 400 rejection. This observation is not HTTP 429 or 5xx and did not map to the known allowlisted auth errors. It does not establish the exact upstream reason or rule out other authorization/input/platform failures. Raw upstream error code/body has not been obtained. Do not change credentials speculatively or repeat failed processing.

Next technical work: read the exact Cobalt request contract and classifier, then obtain only a bounded sanitized upstream error code via authorized diagnostics. Preserve existing privilege boundaries. Instagram retrieval remains FAIL in this probe; R4 PRIVATE PARTIAL, public HOLD, Telegram LIVE BLOCKED.
