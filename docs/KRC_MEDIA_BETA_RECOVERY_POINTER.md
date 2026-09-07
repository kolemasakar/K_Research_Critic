# K-Research & Critic - MEDIA BETA Recovery Pointer
Канонічний покажчик поточного стану MEDIA BETA після R2 pivot на consent-gated Gemini Free direct YouTube processing і handoff-синхронізації перед переходом у новий чат.

Status: ACTIVE POINTER / CHECKPOINT 85 / HANDOFF READY / R2 REPOSITORY PIVOT READY / LIVE GEMINI DEPLOYMENT + CANARY PENDING / R3 HOLD
Updated: 2026-09-07

`K-Research & Critic - MEDIA BETA` remains an additive MEDIA capability planned for the existing published `K-Research & Critic` identity.

## Current canonical checkpoint

Repository:

`kolemasakar/K_Research_Critic`

Branch:

`main`

Path:

`subprojects/media_beta/85_R2_GEMINI_DIRECT_HANDOFF_REPOSITORY_SYNC_2026_09_07.md`

## Current gate state

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

## Current public candidate contract

```text
gpt_store/actions/media_public_free_openapi.yaml
version: 0.8.0-r2-gemini-youtube
status: repository candidate / not publicly activated
```

Historical repository contracts remain preserved:

```text
gpt_store/actions/media_public_cobalt_openapi.yaml  version 0.7.0-r2-cobalt
gpt_store/actions/media_managed_beta_openapi.yaml   version 0.6.0-a9.10
```

The current public candidate routes YouTube only through dedicated consent-gated Gemini Free direct-URL operations. It does not expose Supadata credit operations, ScrapeCreators paid retrieval, local attachments, paid proxy fallback, or paid STT fallback.

## Current free-only routing target

```text
YouTube   -> Gemini Developer API Free Tier direct public URL -> durable KRCM/Neon
Instagram -> self-hosted Cobalt -> AssemblyAI universal-2 Free -> durable KRCM/Neon
Facebook  -> self-hosted Cobalt -> AssemblyAI universal-2 Free -> durable KRCM/Neon
Telegram  -> public Telegram web -> AssemblyAI universal-2 Free -> durable KRCM/Neon
```

YouTube requires explicit disclosure/consent before a new Gemini Free provider request because Free Tier content may be used by Google to improve Google products. No consent -> no provider call / fail closed.

YouTube automatic fallback is forbidden:

```text
Cobalt: none
AssemblyAI: none
Supadata: none
cookies/login: none
paid proxy: none
paid Gemini: none
```

## Current VoiceBridge repository candidate

```text
repository: kolemasakar/VoiceBridge
branch: agent/krc-media-gemini-migration
checkpoint-85 handoff baseline head: bae3db8e646baf003689c1d8a8e502d9d2ad832d
Validate: 34146243530 / SUCCESS
PR #45: OPEN / DRAFT / UNMERGED / mergeable=true
```

The candidate contains dedicated Gemini YouTube routes and no longer contains the temporary Cobalt startup diagnostic used during blocker isolation.

## Current live backend

Read-only verification on 2026-09-07 confirmed:

```text
Render MEDIA service: voicebridge-krc-media-beta-kolemasakar
service id: srv-da1kic5bedkc73d6fk60
configured branch: agent/krc-media-transcript
autoDeploy: no
live commit: 52499e4959aa2673f07239c73054cdbeaec0eeac
live deploy: dep-dafekmid0e5s73c3sg10
status: LIVE
```

The repository Gemini-direct pivot has NOT been deployed to Render. The live YouTube route is still the prior Cobalt path and is not the accepted target for the next canary.

Immediate live baseline/rollback:

`52499e4959aa2673f07239c73054cdbeaec0eeac`

Earlier rollback points:

```text
7c8806713ea75b0809b638f102e31d8d3af86150
2f0f02769dbdf2e8240e6b08867ecef2faaede16
```

## Cobalt YouTube blocker evidence

The Cobalt API key was initially Facebook-only and returned `error.api.service.disabled`. After the owner expanded it to `facebook/youtube/instagram`, a fresh canary progressed past that policy gate but returned:

```text
HTTP 400
provider_error_code: error.api.youtube.login
retrieval credits: 0
STT seconds: 0
```

This is the accepted reason the public YouTube target pivoted away from Cobalt instead of adding cookies/login or a paid proxy.

## Private R2 canary package

```text
instructions: prompts/GPT_STORE_MEDIA_R2_GEMINI_YOUTUBE_CANARY_INSTRUCTIONS.md
manifest: gpt_store/media_r2_gemini_youtube_canary_manifest.yaml
builder_runtime_applied: false
```

The private MEDIA BETA GPT still needs a separately authorized Builder switch before the new authenticated YouTube canary can run. The existing public KRC GPT remains unchanged and R3 remains HOLD.

## Privacy candidate

`docs/PRIVACY_POLICY.md` is version `2.2-candidate` and records the Gemini Free disclosure/consent boundary and mixed provider routing.

## Retained invariant

```text
MEDIA unavailable/fails -> MEDIA unavailable/fails closed
Core KRC               -> remains user-accessible and functional
```

Recovery must start from checkpoint 85.

Recovery command:

`recover KRC MEDIA BETA checkpoint 85 Gemini direct handoff repository sync 2026-09-07`

Before any state-changing action, re-read exact GitHub heads/CI, current Render live deploy, PR #45 state, and current private/public GPT Builder state. Do not deploy/mutate Render or Neon, merge PR #45, apply the private Builder package, or update the public GPT without the applicable explicit owner authorization.
