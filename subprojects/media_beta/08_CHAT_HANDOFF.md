# MEDIA BETA Chat Handoff

Канонічна інструкція відновлення K-Research & Critic - MEDIA BETA у новому чаті.

Version: 5.2
Status: ACTIVE_HANDOFF / CHECKPOINT_88 / R2_YOUTUBE_ACCEPTED / OCI_COBALT_LOCAL_PASS / INSTAGRAM_LOCAL_RETRIEVAL_PASS / PUBLIC_HTTPS_PENDING / R3_HOLD
Checkpoint date: 2026-09-08

## Recovery command

`recover KRC MEDIA BETA checkpoint 88 OCI Cobalt local Instagram retrieval pass public HTTPS pending 2026-09-08`

## Mandatory recovery order

1. `subprojects/media_beta/88_R2_OCI_COBALT_LOCAL_INSTAGRAM_RETRIEVAL_PASS_PUBLIC_HTTPS_PENDING_CHECKPOINT_2026_09_08.md`
2. `docs/KRC_MEDIA_BETA_RECOVERY_POINTER.md`
3. `subprojects/media_beta/00_INDEX.md`
4. `subprojects/media_beta/02_ROADMAP.md`
5. `subprojects/media_beta/06_DECISION_LOG.md`
6. `gpt_store/media_r2_gemini_youtube_canary_manifest.yaml`
7. `gpt_store/actions/media_public_free_openapi.yaml`
8. `prompts/GPT_STORE_MEDIA_R2_GEMINI_YOUTUBE_CANARY_INSTRUCTIONS.md`
9. current VoiceBridge branch / CI / PR #45 state
10. current Render VoiceBridge + Cobalt state
11. current OCI VM/network/firewall/Cobalt state
12. current Neon durable state
13. current private/public Builder state

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
latest known Validate on exact head: 34159780308 / SUCCESS
PR #45: OPEN / DRAFT / UNMERGED / mergeable=true

Render VoiceBridge service: voicebridge-krc-media-beta-kolemasakar
configured branch: agent/krc-media-gemini-migration
autoDeploy: no
plan: free
region: frankfurt
live deploy: dep-dafhul0n74is73a3nncg
live commit: 68a39d9109455c3e9e69ffeb3a7456998f0620db
```

Temporary diagnostic commits/branches remain evidence only and are not production runtime.

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

## Historical Render Cobalt blocker

Old Render Free Cobalt remains present and currently configured until explicit cutover:

```text
service: krc-cobalt-media-beta-kolemasakar
service id: srv-da5ggq6k1f9s738j8d8g
plan: free
region: frankfurt
status: not_suspended
image: ghcr.io/imputnet/cobalt@sha256:63186dd68afd57ce3bb1f62cc4c139f5fa95b9c3e87a3cf5c6e4c7a570523f62
```

Canonical checkpoint-87 blocker wording remains:

`Render Cobalt endpoint edge-level HTTP 429 / non-JSON blocker`

No Render endpoint/environment variable was changed during the OCI local preflight.

## OCI Cobalt current state

```text
instance: krc-cobalt-media-beta
region: eu-frankfurt-1
shape: VM.Standard.E2.1.Micro / Always Free-eligible
public IPv4: 89.168.65.88
private IPv4: 10.0.0.26
OS: Ubuntu 24.04 Minimal x86_64
Docker: 29.1.3
Docker Compose: 2.40.3
swap: 2 GiB
```

Host/runtime hardening:

```text
owner SSH source: 91.199.188.209/32
iptables persistence: enabled
Cobalt bind: 127.0.0.1:9000 only
Cobalt public 9000: NO
```

Pinned Cobalt:

```text
image digest: sha256:63186dd68afd57ce3bb1f62cc4c139f5fa95b9c3e87a3cf5c6e4c7a570523f62
version: 11.7.1
commit: a636575b09de1fc55d9b8cd98cac88f5f2f16b42
API_KEY_URL: file:///keys.json
API_AUTH_REQUIRED: 1
```

Secret values are not stored in KRC docs/repository.

## API-key gate - PASS

```text
without API key -> HTTP 400 / error.api.auth.key.missing
with valid key + unsupported URL -> HTTP 400 / error.api.link.invalid
Cobalt log -> api keys loaded successfully
```

## Instagram OCI local retrieval-only - PASS

Test URL:

`https://www.instagram.com/reel/DEAyVa4SF3E/`

Evidence:

```text
authenticated POST -> HTTP 200
status -> tunnel
filename -> instagram_DEAyVa4SF3E_audio.mp3
fresh tunnel download -> curl rc 0
retrieved bytes -> 214560
```

This is a local retrieval-only acceptance. VoiceBridge/AssemblyAI live canary has not yet been run on the OCI endpoint.

## OCI YouTube diagnostic control

```text
authenticated Cobalt control -> HTTP 400
error.code -> error.api.youtube.login
```

Accepted YouTube remains Gemini direct. Before endpoint cutover, prove the Cobalt endpoint change cannot regress the Gemini-direct path or introduce a Cobalt fallback.

## DNS / HTTPS state

```text
89-168-65-88.sslip.io -> 89.168.65.88 / PASS
public HTTPS reverse proxy -> PENDING
public TLS -> PENDING
dedicated OCI NSG -> PENDING
80/443 OCI + local firewall path -> PENDING
Cobalt API_URL public HTTPS -> PENDING
external authenticated POST/tunnel -> PENDING
```

Do not expose Cobalt port 9000 publicly.

## API-key alignment before cutover

A local OCI key was generated for preflight. The existing VoiceBridge `KRC_MEDIA_COBALT_API_KEY` was not exposed and has not been proven identical.

Preferred continuation: align OCI Cobalt server-side to the existing VoiceBridge secret so the eventual VoiceBridge live change remains limited to `KRC_MEDIA_COBALT_ENDPOINT`.

Do not paste the key into chat, GPT instructions, Action schema, repository, or documentation.

## Current Neon state retained

```text
YouTube durable job: COMPLETED
Instagram old Render-Cobalt job: FAILED
krc_media_stt_charges rows: 0
charged STT seconds: 0
```

No new VoiceBridge/AssemblyAI/Neon job was created by the OCI local retrieval-only probes.

## Current gate state

```text
R0: PASS
R1: COMPLETE
R2: PARTIAL PASS
    YouTube accepted
    OCI Cobalt secure local runtime PASS
    Instagram OCI local retrieval-only PASS
    Instagram live canary PENDING
    Facebook PENDING
    Telegram PENDING
    Core isolation PENDING
R3: HOLD / NOT READY
R4: HOLD
```

## Exact continuation point

```text
1. create/attach dedicated OCI NSG to krc-cobalt-vnic; do not modify shared default Security List
2. add required TCP/80 + TCP/443 ingress
3. add matching local firewall rules while preserving owner-only SSH and OCI instance-service rules
4. deploy HTTPS reverse proxy/TLS for 89-168-65-88.sslip.io
5. change Cobalt API_URL to public HTTPS base URL; keep 9000 loopback-only
6. align OCI API key to existing VoiceBridge server-side key without exposing it
7. external authenticated Instagram retrieval/tunnel preflight over HTTPS
8. verify Gemini-direct YouTube regression protection
9. only after PASS update KRC_MEDIA_COBALT_ENDPOINT
10. repeat bounded Instagram live canary
11. if PASS -> Facebook canary
12. Telegram canary
13. Render/Neon delta + no-paid-fallback verification
14. forced MEDIA failure + Core KRC isolation regression
15. if all PASS -> record full R2 PASS
16. only then -> separate explicit R3 owner gate
```

Do not merge PR #45 and do not modify/update the public KRC GPT without separate explicit owner authorization.

## Terminal marker

`MEDIA_BETA_HANDOFF_V5_2_CHECKPOINT_88_OCI_COBALT_INSTAGRAM_LOCAL_PASS_PUBLIC_HTTPS_PENDING_R3_HOLD`
