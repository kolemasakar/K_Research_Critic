# K-Research & Critic / MEDIA BETA - R2 Instagram Cobalt Edge Blocker + OCI Free Migration Checkpoint 87

Date: 2026-09-07
Status: R2_PARTIAL_PASS / YOUTUBE_ACCEPTED / INSTAGRAM_FAIL_CLOSED_EDGE_BLOCKED / OCI_FREE_MIGRATION_APPROVED / R3_HOLD

## Scope

This checkpoint supersedes checkpoint 86 as the canonical recovery entry point after the bounded Instagram acceptance attempt, sanitized Cobalt diagnostics, rollback to the accepted VoiceBridge runtime, and the owner decision to exclude paid hosting and migrate self-hosted Cobalt to an OCI Always Free VM.

It records verified state and approved architecture only. It does **not** activate the public `K-Research & Critic` GPT, merge VoiceBridge PR #45, enable a paid provider, or mark full R2 complete.

Critical invariant:

```text
MEDIA unavailable/fails -> MEDIA unavailable/fails closed
Core KRC               -> remains user-accessible and functional
```

## KRC product/repository state

```text
repository: kolemasakar/K_Research_Critic
branch: main
pre-checkpoint-87 tip: 7fbec9373f0f2c3d783b26791bb9734793c7024b
public KRC GPT: unchanged / no MEDIA Action
private KRC MEDIA BETA: owner-only
```

Current Action candidate remains:

```text
gpt_store/actions/media_public_free_openapi.yaml
version: 0.8.0-r2-gemini-youtube
public activation: false
```

## VoiceBridge accepted runtime

After all diagnostics, the production candidate branch was restored exactly to the accepted runtime:

```text
repository: kolemasakar/VoiceBridge
branch: agent/krc-media-gemini-migration
head: 68a39d9109455c3e9e69ffeb3a7456998f0620db
Validate: 34147736126 / SUCCESS
PR #45: OPEN / DRAFT / UNMERGED / mergeable=true
```

Diagnostic branches/commits are evidence only and are **not** production runtime.

## Render VoiceBridge rollback state

Current accepted live deployment after diagnostic rollback:

```text
service: voicebridge-krc-media-beta-kolemasakar
service id: srv-da1kic5bedkc73d6fk60
configured branch: agent/krc-media-gemini-migration
autoDeploy: no
live deploy: dep-dafhul0n74is73a3nncg
live commit: 68a39d9109455c3e9e69ffeb3a7456998f0620db
status: LIVE
```

The temporary diagnostic deployment of `908dd03e4847a39902352d3dfcf4a71ae1f1fd5c` is deactivated.

## YouTube R2 evidence retained - PASS

Checkpoint-86 YouTube acceptance remains valid:

```text
Gemini Free disclosure/consent: PASS
Gemini direct execution: PASS
Neon durable completion: PASS
provider_mode: youtube_gemini_direct
provider_model: gemini-3.7-flash
retrieval_provider: gemini_youtube_url
retrieval_credits_charged: 0
stt_seconds_charged: 0
duplicate durable reuse: PASS
new provider work on reuse: NO
```

## Instagram bounded canary - FAIL-CLOSED

Test URL:

`https://www.instagram.com/reel/DEAyVa4SF3E/`

The private MEDIA BETA route correctly attempted the approved free-only path:

```text
Instagram -> Cobalt -> AssemblyAI
```

Observed result:

```text
job status: FAILED
provider_mode: cobalt_retrieval_stt
retrieval_provider: cobalt
retrieval_credits_charged: 0
stt_seconds_charged: 0
AssemblyAI STT started: NO
paid fallback: NO
Supadata/ScrapeCreators fallback: NO
```

Backend error exposed to the MEDIA route:

`COBALT_PUBLIC_MEDIA_INVALID_RESPONSE`

The failure therefore satisfied fail-closed policy, but Instagram functional acceptance did **not** pass.

## Neon durable state after Instagram attempt

Read-only verification after all diagnostics:

```text
KRCM_41341f1e-656e-41cb-b735-7fa8f2015e62
  YouTube / COMPLETED / Gemini direct / retrieval credits 0 / STT seconds 0

KRCM_24db1049-5b9c-42df-85ec-686d80ed9471
  Instagram / FAILED / Cobalt retrieval / retrieval credits 0 / STT seconds 0

krc_media_stt_charges rows: 0
charged STT seconds: 0
```

No provider-consuming diagnostic created a new Neon job or STT charge.

## Cobalt diagnostic evidence

Two bounded Instagram retrieval-only probes returned the same result:

```text
HTTP 429
json_valid: false
provider_status: null
provider_error_code: null
```

A separate YouTube control probe through the same Cobalt endpoint also returned:

```text
endpoint_host: krc-cobalt-media-beta-kolemasakar.onrender.com
probe: youtube_control
HTTP 429
Content-Type: text/plain; charset=utf-8
Server: cloudflare
Retry-After: absent
rate-limit headers: absent
json_valid: false
```

This differs from Cobalt's normal application rate-limit behavior, which returns a JSON error response. Together with the cross-platform YouTube control, the evidence localizes the active blocker to an edge layer before a usable Cobalt application JSON response; it is not specific to the Instagram URL.

The exact originating edge component cannot be proven further from the sanitized evidence, so the canonical wording is:

```text
Cobalt Render endpoint edge-level HTTP 429 / non-JSON blocker
```

Do not overstate this as a proven Cobalt application error.

## Current Render Cobalt state

```text
service: krc-cobalt-media-beta-kolemasakar
service id: srv-da5ggq6k1f9s738j8d8g
plan: free
region: frankfurt
status: not_suspended
image: ghcr.io/imputnet/cobalt@sha256:63186dd68afd57ce3bb1f62cc4c139f5fa95b9c3e87a3cf5c6e4c7a570523f62
live deploy: dep-dafeelf40ujc73av801g
```

The service remains present as the current configured Cobalt endpoint but is **not accepted for Instagram/Facebook R2 traffic** while the `429` blocker persists.

## Owner architecture decision - FREE ONLY

The owner explicitly excluded paid hosting from consideration.

Canonical policy:

```text
Render paid instance: NOT CONSIDERED
paid Cobalt hosting: NOT CONSIDERED
paid retrieval fallback: FORBIDDEN
paid STT fallback: FORBIDDEN
paid proxy fallback: FORBIDDEN
FREE_TIER_ONLY: retained
```

Approved remediation direction:

```text
self-hosted Cobalt -> migrate from Render Free path to OCI Always Free VM
VoiceBridge        -> remain on Render Free
Neon               -> unchanged
private GPT        -> unchanged
public GPT         -> unchanged
```

Target routing after successful migration:

```text
Private KRC MEDIA BETA
  -> VoiceBridge / Render Free
  -> OCI Always Free self-hosted Cobalt
  -> Instagram / Facebook media retrieval
  -> AssemblyAI Free Trial STT
  -> Neon durable KRCM
```

Only `KRC_MEDIA_COBALT_ENDPOINT` should need to change in VoiceBridge after the new Cobalt endpoint passes its own preflight; secrets remain server-side.

## R2 / R3 gate state

```text
R0   PASS
R1   COMPLETE
R2-A PASS
R2-B PASS
R2-C COMPLETE
R2   PARTIAL PASS
     YouTube: PASS
     Instagram: FAIL-CLOSED / BLOCKED pending OCI Cobalt migration
     Facebook: PENDING
     Telegram: PENDING
     Core isolation: PENDING
R3   HOLD / NOT READY
R4   HOLD
```

`R3_READY = FALSE`.

## Exact continuation point

Next work is infrastructure remediation, not another Instagram/Facebook provider canary on the blocked Render Cobalt endpoint:

```text
1. OCI preflight: inspect existing Compute instances and Always Free quota
2. create only an Always Free eligible VM; do not create paid resources
3. deploy Docker + self-hosted Cobalt + HTTPS reverse proxy + API-key protection
4. run retrieval-only Cobalt preflight
5. update only KRC_MEDIA_COBALT_ENDPOINT in VoiceBridge if preflight passes
6. bounded Instagram canary
7. if Instagram PASS -> bounded Facebook canary
8. bounded Telegram canary
9. Render/Neon delta + no-paid-fallback verification
10. forced MEDIA failure + Core KRC isolation regression
11. only if all remaining checks PASS -> record full R2 PASS and separately assess R3
```

Do not merge PR #45 and do not modify/update the public KRC GPT without separate explicit authorization.

## Recovery instruction

Recovery must start from checkpoint 87 and then re-read:

1. `docs/KRC_MEDIA_BETA_RECOVERY_POINTER.md`;
2. this checkpoint;
3. `subprojects/media_beta/00_INDEX.md`;
4. `subprojects/media_beta/02_ROADMAP.md`;
5. `subprojects/media_beta/06_DECISION_LOG.md`;
6. `subprojects/media_beta/08_CHAT_HANDOFF.md`;
7. `gpt_store/media_r2_gemini_youtube_canary_manifest.yaml`;
8. current VoiceBridge branch/CI/PR state;
9. current Render VoiceBridge and Cobalt state;
10. current Neon durable state;
11. current private/public GPT Builder state.

Recovery command:

`recover KRC MEDIA BETA checkpoint 87 Cobalt edge blocker OCI Always Free migration 2026-09-07`
