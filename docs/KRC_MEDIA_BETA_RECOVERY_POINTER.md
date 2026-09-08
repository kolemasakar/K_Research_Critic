# K-Research & Critic - MEDIA BETA Recovery Pointer
Канонічний покажчик поточного стану MEDIA BETA після accepted YouTube Gemini-direct path, OCI Always Free-eligible Cobalt deployment, local API-key hardening, and successful local Instagram retrieval-only preflight.

Status: ACTIVE POINTER / CHECKPOINT 88 / R2 YOUTUBE ACCEPTED / OCI COBALT LOCAL PASS / INSTAGRAM LOCAL RETRIEVAL PASS / PUBLIC HTTPS PENDING / R3 HOLD
Updated: 2026-09-08

`K-Research & Critic - MEDIA BETA` remains an additive MEDIA capability planned for the existing published `K-Research & Critic` identity.

## Current canonical checkpoint

Repository:

`kolemasakar/K_Research_Critic`

Branch:

`main`

Path:

`subprojects/media_beta/88_R2_OCI_COBALT_LOCAL_INSTAGRAM_RETRIEVAL_PASS_PUBLIC_HTTPS_PENDING_CHECKPOINT_2026_09_08.md`

## Current gate state

```text
R0   PASS
R1   COMPLETE
R2-A PASS
R2-B PASS
R2-C COMPLETE
R2   PARTIAL PASS
     YouTube: PASS / Gemini direct
     OCI Cobalt secure local runtime: PASS
     Instagram OCI local retrieval-only: PASS
     Instagram live VoiceBridge canary: PENDING
     Facebook: PENDING
     Telegram: PENDING
     Core isolation: PENDING
R3   HOLD / NOT READY
R4   HOLD
```

`R3_READY = FALSE`.

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

Revalidated before checkpoint-88 documentation sync:

```text
repository: kolemasakar/VoiceBridge
branch: agent/krc-media-gemini-migration
head: 68a39d9109455c3e9e69ffeb3a7456998f0620db
latest known Validate on exact head: 34159780308 / SUCCESS
PR #45: OPEN / DRAFT / UNMERGED / mergeable=true
```

## Current live VoiceBridge backend

```text
Render MEDIA service: voicebridge-krc-media-beta-kolemasakar
service id: srv-da1kic5bedkc73d6fk60
configured branch: agent/krc-media-gemini-migration
autoDeploy: no
plan: free
region: frankfurt
live commit: 68a39d9109455c3e9e69ffeb3a7456998f0620db
live deploy: dep-dafhul0n74is73a3nncg
status: LIVE
```

Temporary diagnostic commits/branches remain evidence only and are not production runtime.

## Accepted live YouTube evidence retained

```text
Gemini Free consent gate: PASS
Gemini direct execution: PASS
Neon durable completion: PASS
provider_mode: youtube_gemini_direct
provider_model: gemini-3.7-flash
retrieval_provider: gemini_youtube_url
retrieval credits: 0
STT seconds: 0
durable duplicate reuse: PASS
new provider call on reuse: NO
```

## Render Cobalt blocker retained as historical evidence

The existing Render Free Cobalt service remains present and currently configured externally, but is not accepted for Instagram/Facebook R2 traffic:

```text
service: krc-cobalt-media-beta-kolemasakar
service id: srv-da5ggq6k1f9s738j8d8g
plan: free
region: frankfurt
status: not_suspended
image: ghcr.io/imputnet/cobalt@sha256:63186dd68afd57ce3bb1f62cc4c139f5fa95b9c3e87a3cf5c6e4c7a570523f62
```

Canonical historical blocker:

`Render Cobalt endpoint edge-level HTTP 429 / non-JSON blocker`

No live Render endpoint/env change has been performed during the OCI local preflight.

## OCI Cobalt current state

```text
instance: krc-cobalt-media-beta
region: eu-frankfurt-1
shape: VM.Standard.E2.1.Micro / Always Free-eligible
OS: Ubuntu 24.04 Minimal x86_64
public IPv4: 89.168.65.88
private IPv4: 10.0.0.26
Docker: 29.1.3
Docker Compose: 2.40.3
swap: 2 GiB
```

Pinned Cobalt:

```text
image: ghcr.io/imputnet/cobalt@sha256:63186dd68afd57ce3bb1f62cc4c139f5fa95b9c3e87a3cf5c6e4c7a570523f62
version: 11.7.1
commit: a636575b09de1fc55d9b8cd98cac88f5f2f16b42
binding: 127.0.0.1:9000 only
API_AUTH_REQUIRED: 1
API key file: mounted read-only / secret not stored in repo
```

SSH is narrowed locally to the observed owner source IPv4 `91.199.188.209/32`; persisted iptables rules retain OCI instance-service rules.

## OCI API-key gate - PASS

```text
without key -> HTTP 400 / error.api.auth.key.missing
with valid key + unsupported URL -> HTTP 400 / error.api.link.invalid
api keys loaded successfully -> confirmed in Cobalt logs
```

## OCI Instagram retrieval-only preflight - PASS

Test URL:

`https://www.instagram.com/reel/DEAyVa4SF3E/`

Authenticated local POST result:

```text
HTTP 200
status: tunnel
filename: instagram_DEAyVa4SF3E_audio.mp3
```

Fresh tunnel download:

```text
curl return code: 0
size: 214560 bytes
```

Canonical wording:

`OCI Cobalt local authenticated Instagram retrieval-only preflight: PASS`

This is not yet a live VoiceBridge/AssemblyAI canary.

## OCI YouTube control

Authenticated Cobalt control returned:

```text
HTTP 400
error.api.youtube.login
```

The accepted production-candidate YouTube route remains Gemini direct. Before endpoint cutover, regression evidence must confirm that changing the Cobalt endpoint cannot alter that accepted YouTube path or introduce a Cobalt fallback.

## Public HTTPS state

DNS candidate resolves:

```text
89-168-65-88.sslip.io -> 89.168.65.88
```

Still pending:

```text
dedicated OCI NSG attached to krc-cobalt-vnic
TCP/80 + TCP/443 ingress
local firewall 80/443 rules
HTTPS reverse proxy + public TLS
Cobalt API_URL -> public HTTPS base URL
external authenticated POST + tunnel verification
```

Port 9000 remains loopback-only and must stay behind the reverse proxy.

## API-key alignment before live cutover

A local OCI API key was generated for preflight. The existing VoiceBridge `KRC_MEDIA_COBALT_API_KEY` value was not exposed or verified identical.

To preserve checkpoint-87 policy, prefer aligning OCI Cobalt server-side to the existing VoiceBridge secret so the eventual live VoiceBridge configuration change remains limited to:

`KRC_MEDIA_COBALT_ENDPOINT`

Do not expose either key in chat, GPT configuration, repository files, or documentation.

## Remaining R2 work before R3 readiness

```text
OCI dedicated NSG + local 80/443 firewall rules
HTTPS reverse proxy and TLS for 89-168-65-88.sslip.io
public authenticated Instagram retrieval/tunnel preflight
server-side API-key alignment
Gemini-direct YouTube regression protection
VoiceBridge KRC_MEDIA_COBALT_ENDPOINT cutover only after public preflight PASS
Instagram functional live canary PASS
Facebook bounded canary PASS
Telegram bounded canary PASS
Render + Neon delta/no-paid-fallback verification
Core KRC isolation regression including forced MEDIA failure
```

## Retained invariant

```text
MEDIA unavailable/fails -> MEDIA unavailable/fails closed
Core KRC               -> remains user-accessible and functional
```

Recovery must start from checkpoint 88.

Recovery command:

`recover KRC MEDIA BETA checkpoint 88 OCI Cobalt local Instagram retrieval pass public HTTPS pending 2026-09-08`

Before any state-changing action, re-read exact GitHub heads/CI, current Render live deploys, PR #45 state, current OCI network/firewall/Cobalt state, Neon durable state, and current private/public GPT Builder state. Do not merge PR #45 or update the public GPT without separate explicit owner authorization.
