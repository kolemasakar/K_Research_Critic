# A9.5 Private GPT Action Zero-Client Integration

Version: 1.0
Status: PACKAGE_AND_BACKEND_PREFLIGHT_ACCEPTED / PRIVATE_GPT_LIVE_E2E_PENDING
Accepted checkpoint: 2026-08-21

## Purpose

Record the A9.5 transition from the accepted browser-assisted A8 workflow to the owner-only managed zero-client Action contract.

This record does **not** mark A9.5 or the whole A9 phase complete. The actual private GPT Builder configuration and private-GPT end-to-end owner test remain pending.

## Required normal owner UX

```text
public YouTube URL in private GPT
 -> analysis mode if missing
 -> managed credit preflight
 -> explicit 1/2 credit decision
 -> managed native transcript after explicit 1 only
 -> internal status/segment retrieval
 -> no beta code from user
 -> no Helper
 -> no manual Job ID
 -> requested K-Research & Critic workflow
 -> result in the same conversation
```

## VoiceBridge implementation

Feature branch:
`agent/krc-media-transcript`

Code change:
- managed HTTP routes keep bearer authentication mandatory;
- only after successful bearer authentication, the owner beta admission code is injected server-side from isolated runtime configuration when the Action request does not contain one;
- missing or invalid bearer is rejected before owner admission injection;
- the underlying managed service continues to use the existing beta gate, durable request key, credit gate and Postgres idempotency contract.

CI-green implementation commit:

`970d7cc5819a623ec1d3cc7a70aceb44bfe311b9`

Validation:
- VoiceBridge Validate #278;
- run `32440143389`;
- result: SUCCESS.

## Isolated live deployment and preflight acceptance

Target only:
`voicebridge-krc-media-beta-kolemasakar`

Live code:
`970d7cc5819a623ec1d3cc7a70aceb44bfe311b9`

Workflow:
- run `32440430655`;
- job `96649891795`;
- result: SUCCESS.

Accepted runtime facts:

```text
health: ok
user_beta_access_code_required: false
owner_access_injected_server_side: true
provider: supadata/native
credit_preflight_required: true
automatic_ai_fallback: false
credits_available: 98
estimated_native_cost: 1
estimated_after: 97
```

The acceptance called only managed capability and preflight endpoints. It did not call the transcript endpoint and spent no transcript credit.

Production VoiceBridge and `main` were not targeted.

The one-time A9.5 deploy/preflight workflow was removed after acceptance so future branch synchronization cannot repeat the acceptance automatically.

## KRC private GPT package

Feature branch:
`agent/video-url-research`

Updated package components:
- `gpt_store/actions/media_managed_beta_openapi.yaml`;
- `prompts/GPT_STORE_MEDIA_BETA_BUILDER_INSTRUCTIONS.md`;
- `prompts/GPT_STORE_MEDIA_MANAGED_BETA_INSTRUCTIONS.md`;
- `gpt_store/media_beta_manifest.yaml`;
- `scripts/validate_store_package.py`;
- `tests/test_media_beta_managed_package.py`.

User-facing Action schema now requires only URL plus optional language hint for preflight. `beta_access_code` is absent from the GPT-facing schema.

Builder instructions require:
- Ukrainian by default;
- no owner beta code request;
- no Helper or separate media opening in normal owner flow;
- mandatory managed credit preflight;
- explicit `1 - Так / 2 - Ні` before billable native transcript start;
- no automatic AI fallback;
- no visible `KRCM_` Job ID in normal UX;
- all transcript pages retrieved internally;
- CriticProfile approval before independent research in fact-check mode.

KRC package validation commit:

`cfb01afb44551519612994cf60918d6c822ffccc`

Validation:
- Tests #545;
- run `32440399651`;
- result: SUCCESS.

## Remaining A9.5 live gate

Before A9.5 can be marked complete:
- update the actual private Custom GPT Builder to the A9.5 Builder instructions;
- replace the old client-assisted Action schema with the managed Action schema;
- keep Action bearer authentication configured with the existing server-side credential;
- keep the GPT private/owner-only;
- run a real owner test from the private GPT;
- confirm the GPT shows the current credit quote and waits for explicit `1` before transcript spend;
- after consent, confirm transcript/status/segment handling occurs without Helper, visible Job ID or beta-code prompt;
- complete the requested analysis in the same conversation.

A billable private-GPT transcript acceptance must not be started until a fresh preflight quote is shown and the owner explicitly replies `1`.

## Checkpoint marker

`A9_5_PACKAGE_AND_BACKEND_PREFLIGHT_READY / A9_5_PRIVATE_GPT_LIVE_CONFIG_PENDING`
