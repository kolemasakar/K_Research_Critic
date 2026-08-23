# A9.7-I Private GPT Builder Update Package

Status: PACKAGE_READY_NOT_APPLIED
Date: 2026-08-23
Scope: existing private owner-only `K-Research & Critic - MEDIA BETA` GPT

## Purpose

Apply the already accepted A9.7 Facebook free path to the actual private GPT without changing VoiceBridge runtime, Render, repository main, or merge state.

Target media routing after Builder update:

`YouTube -> existing native managed flow`

`Instagram Reel -> existing native flow -> separately consented AI fallback when required`

`Facebook Video/Reel -> Cobalt -> AssemblyAI -> durable KRCM`

Paid Facebook fallback remains outside normal routing:

`AWAITING_RETRIEVAL_CONSENT -> local one-credit quote -> NEW explicit user approval -> exactly one ScrapeCreators attempt`

ScrapeCreators is currently unconfigured and not live accepted. Automatic paid continuation is forbidden.

## Package files

Builder instructions to paste into the GPT editor:

`prompts/GPT_STORE_MEDIA_BETA_BUILDER_INSTRUCTIONS.md`

Target Action schema to paste/import into the existing Action:

`gpt_store/actions/media_managed_beta_openapi.yaml`

Canonical long-form reference:

`prompts/GPT_STORE_MEDIA_MANAGED_BETA_INSTRUCTIONS.md`

Manifest package version:

`instructions.builder_package_version = 0.7-beta-a9.7-i`

Target Action schema version:

`instructions.builder_target_action_schema_version = 0.4.0-a9.7-c`

The legacy `instructions.version = 0.6-beta-a9.6` intentionally remains the currently applied Builder version until the owner actually presses Update in the GPT editor.

## Exact Builder procedure

Use ChatGPT on the web. Existing GPT editing is performed through the GPT editor.

1. Open `Explore GPTs` / `My GPTs`.
2. Select the existing private `K-Research & Critic - MEDIA BETA` GPT.
3. Select `Edit GPT`.
4. In Configure/Instructions, replace the complete Instructions field with the complete contents of `prompts/GPT_STORE_MEDIA_BETA_BUILDER_INSTRUCTIONS.md`.
5. Keep capabilities aligned with the manifest: Web search ON; Code Interpreter/Data Analysis ON; Image generation OFF; Apps OFF; Actions ON.
6. Open the existing media Action. Do not create a second competing media Action.
7. Keep authentication as API key / Bearer. Do not expose, rotate, paste into chat, or document the secret. If the editor preserves the existing bearer secret, leave it unchanged. If the editor explicitly requires the secret again, enter the existing `KRC_MEDIA_ACTION_TOKEN` directly in the editor from the owner's secret store.
8. Replace the Action schema with the complete contents of `gpt_store/actions/media_managed_beta_openapi.yaml`.
9. Confirm the schema validates and exposes these operation IDs:
   - `getManagedMediaCapability`
   - `preflightManagedMediaCredits`
   - `startManagedMediaNativeTranscription`
   - `startManagedFacebookFallback`
   - `getManagedMediaTranscriptionStatus`
   - `getManagedMediaTranscriptSegments`
   - `preflightManagedFacebookRetrievalCredit`
   - `continueManagedFacebookPaidRetrieval`
   - `preflightManagedMediaAiCredits`
   - `startManagedMediaAiTranscription`
10. Do not execute a Facebook media request during configuration merely to test the schema. Schema validation itself is sufficient for this package-application step.
11. Select `Update` to apply the draft changes to the existing private GPT.
12. After Update, start a NEW chat with the private GPT for runtime acceptance. Do not reuse an old chat as A9.7-I runtime evidence.

## Expected Facebook behavior after Update

For a public Facebook Video/Reel URL:
- no native Supadata preflight is shown first;
- GPT calls `startManagedFacebookFallback`;
- Cobalt is attempted without ScrapeCreators credit spend;
- if Cobalt succeeds, AssemblyAI STT and durable KRCM segments complete the transcript;
- if the job is `AWAITING_RETRIEVAL_CONSENT`, GPT stops before paid retrieval;
- GPT calls only the local `preflightManagedFacebookRetrievalCredit` before asking for a new one-credit approval;
- an earlier `1` never authorizes ScrapeCreators;
- no automatic paid retry is allowed.

## Runtime acceptance gate after manual application

The Builder package being ready does NOT mean the actual GPT has been updated.

Until the owner confirms the editor Update was completed:
- `builder_runtime_applied = false`;
- `gpt_builder_private_update_required = true`;
- `a9_7_i_private_gpt_e2e_complete = false`.

After owner confirmation, run exactly one NEW-chat Facebook zero-client E2E under a separately stated cost/quota boundary. The acceptance attempt must not authorize ScrapeCreators implicitly. If paid fallback is encountered, stop and request a fresh explicit maximum-one-credit approval.

## Acceptance criteria

A9.7-I runtime acceptance requires all of the following:
- actual private GPT uses the A9.7-I Builder instructions;
- actual Action schema is `0.4.0-a9.7-c`;
- public Facebook URL is routed to `startManagedFacebookFallback` rather than Supadata native/generate;
- no Helper, beta code, Job ID, cookies, or separate media opening is requested;
- successful Cobalt path returns durable transcript segments in the same conversation;
- ScrapeCreators is not invoked without a separate local preflight plus a NEW explicit approval;
- report language remains Ukrainian by default;
- CriticProfile gate and claim-level cross-check/traceability contract remain intact.

## Non-goals

This package does not:
- modify VoiceBridge runtime;
- modify Render configuration;
- call Facebook, Cobalt, AssemblyAI, Supadata, or ScrapeCreators;
- merge either repository;
- modify repository main;
- enable external tester rollout;
- mark the actual private GPT runtime as accepted before a NEW-chat E2E.
