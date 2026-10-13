# P1 — live long-media admission and preliminary checks (2026-10-13)

Scope: first P1 acceptance pass for E2 Instagram, E3 Facebook, E1 YouTube control; Telegram E4 remains blocked. Owner authorized P1 implementation, but actual provider execution is gated by protocol's independently verified candidate URL, duration 480–720s and speech-bearing audio. No start was initiated in this pass.

## Input protocol
`docs/media/KRC_LONG_MEDIA_LIVE_TEST_PROTOCOL_2026-10-10.md` requires public canonical URL, independently measured duration in 480.000–720.000 seconds, audio stream and human speech in start/middle/end checkpoints, confirmed FREE_ONLY capacity, one provider POST, complete read-only status/segments and no duplicate retry. Neither lack of duration nor text search results constitute proof.

## Observations
1. R3C `media_get_capabilities` succeeded: `configured=true`, `mode=zero_client_managed_beta`, `automatic_paid_fallback=false`, `paid_retrieval_fallback=false`, `paid_stt_fallback=false`, `durable_store=postgres`, `duplicate_start_reuses_job=true`; Instagram/Facebook retrieval Cobalt and STT AssemblyAI; YouTube Gemini Free Tier. Request ID `eb564f66-852e-4bf9-81df-d2805aa10804`.
2. R3C Instagram preflight for **historical SHORT reference only** `https://www.instagram.com/reel/Dcea3BiPTBm/` returned `can_continue=true`, `estimated_retrieval_credits=0`, `automatic_paid_fallback=false`, `provider=cobalt`, `stt_provider=assemblyai`, request ID `9b266d95-531a-4fcf-93f3-739d0d009de9`. This does not verify media duration or speech.
3. R3C lookup of the above previously successful short Instagram URL returned **HTTP 404** with `render_origin_confirmed=true`, nonretryable, correlation ID `9e52f774-afbb-4d0a-aa3f-31271b7ba5ca`. Do not infer deletion until job/DB/service provenance reconciled.
4. R3C status read for documented prior Facebook COMPLETE job `KRCM_c7547bbc-cb9b-4f20-b18d-079991116343` returned **HTTP 404**, nonretryable, correlation ID `5e301045-6694-420b-bbd8-c5a77cd7e05b`. This makes historical job accessibility a potential durability/retention issue pending investigation; do NOT infer PostgreSQL corruption.
5. Existing successful Instagram reference: 41.11675 s, 1 segment; Facebook reference: 180.302938 s, 3 segments — neither meets long-media acceptance duration.
6. Public web discovery surfaced Facebook and Instagram pages but did **not** independently establish both 480–720s duration and speech. No independent verified eligible URL yet; it would be unsafe to invoke a consequential provider start with unverified input.
7. E4 Telegram live path stays BLOCKED under current approved policy.

## Verdict
- P1 FREE_ONLY/preflight gate for Instagram: PASS on existing short reference.
- P1 480–720s real Instagram/Facebook candidates: `BLOCKED_MISSING_INDEPENDENT_DURATION_AUDIO_EVIDENCE`.
- P1 Instagram/Facebook long live starts: NOT_RUN; no new jobs, credits or provider POST initiated.
- Existing state consistency: `INVESTIGATE_404` for previously recorded historical Facebook job and Instagram lookup. This is an additional P1/P2 gate.
- No public GPT changes, paid fallback, live Telegram start, production deploy or restart.

## Next actions
1. Acquire at least one legitimate publicly accessible Instagram and Facebook canonical video each with verifiable exact duration 480–720 seconds and audio checkpoints (player metadata/ffprobe). Do not rely on search text or artificially truncate/extend media.
2. Before any POST, investigate 404 origin: route mapping, identity, Neon database and retention/job lifecycle with read-only logs; protect against misleading `durable_store=postgres` capabilities vs actual historical availability.
3. After qualifying inputs are VERIFIED and free capacity checked, single authorized E2/E3 start, scoped status/segments, audio manual spot checks, charge 0, exact evidence ledger.
4. YouTube E1 long control via Gemini Free only with separate explicit Google free-tier data-use acknowledgement and preflight. E4 remains BLOCKED.
