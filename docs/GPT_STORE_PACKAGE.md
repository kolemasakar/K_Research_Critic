# GPT_STORE_PACKAGE
Документ визначає production-пакет K-Research & Critic, перевірки релізу та maintenance-gates для GPT Store.

Version: 1.8
Status: MAINTENANCE

## 1. Purpose

This document is the operator-facing packaging specification for the published K-Research & Critic Custom GPT.

Repository:

```text
kolemasakar/K_Research_Critic
```

Release line:

```text
K-Research & Critic v1.0.x
```

The package follows these invariants:

```text
no developer API key
no mandatory external backend
no Actions
no Apps
no pinned model
user-plan model policy
built-in ChatGPT capabilities for the core path
```

Default user-facing language is Ukrainian (`uk-UA`).

## 2. Package Files

```text
gpt_store/manifest.yaml
prompts/GPT_STORE_INSTRUCTIONS.md
gpt_store/checkpoint.py
gpt_store/checkpoint_example.json
scripts/validate_store_package.py
docs/GPT_STORE_PACKAGE.md
```

The manifest is the canonical human/machine-readable Builder configuration source.

## 3. Builder Configuration

### Name

```text
K-Research & Critic
```

### Description

The canonical public description is stored in `gpt_store/manifest.yaml` because its first line is Ukrainian UTF-8. Copy `product.description` into Builder exactly.

### Default language

```text
uk-UA
```

### Recommended model

Leave the recommended model unset.

The workflow must not depend on a named model. Users may use or switch among runtimes/models exposed by their ChatGPT plan.

### Capabilities

Enable:

```text
Web search
Code Interpreter & Data Analysis
```

Disable for the core package:

```text
Image generation
Apps
Actions
```

### Knowledge

No uploaded Knowledge file is mandatory for the v1.0 public release.

## 4. Conversation Starters

Use the eight bilingual starters from `gpt_store/manifest.yaml`.

The first four are Ukrainian and are intended to occupy the primary visible Store positions; the remaining four are English equivalents.

## 5. Store Workflow Mapping

```text
Supervisor stage
  -> Domain/risk assessment
  -> CriticProfile proposal
  -> USER CHOICE: 1=APPROVE / 2=EDIT / 3=REJECT
  -> Research stage
  -> Critic stage
  -> autonomous REVISE/PASS loop
  -> Final report
  -> Review protocol
```

The Store Edition provides logical multi-agent separation inside one ChatGPT runtime rather than process-isolated model instances.

## 6. Checkpoint and Fresh-chat Recovery

Cross-chat continuation uses an explicit user-controlled checkpoint marked:

```text
K_SUPERVISOR_CHECKPOINT
```

Schema version:

```text
1.0
```

Checkpoint generation is explicit-request only. Normal profile gates and final reports must not auto-create checkpoints.

Safe states:

```text
PROFILE_REVIEW_REQUIRED
PROFILE_APPROVED
REVISE_REQUIRED
APPROVED
FINALIZED
COMPLETED_WITH_LIMITATIONS
FAILED
```

The checkpoint marker remains a stable legacy compatibility identifier in the v1.0 release line.

## 7. Static Validation

Run after Store package changes:

```text
python -m scripts.validate_store_package
python -m pytest
```

CI additionally validates repository policy, typed boundaries, lint correctness, dependency integrity, and coverage.

## 8. Preview Test Matrix

The pre-publication Preview matrix completed successfully on 2026-08-14:

```text
P1 New low-risk research task - PASS
P2 High-risk domain task and conservative risk floor - PASS
P3 Explicit APPROVE gate including numeric alias 1 - PASS
P4 EDIT/2 then approve - PASS
P5 REJECT/3 stops autonomous execution - PASS
P6 Research -> Critic -> PASS - PASS
P7 Forced REVISE then corrected second iteration - PASS
P8 Web-search-unavailable/freshness limitation behavior - PASS
P9 Generate checkpoint at PROFILE_APPROVED - PASS
P10 Paste checkpoint into a fresh GPT conversation and resume - PASS
P11 Malformed checkpoint rejection - PASS
P12 Final report plus review protocol without hidden reasoning - PASS
```

A separate forced-REVISE control scenario also passed.

## 9. Account/Plan Release Matrix

Live validation completed on 2026-08-14.

```text
Free account:
  public-link access: PASS
  numbered CriticProfile gate: PASS
  web-search capability path: PASS
  Research -> Critic -> final output: PASS
  no developer API key/backend requirement: PASS

Paid/Plus account:
  same workflow: PASS
  runtime/reasoning-level switch after profile gate: PASS
  approval/state continuity after switch: PASS
  final report/review semantics preserved: PASS
```

## 10. Publication and Discoverability

Publication completed on 2026-08-14.

```text
publication_state: published
published_at: 2026-08-14
store_category: Research & Analysis
Store search/discoverability: PASS
public Store card: PASS
Ukrainian primary conversation starters: PASS
```

The Builder UI confirmed public distribution and the published GPT was subsequently found through Store search.

## 11. Production Smoke Test

Production smoke testing completed successfully on 2026-08-14.

Scenario:

```text
high-risk geodesy/construction task
CriticProfile approval gate
web_search=AVAILABLE
Research
Critic review
REVISE
corrected research
Critic PASS
final report + review protocol
```

Observed final result:

```text
Critic history: REVISE -> PASS
final reliability score: 0.93
workflow status: FINALIZED
automatic checkpoint: absent
internal citation/tool markup: absent
normal visible sources: present
```

Manifest release metadata records:

```text
production_smoke_test_passed: true
production_smoke_tested_at: 2026-08-14
```

## 12. Release State

Canonical first production release:

```text
product: K-Research & Critic
repository: K_Research_Critic
GitHub release: K-Research & Critic v1.0.0
Git tag: v1.0.0
publication_state: published
published_at: 2026-08-14
store_category: Research & Analysis
production_smoke_test: PASS
repository_mode: MAINTENANCE
```

The `v1.0.0` tag must point to the finalized maintenance-synchronization commit with fully green CI.

## 13. Maintenance Rules

Any later Builder change is a product update and must be revalidated before applying it to the published GPT.

Maintenance work may include:

```text
bug/security fixes
OpenAI/ChatGPT compatibility changes
Store-package compatibility changes
regression fixes
small UX improvements
documentation corrections
v1.0.x maintenance releases
```

The general Modular Agent Platform is no longer developed in this repository. It is transferred to a separate clean `K_Supervisor` project with its own roadmap beginning at Phase 0.
