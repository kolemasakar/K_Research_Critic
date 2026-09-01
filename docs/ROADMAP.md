# ROADMAP
План завершеного Core та поточного ізольованого MEDIA BETA розширення.

Version: 1.10
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

## 4. VoiceBridge Technology Baseline

VoiceBridge has completed its own real-time STT migration and Phase 2 closure.

```text
VoiceBridge main                               a426ae331721dd36291874e45380faf603d854cf
streaming STT default                          Gemini gemini-3.5-transcribe-live
streaming rollback                             AssemblyAI universal-streaming-english
Phase 2 Universal Cloud Audio                  COMPLETE
main exact-head Validate                       SUCCESS
```

This is a shared technology baseline, not a KRC prerecorded provider cutover.

The provider domains remain deliberately separate:

```text
VoiceBridge live streaming:
  STT_PROVIDER=gemini
  state=ACCEPTED DEFAULT

KRC prerecorded:
  KRC_MEDIA_STT_PROVIDER=assemblyai
  active model=AssemblyAI universal-2
  Gemini candidate=gemini-3.5-transcribe
  state=IMPLEMENTED / INACTIVE
```

The KRC forward-port code currently enforces AssemblyAI as the only normal KRC prerecorded selector value until the Gemini activation gate. The Gemini prerecorded provider exists only as a controlled candidate path.

The KRC migration branch was created from VoiceBridge main at `eba77183bee29621aa6c7cb859737a10edb6e4d4`. Current VoiceBridge main is 13 commits ahead of that base; the compared delta consists of Phase 2 documentation/closure changes rather than additional runtime implementation. This does not create an immediate KRC runtime re-port requirement, but current VoiceBridge main documentation is authoritative for VoiceBridge project state.

## 5. Active KRC Prerecorded Provider-Evidence Track

The active KRC-specific technical track remains the prerecorded STT forward migration in VoiceBridge branch `agent/krc-media-gemini-migration`.

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
 -> same-asset AssemblyAI vs Gemini prerecorded A/B
 -> manual factual/hallucination review
```

The byte-capture step is evidence preparation only and must not itself invoke AssemblyAI or Gemini.

The completed VoiceBridge Live A/B cannot substitute for this KRC prerecorded A/B because the model, transport/input mode, corpus, duration/timestamp behavior, and evidence-integrity requirements differ.

## 6. Current Work Mode

Current state:

```text
RELEASE_HOLD_OWNER_TESTING
```

The owner has chosen to continue private testing before deciding on release. Defects found during this period are fixed and revalidated only in isolated beta/technology branches unless the owner explicitly changes the release decision.

Canonical release checkpoint:

```text
subprojects/media_beta/53_RELEASE_HOLD_OWNER_TESTING_CHECKPOINT.md
```

Canonical current engineering overlays:

```text
subprojects/media_beta/60_PROJECT_DOCUMENTATION_AUDIT_AND_M3_ROADMAP_SYNC_2026_09_01.md
subprojects/media_beta/61_VOICEBRIDGE_GEMINI_IMPACT_AUDIT_2026_09_01.md
```

## 7. Independent Release Gates

The next release-management decisions are intentionally separate:

```text
Gate R1 - merge selected KRC MEDIA BETA feature work toward main
Gate R2 - promote/replace MEDIA BETA backend infrastructure
Gate R3 - enable external testers
Gate R4 - public sharing / Store rollout
```

Current state for all four gates: `HOLD`.

A future approval of one gate must not be interpreted as approval of another. M3 technical acceptance would not itself approve any R1-R4 gate.

## 8. Release Preconditions

Before any later release transition, verify at least:
- current feature-branch CI;
- current private-GPT smoke tests;
- privacy/retention terms for active external providers;
- resource/quota limits and monitoring;
- rollback/disable procedure;
- current OpenAI Custom GPT/Action publication requirements when public rollout is considered.

For M4 specifically, deployment-image parity must be proven before canary work.

## 9. Future Optional Cost/Sustainability Work

The sustainable-free-media concept remains optional future architecture. It is not an active requirement during the release hold and must not silently replace the accepted owner beta. Any Cloudflare/local Whisper work requires a new explicit engineering decision and new acceptance tests.

## 10. Successor Platform

The former general Modular Agent Platform direction is developed in a separate repository/project named `K_Supervisor`. It is not a future numbered phase of K-Research & Critic.
