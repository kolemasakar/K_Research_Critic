# MEDIA BETA Current State

Canonical implementation checkpoint for continuation without reconstruction.

Version: 4.6
Status: ACTIVE_CHECKPOINT
Checkpoint date: 2026-08-23

## Executive state

Current phase state:

`A4_COMPLETE / A5_COMPLETE / A6_COMPLETE / A7_EXTERNAL_ROLLOUT_PAUSED / A8_BROWSER_ASSISTED_OWNER_BASELINE_COMPLETE / A9_1_COMPLETE / A9_2_DIRECT_YOUTUBE_BLOCKED / A9_2R_MANAGED_NATIVE_COMPLETE / A9_3_DURABLE_MANAGED_COMPLETE / A9_5_PRIVATE_GPT_ZERO_CLIENT_E2E_COMPLETE / A9_8_OWNER_ZERO_CLIENT_YOUTUBE_COMPLETE / A9_6_INSTAGRAM_MANAGED_COMPLETE / A9_6_FACEBOOK_IN_PROGRESS`

Current accepted owner-only zero-client adapters:
- public prerecorded YouTube;
- public Instagram Reel through managed native first, with separately authorized AI fallback only when native transcript is unavailable.

Not accepted yet:
- Facebook public Video/Reels;
- Telegram public video posts;
- local audio/video attachment.

The public GPT, external tester rollout, merge to `main`, and production VoiceBridge remain outside the current gate.

## Repositories and isolation boundary

KRC:
- repo `kolemasakar/K_Research_Critic`;
- branch `agent/video-url-research`;
- draft PR #8;
- public GPT and `main` unchanged.

VoiceBridge:
- repo `kolemasakar/VoiceBridge`;
- branch `agent/krc-media-transcript`;
- draft PR #28;
- production service and `main` unchanged.

Isolated beta runtime:
- service `voicebridge-krc-media-beta-kolemasakar`;
- service ID `srv-da1kic5bedkc73d6fk60`;
- endpoint `https://voicebridge-krc-media-beta-kolemasakar.onrender.com`;
- auto-deploy false.

Do not merge PR #8 or PR #28 and do not target production without a separate explicit owner decision.

## Accepted owner UX

```text
supported public media URL in ChatGPT
 -> analysis mode if missing
 -> no separate media opening
 -> no Helper
 -> no beta-code prompt
 -> no manual Job ID
 -> native managed credit preflight
 -> explicit user consent
 -> ChatGPT consequential-Action confirmation when shown
 -> native transcript when available
 -> for supported Instagram Reel only: if native unavailable, separate AI preflight + separate explicit consent
 -> CriticProfile created internally
 -> direct analysis OR profile review/edit
 -> requested K-Research & Critic workflow
 -> result in same conversation
```

Remote adapters remain public-only. Do not request platform login/password/cookies/session state/account tokens. Auth/private content must return `UNSUPPORTED_PRIVATE_OR_AUTH_REQUIRED`.

## Language invariant

Default user-facing report language is Ukrainian unless the user explicitly requests another language.

The selected report language controls all user-visible workflow text:
- prompts;
- CriticProfile;
- section headings;
- verdict labels;
- final report;
- claim verification;
- review protocol.

The media/transcript/source language must never switch the report language.
Canonical English verdict keys may be retained only in internal structured state. User-visible verdicts must be localized to the selected report language. For Ukrainian reports use:
- VERIFIED -> `ПІДТВЕРДЖЕНО`;
- PARTLY_SUPPORTED -> `ЧАСТКОВО ПІДТВЕРДЖЕНО`;
- UNSUPPORTED -> `НЕ ПІДТВЕРДЖЕНО`;
- CONTRADICTED -> `СУПЕРЕЧИТЬ ДЖЕРЕЛАМ`;
- MISLEADING -> `ВВОДИТЬ В ОМАНУ`;
- UNVERIFIABLE -> `НЕМОЖЛИВО ПЕРЕВІРИТИ`;
- OPINION -> `ДУМКА`.

This rule was hardened in the Builder source instructions on 2026-08-23 after owner testing exposed report-language leakage from source/transcript language.

## CriticProfile gate runtime acceptance

Status: PASS / RUNTIME_ACCEPTED_PRIVATE_OWNER_BETA.

On 2026-08-23 the actual private `K-Research & Critic - MEDIA BETA` Custom GPT was synchronized with the two-stage CriticProfile gate and tested using a medicine/health research request.

Observed PASS sequence:
- profile created internally without automatic display;
- first direct-run/review/cancel gate displayed correctly;
- option `2` displayed the complete unapproved profile;
- profile edit preserved `REVIEW_REQUIRED` and produced version 2;
- second gate repeated after edit;
- option `1` approved version 2 and immediately started Research -> Critic;
- final Ukrainian report recorded profile version 2, 2 critic iterations, `PASS`, reliability `0.89`, `COMPLETED_WITH_LIMITATIONS`, and 0 media credits.

Canonical record:
`32_CRITICPROFILE_GATE_RUNTIME_ACCEPTANCE.md`.

The acceptance exposed one auditability weakness: the final report stated a three-source cross-check requirement but did not make three-source compliance visible for every material claim. The gate UX remains accepted; the evidence-control contract was hardened afterward.

Current required-cross-check contract:
- default floors: `LOW>=0`, `MEDIUM>=1`, `HIGH>=2`, `CRITICAL>=3`;
- the approved `required_cross_checks` value is mandatory for material factual conclusions and may not be silently reduced;
- count independent underlying evidence, not duplicate URLs, syndication, repeated reporting of one study/source, or the source media/transcript itself;
- if fewer independent sources exist, explicitly report the shortfall, reduce confidence as appropriate, and record a limitation;
- Critic verifies cross-check compliance before `PASS`;
- the review protocol reports required versus achieved cross-checks and evidence-scarcity exceptions.

Because this hardening changed the Builder source after the runtime test, the actual private GPT requires one more manual Builder Instructions synchronization before the strengthened cross-check contract is considered runtime-synchronized. The already accepted two-stage gate behavior itself is unchanged.

## A8 browser-assisted baseline

Status: PASS / COMPLETE_BASELINE.

A8 Helper 0.2.2 / `KRCC_` remains emergency/dev fallback evidence only. It is not the normal owner UX.

Canonical record:
`23_A8_OWNER_ONLY_BROWSER_ASSISTED_ACCEPTANCE.md`.

## A9.1 - Server-side STT privacy parity

Status: PASS / COMPLETE.

AssemblyAI EU routing remains available for the accepted browser-assisted fallback path.

## A9.2 - Direct Render-to-YouTube

Status: BLOCKED / CLOSED AS PRIMARY STRATEGY.

Disposition:
`DIRECT_RENDER_YOUTUBE = BLOCKED_BY_DATACENTER_ANTIBOT`.

## A9.2R - Managed provider native route

Status: PASS / COMPLETE_FOR_NATIVE_OWNER_BETA.

Provider: `Supadata`.
Mode: `native`.

Initial acceptance source:
`https://www.youtube.com/watch?v=IzYyKRx7Qwg`.

Accepted transcript facts:
- detected language `ru`;
- 277 timestamped segments;
- one approved native credit;
- no Helper, YouTube cookies, login/session state or residential proxy;
- no automatic AI fallback.

Canonical record:
`26_A9_MANAGED_PROVIDER_ACCEPTANCE.md`.

## Credit consent invariant

A billable managed transcript request must never start merely because a URL was pasted.

Required native preflight:
- current available credits;
- estimated operation cost;
- estimated remaining balance;
- explicit `1 - Так / 2 - Ні`.

Only explicit `1` authorizes the quoted native operation.

Current native hard cap:
`credit_consent.max_credits = 1`.

If native transcript is unavailable, previous consent does not authorize managed AI generation. Any supported AI fallback requires its own preflight and a new explicit consent.

Automatic AI fallback is prohibited.

## A9.3 - Durable managed jobs and credit-safe idempotency

Status: PASS / COMPLETE.

Accepted live code:
`7736f2e7acc5abbb3415e3753d0ca022c1b8d7b2`.

Accepted durability proof:
- durable `KRCM_` job and timestamped segments before restart;
- same durable result after restart;
- duplicate start reused the same completed job while provider key was intentionally invalid;
- no duplicate valid provider call;
- provider balance changed only by the one approved request, `99 -> 98`;
- uncertain interrupted provider operations are not auto-replayed.

Canonical record:
`27_A9_DURABLE_MANAGED_ACCEPTANCE.md`.

## A9.5 - Private GPT Action integration

Status: PASS / COMPLETE.

### Backend / Action contract

Accepted VoiceBridge owner-auth implementation:
`970d7cc5819a623ec1d3cc7a70aceb44bfe311b9`.

The managed Action path:
- requires bearer authentication;
- injects owner beta admission server-side only after successful bearer auth;
- exposes no user-facing `beta_access_code`;
- preserves durable request keys, credit consent and idempotency;
- exposes managed preflight/start/status/segments operations;
- keeps automatic AI fallback disabled.

### Actual private GPT Builder

The actual `K-Research & Critic - MEDIA BETA` Custom GPT was updated on 2026-08-21:
- managed A9.5 OpenAPI schema imported;
- four managed operations visible;
- bearer API-key authentication preserved;
- zero-client Builder instructions installed;
- GPT remained private/owner-only.

Builder preflight from the actual GPT succeeded with:

```text
credits_available: 98
estimated_credits: 1
credits_after_estimate: 97
```

No transcript credit was spent by preflight.

### Actual private GPT zero-client YouTube E2E

Test source:
`https://www.youtube.com/watch?v=IzYyKRx7Qwg`.

Mode:
`Перевірити факти/твердження`.

Observed end-to-end result:

```text
provider: Supadata
mode: native
source_language: ru
segment_count: 277
credits_charged: 1
provider_balance_before: 98
provider_balance_after: 97
```

The GPT:
- requested no owner beta code, Helper, Job ID, cookies, platform login or provider key;
- obtained the transcript in the same chat;
- detected probable transcript uncertainty;
- built material claims with timestamps;
- produced a DRAFT CriticProfile and stopped for `1 / 2 / 3` approval;
- after owner approval, performed independent source research;
- produced the final fact-check report in the same chat;
- reported final fact-check `reliability_score: 0.91`;
- recorded actual managed transcript charge `1 credit`;
- ended `PASS / COMPLETED`.

The ChatGPT platform displayed its own `Allow` confirmation for the consequential external Action. This remained inside the same chat and did not require opening the video or exposing credentials.

Canonical E2E record:
`30_A9_5_PRIVATE_GPT_ZERO_CLIENT_E2E_ACCEPTANCE.md`.

## A9.6 - Instagram managed adapter

Status: PASS / COMPLETE_FOR_MANAGED_OWNER_BETA.

Backend capability/preflight accepted on isolated MEDIA BETA for public Instagram Reel URLs.

Accepted live flow:
1. Native preflight succeeded with available `97`, estimated native cost `1`, after estimate `96`.
2. Native request was explicitly authorized with hard maximum `1` credit.
3. Native result returned `AWAITING_AI_CONSENT`, no transcript segments, and charged `1` native credit.
4. Automatic AI fallback did not run.
5. Separate AI preflight returned rate `2 credits/min`, hard beta maximum `40` credits, conservative Reel ceiling `20 min`, and worst-case remaining balance `56` from the then-current balance `96`.
6. A new explicit user approval authorized one AI generate request.
7. Final managed result: `COMPLETED`, provider mode `generate`, detected language `en`, `11` segments, cumulative charge `3` credits (`1 native + 2 AI`).

Accepted safety invariants:
- native approval never authorizes AI;
- AI requires a separate quote and separate explicit consent;
- AI hard maximum is not exceeded;
- no automatic fallback;
- no Helper, beta code, cookies, login/session state, Job ID, or provider key in normal UX.

KRC Builder source instructions currently advertise YouTube and Instagram as the supported public adapters.

## A9.6 - Facebook adapter

Status: IN_PROGRESS / NOT_ACCEPTED.

Accepted partial evidence on isolated MEDIA BETA:
- Facebook capability/native preflight implemented;
- native request explicitly authorized with hard maximum `1` credit;
- native result reached `AWAITING_AI_CONSENT` with no segments;
- separate metadata-duration path implemented because Facebook AI ceiling must be duration-derived;
- managed read-only lookup added to recover durable jobs safely;
- metadata-duration acceptance eventually succeeded with `duration_seconds=22`, metadata charge `1`, cumulative job charge `2`, and derived AI hard ceiling `2` credits;
- separate AI preflight succeeded.

Blocking result:
- one separately authorized Facebook AI generate request failed;
- final job status `FAILED`;
- error code `MANAGED_PROVIDER_TRANSCRIPT_INVALID`;
- `segments=0`;
- `credit_charge_uncertain=true`;
- automatic retry is therefore prohibited for that failed operation.

Remediation state:
- Supadata nested async-result parser remediation committed as `f6b32c2a03425deaecadd10fc902671d62eaab5d`;
- latest recorded isolated deploy attempt of that parser remediation failed;
- no new provider retry was authorized by that failed deploy workflow.

Facebook is not a supported user-facing adapter until isolated deploy plus a fresh, separately authorized acceptance run succeeds.

## Completion markers

`OWNER_ONLY_ZERO_CLIENT_YOUTUBE = COMPLETE`

`OWNER_ONLY_MANAGED_INSTAGRAM_REEL = COMPLETE`

`CRITICPROFILE_TWO_STAGE_GATE_RUNTIME = ACCEPTED`

These completion markers apply only to the accepted owner-only private MEDIA BETA paths. They do not authorize public rollout, external testers, production merge, private/authenticated media, automatic AI fallback, Facebook, Telegram, or local upload.

## Next task

`Synchronize the strengthened cross-check Builder Instructions, then continue A9.6 Facebook isolated remediation and acceptance without replaying any uncertain-charge operation.`

Required sequence:
1. synchronize the current Builder Instructions into the actual private GPT and save/update;
2. run a compact non-billable text-research regression confirming the cross-check protocol contract;
3. deploy the committed Facebook nested-result parser remediation to the isolated MEDIA BETA runtime and verify health/capability without billable provider calls;
4. use a fresh Facebook test operation only after a fresh quote and explicit user authorization;
5. validate native -> metadata-duration -> derived AI ceiling -> separate AI consent -> completed transcript;
6. after backend PASS, update KRC Action/Builder package if required and run an actual private-GPT Facebook zero-client E2E;
7. only then move to Telegram; local upload remains a separate transport gate.
