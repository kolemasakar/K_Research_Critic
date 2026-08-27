# K-Research & Critic
Базовий опис production-продукту та ізольованого приватного MEDIA BETA контуру.

Version: 1.3
Status: PRODUCTION_CORE / PRIVATE_MEDIA_BETA_RELEASE_HOLD
Updated: 2026-08-27

## Overview

K-Research & Critic is the published GPT Store research and independent-critique product.
The public text-research Core remains the production baseline. An additive MEDIA BETA is developed and tested separately on feature branches and is not part of the public release until a later explicit owner decision.

Repository:

```text
kolemasakar/K_Research_Critic
```

Public product:

```text
K-Research & Critic
```

Private test product:

```text
K-Research & Critic - MEDIA BETA
```

## Current Product State

```text
Core phases 0-12                              COMPLETE
GPT Store Core publication                    COMPLETE
Core production smoke test                    PASS
Core release line                             v1.0.x
Private MEDIA A9 owner zero-client ingress    ACCEPTED
Private MEDIA A9.10 local attachment          ACCEPTED
Private MEDIA A10 copy-safe output            ACCEPTED
Current MEDIA release decision                RELEASE_HOLD_OWNER_TESTING
Merge to main                                 HOLD
Production media promotion                    HOLD
External media testers                        HOLD
Public media rollout                          HOLD
```

The release hold means the owner continues private testing. It does not roll back the accepted private-beta functionality and it does not authorize any production or public transition.

## Core Workflow

```text
User task
 -> domain/risk resolution
 -> CriticProfile draft
 -> explicit user approval/edit/cancel
 -> Research
 -> Critic
 -> bounded revision loop
 -> sourced final report
 -> review protocol
```

The transcript/media layer never replaces this workflow. It only supplies source content before the CriticProfile gate.

## Private MEDIA BETA

Accepted owner-only zero-client inputs:

```text
prerecorded YouTube
Instagram Reel
public Facebook Video/Reel
supported public Telegram video post
one current-conversation local audio/video attachment
```

Current media routing:

```text
YouTube / Instagram
 -> managed transcript route
 -> explicit provider-credit consent when billable

Facebook
 -> free Cobalt retrieval
 -> AssemblyAI STT after successful retrieval
 -> durable KRCM transcript
 -> Cobalt failure means unavailable and STOP
 -> no active/offered paid fallback

Telegram
 -> public Telegram web/embed retrieval
 -> trusted Telegram CDN media
 -> AssemblyAI STT
 -> durable KRCM transcript
 -> zero retrieval credits
 -> no login/cookies/session/bot token/paid fallback

Local attachment
 -> ChatGPT openaiFileIdRefs transport
 -> trusted OpenAI temporary media delivery
 -> bounded ingestion/normalization
 -> AssemblyAI STT
 -> durable KRCM transcript
 -> zero retrieval credits
```

The A8 browser Helper remains historical fallback evidence only. It is not normal owner UX.

## Repository Isolation

KRC media package:

```text
branch: agent/video-url-research
PR: #8
state: draft / open / unmerged
```

VoiceBridge media backend:

```text
repository: kolemasakar/VoiceBridge
branch: agent/krc-media-transcript
PR: #28
state: draft / open / unmerged
```

Dedicated beta backend:

```text
https://voicebridge-krc-media-beta-kolemasakar.onrender.com
```

Production VoiceBridge and repository `main` are outside the current owner-testing scope.

## Current Builder Package

```text
manifest: gpt_store/media_beta_manifest.yaml
Builder instructions: prompts/GPT_STORE_MEDIA_BETA_BUILDER_INSTRUCTIONS.md
canonical managed reference: prompts/GPT_STORE_MEDIA_MANAGED_BETA_INSTRUCTIONS.md
Action schema: gpt_store/actions/media_managed_beta_openapi.yaml
Builder package: 0.9.1-beta-a10
Action schema: 0.6.0-a9.10
```

The accepted Builder/Action package is frozen during the release hold unless a real owner-test defect requires a separately validated change.

## Evidence and Critic Rules

- A transcript proves what the source said, not that the claim is true.
- Independent claim research begins only after CriticProfile approval.
- Cross-check floors remain `LOW>=0`, `MEDIUM>=1`, `HIGH>=2`, `CRITICAL>=3`.
- Every material factual claim tracks required, achieved independent evidence origins, and any SHORTFALL.
- Evidence-origin counts must be visible and traceable.
- Unresolved SHORTFALL must qualify the result.

## A10 Copy-Safe Output

The ChatGPT UI can render a four-column Markdown table correctly but corrupt its header when copying the entire response. The accepted mitigation is to keep the rendered table and immediately provide an identical fenced `text` copy with literal pipe delimiters.

This mitigation passed owner runtime testing and is treated as accepted A10 behavior.

## Canonical Media Documentation

Start here:

```text
subprojects/media_beta/00_INDEX.md
subprojects/media_beta/03_CURRENT_STATE.md
subprojects/media_beta/53_RELEASE_HOLD_OWNER_TESTING_CHECKPOINT.md
subprojects/media_beta/54_PROJECT_DOCUMENTATION_AUDIT_2026_08_27.md
```

Operator-facing project documents:

```text
docs/ARCHITECTURE.md
docs/ROADMAP.md
docs/TEST_PLAN.md
docs/GPT_STORE_DEPLOYMENT.md
docs/GPT_STORE_PACKAGE.md
docs/VIDEO_INPUT_UPGRADE.md
docs/PRIVACY_POLICY.md
docs/MEDIA_BETA_RUNBOOK.md
```

## Release Rule

No media merge, production promotion, external tester onboarding, or public/Store rollout follows automatically from green CI or private runtime acceptance. Each release gate requires a separate explicit owner decision.

Stable compatibility identifiers such as `K_SUPERVISOR_CHECKPOINT` and `runtime/k_supervisor.db` remain unchanged where required by the established Core contract.
