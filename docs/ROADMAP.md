# ROADMAP
План завершеного Core та поточного ізольованого MEDIA BETA розширення.

Version: 1.9
Status: CORE_MAINTENANCE / MEDIA_BETA_RELEASE_HOLD / M3_ACTIVE
Updated: 2026-09-01

## 1. Core Product

The K-Research & Critic public Core development roadmap is complete through Phase 12 and remains in maintenance.

```text
Phase 0-10                                     COMPLETE
Post-MVP Hybrid Domain Resolver               COMPLETE
Phase 11 Configuration/Cost/Quality Controls  COMPLETE
Phase 12 Test and CI Hardening                COMPLETE
GPT Store Core publication                    COMPLETE
Core production smoke test                    PASS
Release baseline                              v1.0.0
Repository Core mode                          MAINTENANCE
```

The public Core workflow remains the stable production baseline.

## 2. Stable Core Invariants

- mandatory CriticProfile approval;
- frozen approved profile unless a material amendment is re-approved;
- Research/Critic separation and bounded revision;
- explicit evidence, limitations, and final status;
- no hidden chain-of-thought persistence;
- no mandatory external backend for public text Core;
- no general modular-agent-platform expansion in this repository.

## 3. Additive MEDIA BETA Workstream

`K-Research & Critic - MEDIA BETA` is a closed-beta module of the published `K-Research & Critic` product. The KRC repository remains the product and roadmap authority. VoiceBridge supplies media/backend technology, implementation, and validation evidence.

```text
A4-A8 browser-assisted baseline                 HISTORICAL / ACCEPTED FALLBACK
A9 owner zero-client media input                ACCEPTED
A9 YouTube                                      ACCEPTED
A9 Instagram Reel                               ACCEPTED
A9 Facebook free Cobalt path                    ACCEPTED
A9 Facebook Cobalt-failure policy               ACCEPTED
A9.9 public Telegram                            ACCEPTED
A9.10 local attachment                          ACCEPTED
A10 copy-safe claim-summary stabilization       ACCEPTED
```

Accepted owner-only input set:

```text
YouTube
Instagram Reel
Facebook Video/Reel
supported public Telegram video post
one local audio/video attachment
```

## 4. Active Provider-Evidence Track

The currently active technical track is the KRC prerecorded STT forward migration implemented and validated in VoiceBridge branch `agent/krc-media-gemini-migration`.

```text
M0 migration preflight                         COMPLETE
M1 provider abstraction                        PASS
M2 Gemini prerecorded adapter                  PASS / INACTIVE
M3 offline evaluator/contracts/preparation     PASS
first public corpus source tranche             LOCKED
REAL_ASSET_BYTES_CAPTURED                      FALSE
READY_FOR_AB                                   FALSE
M3_LIVE_AB                                     NOT_RUN
CURRENT                                        M3 BYTE CAPTURE + SHA-256
M4 canary                                      NOT_STARTED
M5 cutover                                     NOT_AUTHORIZED
```

Current M3 transition:

```text
SOURCE_LOCKED_PENDING_BYTE_CAPTURE
 -> exact media byte capture
 -> byte-exact asset SHA-256
 -> temporary raw media deletion / no raw-media CI artifact
 -> independent reference transcript preparation and review
 -> reference transcript SHA-256
 -> READY_FOR_AB
 -> same-asset AssemblyAI vs Gemini A/B
 -> manual factual/hallucination review
```

The byte-capture step is evidence preparation only and must not itself invoke AssemblyAI or Gemini.

## 5. Current Work Mode

Current state:

```text
RELEASE_HOLD_OWNER_TESTING
```

The owner has chosen to continue private testing before deciding on release. Defects found during this period are fixed and revalidated only in isolated beta/technology branches unless the owner explicitly changes the release decision.

Canonical release checkpoint:

```text
subprojects/media_beta/53_RELEASE_HOLD_OWNER_TESTING_CHECKPOINT.md
```

Canonical current engineering overlay:

```text
subprojects/media_beta/60_PROJECT_DOCUMENTATION_AUDIT_AND_M3_ROADMAP_SYNC_2026_09_01.md
```

## 6. Independent Release Gates

The next release-management decisions are intentionally separate:

```text
Gate R1 - merge selected KRC MEDIA BETA feature work toward main
Gate R2 - promote/replace MEDIA BETA backend infrastructure
Gate R3 - enable external testers
Gate R4 - public sharing / Store rollout
```

Current state for all four gates: `HOLD`.

A future approval of one gate must not be interpreted as approval of another. M3 technical acceptance would not itself approve any R1-R4 gate.

## 7. Release Preconditions

Before any later release transition, verify at least:
- current feature-branch CI;
- current private-GPT smoke tests;
- privacy/retention terms for active external providers;
- resource/quota limits and monitoring;
- rollback/disable procedure;
- current OpenAI Custom GPT/Action publication requirements when public rollout is considered.

For M4 specifically, deployment-image parity must be proven before canary work.

## 8. Future Optional Cost/Sustainability Work

The sustainable-free-media concept remains optional future architecture. It is not an active requirement during the release hold and must not silently replace the accepted owner beta. Any Cloudflare/local Whisper work requires a new explicit engineering decision and new acceptance tests.

## 9. Successor Platform

The former general Modular Agent Platform direction is developed in a separate repository/project named `K_Supervisor`. It is not a future numbered phase of K-Research & Critic.
