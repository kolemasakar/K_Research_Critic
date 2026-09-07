# K-Research & Critic - MEDIA BETA Recovery Pointer
Канонічний покажчик поточного стану MEDIA BETA після YouTube Gemini live acceptance, Instagram fail-closed canary, Cobalt edge-blocker isolation, rollback to the accepted VoiceBridge runtime, and owner approval of OCI Always Free Cobalt migration.

Status: ACTIVE POINTER / CHECKPOINT 87 / R2 YOUTUBE ACCEPTED / INSTAGRAM EDGE BLOCKED / OCI FREE MIGRATION APPROVED / R3 HOLD
Updated: 2026-09-07

`K-Research & Critic - MEDIA BETA` remains an additive MEDIA capability planned for the existing published `K-Research & Critic` identity.

## Current canonical checkpoint

Repository:

`kolemasakar/K_Research_Critic`

Branch:

`main`

Path:

`subprojects/media_beta/87_R2_INSTAGRAM_COBALT_EDGE_BLOCKER_OCI_FREE_MIGRATION_CHECKPOINT_2026_09_07.md`

## Current gate state

```text
R0   PASS
R1   COMPLETE
R2-A PASS
R2-B PASS
R2-C COMPLETE
R2   PARTIAL PASS: YOUTUBE ACCEPTED / INSTAGRAM EDGE BLOCKED / FACEBOOK+TELEGRAM+CORE PENDING
R3   HOLD / NOT READY
R4   HOLD
```

## Current public candidate contract

```text
gpt_store/actions/media_public_free_openapi.yaml
version: 0.8.0-r2-gemini-youtube
status: repository candidate / private canary active / not publicly activated
```

Current free-only logical routing target:

```text
YouTube   -> Gemini Developer API Free Tier direct public URL -> durable KRCM/Neon
Instagram -> self-hosted Cobalt -> AssemblyAI universal-2 Free -> durable KRCM/Neon
Facebook  -> self-hosted Cobalt -> AssemblyAI universal-2 Free -> durable KRCM/Neon
Telegram  -> public Telegram web -> AssemblyAI universal-2 Free -> durable KRCM/Neon
```

YouTube requires explicit Gemini Free data-use disclosure and consent before a **new** provider request. Reusable completed durable jobs may be reused without a new provider submission.

Automatic fallback remains forbidden:

```text
paid retrieval: none
paid STT: none
paid proxy: none
Supadata public: none
ScrapeCreators public: none
cookies/login: none
```

## VoiceBridge accepted runtime

```text
repository: kolemasakar/VoiceBridge
branch: agent/krc-media-gemini-migration
head: 68a39d9109455c3e9e69ffeb3a7456998f0620db
Validate: 34147736126 / SUCCESS
PR #45: OPEN / DRAFT / UNMERGED / mergeable=true
```

## Current live VoiceBridge backend

```text
Render MEDIA service: voicebridge-krc-media-beta-kolemasakar
service id: srv-da1kic5bedkc73d6fk60
configured branch: agent/krc-media-gemini-migration
autoDeploy: no
live commit: 68a39d9109455c3e9e69ffeb3a7456998f0620db
live deploy: dep-dafhul0n74is73a3nncg
status: LIVE
```

Immediate rollback baseline:

`52499e4959aa2673f07239c73054cdbeaec0eeac`

Temporary diagnostic commits/branches are evidence only and are not production runtime.

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
durable duplicate reuse: PASS
new provider call on reuse: NO
```

## Instagram acceptance / blocker

Bounded Instagram canary failed closed:

```text
status: FAILED
provider_mode: cobalt_retrieval_stt
retrieval_provider: cobalt
retrieval credits: 0
STT seconds: 0
AssemblyAI started: NO
paid fallback: NO
```

Sanitized Cobalt probes:

```text
Instagram #1 -> HTTP 429 / non-JSON
Instagram #2 -> HTTP 429 / non-JSON
YouTube ctrl  -> HTTP 429 / text/plain; charset=utf-8 / server=cloudflare
```

Canonical blocker:

`Render Cobalt endpoint edge-level HTTP 429 / non-JSON blocker`

Current Cobalt Render service remains present but is not accepted for Instagram/Facebook R2 traffic:

```text
service: krc-cobalt-media-beta-kolemasakar
service id: srv-da5ggq6k1f9s738j8d8g
plan: free
region: frankfurt
image: ghcr.io/imputnet/cobalt@sha256:63186dd68afd57ce3bb1f62cc4c139f5fa95b9c3e87a3cf5c6e4c7a570523f62
live deploy: dep-dafeelf40ujc73av801g
```

## Owner infrastructure decision

```text
paid Render instance: NOT CONSIDERED
paid Cobalt hosting: NOT CONSIDERED
FREE_TIER_ONLY: retained
approved remediation: OCI Always Free self-hosted Cobalt
```

Target replacement path:

```text
Private MEDIA BETA -> VoiceBridge / Render Free -> OCI Always Free Cobalt -> Instagram/Facebook -> AssemblyAI Free Trial -> Neon
```

After the OCI endpoint passes retrieval-only preflight, only `KRC_MEDIA_COBALT_ENDPOINT` should be changed in VoiceBridge. Do not move secrets into GPT configuration or chat.

## Current Neon state

```text
YouTube job: COMPLETED
Instagram job: FAILED
krc_media_stt_charges rows: 0
charged STT seconds: 0
```

## Remaining R2 work before R3 readiness

```text
OCI Compute / Always Free quota preflight
OCI self-hosted Cobalt deployment + retrieval-only preflight
Instagram functional canary PASS
Facebook bounded canary PASS
Telegram bounded canary PASS
Render + Neon delta/no-paid-fallback verification
Core KRC isolation regression including forced MEDIA failure
```

Until those checks pass, `R3_READY = FALSE`.

## Retained invariant

```text
MEDIA unavailable/fails -> MEDIA unavailable/fails closed
Core KRC               -> remains user-accessible and functional
```

Recovery must start from checkpoint 87.

Recovery command:

`recover KRC MEDIA BETA checkpoint 87 Cobalt edge blocker OCI Always Free migration 2026-09-07`

Before any state-changing action, re-read exact GitHub heads/CI, current Render live deploys, PR #45 state, Neon durable state, and current private/public GPT Builder state. Do not merge PR #45 or update the public GPT without separate explicit owner authorization.
