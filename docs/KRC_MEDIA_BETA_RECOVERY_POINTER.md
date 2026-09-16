# K-Research & Critic - MEDIA BETA Recovery Pointer

Status: ACTIVE POINTER / CHECKPOINT 89 / R2 COMPLETE / RETRY LIVE PASS / R3 READY FOR INTEGRATION / PUBLIC ACTIVATION HOLD
Updated: 2026-09-16

`K-Research & Critic - MEDIA BETA` remains an additive MEDIA capability planned for the existing published `K-Research & Critic` identity.

## Current canonical checkpoint

Repository: `kolemasakar/K_Research_Critic`
Branch: `main`

Checkpoint:
`subprojects/media_beta/89_R2_FULL_ACCEPTANCE_RETRY_PASS_R3_READY_CHECKPOINT_2026_09_16.md`

Handoff:
`docs/handoffs/BOOTSTRAP_PACKAGE_2026-09-16_KRC_MEDIA_R2_COMPLETE_R3_READY_HANDOFF.md`

Recovery command:

`recover KRC MEDIA BETA checkpoint 89 R2 complete retry pass R3 ready 2026-09-16`

## Gate state

```text
R0   PASS
R1   COMPLETE
R2-A PASS
R2-B PASS
R2-C COMPLETE
R2   COMPLETE / PASS
R3_READY = TRUE
R3   READY FOR INTEGRATION / PUBLIC ACTIVATION HOLD
R4   HOLD
```

`R3_READY = TRUE` authorizes no public mutation by itself. Public Builder changes and PR merges still require explicit owner authorization.

## Accepted VoiceBridge runtime

```text
repository: kolemasakar/VoiceBridge
branch: agent/krc-media-gemini-migration
accepted head: 3e8cb29b3815e1bf98f143682644899b801826e0
Validate #813: SUCCESS
PR #45: OPEN / DRAFT / UNMERGED
```

Render:

```text
service: voicebridge-krc-media-beta-kolemasakar
service id: srv-da1kic5bedkc73d6fk60
autoDeploy: no
accepted deploy: dep-dal6abdg1s2s73ed059g
live commit: 3e8cb29b3815e1bf98f143682644899b801826e0
health: HTTP 200 / status=ok
```

## Accepted free-only route matrix

```text
YouTube   -> Gemini Developer API Free Tier direct -> Neon
Instagram -> OCI self-hosted Cobalt -> AssemblyAI universal-2 Free -> Neon
Facebook  -> OCI Cobalt video+audio -> VoiceBridge ffmpeg mono PCM WAV 16 kHz -> AssemblyAI -> Neon
Telegram  -> telegram_public_web -> AssemblyAI universal-2 Free -> Neon
```

Forbidden automatic fallback remains unchanged:

```text
paid retrieval: none
paid STT: none
paid proxy: none
Supadata public fallback: none
ScrapeCreators public fallback: none
cookies/login fallback: none
```

## R2 accepted live evidence

- YouTube Gemini-direct regression after Cobalt cutover: PASS.
- Instagram control Reel through OCI Cobalt + AssemblyAI: PASS.
- Facebook fresh Reel through Cobalt video+audio + local ffmpeg extraction + AssemblyAI: PASS.
- Telegram speech fixture `https://t.me/techcrimes/12107`: PASS.
- Render/Neon durable execution: PASS.
- No-paid-fallback audit: PASS.
- Forced MEDIA failure / Core isolation: PASS; health remained HTTP 200.

## FAILED free-only retry semantics

Accepted at VoiceBridge head `3e8cb29b3815e1bf98f143682644899b801826e0`:

```text
COMPLETED -> reuse
PROCESSING in-flight -> reuse
FAILED free-only -> fresh deterministic retry job
FAILED paid/credit-charge-uncertain -> automatic replay blocked
```

Live proof used Telegram no-speech fixture `https://t.me/techcrimes/12101` while the prior FAILED record was still retained:

```text
old job: KRCM_a58b1cc8-f072-4aec-88a9-f1fa06a53fcd
old request_key: 7d5fa785d60fb9778d62e0da0f61e68abb0e51922702be299adc78ce73e8a4b7
new job: KRCM_0ca16eb0-e9d2-477e-98d9-27cb923df9d6
new request_key: 63bb22d30582246a686dfe34949d68935050d721ed35cae38825e77eaad1152b
```

The fresh job was created before the old one expired. Both remained free-only with zero retrieval credits, zero paid credits, and `credit_charge_uncertain=false`.

## OCI Cobalt retained state

```text
instance: krc-cobalt-media-beta
region: eu-frankfurt-1
public endpoint: https://89-168-65-88.sslip.io
Cobalt bind: 127.0.0.1:9000 only
public HTTPS: Caddy
API auth: required
```

Do not expose Cobalt API keys or relax the loopback-only port-9000 boundary.

## Public KRC boundary

The published `K-Research & Critic` GPT remains unchanged at R2 closure.
Draft public integration candidate PR #20 is staging/evidence only.
Do not attach/activate MEDIA Actions in the public GPT without explicit owner authorization.
Do not merge VoiceBridge PR #45 without separate owner authorization.

## R3 starting point

Begin R3 by revalidating current GitHub heads/CI, Render live deploy, private MEDIA BETA Builder state, and public KRC Builder state. Then integrate the accepted MEDIA Action/routing into public KRC in bounded steps and regression-test ordinary Core KRC plus YouTube, Instagram, Facebook, and Telegram before any public activation.

Recovery must start from checkpoint 89 and the 2026-09-16 handoff, not checkpoint 88.
