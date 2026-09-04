# K-Research & Critic / MEDIA BETA - R2-C Public Privacy and Render Promotion Readiness Checkpoint 80
Канонічний checkpoint завершення repository-side R2-C: підтверджено AssemblyAI Free evidence, підготовлено public MEDIA Privacy Policy та точний Render promotion/rollback plan без deployment.

Date: 2026-09-04
Status: R2-C_COMPLETE / R2_PROMOTION_READY_FOR_EXPLICIT_OWNER_AUTHORIZATION / NO_DEPLOYMENT

## 1. Scope and retained release gates

R2-C prepares the future public MEDIA backend for an explicit deployment decision. It does not perform that deployment.

No Render deployment, Render environment mutation, Neon mutation, VoiceBridge main merge, ChatGPT Builder Update, public MEDIA activation, provider-consuming canary, or public rollout occurred in this step.

R3 and R4 remain independently held.

## 2. Public MEDIA scope

Initial future public MEDIA support remains limited to supported public URLs from:

```text
youtube
telegram
instagram
facebook
```

Public local-file attachment support is not part of the initial public rollout unless separately reviewed and activated later.

Retained invariant:

```text
MEDIA unavailable/fails -> MEDIA unavailable/fails closed
Core KRC               -> remains usable
```

## 3. AssemblyAI Free account evidence

Owner-supplied AssemblyAI Dashboard/Billing screenshots dated 2026-09-04 show:

```text
Plan Details: Free
free credits spent: $1.68
free credits remaining: $48.32
Pay-as-you-go: not active in the shown Billing view
Upgrade Plan: separate explicit action
```

This closes the prior R2-B current-plan/current-balance evidence blocker.

No paid AssemblyAI continuation is authorized.

## 4. Post-AssemblyAI product decision

Owner decision on 2026-09-04:

```text
AssemblyAI Free remains the active KRC prerecorded STT provider while free credit remains.
After AssemblyAI Free credits are exhausted/effectively unavailable, target prerecorded provider = Gemini.
Automatic paid AssemblyAI continuation = forbidden.
```

Current VoiceBridge code still intentionally enforces:

```text
KRC_MEDIA_STT_PROVIDER=assemblyai
KRC prerecorded model=universal-2
Gemini prerecorded candidate=gemini-3.5-transcribe
Gemini prerecorded active for normal KRC jobs=NO
```

Therefore this product decision does not create an automatic runtime cutover today. The post-exhaustion Gemini route requires a separately validated provider-router implementation and activation before the trigger is reached.

## 5. Gemini Free privacy boundary

Current official Google Gemini API pricing reviewed on 2026-09-04 lists `gemini-3.5-transcribe` with a Free Tier and states that Free Tier content may be used to improve Google products.

Implication for future public KRC MEDIA:

```text
Gemini Free must not be silently activated for public-user media.
Before the first Gemini Free processing request, disclose the provider/data-use boundary.
Require explicit user consent.
No consent -> do not send media to Gemini / fail closed.
No paid Gemini fallback is authorized.
```

The existing Gemini prerecorded adapter uploads normalized audio to the Gemini Files API, calls `gemini-3.5-transcribe`, and attempts provider-file deletion. Provider deletion status must remain explicit and must never be fabricated.

## 6. Public Privacy Policy candidate

Repository document updated:

`docs/PRIVACY_POLICY.md`

Current candidate state:

```text
Version: 2.0-candidate
Status: PUBLIC_MEDIA_CANDIDATE / NOT_YET_ACTIVATED / FREE_TIER_ONLY
```

The policy now covers:

- initial public YouTube/Telegram/Instagram/Facebook scope;
- public-only source boundary;
- anonymous/shared public GPT Action admission;
- secret/credential handling;
- Supadata Free-only route;
- Facebook Cobalt free retrieval and no ScrapeCreators fallback;
- Telegram public-web retrieval and no account/session/bot-token requirement;
- AssemblyAI Free-only use and no paid continuation;
- future Gemini Free disclosure/consent requirement;
- project-side retention and cleanup boundaries;
- provider-side data handling;
- Core/MEDIA failure isolation;
- OpenAI public Action Privacy Policy requirement.

Updating the repository Privacy Policy does not itself activate the Action in the public GPT. That remains an R3 Builder change.

## 7. VoiceBridge R2-C candidate

Repository:

`kolemasakar/VoiceBridge`

Branch:

`agent/krc-media-gemini-migration`

Current R2-C head:

`3a00d67bac0883a55f0f9c5eacf16e11acae85fe`

Canonical Validate:

`33894722818 / SUCCESS`

R2-C planning file:

`docs/planning/2026-09-04_KRC_MEDIA_R2C_PUBLIC_PRIVACY_RENDER_PROMOTION_PLAN.md`

PR #45:

`OPEN / DRAFT / UNMERGED / mergeable=true`

PR #45 was not merged in R2-C.

## 8. Authenticated Render baseline

Workspace:

`tea-d9dsqdjrjlhs73ba1ga0`

MEDIA service:

```text
name: voicebridge-krc-media-beta-kolemasakar
service id: srv-da1kic5bedkc73d6fk60
url: https://voicebridge-krc-media-beta-kolemasakar.onrender.com
region: frankfurt
runtime: docker
plan: free
rootDir: src/cloud
healthCheckPath: /api/v1/health
autoDeploy: no
configured branch: agent/krc-media-transcript
```

Current live deployment:

```text
deploy id: dep-dabnvs3tqb8s73d1c68g
commit: 2f0f02769dbdf2e8240e6b08867ecef2faaede16
status: live
```

Known M4 canary:

```text
commit: 6a9491359795840ec9e79c9edc0ea82f595e9784
status: deactivated
rollback to 2f0f027...: previously confirmed
```

The configured Render branch currently points to a different branch head than the known-good live commit. Therefore a generic branch-head deployment must not be treated as an exact rollback mechanism.

Git comparison also shows that live commit `2f0f027...` and the current migration candidate are diverged. Exact commit identity is mandatory for promotion and rollback evidence.

## 9. Exact promotion/rollback plan

The R2-C VoiceBridge plan defines the deployment sequence but does not execute it.

Required pre-deploy freeze:

```text
re-read Render live deploy id/commit
re-read VoiceBridge candidate head and Validate result
re-read Neon connectivity/schema state
re-read Supadata Free plan/credits
re-read AssemblyAI Free plan/balance
re-read Cobalt health
```

Required public-mode configuration review:

```text
KRC_MEDIA_PUBLIC_MODE=true
KRC_MEDIA_FREE_TIER_ONLY=true
KRC_MEDIA_ASSEMBLYAI_FREE_TRIAL_ONLY=true
KRC_MEDIA_STT_PROVIDER=assemblyai
KRC_MEDIA_TRANSCRIBE_MODEL=gemini-3.5-transcribe
MEDIA_DAILY_STT_SECONDS<=7200
MEDIA_MAX_CONCURRENT_JOBS=1
RATE_LIMIT_REQUESTS_PER_MINUTE<=60
SCRAPECREATORS_API_KEY absent
```

Secrets remain server-side and must not be copied to repository documentation or user output.

Exact deployment candidate for this checkpoint:

`3a00d67bac0883a55f0f9c5eacf16e11acae85fe`

Exact rollback target:

`2f0f02769dbdf2e8240e6b08867ecef2faaede16`

After candidate deployment and before R3, a bounded owner/operator canary must verify health, auth, all four platform paths, fail-closed provider/quota behavior, durable state, no paid fallback, no secret/transcript leakage, and Core health after MEDIA failure injection.

Any public admission bypass, paid-provider path, Core regression, secret leakage, unbounded retry/provider consumption, durable-state corruption, or health instability requires rollback.

## 10. R2-C disposition

```text
AssemblyAI current Free plan/balance evidence  PASS
public Privacy Policy candidate                PREPARED
VoiceBridge R2-C plan                          PREPARED
VoiceBridge R2-C Validate                      PASS
Render live baseline                           VERIFIED
exact candidate/rollback identities            RECORDED
post-AssemblyAI Gemini target                  RECORDED
Gemini automatic fallback implementation       NOT IMPLEMENTED
Render deployment                              NOT PERFORMED
ChatGPT Builder update                         NOT PERFORMED
```

## 11. Gate state

```text
R0   PASS
R1   COMPLETE
R2-A PASS
R2-B PASS
R2-C COMPLETE
R2   PROMOTION READY FOR EXPLICIT OWNER AUTHORIZATION / NOT PROMOTED
R3   HOLD
R4   HOLD
```

## 12. Next owner gate

The next state-changing step is the actual bounded R2 permanent backend promotion/canary using the exact candidate and rollback plan above.

That step requires fresh explicit owner authorization.

R3 must not be inferred from R2 authorization. A successful R2 deployment/canary still requires a separate owner decision before updating the existing published K-Research & Critic GPT.
