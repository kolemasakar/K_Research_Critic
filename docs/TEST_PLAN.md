# TEST_PLAN
План перевірки production Core та ізольованого MEDIA BETA K-Research & Critic.

Version: 1.2
Status: ACTIVE
Updated: 2026-08-27

## 1. Purpose

This document defines the canonical test strategy for K-Research & Critic. It covers the stable public Core and the separate private MEDIA BETA. Historical internal identifiers may retain `K_Supervisor` for compatibility, but the product under test is K-Research & Critic.

## 2. Core Test Objectives

The Core suite verifies:
- domain/risk resolution;
- complete CriticProfile generation;
- research blocked before explicit approval;
- profile freeze and material-amendment re-approval;
- Research/Critic workflow and bounded REVISE/PASS loop;
- evidence/source traceability;
- explicit failure and limitation states;
- final report/review protocol generation;
- checkpoint compatibility;
- configuration, persistence, metrics, logging, and redaction boundaries.

## 3. Deterministic CI Gates

Every applicable push/PR must keep these green:

```text
Python 3.13 full pytest suite
Python 3.14 full pytest suite
python -m pip check
Ruff correctness checks
Mypy typed-boundary checks
repository policy validation
GPT Store package validation
coverage gate
```

Live provider/ChatGPT UI behavior is not represented as automated PASS unless CI actually executes that boundary.

## 4. Core Approval and Research/Critic Tests

Required coverage includes:
- APPROVE / EDIT / REJECT behavior;
- no autonomous research before approval;
- approved-profile immutability;
- one or more revision cycles;
- max-iteration behavior;
- COMPLETED_WITH_LIMITATIONS;
- evidence and contradiction preservation;
- no hidden private reasoning in artifacts;
- checkpoint generation only at allowed explicit boundaries.

## 5. Claim-Level Cross-Check Tests

Risk floors:

```text
LOW      >= 0
MEDIUM   >= 1
HIGH     >= 2
CRITICAL >= 3
```

Tests must prove:
- each material factual claim has required/achieved/exception accounting;
- evidence-origin independence is not URL-counting;
- duplicate/syndicated evidence is not double-counted;
- achieved cannot exceed visible traceable origins;
- SHORTFALL is reported when achieved is below required;
- unconditional PASS is forbidden with unresolved/unqualified SHORTFALL.

## 6. MEDIA BETA Static Contract Tests

The private package must preserve:

```text
publication_state = private_owner_only
managed zero-client ingress
Action bearer authentication
no user beta code
KRCM durable jobs
no normal-flow Helper
Builder instructions <= 8000 characters
Action schema 0.6.0-a9.10
Builder package 0.9.1-beta-a10
```

## 7. MEDIA BETA Route Regression Matrix

### YouTube / Instagram

- native provider preflight before billable operation;
- explicit user consent;
- no automatic AI fallback;
- Instagram AI fallback requires a separate quote and new consent;
- uncertain-charge provider operation is never automatically replayed.

### Facebook

- free Cobalt route is active;
- Cobalt success may proceed to AssemblyAI and durable KRCM;
- Cobalt failure returns unavailable and stops;
- ScrapeCreators remains unconfigured/inactive/reserve-only;
- no automatic or offered paid fallback.

### Telegram

- supported public-post URL normalization;
- public web/embed retrieval only;
- trusted Telegram media host boundary;
- retrieval credits zero;
- no login/cookies/session/bot token;
- no paid fallback;
- unavailable/no-speech is terminal for that request.

### Local attachment

- exactly one current-conversation audio/video attachment;
- ChatGPT `openaiFileIdRefs` transport;
- trusted OpenAI HTTPS delivery only;
- bounded probe and full-ingestion resource limits;
- maximum attachment bytes 32 MiB;
- retrieval credits zero;
- no file ID/signed URL exposure;
- AssemblyAI only after safe ingestion;
- temporary media cleanup;
- durable KRCM transcript/segments.

## 8. MEDIA BETA Workflow Regression

Every accepted media route must preserve:
- transcript first, independent truth research later;
- CriticProfile gate before research;
- user-visible Ukrainian by default unless explicitly changed;
- timestamp/segment traceability where available;
- claim-level cross-check ledger;
- real SHORTFALL preservation;
- no KRCM Job ID or credential exposure.

## 9. A10 Output Regression

Required output behavior:
- visible four-column claim-summary table;
- no intentional header concatenation;
- immediately following copy-safe fenced `text` duplicate;
- identical values in rendered and fenced forms;
- literal pipe delimiters preserved in the fenced form.

The known ChatGPT whole-response Copy defect on the rendered table header is treated as an external UI limitation, not a passing reason to remove the fenced mitigation.

## 10. Current Owner-Testing Hold

During `RELEASE_HOLD_OWNER_TESTING`, owner tests should emphasize:
- varied supported URLs;
- unavailable/private/auth-required sources;
- no-speech and poor-audio media;
- different local attachment formats/sizes within supported limits;
- transcript accuracy and uncertainty disclosure;
- fact-check source independence;
- failure UX;
- quota/cost behavior;
- copy-safe final-report behavior.

Any confirmed defect should gain a regression test when practical.

## 11. Release-Gate Tests

Tests for production promotion, external testers, or public rollout are not current acceptance work. They become mandatory only after the owner explicitly opens the corresponding release gate.

At that time re-check provider terms/privacy, production monitoring/resource limits, current OpenAI Action/Store requirements, rollback, and real target-account smoke tests.

## 12. Current Validation Reference

The release-hold checkpoint records the last accepted implementation and CI evidence. The current branch head and its most recent `Tests` workflow are authoritative after documentation or regression changes.

Canonical media test detail is also maintained in:

```text
subprojects/media_beta/05_TEST_PLAN.md
subprojects/media_beta/53_RELEASE_HOLD_OWNER_TESTING_CHECKPOINT.md
```
