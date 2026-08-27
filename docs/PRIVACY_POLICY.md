# PRIVACY_POLICY
Політика конфіденційності поточного приватного K-Research & Critic MEDIA BETA.

Version: 1.0
Status: PRIVATE_OWNER_ONLY / RELEASE_HOLD_OWNER_TESTING
Updated: 2026-08-27

## 1. Scope

This policy describes the isolated `K-Research & Critic - MEDIA BETA` media-ingestion Action. It does not change the normal public text-research Core.

Current media beta is owner-only. External tester onboarding and public/Store rollout are paused.

## 2. Supported Input Classes

The private beta may process:
- a supported public YouTube URL;
- a supported public Instagram Reel URL;
- a supported public Facebook Video/Reel URL;
- a supported public Telegram post containing video;
- one local audio/video file attached in the current ChatGPT conversation.

Remote platform adapters do not support private, account-gated, friends-only, or session-dependent content. Users are not asked for platform credentials, cookies, or sessions.

## 3. Data Flow

### YouTube / Instagram

The private Action may send the public source URL and language/options required by the managed transcript provider. Billable provider operations are consent-gated.

### Facebook

The backend attempts free Cobalt retrieval. AssemblyAI STT is invoked only after successful media retrieval. If Cobalt cannot retrieve the public media, processing stops as unavailable. ScrapeCreators is not active or offerable in the current flow.

### Telegram

The backend uses the public Telegram web/embed surface and follows only accepted trusted Telegram media delivery. Retrieved media may be sent to AssemblyAI for STT. No Telegram account/session/cookies/bot token or paid retrieval fallback is used.

### Local attachment

ChatGPT supplies a temporary `openaiFileIdRefs` runtime object for the current-conversation attachment. The backend accepts only trusted OpenAI HTTPS media delivery, validates type/size/duration, downloads/normalizes media within bounded limits, and sends the normalized speech content to AssemblyAI when required. File IDs and signed URLs are not exposed to the normal user response.

## 4. Data Categories

Depending on route, processing may include:
- public source URL;
- temporary media bytes;
- attachment metadata required for safe validation;
- transcript text and timestamped segments;
- detected/source language and confidence metadata;
- provider/retrieval mode metadata;
- duration, segment count, quota, and credit accounting metadata;
- internal technical job identifiers.

Unrelated ChatGPT conversation content must not be sent to the media backend.

## 5. Authentication and Credentials

The private GPT Action uses a server-to-server bearer secret. Owner admission and provider credentials are server-side.

The owner must not be asked for:

```text
Action bearer
owner beta admission code
provider API key
platform login/password
cookies/session tokens
OpenAI file ID
signed attachment URL
KRCM Job ID
```

Reusable credentials must not be stored in reports or KRC checkpoints.

## 6. Data Minimization

Only data required to acquire a transcript and preserve source traceability should be processed.

Current controls include:
- public-only remote adapters;
- one local attachment per current request;
- local attachment maximum 32 MiB;
- bounded media processing;
- temporary source-media handling rather than intentional durable source-file retention;
- no full transcript in KRC checkpoint artifacts.

## 7. Durable Backend State

Managed `KRCM_` job state and transcript segments are stored in the isolated durable backend store so accepted jobs can survive process replacement and duplicate requests can be handled safely where defined.

Operational metadata needed for quota/credit/idempotency control may also be retained according to the isolated beta implementation.

The private GPT does not expose internal KRCM Job IDs in normal user-facing output.

## 8. Speech-to-Text Provider Handling

AssemblyAI is used on accepted routes that require STT after successful/safe media acquisition. Provider-side delete requests are performed where implemented by the accepted backend path, and deletion must not be claimed when it cannot be confirmed.

Provider privacy, retention, data-use, regional-routing, and model-training terms can change. They must be re-verified before any future external/public release. This document does not treat an older provider statement as a permanent public-release waiver.

## 9. Managed Transcript Provider Handling

YouTube/Instagram managed transcript operations may use Supadata under the current private package. Billable operations remain explicit-consent gated. User credentials for the provider are not required.

## 10. Browser Helper Boundary

The A8 browser Helper is historical accepted fallback evidence only and is not normal owner UX in the current zero-client MEDIA BETA. The current Builder must not ask the owner to install/use the Helper for normal supported inputs.

## 11. Evidence Boundary

Transcript text is evidence of what the media said. It is not independent evidence that a factual claim is true. Independent web/source verification starts only after CriticProfile approval.

## 12. Current Resource Controls

Current accepted controls include:
- maximum media duration governed by the private media package;
- local attachment maximum 32 MiB;
- bounded STT/quota accounting in the isolated backend;
- zero retrieval credits for Telegram public retrieval and local attachment transport;
- no active paid Facebook or Telegram retrieval fallback;
- no automatic retry of uncertain-charge provider operations.

## 13. Security

- developer/provider secrets must not be committed or shown to users;
- Action authentication is checked before protected media operations;
- arbitrary external attachment URLs are rejected;
- trusted-host and redirect boundaries are enforced by the backend;
- remote source authentication/session import is not supported;
- source-media failures must not be converted into fabricated transcripts.

## 14. Release Hold

Current decision:

```text
private owner testing continues
merge to main = HOLD
production promotion = HOLD
external testers = HOLD
public/Store rollout = HOLD
```

Before any later external/public transition, re-review this policy against the then-current implementation, provider terms, retention behavior, access controls, resource limits, monitoring, and applicable OpenAI Action/Store requirements.

## 15. Contact

Project/privacy questions may be raised with the repository owner through `kolemasakar/K_Research_Critic`.
