# K-Research & Critic - MEDIA BETA Checkpoint 72

Date: 2026-09-02
Status: M4_OWNER_CANARY_ACCEPTED / ROLLBACK_COMPLETE / RELEASE_HOLD_OWNER_TESTING

## Product boundary

`K-Research & Critic - MEDIA BETA` remains the closed-beta media module of the published `K-Research & Critic` product.

Product and roadmap authority remains `kolemasakar/K_Research_Critic`. VoiceBridge remains the technology/backend implementation and validation source.

Public Core behavior is unchanged.

## Current provider boundary

```text
KRC prerecorded active provider: AssemblyAI universal-2
Gemini prerecorded normal activation: FALSE
provider cutover: NOT AUTHORIZED
future Hybrid C/D: PLANNED / NOT IMPLEMENTED
Hybrid C/D trigger: AssemblyAI free credits exhausted plus fresh owner decision
```

M3 remains CLOSED. The seven-case provider evidence did not establish a global winner and does not authorize a current provider cutover.

## M4 progression

Checkpoint 70 identified missing final-image `ffmpeg`/`ffprobe` and `psql` as deployment blockers.

Checkpoint 71 recorded successful M4.1 image-parity remediation and stopped at the owner deployment/canary gate.

The owner then explicitly authorized a bounded owner-only canary.

## Exact M4 owner-only canary

VoiceBridge M4 target:

`6a9491359795840ec9e79c9edc0ea82f595e9784`

Isolated Render service:

`voicebridge-krc-media-beta-kolemasakar`

Pre-canary live/rollback commit:

`2f0f02769dbdf2e8240e6b08867ecef2faaede16`

GitHub Actions run:

`33580592224`

Job:

`100093850490`

Result:

`SUCCESS`

## Pre-deploy evidence

Before deployment the bounded workflow verified:

```text
isolated Render service identity                PASS
isolated branch boundary                        PASS
exact rollback target                           CAPTURED
required Render KRC env presence                PASS
Render/Neon database URL identity               PASS
KRC prerecorded selector                        ASSEMBLYAI/default
ScrapeCreators paid route                       INACTIVE
Cobalt transport reachability                   PASS / no media retrieval
Neon connectivity/schema                        PASS
active nonterminal KRC jobs                     0
```

No secret values are stored in this checkpoint.

## Live target acceptance

Temporary canary deploy:

`dep-dabnveqjnfac73dnkgbg`

Exact M4 target reached live state and passed:

```text
health                                           PASS
owner authentication boundary                    PASS
managed capability                               PASS
durable_store                                    postgres
restart_resilient_jobs                           true
Facebook free provider                           cobalt / configured
Facebook paid provider                           unconfigured
Facebook automatic paid retrieval                false
Telegram public retrieval                        true / zero retrieval credits
Telegram STT                                     assemblyai / configured
local attachment transport                       true
local attachment transcription                   true / assemblyai
owner admission injection                        true
```

The no-provider health/capability checks caused no durable Neon job or STT-charge mutation.

## One real STT canary

Previously accepted Telegram fixture:

`https://t.me/techcrimes/12107`

KRCM job:

`KRCM_8c0f6a9e-b3c9-4c9a-8978-69d6c5acc535`

Observed result:

```text
status                                           COMPLETED
provider                                         assemblyai
provider_mode                                    telegram_public_retrieval_stt
retrieval_provider                               telegram_public_web
retrieval_credits_charged                        0
managed credits_charged                          0
stt_seconds_charged                              53
segment_count                                    1
transcript_characters                            769
provider_data_deleted                            true
```

Transcript text is not stored in product checkpoints.

Durable readback and segment readback passed. Repeating the same request returned the same job with `reused=true`. Neon contained exactly one job row and one STT reservation row for the canary job, proving that the duplicate did not create another provider reservation.

The invalid/private Telegram boundary also returned the expected `INVALID_REQUEST` behavior without a provider call.

## Mandatory rollback

Rollback deploy:

`dep-dabnvs3tqb8s73d1c68g`

Restored commit:

`2f0f02769dbdf2e8240e6b08867ecef2faaede16`

Result:

```text
rollback deploy                                  PASS
restored exact commit                            PASS
post-rollback health                             PASS
runner temporary secret material cleanup         PASS
```

The temporary one-shot canary workflow was removed after execution.

VoiceBridge immutable evidence:

`docs/history/2026-09-02_KRC_MEDIA_M4_OWNER_CANARY_ACCEPTANCE.md`

## Current state

```text
M3                                              CLOSED
M4_PREFLIGHT                                     COMPLETE
M4_IMAGE_PARITY                                  PASS
M4_OWNER_CANARY                                  PASS
M4_REAL_STT                                      PASS
M4_DURABILITY                                    PASS
M4_IDEMPOTENCY                                   PASS
M4_PROVIDER_CLEANUP                              PASS
M4_ROLLBACK                                      PASS
M4_PERMANENT_BACKEND_PROMOTION                  NOT AUTHORIZED
```

## Release gates

The owner-only canary is evidence, not a release authorization.

```text
R1 merge selected MEDIA BETA work toward main    HOLD
R2 backend/production promotion                  HOLD
R3 external testers                              HOLD
R4 public rollout                                HOLD
```

No KRC Builder Action URL change, public rollout, external tester onboarding, Gemini prerecorded activation, Hybrid C/D activation, or automatic paid fallback is authorized by this checkpoint.

## Exact continuation point

`OWNER DECISION: M4 POST-CANARY / R1-R2 REMAIN SEPARATE GATES`

Before any permanent backend promotion, reverify current VoiceBridge head/CI, Render live baseline, rollback target, environment state, Neon connectivity, and release scope.
