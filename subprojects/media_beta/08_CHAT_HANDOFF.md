# MEDIA BETA Chat Handoff

Канонічна інструкція відновлення K-Research & Critic - MEDIA BETA у новому чаті.

Version: 5.0
Status: ACTIVE_HANDOFF / CHECKPOINT_86 / R2_YOUTUBE_LIVE_ACCEPTED / R3_HOLD
Checkpoint date: 2026-09-07

## Recovery command

`recover KRC MEDIA BETA checkpoint 86 YouTube Gemini live acceptance R3 readiness hold 2026-09-07`

## Mandatory recovery order

1. `subprojects/media_beta/86_R2_YOUTUBE_GEMINI_LIVE_ACCEPTANCE_R3_READINESS_HOLD_2026_09_07.md`
2. `docs/KRC_MEDIA_BETA_RECOVERY_POINTER.md`
3. `subprojects/media_beta/00_INDEX.md`
4. `subprojects/media_beta/02_ROADMAP.md`
5. `gpt_store/media_r2_gemini_youtube_canary_manifest.yaml`
6. `gpt_store/actions/media_public_free_openapi.yaml`
7. `prompts/GPT_STORE_MEDIA_R2_GEMINI_YOUTUBE_CANARY_INSTRUCTIONS.md`
8. `docs/PRIVACY_POLICY.md`
9. current VoiceBridge branch / CI / PR #45 state
10. current Render live deploy and private/public Builder state

## Frozen product boundary

```text
public KRC GPT:             already published / user-accessible / unchanged
private KRC MEDIA BETA GPT: owner-only / canary package active
future public identity:     same existing published KRC
```

Critical invariant:

```text
MEDIA failure/unavailability -> MEDIA unavailable/fails closed
Core KRC                    -> remains usable and accessible
```

## Current VoiceBridge / Render state

```text
VoiceBridge branch: agent/krc-media-gemini-migration
VoiceBridge head: 68a39d9109455c3e9e69ffeb3a7456998f0620db
Validate: 34147736126 / SUCCESS
PR #45: OPEN / DRAFT / UNMERGED / mergeable=true

Render service: voicebridge-krc-media-beta-kolemasakar
configured branch: agent/krc-media-gemini-migration
autoDeploy: no
live deploy: dep-dafgkjm7bikc738hmi20
live commit: 68a39d9109455c3e9e69ffeb3a7456998f0620db
rollback baseline: 52499e4959aa2673f07239c73054cdbeaec0eeac
```

## Current private Builder state

```text
instructions version: 0.2.0-r2-gemini-youtube-canary
Action schema version: 0.8.0-r2-gemini-youtube
auth: Bearer API key
Privacy Policy: docs/PRIVACY_POLICY.md / 2.2-candidate
sharing: owner-only
```

Public KRC remains without MEDIA Action.

## Accepted YouTube evidence

```text
capability read: PASS
Gemini Free disclosure/consent before new provider work: PASS
Gemini direct provider execution: PASS
Neon durable completion: PASS
provider_mode: youtube_gemini_direct
provider_model: gemini-3.7-flash
retrieval_provider: gemini_youtube_url
retrieval credits: 0
STT seconds: 0
segment retrieval: PASS
CriticProfile remains separate: PASS
durable duplicate reuse: PASS
new provider submission on reuse: NO
```

## Current gate state

```text
R0: PASS
R1: COMPLETE
R2: PARTIAL PASS - live + YouTube accepted
R3: HOLD / NOT READY
R4: HOLD
```

R2 is not complete until the current live deployment passes bounded Instagram, Facebook, and Telegram canaries, remaining Render/Neon delta/no-paid-fallback verification, and Core KRC failure-isolation regression.

## Exact continuation point

```text
1. reverify current GitHub/Render/Builder state
2. bounded Instagram canary
3. bounded Facebook canary
4. bounded Telegram canary
5. Render + Neon delta/no-paid-fallback verification
6. forced MEDIA failure + Core KRC isolation regression
7. if all PASS -> record full R2 PASS
8. only then -> separate explicit R3 owner gate
```

Do not merge PR #45 and do not modify/update the public KRC GPT without separate explicit owner authorization.

## Terminal marker

`MEDIA_BETA_HANDOFF_V5_0_CHECKPOINT_86_R2_YOUTUBE_PASS_R3_HOLD`
