# KRC P2 — live short Instagram job, pre-restart evidence (2026-10-13)

## Authorized single test
Owner explicitly approved creating a short MEDIA job and testing persistence. One E2 Instagram start, using public short reel `https://www.instagram.com/reel/Dcea3BiPTBm/` after R3C FREE_ONLY capabilities and preflight. No duplicate start.

### FREE_ONLY preflight
- Capabilities request `c96271e5-642b-40da-90b4-b190f9d4067f`: `configured=true`, `automatic_paid_fallback=false`, `paid_retrieval_fallback=false`, `paid_stt_fallback=false`, `durable_store=postgres`, `duplicate_start_reuses_job=true`.
- Instagram preflight request `fcccc6ac-2713-4ba0-bde7-13b81f87e0c8`: `can_continue=true`, `estimated_retrieval_credits=0`, Cobalt + AssemblyAI; scoped lookup returned 404 (no reusable job), connected Neon pre-start had 0 active jobs.

### Consequential E2 start and read-back
- Exactly one `media_instagram_start`, owner authorized, **COMPLETED**, `reused=false`.
- `job_id=KRCM_0b6d30b2-5cad-4a7c-9410-593d990e8263`, created 2026-10-13T20:32:34.709Z, updated 20:32:53.103Z.
- Duration 41.11675s, detected `en`, confidence .9851; segment_count 1, UTF-16 transcript characters 331, timecodes 720–34780ms, `next_cursor=null`, continuous index 0.
- credits_charged 0, retrieval_credits_charged 0, metadata_credits_charged 0, stt_seconds_charged 42, credit_charge_uncertain false, provider_data_deleted true; provider assemblyai.
- Start request `d133e450-373f-4d3b-afd7-8cb6cdfbb10f`; independent status `d8d4003a-e418-4104-8929-5af2d3cc2d4b`; segments read `6408d13a-1b69-46ed-9dd0-d0e21cadc0ee`.
- Transcript actual text not stored in GitHub, verified JS UTF-16 length 331.
- Neon read-only query returned exact matching managed record `COMPLETED`, one JSONB segment, `payload->>'transcript_characters'=331`, `payload->>'credits_charged'=0`, `expires_at=2026-10-13T21:32:53.103Z`. This is direct evidence that **this** job was stored in the connected `krc_media_beta` project, reconciling the earlier Render→Neon provenance uncertainty for this specific job.

## Restart method
- Render VoiceBridge currently deployed commit `072658ff512802262cef00ff424b87eedde1f934`, but remote branch HEAD is `48354ded605a6c703342678695bdce8cabe6d692`. `trigger_deploy` would deploy different source code, so it was NOT used.
- Safer choice: allow Render Free to naturally sleep after idle (prior verified service_stopping generally ~15 minutes after last request) and schedule one read-only cold wake/status/segments before TTL. If a genuine `service_stopping` and new `service_started` are logged before same-job read-back, this constitutes a process-stop/start durability test without changing deployed code. If no stop or state mismatch, mark gate NOT PASSED.
- One exact follow-up check scheduled for **2026-10-13 20:57:29 UTC**, comfortably before expiry at 21:32:53 UTC; no additional MEDIA start, paid fallback, Render deployment, or DB writes by the checker. Scheduled check to document final verdict in separate follow-up file.

## Current verdict
- P2 real E2 start / UTF-16 / status / segments / credits / Neon persisted row: **PASS**.
- P2 actual restart durability: **PENDING OBSERVED PROCESS STOP+START AND SAME-JOB READBACK**.
- E2 audible spot-check human transcript fidelity not proven in this infrastructure test.
