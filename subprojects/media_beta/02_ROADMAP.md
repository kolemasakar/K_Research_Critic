# MEDIA BETA Roadmap

Поточний roadmap K-Research & Critic MEDIA BETA після YouTube acceptance, Render Cobalt edge-blocker isolation, and successful local Instagram retrieval on the owner-approved OCI free-only replacement.

Version: 4.9
Status: R2_PARTIAL_PASS / YOUTUBE_ACCEPTED / OCI_COBALT_LOCAL_PASS / INSTAGRAM_LOCAL_RETRIEVAL_PASS / PUBLIC_HTTPS_PENDING / R3_HOLD
Updated: 2026-09-08

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

`88_R2_OCI_COBALT_LOCAL_INSTAGRAM_RETRIEVAL_PASS_PUBLIC_HTTPS_PENDING_CHECKPOINT_2026_09_08.md`

Recovery command:

`recover KRC MEDIA BETA checkpoint 88 OCI Cobalt local Instagram retrieval pass public HTTPS pending 2026-09-08`

## Current provider routing

Logical free-only routing remains:

```text
YouTube   -> Gemini Developer API Free Tier direct public URL -> durable KRCM/Neon
Instagram -> self-hosted Cobalt -> AssemblyAI universal-2 Free -> durable KRCM/Neon
Facebook  -> self-hosted Cobalt -> AssemblyAI universal-2 Free -> durable KRCM/Neon
Telegram  -> public Telegram web -> AssemblyAI universal-2 Free -> durable KRCM/Neon
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

The existing public KRC identity remains the protected product target. No MEDIA Action is attached to public KRC and checkpoint 88 does not authorize changing it.

## R1 - Repository integration

Status: COMPLETE.

KRC repository contains the public MEDIA candidate Action, private canary package, privacy candidate, regression tests, and recovery documentation.

## R2 - Permanent MEDIA backend promotion/readiness

Status: PARTIAL PASS / OCI PUBLIC-HTTPS REMEDIATION IN PROGRESS.

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
Instagram fail-closed behavior on blocked Render Cobalt: PASS as safety behavior
OCI Always Free-eligible VM creation: PASS
OCI Docker/pinned Cobalt deployment: PASS
OCI local port isolation 127.0.0.1:9000: PASS
OCI API-key fail-closed gate: PASS
OCI authenticated Instagram retrieval-only local preflight: PASS
```

Exact accepted VoiceBridge backend remains:

```text
Render service: voicebridge-krc-media-beta-kolemasakar
branch: agent/krc-media-gemini-migration
autoDeploy: no
live commit: 68a39d9109455c3e9e69ffeb3a7456998f0620db
live deploy: dep-dafhul0n74is73a3nncg
latest known Validate on exact head: 34159780308 / SUCCESS
PR #45: OPEN / DRAFT / UNMERGED / mergeable=true
```

Old blocked Render Cobalt remains present and externally configured until a separate cutover:

```text
Render service: krc-cobalt-media-beta-kolemasakar
plan: free
region: frankfurt
image: ghcr.io/imputnet/cobalt@sha256:63186dd68afd57ce3bb1f62cc4c139f5fa95b9c3e87a3cf5c6e4c7a570523f62
historical blocker: edge HTTP 429 / non-JSON
```

### OCI Cobalt local acceptance

Current VM/runtime:

```text
instance: krc-cobalt-media-beta
shape: VM.Standard.E2.1.Micro / Always Free-eligible
region: eu-frankfurt-1
public IP: 89.168.65.88
private IP: 10.0.0.26
Docker: 29.1.3
Compose: 2.40.3
Cobalt: 11.7.1 / commit a636575b09de1fc55d9b8cd98cac88f5f2f16b42
container port: 127.0.0.1:9000 only
API auth required: yes
```

Security state:

```text
SSH local ingress narrowed to 91.199.188.209/32
iptables persistence: enabled
swap: 2 GiB
missing API key -> blocked / error.api.auth.key.missing
valid API key -> accepted by auth layer
```

Instagram local retrieval-only evidence:

```text
source: https://www.instagram.com/reel/DEAyVa4SF3E/
POST: HTTP 200
status: tunnel
fresh tunnel download: rc=0
bytes: 214560
paid retrieval: none
```

Therefore:

`OCI_COBALT_INSTAGRAM_LOCAL_RETRIEVAL = PASS`.

### Public endpoint still pending

DNS preparation passed:

```text
89-168-65-88.sslip.io -> 89.168.65.88
```

Still required before VoiceBridge cutover:

```text
dedicated OCI NSG attached to krc-cobalt-vnic
80/443 ingress without modifying the shared default Security List
matching local firewall rules while preserving SSH restriction/OCI instance-service rules
HTTPS reverse proxy + public TLS
Cobalt API_URL set to public HTTPS base URL
external authenticated Instagram POST + tunnel preflight
```

Cobalt port 9000 must remain loopback-only.

A local OCI API key exists for preflight. Before live cutover, align OCI Cobalt server-side to the existing VoiceBridge `KRC_MEDIA_COBALT_API_KEY` without exposing the secret, preserving the intended live configuration change as `KRC_MEDIA_COBALT_ENDPOINT` only.

### YouTube regression boundary

The OCI Cobalt diagnostic control returned:

```text
HTTP 400
error.api.youtube.login
```

This does not revoke accepted YouTube R2 evidence because current YouTube processing is Gemini direct. Before changing the Cobalt endpoint, prove the accepted Gemini-direct path is unaffected and no Cobalt fallback can be introduced.

Still required before full R2 PASS:

```text
OCI public HTTPS endpoint/preflight
server-side API-key alignment
Gemini-direct YouTube regression protection
VoiceBridge endpoint cutover only after endpoint preflight PASS
Instagram functional live canary PASS
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
R2  PARTIAL PASS / YouTube accepted / OCI Instagram local retrieval PASS / public HTTPS pending
R3  HOLD / NOT READY
R4  HOLD
```

Every gate remains independent. Successful OCI local retrieval does not authorize endpoint cutover, R3, or public GPT changes.

## Exact continuation point

```text
OCI PUBLIC HTTPS COMPLETION
- dedicated NSG for krc-cobalt-vnic; do not change shared default Security List
- required 80/443 OCI + local firewall path
- HTTPS reverse proxy/TLS for 89-168-65-88.sslip.io
- Cobalt API_URL -> public HTTPS base URL
- keep 9000 loopback-only
- align OCI API key to existing VoiceBridge secret server-side
- external authenticated Instagram POST/tunnel preflight
- verify Gemini-direct YouTube regression protection
- update KRC_MEDIA_COBALT_ENDPOINT only after public preflight PASS
- repeat Instagram live canary
- Facebook
- Telegram
- Render/Neon no-paid-fallback checks
- Core isolation regression

NO PUBLIC GPT CHANGE
NO PR #45 MERGE
```
