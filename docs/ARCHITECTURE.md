# ARCHITECTURE
Короткий опис production-архітектури K-Research & Critic та ізольованого MEDIA BETA розширення.

Version: 1.3
Status: PRODUCTION_CORE_STABLE / MEDIA_BETA_RELEASE_HOLD
Updated: 2026-08-27

## 1. Purpose

K-Research & Critic is a GPT Store-first research and independent-critique product. The public text Core is production/maintenance. The private MEDIA BETA is an additive source-ingestion extension that is accepted for owner testing but remains isolated from public Core and production VoiceBridge.

## 2. Stable Core Architecture

```text
USER
 -> Supervisor
 -> domain/risk resolution
 -> CriticProfile draft
 -> explicit user approval/edit/cancel
 -> Research
 -> Critic
 -> bounded REVISE/PASS loop
 -> final report + review protocol
```

Core invariants:
- no independent research before CriticProfile approval;
- approved profile is frozen unless a material amendment is re-approved;
- Research and Critic remain logically distinct passes;
- evidence, uncertainty, limitations, and final status remain explicit;
- private chain-of-thought is not required or persisted;
- public Core does not require a mandatory developer-owned backend or pinned model.

## 3. Private MEDIA BETA Architecture

MEDIA BETA adds source acquisition before the same CriticProfile/Research/Critic workflow:

```text
supported media input
 -> private Custom GPT Action
 -> Action bearer authentication
 -> isolated VoiceBridge MEDIA BETA
 -> source router / adapter
 -> durable KRCM job + transcript segments
 -> CriticProfile gate
 -> approved Research/Critic workflow
 -> localized final report
```

Accepted owner-only inputs:
- prerecorded YouTube;
- Instagram Reel;
- public Facebook Video/Reel;
- supported public Telegram video post;
- one local current-conversation audio/video attachment.

## 4. Source Adapter Rules

### YouTube / Instagram

Managed transcript routes remain provider-neutral at the KRC workflow boundary. Current Supadata billable operations require explicit preflight and user approval. Instagram AI generation requires a separate quote and a new approval.

### Facebook

```text
public Facebook media
 -> free Cobalt retrieval
 -> AssemblyAI only after retrieval success
 -> durable KRCM
```

Cobalt failure is terminal unavailable for the active MEDIA BETA. ScrapeCreators is reserved compatibility code only: unconfigured, inactive, not offerable, and never an automatic fallback.

### Telegram

```text
public Telegram post
 -> public web/embed surface
 -> trusted Telegram CDN
 -> AssemblyAI
 -> durable KRCM
```

No account, cookies, session, bot token, or paid fallback is part of the accepted route. Retrieval credits are zero.

### Local attachment

```text
one current-conversation audio/video attachment
 -> openaiFileIdRefs runtime object
 -> trusted OpenAI temporary delivery
 -> bounded validation/download/normalization
 -> AssemblyAI
 -> durable KRCM
```

The accepted attachment boundary limits media to 32 MiB, keeps retrieval credits at zero, and does not expose file IDs or signed download URLs to the user.

## 5. Durable Job Boundary

Managed MEDIA jobs use the `KRCM_` namespace and durable Postgres state. Accepted behavior includes:
- restart-readable completed jobs and segments;
- duplicate-start reuse where defined;
- no automatic replay of uncertain-charge provider operations;
- paged segment reads until completion;
- hidden Job IDs in normal user-facing output.

## 6. Security and Trust Boundaries

- Action bearer authentication remains server-side.
- Owner beta admission is injected server-side; the owner is not asked for a beta code.
- Provider keys remain server-side.
- Remote platform adapters accept supported public content only.
- Platform login/password/cookies/session tokens are forbidden.
- Local attachment accepts only the ChatGPT current-conversation file-reference transport.
- Temporary media is not intended as durable source-file storage.
- Full transcripts are not stored in KRC checkpoints.

## 7. Evidence Boundary

The transcript is primary evidence for what was said. It is not an independent corroborating source for truth. Material factual claims are independently researched only after profile approval and are checked under the approved cross-check requirement.

## 8. Cross-Check Contract

Risk floors:

```text
LOW      >= 0
MEDIUM   >= 1
HIGH     >= 2
CRITICAL >= 3
```

Each material factual claim maintains:

```text
required
achieved_independent
exception = NONE | SHORTFALL
```

Achieved counts independent underlying evidence origins, not duplicated URLs or syndication. Counts must be visible and traceable in the final report.

## 9. A10 Presentation Contract

A visually correct four-column claim-summary table is required. Because whole-response Copy can corrupt the rendered header in the ChatGPT UI, the accepted runtime also emits an identical fenced `text` table with literal `|` delimiters. The fenced duplicate is the copy-safe authority for copied output.

## 10. Deployment Isolation

```text
KRC media branch:        agent/video-url-research
KRC draft PR:            #8
VoiceBridge media branch: agent/krc-media-transcript
VoiceBridge draft PR:    #28
beta service:            voicebridge-krc-media-beta-kolemasakar
```

Repository `main`, public Core, and production VoiceBridge remain unchanged by the owner-only beta.

## 11. Current Release State

```text
private owner runtime acceptance = PASS
merge to main                    = HOLD
production promotion             = HOLD
external testers                 = HOLD
public rollout                   = HOLD
```

Authorization for one release gate never implies authorization for another.

## 12. Successor Platform Boundary

General modular-agent-platform development belongs to the separate `K_Supervisor` project. Stable legacy identifiers in K-Research & Critic remain only where compatibility requires them.
