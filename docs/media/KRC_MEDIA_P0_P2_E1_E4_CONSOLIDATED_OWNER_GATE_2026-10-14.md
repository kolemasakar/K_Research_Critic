# KRC MEDIA — consolidated P0–P2 / R3C / E1–E4 readiness gate
Audit date: 2026-10-14 UTC. Authority: owner FREE_ONLY, Instagram/Facebook **short reels/posts only**, no new long-social-video test requirement, E4 Telegram LIVE BLOCKED. This is an evidence-based review, NOT a global RELEASE authorization.

## Current deployment and read-only confirmation
- VoiceBridge Render service `srv-da1kic5bedkc73d6fk60`: deploy `dep-db7do3dg1s2s73a543v0`, status **live**, exact private integration SHA `16186fd5fdc2cb6c890e7ec1a6e964ccc355345d`. Prior deploy `072658ff512802262cef00ff424b87eedde1f934` deactivated. Source branch `agent/krc-media-gemini-migration`; not `main`.
- R3C read-only `media_get_capabilities` request `24d9e3aa-ab0f-4633-9f6b-83c2d2e5cfc7`: configured=true, `durable_store=postgres`, `restart_resilient_jobs=true`, `duplicate_start_reuses_job=true`, owner server-side access, `automatic_paid_fallback=false`, `paid_retrieval_fallback=false`, `paid_stt_fallback=false`, four platform routes **configured**. Route advertised is not proof of an approved live start.
- Connected Neon project `plain-snow-71973546` at `2026-10-14T02:12:32.064Z`: 0 unexpired PROCESSING jobs, 1 unexpired job. Not a forecast of later state. Schema migration `lease_owner`, `lease_heartbeat_at` verified after first new managed status use.

## Cross-cutting gates
| Gate | Acceptance | Evidence and qualification |
|---|---|---|
| P0 sequential cold auto-wake | **PASS 3/3** | 2026-10-13 three independent R3C capability cold cycles, relay_success and VoiceBridge service_started/MCP 200 after token correction |
| P0 concurrent read-only cold requests | **PASS within observed scope** | Two simultaneous R3C+E1 capabilities PASS; one observed relay wake. Actual two-way relay join branch only offline-tested, not proven triggered live |
| P0 429 origin attribution | OPEN, non-release-critical for validated read-only recovery | Cloudflare edge headers observed; Render support attribution not established |
| P1 Instagram short LIVE route | **PASS technical**, audio-accuracy open | 2026-10-14 one 41.11675s reel Cobalt+AssemblyAI, COMPLETED, 1 segment, 331 UTF-16, 42 STT seconds, credits 0, provider_data_deleted true. R3C status/full segments and Neon row independently matched. No independently verified beginning/middle/end human audio comparison |
| P1 Facebook short-format | **PARTIAL** | Historical 2026-10-04 public Facebook 167.28s video COMPLETED/3 segments/2630 chars, readback after real Render process restart; separate prior 180.3s sample. No current 2026-10-14 Facebook live repeat or independently recorded audio-accuracy evaluation. Owner explicitly removed long 480–720s requirement |
| P1 long IG/FB clips (480–720s) | **SUPERSEDED** | Owner decision 2026-10-13: do not search/start/test long social videos; not an OPEN gate |
| P2 previous COMPLETED job across Render cold restart | **PASS** | 2026-10-13 41s Instagram job survived real stop/start, R3C status/segments and matching Neon row prior to TTL |
| P2 native Postgres/psql cross-process crash and idempotence | **PASS ISOLATED** | PostgreSQL 16.15 server, exact adapter; SIGKILL/lease-expiry transition, completed lost-response same-job reuse, free-only Facebook controlled retry |
| P2 active lease and delayed worker fencing | **PASS ISOLATED** | 102s active PROCESSING heartbeat, 90s database advance, concurrent second service returns PROCESSING without a second provider call; expired owner delayed put rejected and state preserved |
| P2 full tests | **PASS 278/278** | Exact patched VoiceBridge private branch; TypeScript build and full test suite 0 FAIL |
| P2 deployed version and schema | **PASS** | Render exact SHA 16186fd5 live, lazy schema migration verified and Instagram smoke end to end |
| Production Render mid-provider crash | NOT TESTED | Do not kill live provider or infer provider-side exactly-once billing under loss of response |
| Global production billing/long-run reliability | OPEN | Reported job credits 0 and disabled paid fallback do not independently prove external invoices/billing/account-state safety |

## Provider/connector admission
| Surface | Connection/current functional evidence | Owner-admissible status |
|---|---|---|
| **R3C read-only gateway** | Current capabilities PASS, safe cold recovery PASS, API reads/status available within TTL | **ACCEPT — read-only gate** |
| **E1 YouTube** | Gemini Free-only and consent disclosure configured. 2026-10-04 historical YouTube `KRCM_fabae184-3b16-46c6-baca-c3df701dd61b` COMPLETED, 1 segment, 220 UTF-16, credits 0 reported; later separate long TED comparator start failed readiness with `consequential_post_attempted=false`. Historic pass cannot close later long-form admission/reliability | **LIMITED / PARTIAL**; explicit Gemini Free data-use consent for new starts, never blind retry |
| **E2 Instagram** | Current 2026-10-14 reel job `KRCM_24813ae3-1762-4ca7-8e4b-568c3fe98b52`: COMPLETED Cobalt/AssemblyAI, one segment 331 UTF-16, 41.11675s, 42 STT seconds, credits 0; persisted Neon lease fields; R3C readback | **ACCEPT LIMITED SHORT-REEL TECHNICAL BETA**, content/audio semantic accuracy remains unverified |
| **E3 Facebook** | Historical 2026-10-04 COMPLETED `KRCM_27482717-917a-454a-a69d-c2a55821a86c`, 167.28s, 3 segments/2630 chars, 0 credits; complete cursor pagination and readback across Render stop/start. No fresh post-lease deploy E3 job. Owner short posts/reels focus | **LIMITED / PARTIAL**, no long-video mandate, additional scoped accuracy/new-deploy check needed for release |
| **E4 Telegram** | A historical 2026-10-04 public Telegram job `KRCM_afe3cfb7-cbec-44b2-a17a-ce2d76bd3e94` COMPLETED, 1 segment/677 chars, 0 credits; this is *historical evidence*, and newer owner operational policy retains **LIVE BLOCKED** | **BLOCKED** — no new Telegram live start or release |
| **R4 public plugin / main** | Separate publication/release authorization not given | **HOLD**, unchanged |

## Practical acceptance decision
1. Continue **read-only R3C** operations under current safeguards.
2. E2 may be used as a **restricted technical beta for short reels** where permitted by current action policies and owner consent; label transcript accuracy as provisional rather than validated against original audio.
3. E1 and E3 stay in **limited supervised test scope**; no unattended repeated media starts or general production claim. E4 stays BLOCKED.
4. No automatic paid fallback, no forced re-processing when provider POST outcome ambiguous; read-only lookup/status before considering new start.
5. Do not promote to public/main/R4 production or claim FULL ACCEPTANCE. Global gate remains **HOLD** pending E1/E3 current scoped quality and cold readiness checks, confirmed operational guardrails, and separate explicit owner release decision.

## Source precedence and unresolved discrepancies
- Current 2026-10-14 observations override earlier historic fail rows *only for the exact checks rerun*. Historical acceptance matrix of 2026-10-10 is not edited here; its Instagram/Facebook 480–720s requirement is superseded.
- Historic all-four LIVE PASS of 2026-10-04 is credible within that single session; not evidence all four are currently approved for live execution. In particular, Telegram earlier PASS and current LIVE BLOCKED are not contradictory when scope and time are distinguished.
- P0 cold read-only three cycles do not prove every start-on-cold provider route; separate E1 start readiness failed on a later occasion.
- Zero recorded credits and free-only config are **not** an independent invoice/charging audit.
- No media was started, restarted or reprocessed during this consolidated audit.

## Supporting documents
- `docs/media/KRC_P0_COLD_AUTO_WAKE_3_OF_3_PASS_2026-10-13.md`
- `docs/media/KRC_P1_CONCURRENT_RELAY_RUNTIME_PATCH_AND_MEDIA_ADMISSION_2026-10-13.md`
- `docs/media/KRC_P1_OWNER_SHORT_REELS_SCOPE_DECISION_2026-10-13.md`
- `docs/media/KRC_ALL_FOUR_MEDIA_LIVE_ACCEPTANCE_PASS_2026-10-04.md`
- `docs/media/KRC_LIVE_ACCEPTANCE_PROGRESS_2026-10-04.md`
- `docs/media/KRC_P2_RENDER_LEASE_DEPLOY_LIVE_REEL_2026-10-14.md`
- `docs/media/KRC_P2_HEARTBEAT_102S_STALE_WRITER_FENCING_PASS_2026-10-14.md`
- `docs/media/KRC_R3C_E1_E4_FINAL_ACCEPTANCE_MATRIX_2026-10-10.md` (historical + dated addendum)
