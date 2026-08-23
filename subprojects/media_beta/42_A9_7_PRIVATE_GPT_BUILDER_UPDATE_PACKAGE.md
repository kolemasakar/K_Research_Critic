# A9.7-I Private GPT Builder Update Package

Status: APPLIED_E2E_PENDING
Date: 2026-08-23
Scope: existing private owner-only `K-Research & Critic - MEDIA BETA` GPT

## Purpose

The A9.7-I Builder package has been applied to the actual private GPT. VoiceBridge runtime, Render, repository main, and merge state remain unchanged.

Applied media routing:

`YouTube -> existing native managed flow`

`Instagram Reel -> existing native flow -> separately consented AI fallback when required`

`Facebook Video/Reel -> Cobalt -> AssemblyAI -> durable KRCM`

Paid Facebook fallback remains outside normal routing:

`AWAITING_RETRIEVAL_CONSENT -> local one-credit quote -> NEW explicit user approval -> exactly one ScrapeCreators attempt`

ScrapeCreators is currently unconfigured and not live accepted. Automatic paid continuation is forbidden.

## Applied package files

Builder instructions:

`prompts/GPT_STORE_MEDIA_BETA_BUILDER_INSTRUCTIONS.md`

Action schema:

`gpt_store/actions/media_managed_beta_openapi.yaml`

Canonical long-form reference:

`prompts/GPT_STORE_MEDIA_MANAGED_BETA_INSTRUCTIONS.md`

Applied Builder version:

`instructions.version = 0.7-beta-a9.7-i`

Target Action schema version:

`instructions.builder_target_action_schema_version = 0.4.0-a9.7-c`

## Builder application record

The owner manually updated the existing private GPT in the ChatGPT web editor and pressed `Update` on 2026-08-23.

Before Update, the imported Action schema was verified in the GPT editor. The parser accepted all required operations after A9.7-I parser-compatibility hardening, including inline `job_id` path parameters and operation descriptions within the GPT Builder length limit.

A read-only `getManagedMediaCapability` Action check succeeded before Update and confirmed:
- managed MEDIA BETA available;
- YouTube, Instagram and Facebook enabled;
- Facebook free retrieval provider Cobalt configured;
- AssemblyAI configured;
- ScrapeCreators not configured;
- automatic AI/paid fallback disabled.

## Applied Action operations

The existing Action exposes:
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

Authentication remains API key / Bearer. Credentials remain server-side and are not stored in repository documentation.

## Expected Facebook behavior

For a public Facebook Video/Reel URL:
- no native Supadata preflight is shown first;
- GPT calls `startManagedFacebookFallback`;
- Cobalt is attempted without ScrapeCreators credit spend;
- if Cobalt succeeds, AssemblyAI STT and durable KRCM segments complete the transcript;
- if the job is `AWAITING_RETRIEVAL_CONSENT`, GPT stops before paid retrieval;
- GPT calls only the local `preflightManagedFacebookRetrievalCredit` before asking for a new one-credit approval;
- an earlier `1` never authorizes ScrapeCreators;
- no automatic paid retry is allowed.

## Runtime acceptance gate

Builder application is complete, but A9.7-I private-GPT E2E acceptance is still pending.

Current state:
- `builder_runtime_applied = true`;
- `gpt_builder_private_update_required = false`;
- `a9_7_i_private_gpt_e2e_complete = false`.

Run exactly one NEW-chat Facebook zero-client E2E under a separately stated cost/quota boundary. The acceptance attempt does not authorize ScrapeCreators implicitly. If paid fallback is encountered, stop and request a fresh explicit maximum-one-credit approval.

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

This package/application does not:
- modify VoiceBridge runtime;
- modify Render configuration;
- merge either repository;
- modify repository main;
- enable external tester rollout;
- mark the private GPT E2E accepted before a NEW-chat runtime test.
