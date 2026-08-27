# MEDIA BETA Current State

Canonical implementation checkpoint for continuation without reconstruction.

Version: 6.4
Status: ACTIVE_CHECKPOINT
Checkpoint date: 2026-08-27

## Executive state

Current phase state:

`A4_COMPLETE / A5_COMPLETE / A6_COMPLETE / A7_EXTERNAL_ROLLOUT_PAUSED / A8_BROWSER_ASSISTED_OWNER_BASELINE_COMPLETE / A9_OWNER_ZERO_CLIENT_MEDIA_INPUT_ACCEPTED / YOUTUBE_ACCEPTED / INSTAGRAM_ACCEPTED / FACEBOOK_COBALT_ACCEPTED / FACEBOOK_FAILURE_POLICY_E2E_ACCEPTED / TELEGRAM_ACCEPTED / LOCAL_ATTACHMENT_PRIVATE_GPT_E2E_ACCEPTED / A10_COPY_SAFE_CLAIM_TABLE_RUNTIME_ACCEPTED / RELEASE_HOLD_OWNER_TESTING`

A9 owner-zero-client media ingress and A10 presentation stabilization are accepted for the private owner runtime. The owner has explicitly chosen an extended private testing period before any release decision.

Accepted owner-only zero-client ingress:
- prerecorded YouTube;
- Instagram Reel;
- Facebook Video/Reel through free Cobalt retrieval -> AssemblyAI -> durable KRCM;
- supported public Telegram video posts through public Telegram web/embed retrieval -> trusted Telegram CDN -> AssemblyAI -> durable KRCM;
- one local audio/video attachment from the current ChatGPT conversation through `openaiFileIdRefs` -> trusted OpenAI attachment delivery -> AssemblyAI -> durable KRCM.

Historical/not-active boundaries:
- Facebook Supadata route is historical/not accepted;
- ScrapeCreators paid Facebook fallback is reserve-only, unconfigured, inactive and not offerable;
- private/authenticated Telegram retrieval is unsupported;
- paid Telegram fallback is unsupported;
- A8 Helper is fallback evidence only and is not normal owner UX.

Repository `main`, production VoiceBridge, external tester rollout and public sharing remain outside the current release gate.

## Repositories and isolation boundary

KRC:
- repo `kolemasakar/K_Research_Critic`;
- branch `agent/video-url-research`;
- implementation baseline before release-hold metadata: `c8588ec1f13c3c576d3f307a001c1d8964b5128e`;
- draft PR #8;
- `main` unchanged.

VoiceBridge:
- repo `kolemasakar/VoiceBridge`;
- branch `agent/krc-media-transcript`;
- implementation head at checkpoint: `20afd2e54b87b4a2a8858961a03e22f78a565189`;
- draft PR #28;
- `main` unchanged.

Isolated beta runtime:
- Render service `voicebridge-krc-media-beta-kolemasakar`;
- production VoiceBridge not targeted.

## Accepted Research/Critic workflow

Two-stage CriticProfile gate is runtime accepted:
- profile created before independent research;
- first gate offers direct run / review-edit / cancel;
- explicit `1` approves before research;
- material profile changes require re-approval.

Claim-level cross-check enforcement is runtime accepted:
- floors `LOW>=0`, `MEDIUM>=1`, `HIGH>=2`, `CRITICAL>=3`;
- every material factual claim maintains `required / achieved_independent / exception`;
- independence is based on underlying evidence, not URL count;
- real shortfalls remain visible and qualified;
- achieved cannot exceed visible independent evidence origins;
- Critic audits material claims before PASS.

Report language defaults to Ukrainian unless explicitly changed by the user.

## A9 accepted runtime markers retained

`CRITICPROFILE_TWO_STAGE_GATE_RUNTIME = ACCEPTED`

`CLAIM_LEVEL_CROSS_CHECK_RUNTIME = ACCEPTED`

`CORE_TRACEABILITY_HARDENING_RUNTIME = ACCEPTED`

`CORE_REPORT_LABEL_LOCALIZATION_RUNTIME = ACCEPTED`

`MEDIA_BETA_TRACEABILITY_HARDENING_RUNTIME = ACCEPTED`

`MEDIA_BETA_REPORT_LABEL_LOCALIZATION_RUNTIME = ACCEPTED`

`a9_7_i_private_gpt_e2e_complete = true`

`managed_telegram_private_gpt_e2e_complete = true`

`managed_attachment_transport_live_accepted = true`

`managed_attachment_ingestion_live_accepted = true`

`managed_attachment_private_gpt_e2e_complete = true`

`rollout_state = A9_10_ATTACHMENT_PRIVATE_GPT_E2E_ACCEPTED`

## A10 stabilization - accepted

Builder package:
- `0.9.1-beta-a10`;
- Action schema `0.6.0-a9.10` unchanged;
- strict four-column Markdown claim-summary contract;
- mandatory fenced copy-safe duplicate;
- backend/VoiceBridge unchanged.

### Runtime evidence

Fresh private-GPT regression against `https://t.me/techcrimes/12107`:

- normal CriticProfile gate: PASS;
- owner selected `1`;
- visible `ПІДСУМОК ЗА ТВЕРДЖЕННЯМИ`: PASS as four distinct columns;
- visible claim values: `3/1 NONE`, `2/1 NONE`, `2/1 NONE`, `0/1 SHORTFALL`;
- real SHORTFALL preserved and final status `ЗАВЕРШЕНО З ОБМЕЖЕННЯМИ`;
- media/STT `53 s / 53 s`, credits `0`;
- ordinary whole-response Copy still collapses the rendered table header because of ChatGPT UI serialization;
- `КОПІЯ ДЛЯ НАДІЙНОГО КОПІЮВАННЯ` survives whole-response Copy with literal `|` delimiters;
- copied fenced-table rows and values exactly match the visible table.

The remaining rendered-table Copy defect is treated as an external UI limitation. The fenced duplicate is the accepted mitigation.

Authoritative A10 markers:
- `builder_runtime_applied = true`;
- `claim_summary_table_hardening_package_ready = true`;
- `claim_summary_table_hardening_runtime_applied = true`;
- `a10_claim_summary_table_runtime_accepted = true`;
- `a10_copy_safe_claim_table_runtime_accepted = true`;
- `gpt_builder_private_update_required = false`;
- `stabilization_state = A10_COPY_SAFE_CLAIM_TABLE_RUNTIME_ACCEPTED`.

Canonical records:
- `51_A10_STABILIZATION_AND_RELEASE_BOUNDARY.md`;
- `52_A10_SAFE_TABLE_RUNTIME_ACCEPTANCE.md`.

## Accepted owner media UX

```text
supported public media URL OR one local audio/video attachment
 -> no Helper / beta code / manual Job ID / platform login
 -> route by source type
 -> transcript acquisition
 -> CriticProfile gate only after transcript availability
 -> explicit owner approval
 -> Research -> Critic
 -> localized final report in same conversation
```

Routes:

```text
YouTube/Instagram
 -> managed native first where applicable
 -> billable Supadata operations retain explicit consent gates

Facebook
 -> startManagedFacebookFallback
 -> Cobalt success -> AssemblyAI -> durable KRCM
 -> Cobalt failure -> media unavailable -> STOP
 -> no active paid Facebook continuation

Telegram
 -> startManagedTelegramPublicTranscription
 -> public Telegram web/embed -> trusted Telegram CDN
 -> AssemblyAI -> durable KRCM
 -> retrieval credits 0
 -> unavailable/no-speech -> STOP
 -> no login/cookies/session/bot token or paid fallback

Local attachment
 -> startManagedAttachmentTranscription
 -> openaiFileIdRefs
 -> trusted *.oaiusercontent.com temporary delivery
 -> bounded ingestion / media normalization
 -> AssemblyAI -> durable KRCM
 -> retrieval credits 0
 -> no Helper or user-facing attachment token
```

## A9.10 local attachment accepted state

Actual owner test:
- local `videoplayback (1).mp4`, approximately 5 MB;
- canonical CriticProfile gate reached;
- owner selected `1`;
- AssemblyAI language confidence `0.9984`;
- source duration `70.668 s`;
- STT accounting `71 s`;
- two durable transcript segments;
- retrieval/provider credits `0`;
- seven material claims evaluated;
- real `0/1 - SHORTFALL` preserved;
- reliability `88/100`;
- final status `COMPLETED_WITH_LIMITATIONS`;
- no KRCM Job ID, OpenAI file ID, signed URL or provider credential exposed.

Canonical records:
- `49_A9_10_ATTACHMENT_TRANSPORT_RUNTIME_ACCEPTANCE.md`;
- `50_A9_10_PRIVATE_GPT_LOCAL_ATTACHMENT_E2E_ACCEPTANCE.md`.

## Credit and replay invariants

- local attachment retrieval credits `0`; AssemblyAI STT accounted separately;
- Telegram public retrieval credits `0`, no paid fallback;
- Facebook active retrieval free Cobalt-only;
- Supadata native hard cap one explicitly approved credit;
- Instagram AI fallback requires separate quote and explicit consent;
- automatic managed AI fallback prohibited;
- `credit_charge_uncertain=true` operations never automatically retried;
- durable duplicate starts reuse existing jobs where defined.

## Release hold owner testing checkpoint

Canonical checkpoint:

`53_RELEASE_HOLD_OWNER_TESTING_CHECKPOINT.md`

Owner decision captured on 2026-08-27:

```text
merge KRC feature branch to main = HOLD
production VoiceBridge promotion = HOLD
external tester onboarding = HOLD
public sharing / Store rollout = HOLD
```

Operational mode is continued private owner testing. Defects found during this period are to be fixed and revalidated in the isolated feature branches unless the owner explicitly changes the release decision.

Last verified implementation CI before the release-hold metadata commits:
- workflow `Tests`;
- run `33010660835`;
- head `c8588ec1f13c3c576d3f307a001c1d8964b5128e`;
- conclusion `SUCCESS`.

## Current next boundary

No additional A10 Builder/runtime repair is pending.

Current work mode is `RELEASE_HOLD_OWNER_TESTING`.

A later owner decision must separately authorize any of:
1. merge KRC feature branch to `main`;
2. production VoiceBridge promotion;
3. external tester onboarding;
4. public sharing/Store rollout.

Authorization for one release gate must not be inferred as authorization for another. Until separately authorized, all four remain paused.
