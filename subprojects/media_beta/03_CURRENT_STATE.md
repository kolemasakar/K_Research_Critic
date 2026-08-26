# MEDIA BETA Current State

Canonical implementation checkpoint for continuation without reconstruction.

Version: 5.8
Status: ACTIVE_CHECKPOINT
Checkpoint date: 2026-08-26

## Executive state

Current phase state:

`A4_COMPLETE / A5_COMPLETE / A6_COMPLETE / A7_EXTERNAL_ROLLOUT_PAUSED / A8_BROWSER_ASSISTED_OWNER_BASELINE_COMPLETE / A9_1_COMPLETE / A9_2_DIRECT_YOUTUBE_BLOCKED / A9_2R_MANAGED_NATIVE_COMPLETE / A9_3_DURABLE_MANAGED_COMPLETE / A9_5_PRIVATE_GPT_ZERO_CLIENT_E2E_COMPLETE / A9_8_OWNER_ZERO_CLIENT_YOUTUBE_COMPLETE / A9_6_INSTAGRAM_MANAGED_COMPLETE / A9_6_FACEBOOK_SUPADATA_NOT_ACCEPTED / A9_7_FACEBOOK_COBALT_LIVE_ACCEPTED / A9_7_I_FACEBOOK_POLICY_BACKEND_HARDENED / A9_7_I_BUILDER_POLICY_APPLIED / A9_7_I_PRIVATE_GPT_E2E_ACCEPTED`

Accepted owner-only zero-client adapters:
- public prerecorded YouTube;
- public Instagram Reel through managed native first, with separately authorized AI fallback only when native transcript is unavailable;
- public Facebook Video/Reels through the free Cobalt retrieval path followed by AssemblyAI STT and durable KRCM persistence.

Deferred / not accepted:
- ScrapeCreators paid Facebook fallback: reserve-only, unconfigured, not live accepted and inactive in current MEDIA BETA routing;
- Telegram public video posts;
- local audio/video attachment.

The active Facebook failure policy is explicit, backend-enforced and now accepted in the actual private GPT:

`Cobalt/free retrieval failure -> FACEBOOK_RETRIEVAL_UNAVAILABLE -> terminal FAILED -> STOP`

No paid Facebook retrieval offer, preflight or continuation belongs to the active MEDIA BETA flow after Cobalt failure.

Repository `main`, external tester rollout, and production VoiceBridge remain outside the current merge gate.

## Repositories and isolation boundary

KRC:
- repo `kolemasakar/K_Research_Critic`;
- branch `agent/video-url-research`;
- draft PR #8;
- repository `main` unchanged.

VoiceBridge:
- repo `kolemasakar/VoiceBridge`;
- branch `agent/krc-media-transcript`;
- draft PR #28;
- repository `main` unchanged.

Isolated beta runtime remains separate from production. No production deployment or merge is authorized by this checkpoint.

## Accepted Research/Critic workflow

Two-stage CriticProfile gate is runtime accepted:
- profile created internally;
- first gate offers direct run / review-edit / cancel;
- explicit `1` approves before research;
- displayed profile edits remain `REVIEW_REQUIRED` until re-approved;
- approval records ISO-8601 timestamp.

Claim-level cross-check enforcement is runtime accepted:
- floors: `LOW>=0`, `MEDIUM>=1`, `HIGH>=2`, `CRITICAL>=3`;
- every material factual claim maintains `required / achieved_independent / exception`;
- independence is based on underlying evidence, not URL count;
- derivative reporting and systematic-review repetition are not double-counted;
- real shortfalls remain visible and qualified;
- Critic audits each material claim before PASS.

Evidence-origin traceability is runtime accepted in BOTH main Core and MEDIA BETA:
- each origin counted in `achieved_independent` is visibly attributable to the claim;
- achieved count cannot exceed visible independent origins;
- real shortfalls remain visible.

Canonical records:
- `31_CRITICPROFILE_GATE_UX_UPDATE.md`;
- `32_CRITICPROFILE_GATE_RUNTIME_ACCEPTANCE.md`;
- `33_CLAIM_LEVEL_CROSS_CHECK_ENFORCEMENT.md`;
- `34_CLAIM_LEVEL_CROSS_CHECK_RUNTIME_ACCEPTANCE.md`;
- `35_CORE_RUNTIME_TRACEABILITY_HARDENING.md`;
- `36_CORE_TRACEABILITY_RUNTIME_ACCEPTANCE.md`;
- `37_MEDIA_BETA_TRACEABILITY_ALIGNMENT.md`;
- `38_REPORT_LANGUAGE_LABEL_LOCALIZATION_HARDENING.md`;
- `39_REPORT_LANGUAGE_AND_MEDIA_TRACEABILITY_RUNTIME_ACCEPTANCE.md`.

## Report-language invariant

Default user-facing report language is Ukrainian unless the user explicitly requests another language.

The selected report language controls all user-visible workflow text, prompts, CriticProfile presentation, section/table labels, verdict labels, final report, claim verification and review protocol. Canonical English/internal keys remain internal unless explicitly requested.

Latest NEW-chat regressions in both actual Custom GPTs passed the localization contract recorded in `39_REPORT_LANGUAGE_AND_MEDIA_TRACEABILITY_RUNTIME_ACCEPTANCE.md`.

## Runtime markers

`CRITICPROFILE_TWO_STAGE_GATE_RUNTIME = ACCEPTED`

`CLAIM_LEVEL_CROSS_CHECK_RUNTIME = ACCEPTED`

`CORE_TRACEABILITY_HARDENING_RUNTIME = ACCEPTED`

`CORE_REPORT_LABEL_LOCALIZATION_RUNTIME = ACCEPTED`

`MEDIA_BETA_TRACEABILITY_LOGIC_RUNTIME = PASS`

`MEDIA_BETA_TRACEABILITY_HARDENING_RUNTIME = ACCEPTED`

`MEDIA_BETA_REPORT_LABEL_LOCALIZATION_RUNTIME = ACCEPTED`

`gpt_builder_private_update_required = false` is retained as a legacy compatibility marker.

`builder_policy_fix_runtime_applied = true` records the owner-confirmed corrected A9.7-I Builder-policy application on 2026-08-26.

`a9_7_i_private_gpt_e2e_complete = true` records the fresh NEW-chat Facebook policy E2E acceptance on 2026-08-26.

## Accepted owner media UX

```text
supported public media URL in ChatGPT
 -> analysis mode if missing
 -> no separate media opening
 -> no Helper
 -> no beta-code prompt
 -> no manual Job ID
 -> YouTube/Instagram: native managed credit preflight where applicable
 -> explicit user consent for billable native/Instagram AI operations
 -> Facebook: startManagedFacebookFallback directly
 -> Facebook Cobalt success: AssemblyAI -> durable KRCM transcript
 -> Facebook Cobalt failure: retrieval unavailable -> STOP
 -> no paid Facebook offer/preflight/continuation in active MEDIA BETA
 -> CriticProfile gate only after transcript availability
 -> Research -> Critic
 -> result in same conversation
```

Remote adapters remain public-only. Do not request platform login/password/cookies/session state/account tokens.

## Credit consent invariant

A billable managed transcript request must never start merely because a URL was pasted.
- native Supadata hard cap: 1 approved credit;
- Instagram AI fallback: separate quote + separate explicit approval;
- AI rate: 2 credits/minute;
- conservative maximum: 40 credits / 20 minutes;
- automatic AI fallback prohibited;
- `credit_charge_uncertain=true` operation must never be automatically retried or replayed.

For current Facebook routing there is no active paid retrieval consent gate because paid retrieval is outside active MEDIA BETA. Historical ScrapeCreators consent/preflight code does not authorize current use.

## Accepted A9 media milestones

### A9.2R - managed native YouTube

PASS. Supadata native zero-client path accepted. Initial owner E2E evidence: source language `ru`, 277 timestamped segments, 1 credit.

### A9.3 - durable managed jobs

PASS. Durable jobs restart-safe; duplicate start reuses completed job; uncertain interrupted provider operations are not replayed. Accepted VoiceBridge commit: `7736f2e7acc5abbb3415e3753d0ca022c1b8d7b2`.

### A9.5 / A9.8 - private GPT integration and owner YouTube E2E

PASS. Owner auth accepted; private GPT zero-client YouTube path complete. Accepted owner-auth commit: `970d7cc5819a623ec1d3cc7a70aceb44bfe311b9`.

### A9.6 - Instagram

PASS for isolated owner beta. Accepted flow: native 1 credit -> `AWAITING_AI_CONSENT` -> separate AI quote/approval -> generated transcript; source language `en`, 11 segments, cumulative 3 credits.

### A9.6 - Facebook Supadata route

HISTORICAL / NOT_ACCEPTED.

The failed/uncertain Supadata Facebook route remains historical and must not be replayed automatically. Canonical deferral record: `40_FACEBOOK_REMEDIATION_DEFERRED.md`.

### A9.7 - Facebook Cobalt free path

LIVE ACCEPTED for the isolated owner beta. H1 evidence: job `KRCM_0d2a512d-c90d-4b41-87b7-3d3f47d258bd` completed through `retrieval_provider=cobalt` and `provider=assemblyai`, with 0 retrieval credits, 23 STT seconds, 1 durable segment, 101 transcript characters, and successful durable reread/segments read. ScrapeCreators and Supadata were not called.

Canonical positive-path acceptance record: `41_A9_7_FACEBOOK_COBALT_LIVE_ACCEPTANCE.md`.

### A9.7-I - Facebook failure-policy hardening

ACCEPTED end-to-end for the current owner-only private MEDIA BETA policy boundary.

Authoritative VoiceBridge commit:

`1b46f15588840eda5b8f14f5206fd966b69c4887` - `A9: make Cobalt failure terminal unavailable`

Backend behavior:
- Cobalt/free retrieval failure becomes `FACEBOOK_RETRIEVAL_UNAVAILABLE`;
- active managed job becomes terminal `FAILED`;
- active retrieval chain does not call the paid retriever;
- supplying a valid historical ScrapeCreators consent object still does not trigger paid fallback;
- paid preflight is not applicable to the terminal failed job;
- duplicate starts reuse terminal durable state rather than replay retrieval.

Regression coverage explicitly asserts no paid fallback and `paidCalls == 0`.

Actual private-GPT NEW-chat acceptance on 2026-08-26:
- public Reel request routed into the free Facebook flow;
- free retrieval failed;
- GPT reported media retrieval unavailable and stopped;
- no paid Facebook fallback was offered;
- reported charged credits: `0`;
- no independent fact-check started without retrieval/transcription.

Canonical records:
- `43_A9_7_I_FACEBOOK_POLICY_FIX_BACKEND_HARDENING.md`;
- `44_A9_7_I_PRIVATE_GPT_FACEBOOK_POLICY_E2E_ACCEPTANCE.md`.

## Action-schema compatibility boundary

The current repository Action schema remains compatibility version `0.4.0-a9.7-c` and still exposes historical paid-preflight/continuation operation definitions. They are reserved compatibility surface only.

The active Builder instructions explicitly forbid calling or offering those operations after Cobalt failure. The backend also makes new Cobalt-failed jobs terminal, preventing the active route from entering the historical retrieval-consent state.

Historical durable jobs may still contain `AWAITING_RETRIEVAL_CONSENT`; this compatibility state does not define new-job routing policy.

## Private GPT state

The corrected Builder policy is applied and the owner NEW-chat Facebook policy E2E is accepted.

Current authoritative markers:
- `builder_package_ready = true`;
- `builder_runtime_applied = true`;
- `builder_policy_fix_runtime_applied = true`;
- `a9_7_i_private_gpt_e2e_complete = true`;
- `rollout_state = A9_7_I_PRIVATE_GPT_E2E_ACCEPTED`.

Positive-path Cobalt retrieval remains accepted by H1 backend evidence; the 2026-08-26 private-GPT acceptance specifically validates the corrected terminal failure behavior.

## Next task

Facebook A9.7-I is closed. Continue A9 zero-client expansion without changing production or public sharing state.

Remaining not-accepted ingress targets:
- Telegram public video posts;
- local audio/video attachment transport and ingestion.

The next implementation task is to audit the existing VoiceBridge/KRC code for Telegram public-media support and define the smallest isolated zero-client adapter path before writing code.
