# K-Research & Critic - MEDIA BETA Recovery Pointer
Канонічний покажчик поточного стану MEDIA BETA після exact Gemini-direct deployment, private Builder activation, YouTube live acceptance і durable reuse validation.

Status: ACTIVE POINTER / CHECKPOINT 86 / R2 YOUTUBE LIVE ACCEPTED / NON-YOUTUBE + CORE ISOLATION PENDING / R3 HOLD
Updated: 2026-09-07

`K-Research & Critic - MEDIA BETA` remains an additive MEDIA capability planned for the existing published `K-Research & Critic` identity.

## Current canonical checkpoint

Repository:

`kolemasakar/K_Research_Critic`

Branch:

`main`

Path:

`subprojects/media_beta/86_R2_YOUTUBE_GEMINI_LIVE_ACCEPTANCE_R3_READINESS_HOLD_2026_09_07.md`

## Current gate state

```text
R0   PASS
R1   COMPLETE
R2-A PASS
R2-B PASS
R2-C COMPLETE
R2   PARTIAL PASS: LIVE + YOUTUBE ACCEPTED / NON-YOUTUBE + CORE ISOLATION PENDING
R3   HOLD / NOT READY
R4   HOLD
```

## Current public candidate contract

```text
gpt_store/actions/media_public_free_openapi.yaml
version: 0.8.0-r2-gemini-youtube
status: repository candidate / not publicly activated
```

Current free-only routing target:

```text
YouTube   -> Gemini Developer API Free Tier direct public URL -> durable KRCM/Neon
Instagram -> self-hosted Cobalt -> AssemblyAI universal-2 Free -> durable KRCM/Neon
Facebook  -> self-hosted Cobalt -> AssemblyAI universal-2 Free -> durable KRCM/Neon
Telegram  -> public Telegram web -> AssemblyAI universal-2 Free -> durable KRCM/Neon
```

YouTube requires explicit Gemini Free data-use disclosure and consent before a **new** provider request. Reusable completed durable jobs may be reused without a new provider submission.

Automatic YouTube fallback remains forbidden:

```text
Cobalt: none
AssemblyAI: none
Supadata: none
cookies/login: none
paid proxy: none
paid Gemini: none
```

## VoiceBridge deployed candidate

```text
repository: kolemasakar/VoiceBridge
branch: agent/krc-media-gemini-migration
head: 68a39d9109455c3e9e69ffeb3a7456998f0620db
Validate: 34147736126 / SUCCESS
PR #45: OPEN / DRAFT / UNMERGED / mergeable=true
```

## Current live backend

```text
Render MEDIA service: voicebridge-krc-media-beta-kolemasakar
service id: srv-da1kic5bedkc73d6fk60
configured branch: agent/krc-media-gemini-migration
autoDeploy: no
live commit: 68a39d9109455c3e9e69ffeb3a7456998f0620db
live deploy: dep-dafgkjm7bikc738hmi20
status: LIVE
```

Immediate rollback baseline:

`52499e4959aa2673f07239c73054cdbeaec0eeac`

## Private R2 canary Builder state

```text
instructions: prompts/GPT_STORE_MEDIA_R2_GEMINI_YOUTUBE_CANARY_INSTRUCTIONS.md
instructions version: 0.2.0-r2-gemini-youtube-canary
action: gpt_store/actions/media_public_free_openapi.yaml
action version: 0.8.0-r2-gemini-youtube
authentication: bearer API key
privacy: docs/PRIVACY_POLICY.md / 2.2-candidate
sharing: owner-only
builder_runtime_applied: true
```

The existing public `K-Research & Critic` GPT remains unchanged and has no MEDIA Action attached.

## Accepted live YouTube evidence

Authenticated private canary passed:

```text
Gemini Free consent gate: PASS
Gemini direct execution: PASS
Neon durable completion: PASS
provider_mode: youtube_gemini_direct
provider_model: gemini-3.7-flash
retrieval_provider: gemini_youtube_url
retrieval credits: 0
STT seconds: 0
segment retrieval: PASS
CriticProfile separation: PASS
durable duplicate reuse: PASS
new provider call on reuse: NO
```

## Remaining R2 work before R3 readiness

```text
Instagram bounded canary
Facebook bounded canary
Telegram bounded canary
Render + Neon delta/no-paid-fallback verification for remaining routes
Core KRC isolation regression including forced MEDIA failure
```

Until those checks pass, `R3_READY = FALSE`.

## Retained invariant

```text
MEDIA unavailable/fails -> MEDIA unavailable/fails closed
Core KRC               -> remains user-accessible and functional
```

Recovery must start from checkpoint 86.

Recovery command:

`recover KRC MEDIA BETA checkpoint 86 YouTube Gemini live acceptance R3 readiness hold 2026-09-07`

Before any state-changing action, re-read exact GitHub heads/CI, current Render live deploy, PR #45 state, and current private/public GPT Builder state. Do not merge PR #45 or update the public GPT without separate explicit owner authorization.
