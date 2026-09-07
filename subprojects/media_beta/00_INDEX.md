# MEDIA BETA Documentation Index

Канонічний індекс документації K-Research & Critic MEDIA BETA.

Version: 6.6
Status: ACTIVE / CHECKPOINT_87 / R2_YOUTUBE_ACCEPTED / INSTAGRAM_EDGE_BLOCKED / OCI_FREE_MIGRATION_APPROVED / R3_HOLD
Updated: 2026-09-07

## Product boundary

`K-Research & Critic - MEDIA BETA` is an additive MEDIA capability intended for the already-published `K-Research & Critic` product. `K_Research_Critic` remains the product/release authority. VoiceBridge provides the isolated MEDIA backend implementation and validation evidence.

Current product reality:

```text
public KRC: already published / user-accessible / unchanged
private KRC MEDIA BETA: owner-only / checkpoint-87 canary package active
future public MEDIA target: same existing public KRC identity
```

Critical invariant:

```text
MEDIA unavailable/fails -> MEDIA unavailable/fails closed
Core KRC               -> remains user-accessible and functional
```

## Canonical reading order

1. `87_R2_INSTAGRAM_COBALT_EDGE_BLOCKER_OCI_FREE_MIGRATION_CHECKPOINT_2026_09_07.md` - current canonical recovery checkpoint.
2. `86_R2_YOUTUBE_GEMINI_LIVE_ACCEPTANCE_R3_READINESS_HOLD_2026_09_07.md` - accepted YouTube live baseline before Instagram acceptance.
3. `85_R2_GEMINI_DIRECT_HANDOFF_REPOSITORY_SYNC_2026_09_07.md` - pre-deployment handoff checkpoint.
4. `84_R2_YOUTUBE_GEMINI_DIRECT_REPOSITORY_READY_2026_09_07.md` - accepted Gemini-direct repository pivot.
5. `83_R2_PUBLIC_ACTION_SCHEMA_REPOSITORY_READY_2026_09_05.md` - previous public Action repository checkpoint.
6. `82_R2_PUBLIC_COBALT_RECONCILIATION_REPOSITORY_SYNC_2026_09_04.md` - Cobalt routing reconciliation.
7. `81_R2_LIVE_PROMOTION_PARTIAL_CANARY_2026_09_04.md` - earlier promotion/partial canary baseline.
8. `80_R2C_PUBLIC_PRIVACY_RENDER_PROMOTION_READY_2026_09_04.md` - privacy/release plan.
9. `79_R2B_FAILURE_ISOLATION_FREE_QUOTA_PASS_2026_09_04.md` - failure-isolation evidence.
10. `78_R2A_PUBLIC_FREE_TIER_ADMISSION_PASS_2026_09_04.md` - public free-only admission policy.

Recovery pointer:

`../../docs/KRC_MEDIA_BETA_RECOVERY_POINTER.md`

## Current Action contract

```text
gpt_store/actions/media_public_free_openapi.yaml
version: 0.8.0-r2-gemini-youtube
status: private canary active / public KRC not activated
```

Historical contracts remain preserved:

```text
gpt_store/actions/media_public_cobalt_openapi.yaml  version 0.7.0-r2-cobalt
gpt_store/actions/media_managed_beta_openapi.yaml   version 0.6.0-a9.10
```

## Current routing architecture

Accepted/pending target:

```text
YouTube   -> Gemini Developer API Free Tier direct public URL -> KRCM/Neon
Instagram -> self-hosted Cobalt -> AssemblyAI universal-2 Free -> KRCM/Neon
Facebook  -> self-hosted Cobalt -> AssemblyAI universal-2 Free -> KRCM/Neon
Telegram  -> public Telegram web -> AssemblyAI universal-2 Free -> KRCM/Neon
```

Current infrastructure exception:

```text
Render Free Cobalt endpoint -> HTTP 429 text/plain edge blocker
Instagram acceptance       -> FAIL-CLOSED / BLOCKED
approved remediation       -> migrate self-hosted Cobalt to OCI Always Free VM
paid hosting               -> NOT CONSIDERED
```

No paid retrieval, paid STT, paid proxy, user-cookie/login, or automatic paid fallback is authorized.

## VoiceBridge and Render state

```text
VoiceBridge repository: kolemasakar/VoiceBridge
branch: agent/krc-media-gemini-migration
head: 68a39d9109455c3e9e69ffeb3a7456998f0620db
Validate: 34147736126 / SUCCESS
PR #45: OPEN / DRAFT / UNMERGED / mergeable=true

Render VoiceBridge service: voicebridge-krc-media-beta-kolemasakar
configured branch: agent/krc-media-gemini-migration
autoDeploy: no
live deploy: dep-dafhul0n74is73a3nncg
live commit: 68a39d9109455c3e9e69ffeb3a7456998f0620db
status: LIVE
rollback baseline: 52499e4959aa2673f07239c73054cdbeaec0eeac

Render Cobalt service: krc-cobalt-media-beta-kolemasakar
plan: free
live deploy: dep-dafeelf40ujc73av801g
status: present but not accepted for Instagram/Facebook while edge 429 persists
```

Diagnostic commits/branches are evidence only and are not production runtime.

## Private R2 canary package

```text
instructions: prompts/GPT_STORE_MEDIA_R2_GEMINI_YOUTUBE_CANARY_INSTRUCTIONS.md
manifest: gpt_store/media_r2_gemini_youtube_canary_manifest.yaml
Builder applied: true
sharing: owner-only
```

The final Action schema uses inline pagination parameters for GPT Builder compatibility.

## Live acceptance state

```text
YouTube capability read: PASS
explicit Gemini Free data-use consent: PASS
Gemini provider execution: PASS
Neon durable completion: PASS
duplicate durable reuse: PASS
new provider work on reuse: NO

Instagram bounded canary: FAIL-CLOSED / BLOCKED
Cobalt retrieval credits: 0
AssemblyAI STT started: NO
STT charge rows after diagnostic: 0
paid fallback: NO
```

Cobalt diagnostic evidence:

```text
Instagram probe #1: HTTP 429 / non-JSON
Instagram probe #2: HTTP 429 / non-JSON
YouTube control:      HTTP 429 / text/plain / server=cloudflare
canonical blocker:    Render Cobalt endpoint edge-level 429 / non-JSON
```

## Gate state

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

Full R2 still requires OCI Cobalt migration/preflight, successful Instagram and Facebook canaries, Telegram canary, remaining Render/Neon no-paid-fallback verification, and Core KRC failure-isolation regression.

## Next sequence

```text
1. recover checkpoint 87
2. OCI Compute / Always Free quota preflight
3. create only an Always Free eligible VM
4. deploy self-hosted Cobalt + HTTPS reverse proxy + API-key protection
5. retrieval-only Cobalt preflight
6. update only KRC_MEDIA_COBALT_ENDPOINT after preflight PASS
7. repeat bounded Instagram canary
8. if PASS -> Facebook canary
9. Telegram canary
10. Render + Neon delta/no-paid-fallback verification
11. Core KRC isolation regression including forced MEDIA failure
12. if all PASS -> record full R2 PASS
13. only then -> separate explicit R3 owner gate
```

## Recovery command

`recover KRC MEDIA BETA checkpoint 87 Cobalt edge blocker OCI Always Free migration 2026-09-07`
