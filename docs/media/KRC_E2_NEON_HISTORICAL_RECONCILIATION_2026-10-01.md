# KRC E2 historical and current evidence reconciliation — 2026-10-01

## Historical verified checkpoints (19 September)
- `subprojects/media_beta/137_R3E2_INSTAGRAM_LIVE_CANARY_DURABLE_FREE_ONLY_PASS_2026_09_19.md`: real E2E for `https://www.instagram.com/reel/DF1CIrPSVmf/`, job `KRCM_04e6d847-449c-4d0f-82c7-b494871d9322` COMPLETED, one segment, Cobalt retrieval, AssemblyAI STT, 43 seconds quota ledger, zero KRC credit charge.
- `subprojects/media_beta/138_R3E2_RESTART_REPLAY_STATUS_SEGMENTS_PASS_2026_09_19.md`: status and segment read after VoiceBridge/E2 restarts PASS, no new provider work during replay.
- Historical success does not imply today's deployment or a different test URL works.

## Current read-only live checks
- Canonical VoiceBridge `/api/v1/health` HTTP 200, existing E2 `/healthz` status ok, `confirmation_probe_only:true`, binding configured.
- Lookup of new test URL `https://www.instagram.com/reel/Dcea3BiPTBm/` returned 404 after warmup.
- Render VoiceBridge logs show only service lifecycle entries in the checked window; no accessible per-job start record. AssemblyAI owner screenshot balance $48.31 before and after attempted start, no visible delta; usage reporting delay not excluded.
- Direct read-only Neon check used **the historical checkpoint's exact** project `plain-snow-71973546`, branch `br-summer-union-b2qlszfv`, database `krc_media_beta`: tables `krc_managed_media_jobs`, `krc_media_client_jobs`, `krc_media_stt_charges` currently each contain **zero rows**. A URL/job-specific lookup returned no rows. This does **not** establish that no provider work occurred; investigate retention, branch/database migration, cleanup and backend's current database binding without exposing credentials.

## Status and next gate
- Historical Instagram E2E: PASS on 2026-09-19.
- Today's attempted E2E: INCONCLUSIVE; do not retry start blindly.
- Current E2 safe probe mode: PASS.
- Next: read-only inspect current VoiceBridge database binding *fingerprint/hostname and database name only*, identify any migration or TTL cleanup, correlate actual current durable store with attempt window, then decide whether another one-job test is necessary.
- Owner requested deletion of unused extra E2 **after verification**. It has not been deleted; connected Render tools lack delete operation.
