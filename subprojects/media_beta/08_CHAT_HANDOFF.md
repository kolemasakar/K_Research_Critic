# MEDIA BETA Chat Handoff

Канонічна інструкція відновлення K-Research & Critic - MEDIA BETA у новому чаті.

Version: 5.1
Status: ACTIVE_HANDOFF / CHECKPOINT_87 / R2_YOUTUBE_ACCEPTED / INSTAGRAM_EDGE_BLOCKED / OCI_FREE_MIGRATION_APPROVED / R3_HOLD
Checkpoint date: 2026-09-07

## Recovery command

`recover KRC MEDIA BETA checkpoint 87 Cobalt edge blocker OCI Always Free migration 2026-09-07`

## Mandatory recovery order

1. `subprojects/media_beta/87_R2_INSTAGRAM_COBALT_EDGE_BLOCKER_OCI_FREE_MIGRATION_CHECKPOINT_2026_09_07.md`
2. `docs/KRC_MEDIA_BETA_RECOVERY_POINTER.md`
3. `subprojects/media_beta/00_INDEX.md`
4. `subprojects/media_beta/02_ROADMAP.md`
5. `subprojects/media_beta/06_DECISION_LOG.md`
6. `gpt_store/media_r2_gemini_youtube_canary_manifest.yaml`
7. `gpt_store/actions/media_public_free_openapi.yaml`
8. `prompts/GPT_STORE_MEDIA_R2_GEMINI_YOUTUBE_CANARY_INSTRUCTIONS.md`
9. current VoiceBridge branch / CI / PR #45 state
10. current Render VoiceBridge + Cobalt state
11. current Neon durable state
12. current private/public Builder state

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

Render VoiceBridge service: voicebridge-krc-media-beta-kolemasakar
configured branch: agent/krc-media-gemini-migration
autoDeploy: no
live deploy: dep-dafhul0n74is73a3nncg
live commit: 68a39d9109455c3e9e69ffeb3a7456998f0620db
rollback baseline: 52499e4959aa2673f07239c73054cdbeaec0eeac
```

Temporary diagnostic commit `908dd03e4847a39902352d3dfcf4a71ae1f1fd5c` was deployed only for sanitized probing and is deactivated. Diagnostic branches are not production runtime.

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
durable duplicate reuse: PASS
new provider submission on reuse: NO
```

## Instagram / Cobalt blocker state

Instagram bounded canary failed closed:

```text
job: KRCM_24db1049-5b9c-42df-85ec-686d80ed9471
status: FAILED
provider_mode: cobalt_retrieval_stt
retrieval_provider: cobalt
retrieval credits: 0
STT seconds: 0
AssemblyAI started: NO
paid fallback: NO
```

Sanitized retrieval-only diagnostics:

```text
Instagram probe #1 -> HTTP 429 / non-JSON
Instagram probe #2 -> HTTP 429 / non-JSON
YouTube control     -> HTTP 429 / text/plain / server=cloudflare
```

Canonical blocker wording:

`Render Cobalt endpoint edge-level HTTP 429 / non-JSON blocker`

Current Render Cobalt service remains present but is not accepted for Instagram/Facebook R2 traffic:

```text
service: krc-cobalt-media-beta-kolemasakar
plan: free
region: frankfurt
image: ghcr.io/imputnet/cobalt@sha256:63186dd68afd57ce3bb1f62cc4c139f5fa95b9c3e87a3cf5c6e4c7a570523f62
live deploy: dep-dafeelf40ujc73av801g
```

## Owner decision

```text
paid Render instance: NOT CONSIDERED
paid Cobalt hosting: NOT CONSIDERED
FREE_TIER_ONLY: retained
approved remediation: migrate self-hosted Cobalt to OCI Always Free VM
```

VoiceBridge, Neon, private GPT and public GPT remain otherwise unchanged. After OCI Cobalt preflight PASS, only `KRC_MEDIA_COBALT_ENDPOINT` should be changed in VoiceBridge.

## Current Neon state

```text
YouTube durable job: COMPLETED
Instagram durable job: FAILED
krc_media_stt_charges rows: 0
charged STT seconds: 0
```

## Current gate state

```text
R0: PASS
R1: COMPLETE
R2: PARTIAL PASS - YouTube accepted / Instagram infrastructure blocked
R3: HOLD / NOT READY
R4: HOLD
```

## Exact continuation point

```text
1. OCI Compute / Always Free quota preflight
2. create only an Always Free eligible VM; no paid resources
3. deploy Docker + Cobalt + HTTPS reverse proxy + API-key protection
4. retrieval-only OCI Cobalt preflight
5. after PASS update only KRC_MEDIA_COBALT_ENDPOINT
6. repeat bounded Instagram canary
7. if PASS -> Facebook canary
8. Telegram canary
9. Render/Neon delta + no-paid-fallback verification
10. forced MEDIA failure + Core KRC isolation regression
11. if all PASS -> record full R2 PASS
12. only then -> separate explicit R3 owner gate
```

Do not merge PR #45 and do not modify/update the public KRC GPT without separate explicit owner authorization.

## Terminal marker

`MEDIA_BETA_HANDOFF_V5_1_CHECKPOINT_87_COBALT_EDGE_BLOCKED_OCI_FREE_MIGRATION_R3_HOLD`
