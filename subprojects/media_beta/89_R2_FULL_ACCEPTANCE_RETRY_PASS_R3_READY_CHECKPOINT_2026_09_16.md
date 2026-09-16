# K-Research & Critic - MEDIA BETA Checkpoint 89

Date: 2026-09-16
Status: R2 COMPLETE / FULL ACCEPTANCE PASS / R3 READY FOR INTEGRATION

## Canonical state

KRC repository: `kolemasakar/K_Research_Critic`, branch `main`.
VoiceBridge repository: `kolemasakar/VoiceBridge`, branch `agent/krc-media-gemini-migration`.
VoiceBridge accepted head: `3e8cb29b3815e1bf98f143682644899b801826e0`.
GitHub Actions Validate #813: SUCCESS; `cloud`, `krc-image-parity`, `browser-extension`, and `repository-docs` all PASS.
PR #45 remains OPEN / DRAFT / UNMERGED.

Render MEDIA service: `voicebridge-krc-media-beta-kolemasakar` (`srv-da1kic5bedkc73d6fk60`).
Accepted deploy: `dep-dal6abdg1s2s73ed059g`.
Accepted live commit: `3e8cb29b3815e1bf98f143682644899b801826e0`.
Post-deploy health: HTTP 200, `status=ok`, `service=voicebridge-cloud`.

## Accepted free-only routing

```text
YouTube   -> Gemini Developer API Free Tier direct URL -> durable KRCM/Neon
Instagram -> OCI self-hosted Cobalt -> AssemblyAI universal-2 Free -> durable KRCM/Neon
Facebook  -> OCI self-hosted Cobalt video+audio -> VoiceBridge ffmpeg audio normalization -> AssemblyAI universal-2 Free -> durable KRCM/Neon
Telegram  -> public Telegram web -> AssemblyAI universal-2 Free -> durable KRCM/Neon
```

Automatic paid fallback remains forbidden: no paid retrieval, paid STT, paid proxy, Supadata public fallback, ScrapeCreators public fallback, or cookie/login fallback.

## OCI Cobalt accepted state

Instance: `krc-cobalt-media-beta`, Frankfurt, OCI Always Free-eligible VM.
Public endpoint: `https://89-168-65-88.sslip.io`.
Cobalt remains bound to `127.0.0.1:9000` behind Caddy HTTPS.
Public unauthenticated request fails closed; authenticated Instagram/Facebook tunnel generation works.
Cobalt API key remains server-side and is not stored in repository documentation.

## R2 live acceptance evidence

### YouTube

Accepted after OCI Cobalt cutover regression test. Route remained Gemini-direct.
Durable evidence retained: provider mode `youtube_gemini_direct`, provider `gemini`, retrieval provider `gemini_youtube_url`, retrieval credits 0, STT seconds 0.

### Instagram

Control Reel `https://www.instagram.com/reel/DF1CIrPSVmf/` completed through Cobalt + AssemblyAI.
Durable evidence retained: status COMPLETED, provider mode `cobalt_retrieval_stt`, retrieval provider `cobalt`, language `en`, transcript non-empty, retrieval credits 0.

### Facebook

The initial `downloadMode=audio` implementation was replaced because upstream Cobalt does not support Facebook only-audio as the canonical path.
Accepted route is Cobalt video+audio followed by local `ffmpeg` extraction/normalization to mono PCM WAV / 16 kHz before AssemblyAI.
Fresh Reel `https://www.facebook.com/reel/636216875539019` completed end-to-end with a non-empty transcript and KRC fact-check.

### Telegram

`https://t.me/techcrimes/12107` completed end-to-end through `telegram_public_web` and AssemblyAI with one transcript segment, 53 STT seconds, retrieval credits 0.
`https://t.me/techcrimes/12101` is retained as a deliberate no-recognizable-speech failure fixture.

## No-paid-fallback and isolation acceptance

R2 canary evidence showed zero paid retrieval jobs, zero paid credit jobs, zero `credit_charge_uncertain` jobs, and zero ScrapeCreators/Supadata retrieval jobs.
Forced MEDIA failure did not affect Core service health; `/api/v1/health` remained HTTP 200 / `ok`.
Runtime regression tests also cover provider/auth/store failures while requiring Core health to stay available.

## FAILED free-only retry semantics - accepted

The previous behavior could indefinitely reuse a durable FAILED free-only job for the same URL/language/access key.
VoiceBridge head `3e8cb29b3815e1bf98f143682644899b801826e0` introduces deterministic retry chaining for free-only routes while preserving idempotency and paid/uncertain charge protection.

Accepted semantics:

```text
COMPLETED -> reuse
PROCESSING in-flight -> reuse / concurrency protection
FAILED free-only -> fresh deterministic retry job
FAILED with paid charge or credit_charge_uncertain -> automatic replay remains blocked
```

Local validation: 246/246 cloud tests PASS.
GitHub runner validation: PASS.
Validate #813: SUCCESS.

Live Telegram proof on `https://t.me/techcrimes/12101` while the prior FAILED job was still retained:

```text
old job: KRCM_a58b1cc8-f072-4aec-88a9-f1fa06a53fcd
old request_key: 7d5fa785d60fb9778d62e0da0f61e68abb0e51922702be299adc78ce73e8a4b7
new job: KRCM_0ca16eb0-e9d2-477e-98d9-27cb923df9d6
new request_key: 63bb22d30582246a686dfe34949d68935050d721ed35cae38825e77eaad1152b
both status: FAILED / STT_TRANSCRIPTION_FAILED
both retrieval_provider: telegram_public_web
both retrieval credits: 0
both credits: 0
both credit_charge_uncertain: false
```

The new job was created before the old job expired, proving that stale FAILED reuse is no longer blocking a fresh free-only backend start.

## R2 closure

```text
R0: PASS
R1: COMPLETE
R2-A: PASS
R2-B: PASS
R2-C: COMPLETE
R2: COMPLETE / PASS
R3_READY: TRUE
R3 activation: HOLD pending explicit owner authorization
R4: HOLD
```

R3 readiness means the MEDIA backend has satisfied the R2 functional, free-only, durable retry, and isolation gates. It does not mean the public `K-Research & Critic` GPT has been modified.

## Public KRC boundary

The published `K-Research & Critic` remains unchanged and still requires R3 integration work before MEDIA activation.
Draft PR #20 in `K_Research_Critic` remains staging/evidence only unless separately authorized.
Do not attach or activate MEDIA Actions in the public GPT without explicit owner authorization.
Do not merge VoiceBridge PR #45 without separate owner authorization.

## Next phase

R3 should start with a read-only revalidation of current GitHub heads, CI, Render live deploy, private MEDIA BETA Builder state, and public KRC Builder state. Then integrate the accepted MEDIA Action/routing into the public KRC identity, test YouTube/Instagram/Facebook/Telegram plus ordinary non-media Core KRC regression, and only then consider public activation.

Recovery command:

`recover KRC MEDIA BETA checkpoint 89 R2 complete retry pass R3 ready 2026-09-16`
