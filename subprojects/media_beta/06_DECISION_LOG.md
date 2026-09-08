# MEDIA BETA Decision Log
Реєстр чинних і історичних рішень MEDIA BETA з актуальними release-hold рішеннями.

Version: 2.7
Status: ACTIVE
Updated: 2026-09-08

This file is the compact current decision index. Detailed historical rationale remains available in Git history and the numbered phase/acceptance records.

## Historical Decisions D001-D022

`D001` Media input is additive to the KRC Core - APPROVED.

`D002` CriticProfile approval remains mandatory before independent research - APPROVED.

`D003` Transcript proves what was said, not truth - APPROVED.

`D004` Closed beta precedes public scaling - APPROVED; original multi-tester target is now operationally superseded by owner-only hold state.

`D005` MEDIA BETA uses separate private product identity - APPROVED.

`D006` MEDIA BETA backend is isolated from production VoiceBridge - APPROVED.

`D007` Historical multi-tester admission used per-tester codes - APPROVED_HISTORICAL; normal current owner flow no longer asks for a code.

`D008` Subtitle-first principle - retained where reliable, but historical browser-helper implementation decisions are not current normal UX.

`D009` AssemblyAI is a beta reliability/STT provider, not a permanent public-free commitment - APPROVED.

`D010` Bounded beta resource limits - APPROVED.

`D011` Users do not provide provider API keys - APPROVED.

`D012` Full transcript is excluded from KRC checkpoints - APPROVED.

`D013` Sustainable free hybrid is a future direction, not current active architecture - APPROVED_DIRECTION.

`D014` Unlimited-free is interpreted operationally, not literally - APPROVED_DIRECTION.

`D015` Resource limits change only by explicit decision - APPROVED.

`D016` Browser-assisted ingress was the A4 fallback architecture - APPROVED_HISTORICAL / FALLBACK_ONLY.

`D017` Zero-client media router is public-only for remote platforms and multi-platform - APPROVED.

`D018` Local audio/video upload is a separate approved ingress class - APPROVED; live acceptance later completed in A9.10.

`D019` Managed transcript provider became primary zero-client YouTube approach - APPROVED.

`D020` Billable managed-provider operations require explicit user consent - APPROVED.

`D021` Managed KRCM jobs are durable and duplicate starts are credit-safe - APPROVED / LIVE_ACCEPTED.

`D022` Private owner Action hides beta admission behind bearer authentication and server-side owner admission - APPROVED / LIVE_ACCEPTED.

## D023 - Facebook Active Route Is Free Cobalt Only

Decision: APPROVED / LIVE_ACCEPTED
Date: 2026-08-24

Active Facebook behavior:

```text
Cobalt success -> AssemblyAI -> durable KRCM
Cobalt failure -> unavailable -> STOP
```

ScrapeCreators remains reserve-only, unconfigured, inactive, and not offerable. Automatic or offered paid fallback after Cobalt failure is forbidden.

Reason: preserve zero-client owner UX and prevent silent/accidental paid retrieval.

## D024 - Telegram Public Adapter Is Zero-Credit and No-Auth

Decision: APPROVED / LIVE_ACCEPTED
Date: 2026-08-26

Supported public Telegram video posts use public web/embed retrieval, trusted Telegram media delivery, AssemblyAI STT, and durable KRCM. Retrieval credits are zero. No login, cookies, session, bot token, or paid fallback is allowed.

Reason: maintain a public-only, credential-free adapter with explicit terminal failure behavior.

## D025 - Local openaiFileIdRefs Attachment Ingestion Is Accepted

Decision: APPROVED / LIVE_ACCEPTED
Date: 2026-08-26

One current-conversation audio/video attachment may use ChatGPT `openaiFileIdRefs` transport to the isolated backend. The backend accepts trusted OpenAI temporary HTTPS delivery, validates media, limits attachment size to 32 MiB, normalizes audio/video, uses AssemblyAI STT, and stores durable KRCM segments. Retrieval credits are zero. File IDs/signed URLs are not user-visible.

Reason: provide a stable zero-client source path for owner-local media without platform authentication.

## D026 - Copy-Safe Fenced Claim Table Is the Accepted UI Mitigation

Decision: APPROVED / LIVE_ACCEPTED
Date: 2026-08-26

The normal four-column table remains required. Because ChatGPT whole-response Copy can collapse the rendered table header, the final report also includes an identical fenced `text` table with literal pipe delimiters.

The fenced duplicate passed owner copy testing and is the accepted mitigation. The external rendered-table Copy defect alone does not reopen A10.

## D027 - Release Hold Owner Testing

Decision: APPROVED
Date: 2026-08-27

After A9/A9.10/A10 acceptance, the owner chose continued private testing before release.

```text
merge to main = HOLD
production promotion = HOLD
external testers = HOLD
public rollout = HOLD
```

Defects are fixed/revalidated in isolated feature branches during the hold.

## D028 - Release Gates Are Independent

Decision: APPROVED
Date: 2026-08-27

Merge, production promotion, external tester onboarding, and public rollout are separate decisions. Approval of one must never be inferred as approval of another.

Reason: repository integration, infrastructure deployment, audience expansion, and public publication carry different risks and controls.

## D029 - Post-AssemblyAI Free-Credit Hybrid C/D Is the Planned Free-First Direction

Decision: APPROVED_PLAN / NOT_IMPLEMENTED
Date: 2026-09-02

The owner selected the combined Hybrid C/D direction as the planned STT architecture **after AssemblyAI free credits are exhausted**.

Current runtime remains unchanged:

```text
active KRC prerecorded provider: AssemblyAI universal-2
Gemini normal prerecorded activation: FALSE
hybrid implementation now: FALSE
```

Planned future routing direction:

```text
Gemini 3.5 Transcribe Live
  -> preferred free route for eligible jobs without word timestamps/diarization

Gemini 3.5 Transcribe unary
  -> free feature route when timestamps and/or diarization are required and quota allows

AssemblyAI universal-2
  -> retained rollback/fallback technology
  -> billable fallback disabled by default after free credits expire
  -> paid use requires separate explicit owner authorization
```

No automatic paid provider fallback is authorized.

Before implementation, mutable assumptions must be revalidated: Gemini model availability, Free Tier limits, language coverage, Live session restrictions, privacy/data-use policy, and actual remaining AssemblyAI balance.

Targeted validation before cutover must cover code-switching, noisy Ukrainian/Russian, multi-speaker media, telephone-bandwidth speech, longer real-world media, numeric/date/name fidelity, and Gemini unary-versus-Live parity where applicable.

Detailed product plan:

`69_POST_ASSEMBLYAI_FREE_CREDITS_HYBRID_STT_PLAN_2026_09_02.md`

Technical implementation plan:

`kolemasakar/VoiceBridge` -> `docs/planning/2026-09-02_KRC_POST_ASSEMBLYAI_FREE_CREDITS_HYBRID_STT_IMPLEMENTATION_PLAN.md`

This decision does not authorize code changes, provider activation, deployment, merge, external testing, public rollout, or provider-consuming validation now.

## D030 - Close M3 With AssemblyAI Retained; M4 Starts as Repository-Only Preflight

Decision: APPROVED / M3_CLOSED / M4_PREFLIGHT
Date: 2026-09-02

The owner continued the project after recording D029. Because Hybrid C/D is explicitly deferred until AssemblyAI free credits are exhausted, the current M3 provider decision is closed without a cutover.

```text
M3: CLOSED
current KRC prerecorded provider: AssemblyAI universal-2
Gemini normal prerecorded activation: FALSE
provider cutover now: FALSE
future Hybrid C/D: PLANNED / NOT_IMPLEMENTED
```

The next phase is M4 infrastructure readiness. M4 begins with repository/image parity verification only; no deployment or canary is implied.

The first M4 preflight found two hard blockers in the current VoiceBridge cloud Docker image definition:

```text
ffmpeg/ffprobe required by accepted local attachment processing: MISSING
psql required by durable PostgreSQL/Neon persistence: MISSING
```

Therefore:

```text
M4_PREFLIGHT: COMPLETE
M4_CANARY_READY: FALSE
M4_DEPLOYMENT: NOT_AUTHORIZED
```

Required next work is feature-branch image remediation plus CI image-parity evidence. Any actual deployment/canary requires a separate owner authorization after those checks pass.

Canonical checkpoint:

`70_M3_CLOSED_M4_PREFLIGHT_BLOCKED_CHECKPOINT_2026_09_02.md`

VoiceBridge preflight authority:

`docs/history/2026-09-02_KRC_MEDIA_M4_DEPLOYMENT_IMAGE_PARITY_PREFLIGHT.md`

## D031 - M4 Final-Image Parity Remediation Is Accepted

Decision: ACCEPTED / OWNER_CANARY_AUTHORIZATION_PENDING
Date: 2026-09-02

VoiceBridge M4.1 feature-branch remediation installed the required runtime tooling and added CI validation of the final Docker image.

Exact validated evidence:

```text
VoiceBridge acceptance commit: 6a9491359795840ec9e79c9edc0ea82f595e9784
Validate run: 33577022166
krc-image-parity: SUCCESS
cloud: SUCCESS
browser-extension: SUCCESS
repository-docs: SUCCESS
```

The final image proves working `ffmpeg`, `ffprobe`, and `psql`, and passes a no-provider-call KRC managed-route startup smoke.

Therefore:

```text
M4_IMAGE_PARITY: PASS
M4_CANARY_PREREQUISITE_IMAGE_PARITY: PASS
M4_DEPLOYMENT: NOT_PERFORMED
M4_CANARY: NOT_RUN
```

Repository/CI readiness does not authorize an external deployment. A separate owner decision is mandatory before deployment or an owner-only canary.

Canonical checkpoint:

`71_M4_IMAGE_PARITY_READY_OWNER_CANARY_DECISION_CHECKPOINT_2026_09_02.md`

## D032 - M4 Bounded Owner-Only Canary Is Accepted and Rolled Back

Decision: ACCEPTED / ROLLBACK_COMPLETE / PERMANENT_PROMOTION_NOT_AUTHORIZED
Date: 2026-09-02

The owner explicitly authorized a bounded M4 owner-only canary against the isolated MEDIA BETA Render/Neon contour.

Exact execution evidence:

```text
VoiceBridge M4 target: 6a9491359795840ec9e79c9edc0ea82f595e9784
workflow run: 33580592224
result: SUCCESS
real STT route: public Telegram -> AssemblyAI universal-2
STT seconds: 53
retrieval credits: 0
provider cleanup: PASS
Neon durable readback: PASS
duplicate reuse: PASS
single STT reservation: PASS
invalid/private Telegram boundary: PASS
mandatory rollback: PASS
```

The isolated Render service was restored to exact pre-canary commit:

`2f0f02769dbdf2e8240e6b08867ecef2faaede16`

The one-shot canary workflow was removed after execution. No permanent backend promotion occurred.

Therefore:

```text
M4_OWNER_CANARY: PASS
M4_PERMANENT_BACKEND_PROMOTION: NOT_AUTHORIZED
R1 merge: HOLD
R2 backend promotion: HOLD
R3 external testers: HOLD
R4 public rollout: HOLD
```

The canary does not activate Gemini prerecorded, Hybrid C/D, or any automatic paid fallback.

Canonical checkpoint:

`72_M4_OWNER_CANARY_ACCEPTED_ROLLBACK_COMPLETE_CHECKPOINT_2026_09_02.md`

VoiceBridge authority:

`docs/history/2026-09-02_KRC_MEDIA_M4_OWNER_CANARY_ACCEPTANCE.md`

## D033 - Preserve the Existing Published KRC Identity; MEDIA Integration Uses a Separate Safety-Gated Update Sequence

Decision: APPROVED_PLAN / NOT_EXECUTED
Date: 2026-09-04

The owner confirmed the current product reality:

```text
KRC public GPT: already published and user-accessible
KRC MEDIA BETA GPT: owner-only / not separately published
```

The integration strategy must preserve the existing public KRC identity. Repository integration must not be treated as a GPT publication event, and the private MEDIA BETA GPT must never become a dependency required to use Core KRC.

Mandatory invariant:

```text
MEDIA unavailable/fails -> MEDIA operation fails closed or becomes unavailable
Core KRC              -> remains accessible and functional
```

The owner approved the following independent gate sequence:

```text
R0  Public KRC Update Safety Preflight
R1  Repository integration
R2  Permanent MEDIA backend promotion/readiness
R3  Update the existing published KRC GPT
R4  Post-update public-access + Core regression verification
```

### R0 is mandatory before R1-R3 execution

R0 must be no-live-change and must verify at execution time:

- the existing public KRC is still accessible;
- the same GPT identity is editable by the owner;
- an Update path for that existing published GPT is available;
- current sharing/publication state is recorded;
- current OpenAI requirements for updating a published GPT and public Actions are revalidated;
- required Privacy Policy URL/state is valid;
- current GPT configuration is captured sufficiently for rollback/reconstruction;
- public KRC URL/identity can be preserved.

If safe update of the same existing published GPT cannot be confirmed without creating/republishing a new GPT, STOP.

R1, R2, R3, and R4 remain separately authorized gates. Approval of repository integration does not authorize backend promotion or live GPT Update. Approval of backend readiness does not authorize live GPT Update.

Before R3 `Update`, Preview must prove both Core regression safety and MEDIA functionality, including a forced MEDIA failure where Core remains usable. The exact pre-update GPT configuration must be retained for rollback/reconstruction.

Immediately after any separately authorized R3 Update, R4 must verify the same public KRC identity/URL remains accessible and that Core works independently of MEDIA.

Detailed product plan:

`planning/PUBLIC_KRC_MEDIA_INTEGRATION_UPDATE_SAFETY_PLAN_2026_09_04.md`

VoiceBridge technical plan:

`kolemasakar/VoiceBridge` -> `docs/planning/2026-09-04_KRC_PUBLIC_GPT_MEDIA_INTEGRATION_SAFETY_PREFLIGHT.md`

This decision changes planning/governance only. It does not authorize or perform repository merge, permanent Render promotion, live GPT Update, new GPT publication, external tester expansion, public MEDIA rollout, Gemini prerecorded activation, Hybrid C/D implementation, or automatic paid fallback.

## D034 - Paid Cobalt Hosting Is Excluded; Migrate the Self-Hosted Cobalt Route to OCI Always Free

Decision: APPROVED / R2_REMEDIATION / R3_HOLD
Date: 2026-09-07

The R2 bounded Instagram canary correctly failed closed before STT, with zero retrieval credits and zero STT charges. Two Instagram retrieval-only diagnostics and an independent YouTube control reproduced an `HTTP 429` non-JSON response from the current Render Cobalt endpoint. The control response was `text/plain; charset=utf-8` with `server=cloudflare`, so the accepted blocker description is an edge-level non-JSON response before a usable Cobalt application JSON response.

The owner explicitly rejected paid hosting as a remediation path:

```text
Render paid instance: NOT CONSIDERED
paid Cobalt hosting: NOT CONSIDERED
paid retrieval fallback: FORBIDDEN
paid STT fallback: FORBIDDEN
paid proxy fallback: FORBIDDEN
FREE_TIER_ONLY: RETAINED
```

Approved remediation:

```text
self-hosted Cobalt -> migrate from Render Free path to OCI Always Free VM
VoiceBridge        -> remain on Render Free
Neon               -> unchanged
private MEDIA BETA -> unchanged
public KRC         -> unchanged
```

Execution constraints:

- OCI preflight must confirm an Always Free eligible resource before creation;
- no paid OCI resource may be created as part of this decision;
- Cobalt must remain API-key protected and exposed through HTTPS;
- no provider secret is placed in GPT instructions, Action schema, or chat;
- after OCI retrieval-only preflight PASS, only `KRC_MEDIA_COBALT_ENDPOINT` should change in VoiceBridge;
- Instagram must be re-canary-tested before Facebook;
- full R2 still requires Instagram, Facebook, Telegram, no-paid-fallback delta verification, and Core KRC isolation regression;
- R3 and R4 remain HOLD.

Canonical checkpoint:

`87_R2_INSTAGRAM_COBALT_EDGE_BLOCKER_OCI_FREE_MIGRATION_CHECKPOINT_2026_09_07.md`

## D035 - OCI Cobalt Local Secure Runtime and Instagram Retrieval Are Accepted; Public Cutover Remains Held

Decision: ACCEPTED_LOCAL_PREFLIGHT / PUBLIC_HTTPS_PENDING / LIVE_ENDPOINT_CUTOVER_NOT_AUTHORIZED / R3_HOLD
Date: 2026-09-08

The owner-approved free-only OCI remediation reached a working local runtime on a dedicated `VM.Standard.E2.1.Micro` instance selected as Always Free-eligible in the OCI console.

Accepted OCI runtime evidence:

```text
instance: krc-cobalt-media-beta
region: eu-frankfurt-1
public IPv4: 89.168.65.88
private IPv4: 10.0.0.26
Docker: 29.1.3
Docker Compose: 2.40.3
Cobalt image: ghcr.io/imputnet/cobalt@sha256:63186dd68afd57ce3bb1f62cc4c139f5fa95b9c3e87a3cf5c6e4c7a570523f62
Cobalt version: 11.7.1
Cobalt commit: a636575b09de1fc55d9b8cd98cac88f5f2f16b42
binding: 127.0.0.1:9000 only
```

The host was hardened for the current owner access path:

```text
SSH source 91.199.188.209/32 -> locally allowed
iptables persistence -> enabled
swap -> 2 GiB
```

Cobalt API-key protection is accepted:

```text
API_AUTH_REQUIRED=1
missing key -> error.api.auth.key.missing
valid key -> auth passes to normal URL validation
```

Authenticated local Instagram retrieval-only preflight against:

`https://www.instagram.com/reel/DEAyVa4SF3E/`

passed:

```text
POST -> HTTP 200
status -> tunnel
fresh tunnel download -> curl rc 0
retrieved bytes -> 214560
paid retrieval provider -> none
```

Therefore:

```text
OCI_COBALT_SECURE_LOCAL_RUNTIME: PASS
OCI_COBALT_INSTAGRAM_LOCAL_RETRIEVAL: PASS
```

A diagnostic OCI Cobalt YouTube control returned `error.api.youtube.login`. This does not revoke the accepted YouTube R2 route because YouTube remains Gemini direct. Before changing the Cobalt endpoint, regression evidence must confirm the Gemini-direct YouTube path is unaffected and no Cobalt fallback is introduced.

Public cutover remains held because the OCI Cobalt service is still local-only and `API_URL` still points to `http://127.0.0.1:9000/`.

DNS preparation passed:

```text
89-168-65-88.sslip.io -> 89.168.65.88
```

Required before live cutover:

```text
dedicated OCI NSG attached to krc-cobalt-vnic
required 80/443 OCI + local firewall ingress
HTTPS reverse proxy + public TLS
Cobalt API_URL -> public HTTPS base URL
external authenticated Instagram POST + tunnel verification
```

Port 9000 must remain loopback-only.

A local OCI API key was generated for preflight. The existing VoiceBridge `KRC_MEDIA_COBALT_API_KEY` value was not exposed and has not been proven identical. To preserve D034's intended single-variable live change, OCI should be aligned server-side to the existing VoiceBridge secret before cutover rather than exposing or rotating the secret through chat/GPT/repository documentation.

No live Render environment variable was changed. PR #45 remains open/draft/unmerged. Public KRC remains unchanged.

Canonical checkpoint:

`88_R2_OCI_COBALT_LOCAL_INSTAGRAM_RETRIEVAL_PASS_PUBLIC_HTTPS_PENDING_CHECKPOINT_2026_09_08.md`
