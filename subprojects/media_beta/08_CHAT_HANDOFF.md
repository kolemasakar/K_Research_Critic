# MEDIA BETA Chat Handoff
Канонічна інструкція відновлення MEDIA BETA у новому чаті без повернення до застарілого A9 planning state.

Version: 3.0
Status: ACTIVE_HANDOFF / RELEASE_HOLD_OWNER_TESTING
Checkpoint date: 2026-08-27

## Recovery Command

`recover MEDIA BETA release hold`

## Mandatory Recovery Order

1. `subprojects/media_beta/00_INDEX.md`
2. `subprojects/media_beta/03_CURRENT_STATE.md`
3. `subprojects/media_beta/53_RELEASE_HOLD_OWNER_TESTING_CHECKPOINT.md`
4. `subprojects/media_beta/54_PROJECT_DOCUMENTATION_AUDIT_2026_08_27.md`
5. `subprojects/media_beta/02_ROADMAP.md`
6. `subprojects/media_beta/06_DECISION_LOG.md`
7. `subprojects/media_beta/04_OPERATIONS_RUNBOOK.md`
8. `subprojects/media_beta/05_TEST_PLAN.md`

Then verify live GitHub state for KRC PR #8 and VoiceBridge PR #28 before any write.

## Repository Context

```text
KRC repo: kolemasakar/K_Research_Critic
KRC branch: agent/video-url-research
KRC PR: #8 draft/open/unmerged

VoiceBridge repo: kolemasakar/VoiceBridge
VoiceBridge branch: agent/krc-media-transcript
VoiceBridge PR: #28 draft/open/unmerged
```

Production branches and public rollout remain outside current authorization.

## Current Checkpoint

```text
A9_OWNER_ZERO_CLIENT_MEDIA_INPUT_ACCEPTED
A9_10_LOCAL_ATTACHMENT_ACCEPTED
A10_COPY_SAFE_CLAIM_TABLE_RUNTIME_ACCEPTED
RELEASE_HOLD_OWNER_TESTING
```

The old markers `A9_IMPLEMENTATION_NOT_STARTED` and `A9_ZERO_CLIENT_MEDIA_ROUTER_PLANNED` are historical and must not be restored as current state.

## Accepted Owner Inputs

```text
YouTube
Instagram Reel
Facebook Video/Reel via free Cobalt
public Telegram video posts
one local audio/video attachment
```

## Critical Policy Recovery

- Facebook: Cobalt fail -> unavailable; no paid fallback.
- Telegram: public-only, zero retrieval credits, no login/session/paid fallback.
- Local attachment: openaiFileIdRefs, trusted OpenAI delivery, max 32 MiB, zero retrieval credits.
- no normal-flow Helper or user beta code;
- no KRCM/file/signed-URL exposure;
- CriticProfile gate before research;
- per-claim independent cross-check accounting;
- A10 fenced copy-safe summary remains mandatory.

## Current Package

```text
Builder package: 0.9.1-beta-a10
Action schema: 0.6.0-a9.10
Builder already applied: yes
```

Do not ask the owner to re-apply Builder content unless the package itself has changed and needs a new runtime acceptance.

## Current Release Decision

```text
merge = HOLD
production promotion = HOLD
external testers = HOLD
public rollout = HOLD
```

Do not infer authorization to change any of these from a request to fix/test the private beta.

## Continuation Rule

During the hold, continue only owner testing, defect remediation, regression hardening, and documentation maintenance. If branch heads differ from the checkpoint, inspect the delta before modifying code.

## Terminal Marker

`MEDIA_BETA_HANDOFF_V3_RELEASE_HOLD`
