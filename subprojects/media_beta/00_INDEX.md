# MEDIA BETA Documentation Index

Канонічний індекс документації K-Research & Critic MEDIA BETA.

Version: 6.7
Status: ACTIVE / CHECKPOINT_88 / R2_YOUTUBE_ACCEPTED / OCI_COBALT_LOCAL_PASS / INSTAGRAM_LOCAL_RETRIEVAL_PASS / PUBLIC_HTTPS_PENDING / R3_HOLD
Updated: 2026-09-08

## Product boundary

`K-Research & Critic - MEDIA BETA` is an additive MEDIA capability intended for the already-published `K-Research & Critic` product. `K_Research_Critic` remains the product/release authority. VoiceBridge provides the isolated MEDIA backend implementation and validation evidence.

Current product reality:

```text
public KRC: already published / user-accessible / unchanged
private KRC MEDIA BETA: owner-only / checkpoint-88 canary package active
future public MEDIA target: same existing public KRC identity
```

Critical invariant:

```text
MEDIA unavailable/fails -> MEDIA unavailable/fails closed
Core KRC               -> remains user-accessible and functional
```

## Canonical reading order

1. `88_R2_OCI_COBALT_LOCAL_INSTAGRAM_RETRIEVAL_PASS_PUBLIC_HTTPS_PENDING_CHECKPOINT_2026_09_08.md` - current canonical recovery checkpoint.
2. `87_R2_INSTAGRAM_COBALT_EDGE_BLOCKER_OCI_FREE_MIGRATION_CHECKPOINT_2026_09_07.md` - Render edge blocker + approved OCI migration baseline.
3. `86_R2_YOUTUBE_GEMINI_LIVE_ACCEPTANCE_R3_READINESS_HOLD_2026_09_07.md` - accepted YouTube live baseline.
4. `85_R2_GEMINI_DIRECT_HANDOFF_REPOSITORY_SYNC_2026_09_07.md` - pre-deployment handoff checkpoint.
5. `84_R2_YOUTUBE_GEMINI_DIRECT_REPOSITORY_READY_2026_09_07.md` - accepted Gemini-direct repository pivot.
6. `83_R2_PUBLIC_ACTION_SCHEMA_REPOSITORY_READY_2026_09_05.md` - public Action repository checkpoint.
7. `82_R2_PUBLIC_COBALT_RECONCILIATION_REPOSITORY_SYNC_2026_09_04.md` - Cobalt routing reconciliation.
8. `81_R2_LIVE_PROMOTION_PARTIAL_CANARY_2026_09_04.md` - earlier promotion/partial canary baseline.
9. `80_R2C_PUBLIC_PRIVACY_RENDER_PROMOTION_READY_2026_09_04.md` - privacy/release plan.
10. `79_R2B_FAILURE_ISOLATION_FREE_QUOTA_PASS_2026_09_04.md` - failure-isolation evidence.
11. `78_R2A_PUBLIC_FREE_TIER_ADMISSION_PASS_2026_09_04.md` - public free-only admission policy.

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

Accepted/pending free-only target:

```text
YouTube   -> Gemini Developer API Free Tier direct public URL -> KRCM/Neon
Instagram -> self-hosted Cobalt -> AssemblyAI universal-2 Free -> KRCM/Neon
Facebook  -> self-hosted Cobalt -> AssemblyAI universal-2 Free -> KRCM/Neon
Telegram  -> public Telegram web -> AssemblyAI universal-2 Free -> KRCM/Neon
```

Infrastructure state:

```text
Render Free Cobalt endpoint -> historical HTTP 429 / non-JSON edge blocker
OCI Cobalt local secure runtime -> PASS
OCI Instagram local retrieval-only -> PASS
OCI public HTTPS endpoint -> PENDING
VoiceBridge endpoint cutover -> NOT PERFORMED
paid hosting -> NOT CONSIDERED
```

No paid retrieval, paid STT, paid proxy, user-cookie/login, or automatic paid fallback is authorized.

## VoiceBridge and Render state

```text
VoiceBridge repository: kolemasakar/VoiceBridge
branch: agent/krc-media-gemini-migration
head: 68a39d9109455c3e9e69ffeb3a7456998f0620db
latest known Validate on exact head: 34159780308 / SUCCESS
PR #45: OPEN / DRAFT / UNMERGED / mergeable=true

Render VoiceBridge service: voicebridge-krc-media-beta-kolemasakar
configured branch: agent/krc-media-gemini-migration
autoDeploy: no
live deploy: dep-dafhul0n74is73a3nncg
live commit: 68a39d9109455c3e9e69ffeb3a7456998f0620db
status: LIVE

Render Cobalt service: krc-cobalt-media-beta-kolemasakar
plan: free
status: present / not accepted for Instagram/Facebook while historical edge blocker remains
```

Diagnostic commits/branches are evidence only and are not production runtime.

## OCI Cobalt state

```text
instance: krc-cobalt-media-beta
shape: VM.Standard.E2.1.Micro / Always Free-eligible
region: eu-frankfurt-1
public IPv4: 89.168.65.88
private IPv4: 10.0.0.26
OS: Ubuntu 24.04 Minimal x86_64
Docker: 29.1.3
Docker Compose: 2.40.3
swap: 2 GiB
```

Pinned Cobalt:

```text
image digest: sha256:63186dd68afd57ce3bb1f62cc4c139f5fa95b9c3e87a3cf5c6e4c7a570523f62
version: 11.7.1
commit: a636575b09de1fc55d9b8cd98cac88f5f2f16b42
binding: 127.0.0.1:9000 only
API key required: yes
```

Security/preflight:

```text
owner SSH source 91.199.188.209/32 -> locally allowed
iptables persistence -> enabled
API-key missing request -> blocked / error.api.auth.key.missing
valid API key -> auth accepted
```

## Live acceptance state

```text
YouTube capability read: PASS
explicit Gemini Free data-use consent: PASS
Gemini provider execution: PASS
Neon durable completion: PASS
duplicate durable reuse: PASS
new provider work on reuse: NO

Instagram OCI local authenticated retrieval-only: PASS
Instagram test POST: HTTP 200 / status=tunnel
fresh tunnel download: 214560 bytes / curl rc=0
Instagram live VoiceBridge canary: PENDING
```

OCI YouTube Cobalt control returned `error.api.youtube.login`; this is diagnostic only. The accepted YouTube route remains Gemini direct and must be protected from regression during the future Cobalt endpoint cutover.

## Public HTTPS preparation

```text
89-168-65-88.sslip.io -> 89.168.65.88 / DNS PASS
dedicated OCI NSG -> PENDING
80/443 public ingress -> PENDING
HTTPS reverse proxy/TLS -> PENDING
Cobalt API_URL public HTTPS value -> PENDING
external authenticated POST/tunnel verification -> PENDING
```

Port 9000 remains loopback-only.

A local OCI API key exists for preflight. Before cutover, align OCI Cobalt server-side to the existing VoiceBridge `KRC_MEDIA_COBALT_API_KEY` without exposing the secret so the eventual VoiceBridge change can remain limited to `KRC_MEDIA_COBALT_ENDPOINT`.

## Gate state

```text
R0   PASS
R1   COMPLETE
R2-A PASS
R2-B PASS
R2-C COMPLETE
R2   PARTIAL PASS
     YouTube: PASS
     OCI secure local runtime: PASS
     Instagram OCI local retrieval-only: PASS
     Instagram live canary: PENDING
     Facebook: PENDING
     Telegram: PENDING
     Core isolation: PENDING
R3   HOLD / NOT READY
R4   HOLD
```

## Next sequence

```text
1. recover checkpoint 88
2. create/attach dedicated OCI NSG to krc-cobalt-vnic without changing shared default Security List
3. enable required 80/443 path in OCI + local firewall while preserving SSH restriction and OCI instance-service rules
4. deploy HTTPS reverse proxy/TLS for 89-168-65-88.sslip.io
5. set Cobalt API_URL to public HTTPS base URL; keep 9000 loopback-only
6. align OCI API key to existing VoiceBridge server-side key
7. external authenticated Instagram POST + tunnel preflight
8. verify Gemini-direct YouTube regression protection
9. only after PASS update KRC_MEDIA_COBALT_ENDPOINT
10. bounded Instagram live canary
11. if PASS -> Facebook canary
12. Telegram canary
13. Render + Neon delta/no-paid-fallback verification
14. Core KRC isolation regression including forced MEDIA failure
15. if all PASS -> record full R2 PASS
16. only then -> separate explicit R3 owner gate
```

## Recovery command

`recover KRC MEDIA BETA checkpoint 88 OCI Cobalt local Instagram retrieval pass public HTTPS pending 2026-09-08`
