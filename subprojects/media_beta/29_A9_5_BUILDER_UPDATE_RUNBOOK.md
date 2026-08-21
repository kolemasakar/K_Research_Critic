# A9.5 Private GPT Builder Update Runbook

Version: 1.0
Status: READY_TO_EXECUTE
Updated: 2026-08-21

## Purpose

Switch the actual private owner-only `K-Research & Critic - MEDIA BETA` GPT from the accepted A8 browser-assisted Action contract to the A9.5 managed zero-client Action contract.

This is a Builder configuration change only. Do not change the public GPT, VoiceBridge production, repository `main`, or sharing state.

## Preconditions

Accepted before this runbook:
- VoiceBridge managed native route is live in isolated beta;
- managed `KRCM_` jobs are durable and duplicate starts are credit-safe;
- private Action bearer authentication remains configured server-side;
- server-side owner beta admission works after bearer authentication;
- owner beta access code is no longer required in the GPT-facing request;
- KRC A9.5 package validation is green;
- current managed provider balance before a new billable acceptance is 98 credits;
- preflight cost estimate for current native mode is 1 credit.

## Builder changes

Open the existing private `K-Research & Critic - MEDIA BETA` GPT in the web GPT editor.

### Instructions

Replace the current Builder Instructions with the complete contents of:

`prompts/GPT_STORE_MEDIA_BETA_BUILDER_INSTRUCTIONS.md`

Required version semantics:
`0.5-beta-a9.5`

Do not append the new instructions to the old Helper instructions. Replace the old normal-flow contract so conflicting client-assisted instructions cannot remain active.

### Action schema

In the existing Action, replace the client-assisted schema with the complete contents of:

`gpt_store/actions/media_managed_beta_openapi.yaml`

Expected detected operation IDs:
- `preflightManagedMediaCredits`;
- `startManagedMediaNativeTranscription`;
- `getManagedMediaTranscriptionStatus`;
- `getManagedMediaTranscriptSegments`.

The schema must not contain `beta_access_code`.

### Authentication

Keep API-key authentication using Bearer mode and preserve the already configured private Action bearer secret.

Do not paste the bearer token into Instructions, Knowledge, chat, repository files or screenshots.

If the editor unexpectedly loses the existing authentication configuration, STOP rather than exposing or guessing the secret. Reconfigure it only from the secure owner credential source.

### Sharing

Keep the GPT private/owner-only (`Only me`).

Do not resume external tester or public sharing as part of A9.5.

### Save/update

Use the Builder update/save action only after the schema validates and the expected four managed operations are detected.

## First non-billable Preview test

Use the accepted source:

`https://www.youtube.com/watch?v=IzYyKRx7Qwg`

Initial prompt may be simply the URL, or URL plus desired analysis mode.

Expected GPT behavior before any transcript spend:
- no beta-code prompt;
- no Helper instruction;
- no request to open YouTube separately;
- no visible Job ID;
- managed preflight runs;
- user sees the current credit quote;
- GPT stops for explicit `1 - Так / 2 - Ні`.

Current backend preflight evidence before Builder switch was:

```text
credits_available: 98
estimated_credits: 1
credits_after_estimate: 97
```

The actual Preview must display fresh values returned at that time; do not hard-code 98/97 into the GPT.

## Billable acceptance gate

Do not continue to transcript processing until the fresh Preview quote is shown and the owner explicitly chooses `1`.

Option `2` or any ambiguous answer must result in no transcript call.

After explicit `1`, expected behavior:
- managed native request hard cap 1 credit;
- no owner beta-code prompt;
- no Helper;
- no manual `KRCM_` Job ID;
- status/segment retrieval handled internally;
- all transcript pages retrieved;
- if native unavailable, stop at `AWAITING_AI_CONSENT` and require a separate future AI quote/consent;
- if completed, continue into requested K-Research & Critic workflow.

For fact-check mode, CriticProfile approval remains mandatory before independent research.

## Acceptance markers

Non-billable Builder preflight acceptance:

`A9_5_PRIVATE_GPT_PREFLIGHT_ACCEPTED`

Full owner zero-client transcript + analysis acceptance:

`OWNER_ONLY_ZERO_CLIENT_COMPLETE`

Do not mark either state from repository package validation alone.

## Rollback

If Builder Preview fails:
- do not modify public GPT or production backend;
- retain the isolated A9.5 backend;
- use GPT version history or restore the prior Builder configuration if needed;
- A8 Helper 0.2.2 evidence remains the accepted fallback baseline;
- record exact failure class before changing backend code.
