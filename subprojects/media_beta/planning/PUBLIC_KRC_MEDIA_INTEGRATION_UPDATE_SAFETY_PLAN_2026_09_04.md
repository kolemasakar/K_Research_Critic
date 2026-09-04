# Public KRC + MEDIA integration update-safety plan

Date: 2026-09-04
Status: APPROVED_PLAN / NOT_EXECUTED / LIVE_KRC_UNCHANGED
Scope: Safe future integration of KRC MEDIA capabilities into the already-published K-Research & Critic GPT
Product authority: `kolemasakar/K_Research_Critic`

## Problem statement

Current product reality:

```text
K-Research & Critic (KRC)
  -> already published
  -> already accessible to users
  -> must remain accessible

K-Research & Critic - MEDIA BETA
  -> was not published separately
  -> currently owner-only/private
  -> must NOT become a dependency that can disable public Core access
```

Owner-reported current OpenAI constraint: publishing new custom GPTs in the personal workspace is unavailable. This is a mutable external product-policy constraint and must be reverified before any live GPT update.

The integration strategy is therefore to preserve the identity of the already-published KRC and, only after dedicated safety gates pass, add MEDIA capability to that same existing GPT through its normal edit/draft/update path if that path remains available.

## Core safety principle

MEDIA must be additive and failure-isolated.

```text
MEDIA backend unavailable
MEDIA Action unavailable
MEDIA source unsupported
MEDIA quota exhausted
MEDIA auth/admission failure
        |
        v
MEDIA request fails closed / becomes unavailable
        |
        +----> KRC Core remains fully usable
```

A MEDIA failure must never make the public KRC itself unavailable or force public users into the private MEDIA BETA identity.

## Repository merge is not a GPT publication event

Repository integration and ChatGPT product configuration are separate operations.

```text
GitHub merge/integration
        !=
ChatGPT GPT Update
```

R1 may integrate code/docs while the live published KRC remains untouched. No assumption is allowed that GitHub state automatically updates Builder configuration.

## New gated sequence

### R0 - Public KRC Update Safety Preflight

Status now: PLANNED / REQUIRED BEFORE R1-R3 EXECUTION.

Verify without changing the live GPT:

- the existing published KRC is still accessible to users;
- its current sharing/publication state is known and recorded;
- owner can still open Edit for the same GPT;
- an `Update` path for that existing GPT is actually available at execution time;
- current OpenAI rules for updating an already-published GPT are rechecked;
- current public-Action requirements are rechecked;
- any required Privacy Policy URL is valid and reachable;
- current GPT configuration is captured sufficiently for rollback/reconstruction: instructions, Actions schema/configuration, knowledge references, capability toggles, identity/description and other material settings;
- the current public GPT URL/identity is preserved.

If any of these conditions cannot be verified, STOP before changing the live GPT.

### R1 - Repository integration

Purpose: integrate selected MEDIA implementation and documentation into the KRC repository while preserving Core behavior.

Required before merge:

- exact diff/scope review;
- Core regression tests;
- MEDIA tests;
- no instruction replacement that removes existing KRC workflow;
- no dependency that makes Core startup/use conditional on MEDIA backend health;
- MEDIA routes remain optional/additive;
- current published GPT remains untouched during repository work.

R1 does not authorize R2 or R3.

### R2 - Permanent MEDIA backend readiness/promotion

Purpose: make the tested MEDIA backend target permanently available for the future integrated public KRC, but only after a separate owner decision.

Required checks:

- exact Render target and rollback target;
- Neon connectivity/durability;
- provider configuration;
- AssemblyAI remains the active prerecorded provider while current credits remain the accepted operating choice;
- Gemini prerecorded normal activation remains false;
- Hybrid C/D remains deferred until its separate trigger;
- Cobalt failure -> unavailable;
- no automatic paid fallback;
- public-user admission/auth model is intentionally designed and tested;
- private owner-only admission assumptions are not accidentally imposed on public KRC users;
- backend/API failures cannot disable non-MEDIA KRC work.

R2 does not authorize a live GPT update.

### R3 - Update the existing published KRC GPT

This is the critical live-product gate.

Only the existing published KRC identity may be edited; do not depend on creating/publishing a new GPT.

Planned path, subject to revalidation of the actual Builder UI/capabilities at that time:

```text
existing published KRC
  -> Edit
  -> modify draft only
  -> add MEDIA instructions/action capability additively
  -> Preview/Core regression
  -> Preview/MEDIA regression
  -> explicit owner authorization
  -> Update existing GPT
```

Before `Update`:

- Core research/critic workflow passes in Preview;
- CriticProfile gate remains intact;
- per-claim provenance/cross-check accounting remains intact;
- A10 copy-safe output remains intact;
- MEDIA Action calls succeed in Preview against the intended backend;
- MEDIA failure simulation proves Core remains usable;
- current public sharing state and rollback mechanism are confirmed;
- exact pre-update GPT configuration snapshot is retained;
- owner explicitly authorizes the live Update.

If Builder requires a new publication event instead of an update to the existing published GPT, STOP. Do not risk replacing the public KRC with an inaccessible/private identity.

### R4 - Post-update public-access verification

Immediately after R3, verify from a non-owner/public-user perspective where feasible:

- existing public KRC URL still resolves;
- existing Core KRC tasks work without invoking MEDIA;
- MEDIA capability is visible/usable only as intended;
- unsupported MEDIA inputs fail locally without degrading Core;
- backend auth/admission does not expose secrets and does not block ordinary KRC Core use;
- no unexpected change to public sharing state;
- no accidental dependence on the private MEDIA BETA GPT identity.

If any critical check fails, activate the previously verified GPT/backend rollback procedure and keep public Core available.

## Gate semantics after this decision

```text
R0  Public KRC Update Safety Preflight
R1  Repository integration
R2  Permanent MEDIA backend promotion/readiness
R3  Update existing published KRC GPT
R4  Post-update public-access + Core regression verification
```

Every gate is independent. Approval of one must never be inferred as approval of the next.

## Current state remains unchanged

```text
public KRC:                       PUBLISHED / USER-ACCESSIBLE
private MEDIA BETA GPT:          OWNER-ONLY
M4 owner canary:                 PASS
M4 canary rollback:              COMPLETE
permanent MEDIA backend:         NOT PROMOTED BY THIS PLAN
repository merge:                NOT AUTHORIZED BY THIS PLAN
live KRC GPT update:             NOT AUTHORIZED BY THIS PLAN
AssemblyAI universal-2:          CURRENT KRC PRERECORDED PROVIDER
Gemini prerecorded normal:       INACTIVE
Hybrid C/D:                      PLANNED / DEFERRED
```

## Explicit stop conditions

STOP before live update if any of the following is true:

- existing KRC public identity cannot be safely preserved;
- current published KRC cannot be edited/updated without republishing as a new GPT;
- public sharing state cannot be verified;
- required Action/privacy requirements are not met;
- MEDIA backend admission remains owner-only in a way that would block public users;
- Core regression fails;
- MEDIA failure can cascade into Core failure;
- rollback method is not established.

## Recovery authority

Operational recovery remains checkpoint 72 until a later explicitly authorized state transition occurs:

`72_M4_OWNER_CANARY_ACCEPTED_ROLLBACK_COMPLETE_CHECKPOINT_2026_09_02.md`

This document changes planning/governance only. It does not change the live GPT, Builder configuration, Render deployment, Neon data, provider selector, GitHub merge state, or public availability.