# K-Research & Critic / MEDIA BETA - R2 OCI Cobalt Local Instagram Retrieval PASS + Public HTTPS Pending Checkpoint 88

Date: 2026-09-08
Status: R2_PARTIAL_PASS / YOUTUBE_ACCEPTED / OCI_COBALT_LOCAL_SECURE_RUNTIME_PASS / INSTAGRAM_RETRIEVAL_LOCAL_PASS / PUBLIC_HTTPS_PENDING / R3_HOLD

## Scope

This checkpoint supersedes checkpoint 87 as the canonical recovery entry point after the owner-approved free-only Cobalt migration reached a working local OCI runtime and reproduced successful Instagram retrieval without any paid provider fallback.

It records infrastructure/runtime evidence only. It does **not** change the live VoiceBridge Cobalt endpoint, merge VoiceBridge PR #45, modify the public `K-Research & Critic` GPT, activate paid hosting, or mark full R2 complete.

Critical invariant:

```text
MEDIA unavailable/fails -> MEDIA unavailable/fails closed
Core KRC               -> remains user-accessible and functional
```

## KRC repository state before checkpoint-88 sync

```text
repository: kolemasakar/K_Research_Critic
branch: main
pre-checkpoint-88 tip: 196c0185b082d10296904be5e28a35be43d8d2c2
Tests run 34161010330: SUCCESS
public KRC GPT: unchanged / no MEDIA Action
private KRC MEDIA BETA: owner-only
```

Current Action candidate remains:

```text
gpt_store/actions/media_public_free_openapi.yaml
version: 0.8.0-r2-gemini-youtube
public activation: false
```

## VoiceBridge accepted runtime revalidated

```text
repository: kolemasakar/VoiceBridge
branch: agent/krc-media-gemini-migration
head: 68a39d9109455c3e9e69ffeb3a7456998f0620db
latest known Validate on exact head: 34159780308 / SUCCESS
PR #45: OPEN / DRAFT / UNMERGED / mergeable=true
```

The accepted VoiceBridge code/runtime remains unchanged by the OCI work.

Current Render VoiceBridge state was re-read before this documentation sync:

```text
service: voicebridge-krc-media-beta-kolemasakar
service id: srv-da1kic5bedkc73d6fk60
configured branch: agent/krc-media-gemini-migration
autoDeploy: no
plan: free
region: frankfurt
live deploy: dep-dafhul0n74is73a3nncg
live commit: 68a39d9109455c3e9e69ffeb3a7456998f0620db
status: LIVE
```

## Existing Render Cobalt remains configured but unaccepted

The old Render Free Cobalt service still exists and remains the currently configured external endpoint until an explicit cutover:

```text
service: krc-cobalt-media-beta-kolemasakar
service id: srv-da5ggq6k1f9s738j8d8g
plan: free
region: frankfurt
status: not_suspended
image: ghcr.io/imputnet/cobalt@sha256:63186dd68afd57ce3bb1f62cc4c139f5fa95b9c3e87a3cf5c6e4c7a570523f62
```

Its checkpoint-87 edge blocker remains historical evidence:

```text
Render Cobalt endpoint -> HTTP 429 / non-JSON edge response
Instagram/Facebook acceptance on that endpoint -> NOT ACCEPTED
```

No Render environment variable was changed during the OCI local preflight.

## OCI Always Free-eligible VM created

A dedicated OCI Compute VM was created using the live-console `Always Free-eligible` shape selection:

```text
instance: krc-cobalt-media-beta
region: eu-frankfurt-1
availability domain: AD-1
shape: VM.Standard.E2.1.Micro
OCPU: 1
RAM: 1 GB
OS: Ubuntu 24.04 Minimal x86_64
public IPv4: 89.168.65.88
private IPv4: 10.0.0.26
hostname: krc-cobalt
VCN: kgm-e4-vcn
subnet: kgm-e4-public-subnet
```

No paid Cobalt hosting path was introduced.

## OCI host hardening / runtime state

SSH access was verified using the owner key. Local iptables was narrowed so new SSH connections are accepted only from the observed owner source IPv4:

```text
91.199.188.209/32 -> TCP/22 ACCEPT
other new TCP/22  -> rejected by existing INPUT terminal reject
```

`iptables-persistent` is installed/enabled and rules are saved. OCI instance-service rules were retained.

A 2 GiB swap file was configured because the VM has ~1 GiB RAM:

```text
/swapfile: 2 GiB
fstab persistence: configured
```

Docker runtime:

```text
Docker: 29.1.3
Docker Compose: 2.40.3
Docker service: active
```

## Pinned Cobalt runtime

The exact approved image digest was pulled and deployed:

```text
ghcr.io/imputnet/cobalt@sha256:63186dd68afd57ce3bb1f62cc4c139f5fa95b9c3e87a3cf5c6e4c7a570523f62
runtime architecture: amd64 / linux
Cobalt version: 11.7.1
Cobalt commit: a636575b09de1fc55d9b8cd98cac88f5f2f16b42
```

Current Docker binding is intentionally local-only:

```text
127.0.0.1:9000 -> container 9000/tcp
public 0.0.0.0:9000 exposure: NO
```

The container uses:

```text
API_URL=http://127.0.0.1:9000/
API_KEY_URL=file:///keys.json
API_AUTH_REQUIRED=1
read_only=true
restart=unless-stopped
```

The API-key file is mounted read-only. The key value is not stored in this repository or checkpoint.

## API-key fail-closed gate - PASS

Runtime evidence:

```text
[✓] api keys loaded successfully!
```

Without an API key, a valid YouTube-form request was rejected before retrieval:

```text
HTTP 400
error.code: error.api.auth.key.missing
```

With the correct key, authentication passed and an unsupported `example.com` URL progressed to normal request validation:

```text
HTTP 400
error.code: error.api.link.invalid
```

Therefore:

```text
missing key -> BLOCK
valid key   -> auth accepted
API-key fail-closed gate -> PASS
```

## Instagram retrieval-only local preflight - PASS

Test URL:

`https://www.instagram.com/reel/DEAyVa4SF3E/`

Authenticated Cobalt POST using the same payload shape as the VoiceBridge retriever returned:

```text
HTTP 200
status: tunnel
filename: instagram_DEAyVa4SF3E_audio.mp3
```

A fresh tunnel URL was consumed immediately and the media stream downloaded successfully:

```text
curl return code: 0
downloaded bytes: 214560
```

This proves the OCI-hosted pinned Cobalt application can currently retrieve usable Instagram media from the checkpoint test URL without a paid retrieval provider.

Canonical acceptance wording:

```text
OCI Cobalt local authenticated Instagram retrieval-only preflight: PASS
```

This is **not yet** a public VoiceBridge/AssemblyAI end-to-end canary because HTTPS exposure and endpoint cutover have not occurred.

## YouTube OCI Cobalt control - diagnostic FAIL, accepted YouTube route unchanged

Authenticated Cobalt control request to:

`https://www.youtube.com/watch?v=jNQXAC9IVRw`

returned:

```text
HTTP 400
error.code: error.api.youtube.login
```

This is a diagnostic result for the OCI Cobalt instance. It does not revoke the already accepted R2 YouTube path, which remains Gemini Developer API direct URL processing.

Before any Cobalt endpoint cutover, regression evidence must confirm that the accepted Gemini-direct YouTube route remains unchanged and no unintended Cobalt fallback is introduced.

## DNS / public HTTPS preparation

The free hostname candidate resolves correctly:

```text
89-168-65-88.sslip.io -> 89.168.65.88
```

Public HTTPS is **not yet configured**.

Still pending:

```text
dedicated OCI NSG for the Cobalt VNIC
TCP/80 + TCP/443 ingress
local firewall 80/443 rules
HTTPS reverse proxy
public TLS certificate
Cobalt API_URL -> public HTTPS base URL
external authenticated POST/tunnel verification
```

Port 9000 must remain loopback-only behind the reverse proxy.

## API-key alignment before cutover

A local OCI API key was generated for the preflight. The existing VoiceBridge `KRC_MEDIA_COBALT_API_KEY` value was not read into chat and has not been proven identical to the OCI preflight key.

Checkpoint-87 policy remains authoritative: prefer preserving the existing VoiceBridge secret and aligning OCI Cobalt to it server-side so that the eventual live change can remain limited to:

```text
KRC_MEDIA_COBALT_ENDPOINT
```

Do not expose either key in chat, GPT configuration, repository files, or documentation.

## Free-only policy retained

```text
Render paid instance: NOT CONSIDERED
paid Cobalt hosting: NOT CONSIDERED
paid retrieval fallback: FORBIDDEN
paid STT fallback: FORBIDDEN
paid proxy fallback: FORBIDDEN
Supadata public: none
ScrapeCreators public: none
cookies/login: none
```

## Current R2 / R3 gate state

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

## Exact continuation point

```text
1. create/attach a dedicated OCI NSG to krc-cobalt-vnic; do not modify the shared default Security List
2. add only required public HTTP/HTTPS ingress for the Cobalt reverse proxy
3. configure local firewall for 80/443 while preserving owner-only SSH and OCI instance-service rules
4. deploy HTTPS reverse proxy for 89-168-65-88.sslip.io
5. change Cobalt API_URL to the public HTTPS base URL; keep container port 9000 loopback-only
6. align OCI API key with the existing VoiceBridge server-side key without exposing the secret
7. external authenticated Instagram retrieval/tunnel preflight over HTTPS
8. verify accepted Gemini-direct YouTube route cannot regress from the Cobalt endpoint change
9. only after public endpoint preflight PASS, update KRC_MEDIA_COBALT_ENDPOINT in VoiceBridge
10. bounded Instagram live canary
11. if Instagram PASS -> bounded Facebook canary
12. bounded Telegram canary
13. Render/Neon delta + no-paid-fallback verification
14. forced MEDIA failure + Core KRC isolation regression
15. only if all remaining checks PASS -> record full R2 PASS and separately assess R3
```

Do not merge PR #45 and do not modify/update the public KRC GPT without separate explicit owner authorization.

## Recovery instruction

Recovery must start from checkpoint 88 and then re-read:

1. `docs/KRC_MEDIA_BETA_RECOVERY_POINTER.md`;
2. this checkpoint;
3. `subprojects/media_beta/00_INDEX.md`;
4. `subprojects/media_beta/02_ROADMAP.md`;
5. `subprojects/media_beta/06_DECISION_LOG.md`;
6. `subprojects/media_beta/08_CHAT_HANDOFF.md`;
7. `gpt_store/media_r2_gemini_youtube_canary_manifest.yaml`;
8. current VoiceBridge branch/CI/PR state;
9. current Render VoiceBridge/Cobalt state;
10. current OCI VM/network/firewall/Cobalt state;
11. current Neon durable state;
12. current private/public GPT Builder state.

Recovery command:

`recover KRC MEDIA BETA checkpoint 88 OCI Cobalt local Instagram retrieval pass public HTTPS pending 2026-09-08`
