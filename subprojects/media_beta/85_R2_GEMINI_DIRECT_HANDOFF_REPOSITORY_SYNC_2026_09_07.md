# K-Research & Critic / MEDIA BETA - R2 Gemini Direct Handoff Repository Sync Checkpoint 85

Канонічна точка переходу в новий чат після завершення repository-only pivot YouTube на consent-gated Gemini Developer API Free Tier direct URL processing і повної синхронізації recovery-документації.

Date: 2026-09-07
Status: HANDOFF_READY / R2_REPOSITORY_PIVOT_READY / LIVE_GEMINI_DEPLOYMENT_AND_AUTHENTICATED_CANARY_PENDING / R3_HOLD

## Scope

This checkpoint supersedes checkpoint 84 as the canonical handoff/recovery entry point. It does not introduce a new architecture change; it freezes and reconciles the already accepted checkpoint-84 state before transition to a new chat.

No Render environment change, Render deployment, Neon mutation, GPT Builder update, public GPT update, provider-consuming request, or VoiceBridge PR merge is authorized or performed by this checkpoint.

Critical invariant:

```text
MEDIA unavailable/fails -> MEDIA unavailable/fails closed
Core KRC               -> remains user-accessible and functional
```

## Accepted routing target

```text
YouTube   -> Gemini Developer API Free Tier direct public URL -> durable KRCM/Neon
Instagram -> self-hosted Cobalt -> AssemblyAI universal-2 Free -> durable KRCM/Neon
Facebook  -> self-hosted Cobalt -> AssemblyAI universal-2 Free -> durable KRCM/Neon
Telegram  -> public Telegram web -> AssemblyAI universal-2 Free -> durable KRCM/Neon
```

YouTube automatic fallback remains forbidden:

```text
Cobalt: none
AssemblyAI: none
Supadata: none
user cookies/login: none
paid proxy: none
paid Gemini: none
```

## Gemini Free consent boundary

For a new YouTube provider submission, the user must first receive a clear disclosure that content sent through the Gemini Developer API Free Tier may be used by Google to improve Google products and then explicitly consent.

Required consent payload:

```json
{
  "gemini_free_consent": {
    "provider": "google_gemini",
    "tier": "free",
    "data_use_acknowledged": true
  }
}
```

No consent -> `GEMINI_FREE_CONSENT_REQUIRED` -> no Gemini provider call / fail closed.

The generic MEDIA-start confirmation is not part of the accepted YouTube flow. The later CriticProfile approval is a separate research-control gate.

## VoiceBridge repository state

Repository:

`kolemasakar/VoiceBridge`

```text
branch: agent/krc-media-gemini-migration
candidate head: bae3db8e646baf003689c1d8a8e502d9d2ad832d
Validate: 34146243530 / SUCCESS
PR #45: OPEN / DRAFT / UNMERGED / mergeable=true
```

Dedicated implementation:

```text
src/cloud/src/public_gemini_youtube.ts
src/cloud/tests/public_gemini_youtube.test.ts
```

Validated properties:

```text
public YouTube URL sent directly to Gemini
server-side x-goog-api-key
no user Cookie/Authorization credential forwarding
explicit Free Tier consent before provider work
no provider call without consent
provider_mode=youtube_gemini_direct
retrieval_provider=gemini_youtube_url
retrieval_credits_charged=0
stt_seconds_charged=0
durable duplicate reuse
provider failure -> fail closed
no automatic Cobalt/AssemblyAI/paid fallback for YouTube
```

Temporary Cobalt startup-diagnostic code was removed before the final accepted VoiceBridge validation.

## KRC repository state entering handoff sync

Repository:

`kolemasakar/K_Research_Critic`

```text
branch: main
pre-handoff-sync tip: fd9e432ea58f650f64c77d26ef8149eb8ce0b886
Tests: 34146977260 / SUCCESS
Python 3.13: SUCCESS
Python 3.14: SUCCESS
Quality gates: SUCCESS
```

Current repository package:

```text
gpt_store/actions/media_public_free_openapi.yaml
  version: 0.8.0-r2-gemini-youtube

prompts/GPT_STORE_MEDIA_R2_GEMINI_YOUTUBE_CANARY_INSTRUCTIONS.md

gpt_store/media_r2_gemini_youtube_canary_manifest.yaml
  builder_runtime_applied: false

docs/PRIVACY_POLICY.md
  version: 2.2-candidate
```

Historical contracts remain preserved:

```text
gpt_store/actions/media_public_cobalt_openapi.yaml  version 0.7.0-r2-cobalt
gpt_store/actions/media_managed_beta_openapi.yaml   version 0.6.0-a9.10
```

## Current live backend - read-only verification

Read-only Render verification immediately before this handoff sync confirmed:

```text
service: voicebridge-krc-media-beta-kolemasakar
service id: srv-da1kic5bedkc73d6fk60
configured branch: agent/krc-media-transcript
autoDeploy: no
live deploy: dep-dafekmid0e5s73c3sg10
live commit: 52499e4959aa2673f07239c73054cdbeaec0eeac
status: LIVE
```

The Gemini-direct repository candidate is NOT deployed. The current live YouTube path therefore remains the pre-pivot Cobalt route and is not the target state for the next canary.

Immediate live baseline / rollback:

`52499e4959aa2673f07239c73054cdbeaec0eeac`

Earlier rollback points:

```text
7c8806713ea75b0809b638f102e31d8d3af86150
2f0f02769dbdf2e8240e6b08867ecef2faaede16
```

## Why YouTube pivoted from Cobalt

The Cobalt API key was initially scoped only to Facebook and returned `error.api.service.disabled` for YouTube. After the owner expanded `allowedServices` to `facebook`, `youtube`, and `instagram`, a fresh post-change YouTube request progressed beyond that gate but returned:

```text
HTTP 400
provider_error_code: error.api.youtube.login
retrieval credits: 0
STT seconds: 0
```

Under the accepted free-only policy, user cookies/login and paid proxy fallback are forbidden. This is the accepted reason for the Gemini direct-URL pivot.

## Private and public GPT Builder boundary

Private canary package is repository-ready but not applied:

```text
instructions: prompts/GPT_STORE_MEDIA_R2_GEMINI_YOUTUBE_CANARY_INSTRUCTIONS.md
manifest: gpt_store/media_r2_gemini_youtube_canary_manifest.yaml
builder_runtime_applied: false
```

The existing public `K-Research & Critic` GPT remains unchanged and still has no MEDIA Action attached. R3 remains HOLD.

## Gate state

```text
R0   PASS
R1   COMPLETE
R2-A PASS
R2-B PASS
R2-C COMPLETE
R2   REPOSITORY PIVOT READY / LIVE GEMINI DEPLOYMENT + AUTHENTICATED CANARY PENDING
R3   HOLD
R4   HOLD
```

## Next state-changing sequence after recovery

The next chat must reverify current heads and live state before mutation, then continue only with explicit applicable authorization:

```text
1. exact VoiceBridge Gemini-direct candidate deployment
2. health/startup verification
3. apply private MEDIA BETA checkpoint-85 canary Builder package
4. bounded authenticated YouTube Gemini Free consent canary
5. bounded Instagram / Facebook / Telegram canaries
6. Render + Neon delta checks and no-paid-fallback verification
7. Core KRC isolation regression
8. only after R2 PASS: separate R3 owner gate for existing public KRC GPT
```

Do not merge PR #45 or change the public GPT as part of R2 canary work unless separately authorized.

## Recovery instruction

Recovery must start from checkpoint 85 and then re-read:

1. `docs/KRC_MEDIA_BETA_RECOVERY_POINTER.md`;
2. this checkpoint;
3. `gpt_store/actions/media_public_free_openapi.yaml`;
4. `prompts/GPT_STORE_MEDIA_R2_GEMINI_YOUTUBE_CANARY_INSTRUCTIONS.md`;
5. `gpt_store/media_r2_gemini_youtube_canary_manifest.yaml`;
6. `docs/PRIVACY_POLICY.md`;
7. VoiceBridge branch `agent/krc-media-gemini-migration` current exact head and Validate state;
8. current Render live deployment for `srv-da1kic5bedkc73d6fk60`;
9. VoiceBridge PR #45 state;
10. current private and public GPT Builder states.

Recovery command:

`recover KRC MEDIA BETA checkpoint 85 Gemini direct handoff repository sync 2026-09-07`
