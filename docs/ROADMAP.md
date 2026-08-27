# ROADMAP
План завершеного Core та поточного ізольованого MEDIA BETA розширення.

Version: 1.8
Status: CORE_MAINTENANCE / MEDIA_BETA_RELEASE_HOLD
Updated: 2026-08-27

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

The media upgrade is a narrow input/UX extension developed separately from public Core.

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

## 4. Current Work Mode

Current state:

```text
RELEASE_HOLD_OWNER_TESTING
```

The owner has chosen to continue private testing before deciding on release. Defects found during this period are fixed and revalidated only in the isolated feature branches unless the owner explicitly changes the release decision.

Canonical checkpoint:

```text
subprojects/media_beta/53_RELEASE_HOLD_OWNER_TESTING_CHECKPOINT.md
```

## 5. Independent Release Gates

The next release-management decisions are intentionally separate:

```text
Gate R1 - merge KRC media feature branch to main
Gate R2 - promote VoiceBridge media backend to production
Gate R3 - enable external testers
Gate R4 - public sharing / Store rollout
```

Current state for all four gates: `HOLD`.

A future approval of one gate must not be interpreted as approval of another.

## 6. Release Preconditions

Before any later release transition, verify at least:
- current feature-branch CI;
- current private-GPT smoke tests;
- privacy/retention terms for active external providers;
- resource/quota limits and monitoring;
- rollback/disable procedure;
- current OpenAI Custom GPT/Action publication requirements when public rollout is considered.

## 7. Future Optional Cost/Sustainability Work

The sustainable-free-media concept remains optional future architecture. It is not an active requirement during the release hold and must not silently replace the accepted owner beta. Any Cloudflare/local Whisper work requires a new explicit engineering decision and new acceptance tests.

## 8. Successor Platform

The former general Modular Agent Platform direction is developed in a separate repository/project named `K_Supervisor`. It is not a future numbered phase of K-Research & Critic.
