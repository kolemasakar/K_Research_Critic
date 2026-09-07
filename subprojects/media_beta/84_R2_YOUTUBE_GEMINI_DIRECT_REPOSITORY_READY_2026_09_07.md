# K-Research & Critic / MEDIA BETA - R2 YouTube Gemini Direct Repository-Ready Checkpoint 84

Канонічна точка відновлення після R2 pivot з self-hosted Cobalt YouTube retrieval на consent-gated Gemini Developer API Free Tier direct YouTube URL processing.

Date: 2026-09-07
Status: R2_REPOSITORY_PIVOT_READY / YOUTUBE_GEMINI_DIRECT / LIVE_DEPLOYMENT_AND_AUTHENTICATED_CANARY_PENDING / R3_HOLD

## Scope

This checkpoint supersedes checkpoint 83 as the canonical repository recovery point.

It records the repository-only R2 architecture pivot approved by the owner after live Cobalt YouTube canaries demonstrated a datacenter anti-bot/login blocker. No new Gemini live deployment, no Neon mutation, no GPT Builder change, no public KRC change, and no PR merge were performed while implementing this checkpoint.

Critical invariant:

```text
MEDIA unavailable/fails -> MEDIA unavailable/fails closed
Core KRC               -> remains user-accessible and functional
```

## Cobalt YouTube canary evidence that caused the pivot

The self-hosted Cobalt service remained healthy and authenticated. The Cobalt API key was initially scoped only to Facebook, which caused the first bounded YouTube diagnostic to return:

```text
HTTP 400
error.api.service.disabled
```

The owner updated the Cobalt key policy to allow:

```text
facebook
youtube
instagram
```

After the Cobalt restart, a fresh YouTube job was created after the policy change and still failed before STT. A sanitized VoiceBridge diagnostic using the configured Cobalt API key then returned:

```text
HTTP 400
provider_status: error
provider_error_code: error.api.youtube.login
```

Cobalt 11.7.1 maps this state to YouTube `LOGIN_REQUIRED` / bot-check behavior. This established that a zero-cookie, zero-login, self-hosted Cobalt path from the current Render datacenter cannot be treated as a dependable public YouTube route under the accepted free-only policy.

The fresh post-policy canary job was:

```text
job_id: KRCM_3972b99f-f839-4bfb-b158-f69b2d216801
source: https://www.youtube.com/watch?v=5i-4Pk5Idb4
created_at: 2026-09-07T16:43:18.517Z
provider_mode: cobalt_retrieval_stt
retrieval_provider: cobalt
status: FAILED
retrieval_credits_charged: 0
stt_seconds_charged: 0
```

No AssemblyAI STT work and no paid fallback were triggered by these failed YouTube retrieval attempts.

## Accepted public routing pivot

The owner explicitly approved option 1: repository-only implementation of direct Gemini YouTube processing with an explicit Free Tier data-use consent gate.

Target public routing is now:

```text
YouTube   -> Gemini Developer API Free Tier direct public URL -> durable KRCM/Neon
Instagram -> self-hosted Cobalt -> AssemblyAI universal-2 Free -> durable KRCM/Neon
Facebook  -> self-hosted Cobalt -> AssemblyAI universal-2 Free -> durable KRCM/Neon
Telegram  -> public Telegram web -> AssemblyAI universal-2 Free -> durable KRCM/Neon
```

The YouTube route explicitly forbids:

```text
Cobalt automatic fallback
AssemblyAI automatic fallback
Supadata fallback
user cookies
YouTube login/session data
paid proxy fallback
paid Gemini fallback
```

Supadata remains historical/private compatibility code only and is inactive in the public candidate.

## Gemini Free consent boundary

Google Gemini Free Tier has a materially different data-use boundary. Therefore a direct YouTube request has two stages:

```text
preflight / durable lookup
    -> no Gemini provider submission

new Gemini provider submission
    -> clear disclosure
    -> explicit user consent required
    -> only then send public YouTube URL to Gemini
```

Required consent payload:

```json
{
  "gemini_free_consent": {
    "provider": "google_gemini",
    "tier": "free",
    "data_use_acknowledged": true
  }
}
```

No consent -> `GEMINI_FREE_CONSENT_REQUIRED` -> fail closed before provider work.

The disclosure states that content sent through Gemini Developer API Free Tier may be used by Google to improve Google products.

This is the only provider-specific confirmation required for the YouTube route. A generic MEDIA-start confirmation must not be added before or after it. The later CriticProfile approval remains a separate research-control gate.

## VoiceBridge repository candidate

Repository:

`kolemasakar/VoiceBridge`

```text
branch: agent/krc-media-gemini-migration
candidate head: bae3db8e646baf003689c1d8a8e502d9d2ad832d
Validate: 34146243530 / SUCCESS
PR #45: OPEN / DRAFT / UNMERGED
```

Implementation adds:

```text
src/cloud/src/public_gemini_youtube.ts
src/cloud/tests/public_gemini_youtube.test.ts
```

and registers the handler before the legacy public Cobalt handler in `managed_server.ts`.

New repository route surface:

```text
GET  /api/v1/media/public-capabilities
POST /api/v1/media/youtube-gemini/preflight
POST /api/v1/media/youtube-gemini/lookup
POST /api/v1/media/youtube-gemini/transcriptions
GET  /api/v1/media/youtube-gemini/transcriptions/{job_id}
GET  /api/v1/media/youtube-gemini/transcriptions/{job_id}/segments
```

Implementation properties validated by tests:

```text
public YouTube URL is sent directly to Gemini
x-goog-api-key is used server-side
no user Authorization or Cookie header is added
explicit Free Tier data-use consent is required before provider work
no provider call occurs without consent
provider_mode=youtube_gemini_direct
retrieval_provider=gemini_youtube_url
retrieval_credits_charged=0
stt_seconds_charged=0
duplicate start reuses durable job
provider failure -> fail closed
no Cobalt/AssemblyAI/paid fallback for YouTube
```

The temporary Cobalt startup diagnostic code used to isolate the live blocker was removed from the repository candidate before the final VoiceBridge validation. `34146243530` passed `cloud`, `krc-image-parity`, `repository-docs`, and `browser-extension`.

## KRC public Action candidate

New mixed free-only Action schema:

```text
path: gpt_store/actions/media_public_free_openapi.yaml
version: 0.8.0-r2-gemini-youtube
release state: R2_REPOSITORY_CANDIDATE_NOT_PUBLICLY_ACTIVATED
```

It exposes YouTube only through the dedicated Gemini routes and keeps Instagram, Facebook, and Telegram on their accepted free-only routes.

The previous Cobalt public candidate remains in the repository as historical R2 evidence:

```text
gpt_store/actions/media_public_cobalt_openapi.yaml
version: 0.7.0-r2-cobalt
```

The private historical MEDIA BETA contract also remains preserved:

```text
gpt_store/actions/media_managed_beta_openapi.yaml
version: 0.6.0-a9.10
```

New KRC schema regression:

`tests/test_krc_media_public_gemini_youtube_action_schema.py`

It verifies the dedicated Gemini YouTube route, required explicit consent payload, zero paid fallbacks, mixed platform routing, and inline GPT Builder `job_id` parameters.

## Private R2 canary Builder package

Repository-only canary package:

```text
instructions: prompts/GPT_STORE_MEDIA_R2_GEMINI_YOUTUBE_CANARY_INSTRUCTIONS.md
manifest: gpt_store/media_r2_gemini_youtube_canary_manifest.yaml
builder_runtime_applied: false
```

The package requires one Gemini Free disclosure/consent decision for new YouTube provider work and explicitly removes the old duplicate MEDIA-start/Supadata credit confirmation behavior.

The private `K-Research & Critic - MEDIA BETA` Builder has NOT yet been switched to this package. The public `K-Research & Critic` GPT remains unchanged.

## Privacy candidate

`docs/PRIVACY_POLICY.md` is updated to `2.2-candidate` and now records:

- YouTube direct Gemini Free routing;
- explicit pre-provider consent;
- Google Free Tier data-use disclosure;
- no Cobalt/AssemblyAI/cookie/login/paid-proxy fallback on YouTube;
- Instagram/Facebook Cobalt -> AssemblyAI Free;
- Telegram public web -> AssemblyAI Free;
- no paid Gemini or AssemblyAI continuation.

The policy remains a repository candidate and does not itself activate a public Action.

## Current live backend baseline

Repository-only pivot means live Render was not changed to the Gemini-direct candidate in this step.

Last confirmed stable VoiceBridge live state before this checkpoint:

```text
service: voicebridge-krc-media-beta-kolemasakar
service id: srv-da1kic5bedkc73d6fk60
live commit: 52499e4959aa2673f07239c73054cdbeaec0eeac
latest confirmed normal-mode deploy: dep-dafekmid0e5s73c3sg10
status: LIVE
Cobalt diagnostic flag: false
```

The live code still routes the public YouTube managed path through Cobalt and therefore does not satisfy the new Gemini-direct target.

Immediate pre-pivot live rollback/baseline:

`52499e4959aa2673f07239c73054cdbeaec0eeac`

Earlier rollback points remain:

```text
7c8806713ea75b0809b638f102e31d8d3af86150
2f0f02769dbdf2e8240e6b08867ecef2faaede16
```

## Release gate state

```text
R0   PASS
R1   COMPLETE
R2-A PASS
R2-B PASS
R2-C COMPLETE
R2   REPOSITORY PIVOT READY / LIVE GEMINI DEPLOYMENT + AUTHENTICATED CANARY PENDING
R3   HOLD
R4   HOLD
```

R2 must not be marked complete until the exact accepted VoiceBridge candidate is deployed with the Gemini Free-only guard, the private canary Builder package is applied, bounded authenticated canaries pass for YouTube/Instagram/Facebook/Telegram, and Core isolation is reverified.

R3 remains a separate owner gate. No public GPT Builder update is authorized by this checkpoint.

## Recovery instruction

Recovery must start from checkpoint 84 and then re-read:

1. `docs/KRC_MEDIA_BETA_RECOVERY_POINTER.md`;
2. `gpt_store/actions/media_public_free_openapi.yaml`;
3. `prompts/GPT_STORE_MEDIA_R2_GEMINI_YOUTUBE_CANARY_INSTRUCTIONS.md`;
4. `gpt_store/media_r2_gemini_youtube_canary_manifest.yaml`;
5. `docs/PRIVACY_POLICY.md`;
6. VoiceBridge branch `agent/krc-media-gemini-migration` exact head and Validate state;
7. current Render live deployment for `srv-da1kic5bedkc73d6fk60`;
8. VoiceBridge PR #45 state;
9. current private and public GPT Builder states before any activation.

Do not deploy/mutate Render or Neon, merge PR #45, apply the private Builder package, or update the public GPT without the applicable explicit owner authorization.
