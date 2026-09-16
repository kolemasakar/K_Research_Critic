# BOOTSTRAP PACKAGE - KRC MEDIA BETA - R2 COMPLETE / R3 READY

Date: 2026-09-16
Project: K-Research & Critic - MEDIA BETA
Canonical checkpoint: `subprojects/media_beta/89_R2_FULL_ACCEPTANCE_RETRY_PASS_R3_READY_CHECKPOINT_2026_09_16.md`

## Recovery instruction

Start by reading this handoff, then checkpoint 89, then `docs/KRC_MEDIA_BETA_RECOVERY_POINTER.md`.
Do not infer state from older checkpoint 88 or PR descriptions that have not yet been synchronized.

Recovery command:

`recover KRC MEDIA BETA checkpoint 89 R2 complete retry pass R3 ready 2026-09-16`

## Authoritative repository state

KRC repository: `kolemasakar/K_Research_Critic`, branch `main`.
VoiceBridge repository: `kolemasakar/VoiceBridge`, branch `agent/krc-media-gemini-migration`.
VoiceBridge accepted head: `3e8cb29b3815e1bf98f143682644899b801826e0`.
Validate #813: SUCCESS across cloud, image parity, browser extension, and repository docs.
PR #45: OPEN / DRAFT / UNMERGED.

Public KRC integration candidate PR #20 remains staging only. The public GPT has not been modified by R2 closure.

## Accepted live backend

Render service: `voicebridge-krc-media-beta-kolemasakar`.
Service id: `srv-da1kic5bedkc73d6fk60`.
Accepted deploy: `dep-dal6abdg1s2s73ed059g`.
Accepted live commit: `3e8cb29b3815e1bf98f143682644899b801826e0`.
Health after deploy and after retry canary: HTTP 200 / `status=ok`.

OCI Cobalt public endpoint: `https://89-168-65-88.sslip.io`.
Cobalt remains loopback-only on `127.0.0.1:9000` behind Caddy HTTPS and API-key auth.
Do not expose or rotate secrets during recovery unless separately authorized.

## Accepted R2 route matrix

```text
YouTube   -> Gemini Developer API Free Tier direct -> Neon
Instagram -> OCI Cobalt -> AssemblyAI universal-2 Free -> Neon
Facebook  -> OCI Cobalt video+audio -> VoiceBridge ffmpeg mono PCM WAV 16 kHz -> AssemblyAI -> Neon
Telegram  -> telegram_public_web -> AssemblyAI universal-2 Free -> Neon
```

No automatic paid retrieval, paid STT, paid proxy, Supadata public fallback, ScrapeCreators public fallback, or cookie/login fallback is authorized.

## Live acceptance summary

YouTube: PASS after Cobalt cutover; remained Gemini-direct.
Instagram: PASS on `https://www.instagram.com/reel/DF1CIrPSVmf/` with non-empty transcript.
Facebook: PASS on `https://www.facebook.com/reel/636216875539019` after switching from unsupported Facebook-only-audio request to video+audio plus local ffmpeg extraction/normalization.
Telegram: PASS on `https://t.me/techcrimes/12107`, one transcript segment, 53 STT seconds, retrieval credits 0.
Core isolation: PASS; forced MEDIA failures leave Core health at HTTP 200.
No-paid-fallback audit: PASS; paid retrieval/credits, uncertain-charge jobs, ScrapeCreators, and Supadata counts were zero in the accepted R2 canary window.

## Retry semantics fix

Problem reproduced during Facebook diagnostics: durable FAILED free-only jobs could be reused indefinitely for the same logical request and prevent fresh provider work.

Accepted VoiceBridge behavior at head `3e8cb29b3815e1bf98f143682644899b801826e0`:

```text
COMPLETED -> reuse
PROCESSING in-flight -> reuse
FAILED free-only -> deterministic fresh retry request key and new job
FAILED paid/credit-charge-uncertain -> automatic replay blocked
```

Local cloud validation: 246/246 PASS.
GitHub Validate #813: PASS.

Live proof using Telegram no-speech fixture `https://t.me/techcrimes/12101` while the previous FAILED record was still live:

```text
old: KRCM_a58b1cc8-f072-4aec-88a9-f1fa06a53fcd
old request_key: 7d5fa785d60fb9778d62e0da0f61e68abb0e51922702be299adc78ce73e8a4b7
new: KRCM_0ca16eb0-e9d2-477e-98d9-27cb923df9d6
new request_key: 63bb22d30582246a686dfe34949d68935050d721ed35cae38825e77eaad1152b
```

The new FAILED job was created before the old job expired. Both remained free-only with zero retrieval credits, zero paid credits, and `credit_charge_uncertain=false`. Therefore FAILED free-only retry semantics are accepted live.

## Gate state

```text
R2 = COMPLETE / PASS
R3_READY = TRUE
R3 activation = HOLD pending explicit owner authorization
R4 = HOLD
```

`R3_READY = TRUE` means R3 integration may begin. It does not authorize public GPT mutation or PR merge.

## First actions in the new chat

1. Read current KRC main head and VoiceBridge branch head; confirm checkpoint 89 remains current.
2. Confirm PR #45 remains DRAFT/UNMERGED and Render live commit remains `3e8cb29b...`.
3. Confirm public KRC GPT is still unchanged before any R3 mutation.
4. Review the staged public MEDIA Action schema and routing instructions for R3 integration.
5. Perform R3 in bounded steps with explicit owner approval before public Builder changes.
6. Regression test ordinary non-media Core KRC plus all four accepted media platforms before public activation.

## Hard boundaries

- Do not merge PR #45 without separate owner authorization.
- Do not merge/activate public integration candidate PR #20 merely because R3 is ready.
- Do not modify the published KRC GPT without explicit owner authorization.
- Keep YouTube Gemini-direct; do not introduce Cobalt fallback for YouTube.
- Keep Facebook on Cobalt video+audio plus VoiceBridge ffmpeg extraction; do not revert to Cobalt only-audio.
- Preserve free-only and fail-closed policy.
- Preserve Core KRC isolation from MEDIA failures.
- Do not use unrelated KGM infrastructure or credentials for KRC.
