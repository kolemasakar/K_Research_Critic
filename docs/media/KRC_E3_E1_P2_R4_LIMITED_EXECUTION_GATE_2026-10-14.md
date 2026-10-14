# KRC R4 limited PRIVATE candidate — four-direction execution, operations and release gate
Date: 2026-10-14 UTC. Owner instruction: execute E3 Facebook + E1 YouTube readiness + P2 operational checks + prepare R4 limited private release. This file records **what actually ran**, not aspirational acceptance.

## 1. E3 Facebook post-deploy live
- Platform source: `https://www.facebook.com/NASASCaN/videos/8368792419872400/` (previously vetted NASA SCaN public video), duration `167.275938` seconds. This is a speech-bearing short-form video post relative to the prior expressly cancelled 480–720s requirement, not a new long-video test.
- One E3 `media_facebook_start`: new job `KRCM_19880d52-305d-48e5-8bf1-f793bba81391`, request `c72ddb29-6a4b-4785-93d7-08938597af01`, created `2026-10-14T02:21:54.527Z`, completed `02:22:10.835Z`, COMPLETED. Cobalt retrieval and AssemblyAI STT, detected en, language_confidence 0.9977, segments=3, UTF16 transcript chars=2630, STT seconds=168, credits_charged=0, retrieval_credits_charged=0, credit_charge_uncertain=false, provider_data_deleted=true.
- Independent R3C status request `4d5b6ab5-7992-48b1-b3c4-220609977c43` and full segments request `2cb7c7e6-3e47-4a9c-bd4c-8453993bcdcc`: indexes 0/1/2, end timestamps 60660/120500/165140ms, next_cursor=null. UTF16 count matches 2630.
- Independent Neon `krc_managed_media_jobs` showed identical job_id/COMPLETED, 3 segments, 2630 UTF16 characters, credits=0, lease_owner present, TTL expires `2026-10-14T03:22:10.835Z`.
- Content quality *semantic* cross-reference of three checkpoints to official NASA source: (0) DSN network antennas and Earth-space communication, (1) radio frequency/Doppler-based spacecraft motion, (2) infer bodies' gravitational fields and inner structure. NASA official source: `https://www.nasa.gov/stem-content/how-nasa-uses-gravity-and-radio-waves-to-study-planets-and-moons-video/`, official video duration 2m47s (corresponds to 167.275938s), and `https://www.nasa.gov/communicating-with-missions/dsn/`. This confirms **topic/source consistency only**, not acoustic word-error rate or exact transcription against independently listened audio.
- E3: TECHNICAL LIVE + FULL READBACK + NEON DURABILITY **PASS**; phonetic accuracy STILL OPEN; do not claim separately listened original audio.

## 2. E1 YouTube cold-readiness boundary
- The known public YouTube control URL was `https://www.youtube.com/watch?v=jNQXAC9IVRw`.
- R3C read-only YouTube preflight request `3ef14c1f-08f9-45f6-8999-4aed67695036`: can_continue=true, explicit Gemini Developer API Free Tier data-use consent required, gemini-3.7-flash, zero automatic paid fallback.
- Independently E1 YouTube connector preflight `fc543217-e015-40d8-a61b-808f2b358ae4`: same safe readiness/consent signals.
- Read-only lookup 404 request `59e545c7-4b83-456f-80a5-56accecf023b`: no current durable job matching URL, consistent with TTL or absent record.
- **No E1 media_youtube_start or consequential POST was issued in this session**. Thus READ-ONLY PREPARED/ROUTE PASS, but genuinely cold *consequential start* remains NOT TESTED. 2026-10-04 historical YouTube COMPLETED sample is historical evidence only; later separate attempted TED long-form start was blocked at readiness with `consequential_post_attempted=false`. User consent for Gemini Free does not justify blind repetition after ambiguous provider call.
- A bounded cold E1 **read-only** test after a logged Render stop, if performed, must be recorded separately; only infer COLD_PASS if log proves prior stop and new start + MCP read-only success.

## 3. P2 operations and resource/safety
- Render VoiceBridge continues exact SHA `16186fd5fdc2cb6c890e7ec1a6e964ccc355345d`, deploy `dep-db7do3dg1s2s73a543v0` live, autoDeploy disabled, private branch, Free 1 instance.
- R3C current capabilities request `baa2d63f-62e3-4388-bb42-7edd4f9acad5`: configured true, durable_store postgres, restart_resilient_jobs true, duplicate_start_reuses_job true, `automatic_paid_fallback=false`, `paid_retrieval_fallback=false`, `paid_stt_fallback=false`.
- Read-only Neon operational query after E3 showed 0 active PROCESSING, 2 retained active jobs, and zero records with positive claimed credits. This is job ledger, **not independent provider invoice**.
- Prior exact adapter P2: native PostgreSQL 16.15, actual SIGKILL, lease 90s, 15s heartbeat, 102s soak and fencing PASS; full patched VoiceBridge 278/278 PASS. No actual Render SIGKILL while external processing. P2 engine-level release readiness PASS; production cross-provider exactly-once/billing guarantee not proven.
- Maintain single consequential POST after explicit confirm and authenticated preflight, no blind retries on ambiguous outcome. Log edge-vs-origin 429 separately; sleep/wake can transiently fail.

## 4. R4 limited private build (prepared, **not installed or published**)
- New separate candidate directory on private integration branch: `plugins/krc_r4_limited_private_20261014/`. Original five-app candidate remains untouched, and canonical KRC Core snapshot copied byte-for-byte.
- New manifests `plugin.json` and `.codex-plugin/plugin.json` agree on name `k-research-critic-r4-limited-private`, version 0.1.0, and private short-reel-only + FREE_ONLY instructions.
- New `.app.json` includes ONLY:
  - R3C read-only: `asdk_app_6aaaf8ca113c8191a4ac53f8793833a4`
  - E1 YouTube Gemini Free: `asdk_app_6ab26b061fb4819180fa096638f1e4df`
  - E2 Instagram: `asdk_app_6aaeae197c9081918b90e46f5bb09615`
  - E3 Facebook: `asdk_app_6aaf262767d8819199146dc84b8e1ee8`
- E4 Telegram registered mapping `asdk_app_6aaf292e653481918c75767dea004c5c` intentionally **ABSENT** from this new separate candidate. This does not uninstall or globally block the separate legacy E4 connector, but means the restricted R4 candidate does not advertise it.
- Manifest cross-check: naming/display parity PASS; E4 absent PASS; original Core Skill snapshot byte-parity PASS.
- **Creator schema validation and actual private plugin creation not yet performed**. No marketplace listing/publication, no existing public GPT mutation. Do not claim installed/private release is DONE.
- Need host-uploadable archive packaging and Plugin Creator schema validation before installing for private acceptance, followed by one R3C read-only smoke. New restricted package does not silently promote P2 E1/E3 to general unattended usage.

## Final decision
- **E3 functional/live TECHNICAL PASS**, audio accuracy metric unverified.
- **E1 safe read-only readiness PASS**, cold consequential-start admission open.
- **P2 tested operational guardrails PASS**, production provider crash/billing still open.
- **R4 limited four-app candidate PREPARED IN PRIVATE REPO**, not yet schema-validated as a plugin nor created.
- **Global/public KRC R4 release HOLD**; no new Telegram LIVE or paid fallback. Require explicit separate acceptance to promote beyond private tests.

## Appendix — reproducible restricted package archive
- On authorized `krc-cobalt`, private integration GitHub source was cloned without touching production or public main, candidate directory `plugins/krc_r4_limited_private_20261014/` zipped with only four manifest/Core files.
- Created `/tmp/krc_r4_limited_private_20261014.zip`, size **5621 bytes**, SHA-256 **`2dc1e71be561912a29df52df063b333fdf2fb8bf45c9cbad3764a217b60828d8`**.
- ZIP CRC integrity, exactly four members, four app mapping count, manifest names and exact original Core byte parity: **PASS**.
- This is a prepared private archive on authorized remote host, not a sandbox download or installed Plugin Creator release. Plugin Creator schema validation and host-upload remain separate gates. E4 omitted from package mapping, not globally disabled in previously existing connector.
