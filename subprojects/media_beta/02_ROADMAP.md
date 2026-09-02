# MEDIA BETA Roadmap
Поточний roadmap приватного K-Research & Critic MEDIA BETA.

Version: 4.2
Status: RELEASE_HOLD_OWNER_TESTING / M3_CLOSED / M4_PREFLIGHT_BLOCKED
Updated: 2026-09-02

## Product position

`K-Research & Critic - MEDIA BETA` is a closed-beta module of the published `K-Research & Critic` product.

```text
product/roadmap authority: kolemasakar/K_Research_Critic
public Core: main
closed-beta product branch: agent/video-url-research
technology/backend implementation source: kolemasakar/VoiceBridge
KRC media migration branch: agent/krc-media-gemini-migration
```

VoiceBridge supplies technology, implementation, and validation evidence. It does not independently authorize KRC product release gates.

## Accepted runtime baseline

```text
A8 browser-assisted owner baseline          COMPLETE / FALLBACK_ONLY
A9 owner zero-client media input            COMPLETE / ACCEPTED
A9.10 local attachment                      COMPLETE / ACCEPTED
A10 copy-safe claim-summary stabilization   COMPLETE / ACCEPTED
Builder package                              0.9.1-beta-a10
Action schema                                0.6.0-a9.10
release state                                RELEASE_HOLD_OWNER_TESTING
```

Accepted policy remains unchanged:

```text
Facebook Cobalt failure -> unavailable
NO automatic paid fallback
ScrapeCreators reserve only / inactive
Telegram public-only / zero retrieval credits
local attachment max 32 MiB / zero retrieval credits
```

## Provider boundary

```text
VoiceBridge live default: Gemini gemini-3.5-transcribe-live
KRC prerecorded active provider: AssemblyAI universal-2
Gemini prerecorded candidate: gemini-3.5-transcribe
Gemini normal prerecorded activation: FALSE
provider cutover now: FALSE
```

## M3 - Provider evidence

Status: CLOSED.

```text
M0 migration preflight                         COMPLETE
M1 provider abstraction                        PASS
M2 Gemini prerecorded adapter                  PASS / INACTIVE
M3 offline evaluator                           PASS
M3 first clean-public reference review         COMPLETE 3/3
M3 first provider A/B                          COMPLETE 3/3 x 2
M3B expanded corpus byte acceptance            COMPLETE 4/4
M3B independent reference review               COMPLETE 4/4
M3B second provider A/B                        COMPLETE 4/4 x 2
M3 manual factual/hallucination review          COMPLETE
M3 closure                                      CLOSED / RETAIN_ASSEMBLYAI_CURRENT_PROVIDER
```

Seven-case synthesis:

```text
reviewed reference tokens: 117
AssemblyAI lexical WER: 13.68%
Gemini lexical WER: 14.53%
SEVEN_CASE_GLOBAL_WINNER: NOT_ESTABLISHED
```

The evidence does not justify a current provider cutover.

## Deferred free-first Hybrid C/D

Status: PLANNED / NOT_IMPLEMENTED.

D029 records the future architecture to be reconsidered only after AssemblyAI free credits are exhausted:

```text
Gemini Transcribe Live -> preferred free route for eligible jobs
Gemini unary Transcribe -> timestamps/diarization feature route when free quota permits
AssemblyAI universal-2 -> retained rollback/fallback; billable use disabled by default
```

Detailed plan:

`69_POST_ASSEMBLYAI_FREE_CREDITS_HYBRID_STT_PLAN_2026_09_02.md`

No implementation is authorized before the trigger and a fresh owner decision.

## M4 - New-infrastructure readiness

Status: PREFLIGHT_COMPLETE / CANARY_BLOCKED_ON_IMAGE_PARITY.

Repository-only preflight against the VoiceBridge KRC migration branch found:

```text
shared server mounts KRC managed routes        PASS_STATIC
KRC configuration/env surface                  PASS_STATIC
Node 24 runtime contract                       PASS_STATIC
Facebook Cobalt HTTP transport                 PASS_STATIC
Telegram public route                          PASS_STATIC
ffmpeg/ffprobe in final runtime image           FAIL / MISSING
psql in final runtime image                     FAIL / MISSING
```

Why these are hard blockers:

- accepted local attachment processing spawns `ffmpeg` and `ffprobe`;
- durable KRC PostgreSQL/Neon persistence spawns `psql`;
- the current `node:24-alpine` runtime Docker stage installs only Node production dependencies.

VoiceBridge evidence:

`docs/history/2026-09-02_KRC_MEDIA_M4_DEPLOYMENT_IMAGE_PARITY_PREFLIGHT.md`

### M4 next engineering step

```text
M4.1 image parity remediation
 -> add minimum final-image packages for ffmpeg/ffprobe + psql
 -> add CI final-image command validation
 -> add no-provider-call KRC startup smoke
 -> full VoiceBridge validation
 -> STOP at owner deployment/canary authorization gate
```

No deployment or canary is authorized by repository readiness work.

## M5 - Provider/new-infrastructure cutover

Status: NOT_AUTHORIZED.

M5 remains separate from both the current M4 infrastructure work and the deferred post-credit Hybrid C/D plan.

## Release hold

```text
R1 merge selected MEDIA BETA work toward main   HOLD
R2 backend/production promotion                 HOLD
R3 external testers                             HOLD
R4 public sharing / Store rollout               HOLD
```

## Current checkpoint

`70_M3_CLOSED_M4_PREFLIGHT_BLOCKED_CHECKPOINT_2026_09_02.md`

## Exact continuation point

```text
M4.1 VOICEBRIDGE IMAGE-PARITY REMEDIATION / NO DEPLOYMENT
```
