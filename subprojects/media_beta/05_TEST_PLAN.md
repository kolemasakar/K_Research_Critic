# MEDIA BETA Test Plan
План регресій та live-перевірок для прийнятого owner-only zero-client MEDIA BETA.

Version: 2.0
Status: ACTIVE_RELEASE_HOLD_TESTING
Updated: 2026-08-27

## 1. Objectives

Prove that owner-only media ingestion remains functional without weakening the CriticProfile, evidence, privacy, cost, and isolation boundaries.

## 2. Repository CI

KRC changes must keep:

```text
Python 3.13 PASS
Python 3.14 PASS
dependency integrity PASS
Ruff PASS
Mypy PASS
repository policy PASS
GPT Store package validation PASS
coverage gate PASS
```

VoiceBridge implementation changes must keep its relevant build/test/live isolated gates green before owner retest.

## 3. Package Contract

Validate:
- private owner-only manifest;
- Builder package `0.9.1-beta-a10`;
- Action schema `0.6.0-a9.10`;
- managed zero-client ingress;
- no user beta code;
- no normal-flow Helper;
- durable KRCM state;
- hidden internal IDs/credentials.

## 4. YouTube / Instagram

Test:
- supported URL acceptance;
- native credit preflight;
- explicit consent before billable work;
- no automatic AI fallback;
- Instagram AI second preflight and new consent;
- completed segment retrieval;
- uncertain-charge no-retry rule.

## 5. Facebook

Positive:

```text
public media -> Cobalt -> AssemblyAI -> durable KRCM
```

Negative:

```text
Cobalt failure -> unavailable -> STOP
```

Regression assertions:
- no ScrapeCreators call;
- no automatic paid fallback;
- no paid fallback offer;
- no Supadata generate workaround for active Facebook failure policy.

## 6. Telegram

Positive:
- supported public post normalization;
- public web/embed retrieval;
- trusted media host;
- AssemblyAI transcript;
- durable KRCM;
- retrieval credits zero.

Negative:
- private/invite/auth-required/non-post forms rejected;
- no login/cookies/session/bot token request;
- no paid fallback;
- no-speech/unavailable stops cleanly.

## 7. Local Attachment

Transport probe regression:
- runtime `openaiFileIdRefs` object accepted;
- trusted OpenAI HTTPS host boundary;
- bounded Range probe;
- zero retrieval/STT charge for probe;
- no sensitive URL/file-id echo.

Full ingestion regression:
- exactly one audio/video file;
- type/size/duration validation;
- maximum 32 MiB;
- safe full download/normalization;
- AssemblyAI STT;
- durable KRCM segments;
- retrieval credits zero;
- temporary media cleanup;
- no Helper/file token request.

## 8. CriticProfile / Claim Audit

For every fact-check regression:
- profile before research;
- explicit approval required;
- material edits require re-approval;
- per-claim required/achieved/exception accounting;
- achieved only counts visible independent origins;
- SHORTFALL preserved and final result qualified.

## 9. A10 Output

Verify:
- rendered four-column table;
- fenced copy-safe duplicate immediately follows;
- same claim rows/values in both;
- fenced literal pipes survive whole-response Copy;
- real SHORTFALL remains visible.

## 10. Owner Hold Regression Set

During continued private testing, rotate through:
- different public sources on every accepted platform;
- source unavailable/private/auth-required cases;
- long/short speech;
- multiple languages;
- poor audio/no speech;
- local files across accepted types and near limits;
- numerical/name/date transcription uncertainty;
- claim sets with both PASS and SHORTFALL;
- source-independence edge cases.

## 11. Release Tests Are Deferred

Production smoke, external tester onboarding, scale, and public Store release tests are deferred while all release gates are HOLD. They become mandatory only after the matching owner decision.

## 12. Exit Rule for Hold Fixes

A defect fix is accepted when:
- regression coverage exists when practical;
- relevant CI is green;
- no release boundary was widened;
- private runtime is retested when behavior changed;
- current-state/audit documentation is updated.
