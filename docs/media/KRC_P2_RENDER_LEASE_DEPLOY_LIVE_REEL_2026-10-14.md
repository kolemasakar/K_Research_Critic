# KRC P2 — Controlled Render deployment and post-deploy short-reel verification (2026-10-14)

## Authorization and exact change
Owner instructed "роби" after validated P2 lease patch. One explicit Render deployment was triggered on service `srv-da1kic5bedkc73d6fk60`, workspace `tea-d9dsqdjrjlhs73ba1ga0`, on private branch `agent/krc-media-gemini-migration`, auto-deploy disabled, Free service, one instance. Deploy `dep-db7do3dg1s2s73a543v0`, exact commit **`16186fd5fdc2cb6c890e7ec1a6e964ccc355345d`**, live at `2026-10-14T01:34:38.806Z`. Render app log service_started at `01:34:33.318Z`. Docker build compilation PASS. No main/public deployment, paid fallback or Telegram LIVE.

## Read-only capabilities and schema
- R3C `media_get_capabilities` request `e4a2b48d-a7ea-4ed6-a2b3-2e4e368b681f`: configured true, durable_store postgres, restart_resilient_jobs true, duplicate_start_reuses_job true, automatic_paid_fallback false, paid_retrieval_fallback false, paid_stt_fallback false, Gemini YouTube separate consent.
- Prior to managed job/status service initialization, connected Neon database had no lease columns, since migration runs on first managed durable store use.
- Old, expired Instagram job read-only status returned HTTP 404, expected with TTL; this triggered lazy schema initialization.
- Read-only Neon `information_schema.columns` afterward confirmed **lease_owner** and **lease_heartbeat_at** present in `krc_managed_media_jobs`. No initialization error seen in Render log window.

## Post-deploy short Instagram LIVE verification
- URL `https://www.instagram.com/reel/Dcea3BiPTBm/`, representative 41.11675s reel, consistent with owner short-only scope.
- Preflight: `can_continue=true`, `consent_required=false`, retrieval Cobalt, AssemblyAI STT, estimated retrieval credits 0, automatic_paid_fallback false.
- Lookup before start HTTP 404 (absent).
- Initial E2 start failed in `warmup` with HTTP 429, `consequential_post_attempted=false`. Followed by read-only lookup HTTP 404, health ready, then **one** consequential MEDIA start was sent; returned success.
- Job `KRCM_24813ae3-1762-4ca7-8e4b-568c3fe98b52`, `created_at=2026-10-14T01:58:28.315Z`, `updated_at=2026-10-14T01:58:43.604Z`, `COMPLETED`, `reused=false`, 1 segment, 331 UTF-16 transcript characters, detected English confidence 0.9851, duration 41.11675s, `stt_seconds_charged=42`, `credits_charged=0`, Cobalt credits 0, `provider_data_deleted=true`.
- Independent R3C status request `b5b75a5d-45f9-4eec-a2d0-0cf5981cae0a` confirmed exact job/status/size/cost; segments read request `0fbd21fa-39db-4fe5-a80c-6ef36f2fdb97` returned one index-0 segment timecodes 720–34780ms, full 331-character transcript, next_cursor null.
- Independent read-only Neon query confirmed same persisted ID, status COMPLETED, lease_owner present, lease_heartbeat_at present, segment count 1, credits 0, expires_at 2026-10-14T02:58:43.604Z.

## Verdict
- **Controlled deploy = PASS.**
- **Lazy PostgreSQL schema migration = PASS.**
- **Post-deploy short Instagram Cobalt+AssemblyAI LIVE integration and persisted record = PASS.**
- **Post-deploy zero paid-fallback configuration = PASS** (reported config and zero credits per job, not a complete billing audit).
- **90s+ active PROCESSING heartbeat soak = NOT RUN here**, as a 41s short reel finishes before lease expiry. Cross-process mock provider and timed crash regression passed on isolated exact PostgreSQL earlier. Live running worker crash and fencing late write remain untested.
- **KRC MEDIA general release remains HOLD.** Preserve FREE_ONLY and disabled Telegram LIVE, no unsupported long IG/FB acceptance.
