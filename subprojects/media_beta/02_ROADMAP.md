# MEDIA BETA Roadmap

Поточний roadmap K-Research & Critic MEDIA BETA після YouTube acceptance та Instagram Cobalt edge-blocker isolation.

Version: 4.8
Status: R2_PARTIAL_PASS / YOUTUBE_ACCEPTED / INSTAGRAM_EDGE_BLOCKED / OCI_FREE_MIGRATION_APPROVED / R3_HOLD
Updated: 2026-09-07

## Product position

`K-Research & Critic - MEDIA BETA` is a private owner-only validation surface for an additive MEDIA capability planned for the already-published `K-Research & Critic` GPT.

```text
product/release authority: kolemasakar/K_Research_Critic
public KRC: existing published GPT / unchanged
private MEDIA BETA GPT: owner-only
backend implementation: kolemasakar/VoiceBridge
VoiceBridge branch: agent/krc-media-gemini-migration
```

Critical invariant:

```text
MEDIA unavailable/fails -> MEDIA unavailable/fails closed
Core KRC               -> remains usable and accessible
```

## Canonical recovery authority

`87_R2_INSTAGRAM_COBALT_EDGE_BLOCKER_OCI_FREE_MIGRATION_CHECKPOINT_2026_09_07.md`

Recovery command:

`recover KRC MEDIA BETA checkpoint 87 Cobalt edge blocker OCI Always Free migration 2026-09-07`

## Current provider routing

Logical free-only routing remains:

```text
YouTube   -> Gemini Developer API Free Tier direct public URL -> durable KRCM/Neon
Instagram -> self-hosted Cobalt -> AssemblyAI universal-2 Free -> durable KRCM/Neon
Facebook  -> self-hosted Cobalt -> AssemblyAI universal-2 Free -> durable KRCM/Neon
Telegram  -> public Telegram web -> AssemblyAI universal-2 Free -> durable KRCM/Neon
```

Current infrastructure remediation:

```text
Render Free Cobalt -> blocked by reproducible edge HTTP 429 / non-JSON
paid Render/Cobalt hosting -> NOT CONSIDERED
approved replacement -> OCI Always Free self-hosted Cobalt
```

Policy:

```text
Supadata public: inactive
ScrapeCreators public paid retrieval: forbidden
paid retrieval fallback: false
paid STT fallback: false
paid proxy fallback: false
paid hosting remediation: excluded
YouTube Cobalt fallback: none
YouTube AssemblyAI fallback: none
user cookies/login: forbidden
```

## R0 - Public KRC Update Safety Preflight

Status: PASS.

The existing public KRC identity remains the protected product target. No MEDIA Action is attached to public KRC and checkpoint 87 does not authorize changing it.

## R1 - Repository integration

Status: COMPLETE.

KRC repository contains the public MEDIA candidate Action, private canary package, privacy candidate, regression tests, and recovery documentation.

## R2 - Permanent MEDIA backend promotion/readiness

Status: PARTIAL PASS / INFRASTRUCTURE REMEDIATION REQUIRED.

Completed:

```text
R2-A public free-tier admission: PASS
R2-B failure isolation/free quota: PASS
R2-C privacy/promotion preparation: COMPLETE
exact VoiceBridge Gemini-direct deployment: PASS
Render VoiceBridge health/startup: PASS
private MEDIA BETA Builder activation: PASS
Action bearer auth: PASS
capability read: PASS
YouTube Gemini consent canary: PASS
YouTube durable completion: PASS
YouTube transcript retrieval: PASS
YouTube duplicate reuse/idempotency: PASS
YouTube no-paid/no-fallback boundary: PASS
Instagram fail-closed behavior: PASS as safety behavior
```

Instagram functional acceptance is **not** complete:

```text
Instagram canary: FAILED / COBALT_PUBLIC_MEDIA_INVALID_RESPONSE
Cobalt retrieval: HTTP 429 non-JSON
AssemblyAI STT: not started
retrieval credits: 0
STT charge rows: 0
paid fallback: none
```

Sanitized diagnostics reproduced `429` twice for Instagram and once for an independent YouTube control through the same Render Cobalt endpoint. YouTube control returned `text/plain; charset=utf-8` with `server=cloudflare`, so the canonical blocker is an edge-level non-JSON response before a usable Cobalt application response.

Exact accepted VoiceBridge backend after rollback:

```text
Render service: voicebridge-krc-media-beta-kolemasakar
branch: agent/krc-media-gemini-migration
autoDeploy: no
live commit: 68a39d9109455c3e9e69ffeb3a7456998f0620db
live deploy: dep-dafhul0n74is73a3nncg
rollback baseline: 52499e4959aa2673f07239c73054cdbeaec0eeac
```

Current blocked Cobalt host:

```text
Render service: krc-cobalt-media-beta-kolemasakar
plan: free
region: frankfurt
image: ghcr.io/imputnet/cobalt@sha256:63186dd68afd57ce3bb1f62cc4c139f5fa95b9c3e87a3cf5c6e4c7a570523f62
live deploy: dep-dafeelf40ujc73av801g
```

### R2 infrastructure remediation - approved

The owner explicitly rejected paid instances/hosting and approved this direction:

```text
1. OCI Always Free quota/Compute preflight
2. create only an Always Free eligible VM
3. deploy Docker + Cobalt + HTTPS reverse proxy + API-key protection
4. retrieval-only preflight against OCI Cobalt
5. update only KRC_MEDIA_COBALT_ENDPOINT after PASS
6. repeat Instagram canary
```

Still required before full R2 PASS:

```text
OCI Cobalt deployment/preflight
Instagram functional canary PASS
Facebook bounded canary PASS
Telegram bounded canary PASS
Render + Neon delta/no-paid-fallback verification
Core KRC isolation regression including forced MEDIA failure
```

## R3 - Update existing published KRC GPT

Status: HOLD / NOT READY.

R3 cannot start until full R2 PASS is recorded.

No current authorization exists to modify or update the public GPT.

## R4 - Post-update public verification

Status: HOLD until R3.

Required after any future R3 update:

- same public KRC identity/URL remains accessible;
- Core tasks work without MEDIA;
- MEDIA works only as intended;
- MEDIA failure does not degrade Core;
- sharing state remains intact;
- rollback remains available.

## Current gate model

```text
R0  PASS
R1  COMPLETE
R2  PARTIAL PASS / YouTube accepted / Instagram infrastructure blocker
R3  HOLD / NOT READY
R4  HOLD
```

Every gate remains independent. Approval of OCI remediation does not authorize R3 or public GPT changes.

## Exact continuation point

```text
OCI ALWAYS FREE COBALT MIGRATION
- inspect OCI Compute/Always Free quota
- no paid resource creation
- deploy and secure Cobalt
- retrieval-only preflight
- update KRC_MEDIA_COBALT_ENDPOINT only after PASS
- repeat Instagram
- Facebook
- Telegram
- Render/Neon no-paid-fallback checks
- Core isolation regression

NO PUBLIC GPT CHANGE
NO PR #45 MERGE
```
