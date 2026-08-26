# A9.7-I Facebook Policy Fix - Backend Hardening

Status: CODE_AND_CI_ACCEPTED / BUILDER_REAPPLY_PENDING
Date: 2026-08-26
Scope: isolated owner-only MEDIA BETA

## Purpose

Record the final A9.7-I policy correction for Facebook retrieval failure and align the KRC source of truth with the VoiceBridge backend enforcement.

Active policy:

`Cobalt failure -> media retrieval unavailable -> STOP`

ScrapeCreators is reserve-only and outside the active MEDIA BETA Facebook flow.

## Authority

KRC policy source:
- `prompts/GPT_STORE_MEDIA_BETA_BUILDER_INSTRUCTIONS.md`;
- `prompts/GPT_STORE_MEDIA_MANAGED_BETA_INSTRUCTIONS.md`;
- `gpt_store/media_beta_manifest.yaml`.

VoiceBridge implementation source:
- repo `kolemasakar/VoiceBridge`;
- branch `agent/krc-media-transcript`;
- commit `1b46f15588840eda5b8f14f5206fd966b69c4887`;
- commit message `A9: make Cobalt failure terminal unavailable`.

This record supersedes the active-routing interpretation in the earlier Builder application record `42_A9_7_PRIVATE_GPT_BUILDER_UPDATE_PACKAGE.md`. Record 42 remains historical evidence of what was previously applied to the private GPT.

## Backend changes

The VoiceBridge policy-hardening commit changes the active Facebook path so that:
- free Cobalt retrieval is attempted first;
- free success can continue to AssemblyAI STT;
- free failure raises `FACEBOOK_RETRIEVAL_UNAVAILABLE`;
- the managed job becomes terminal `FAILED` rather than `AWAITING_RETRIEVAL_CONSENT` for new active failures;
- `FacebookMediaRetrievalChain` never invokes the paid retriever after Cobalt failure;
- an explicitly supplied historical ScrapeCreators consent object does not activate paid fallback;
- preflight on the new terminal failed job is not applicable;
- duplicate starts reuse terminal durable state and do not replay Cobalt or a paid provider.

## Regression coverage

Updated Facebook retrieval tests cover:
- free Cobalt success with zero paid calls;
- Cobalt failure -> `FACEBOOK_RETRIEVAL_UNAVAILABLE`;
- no paid call without consent;
- no paid call even when a valid historical ScrapeCreators consent object is supplied;
- managed-service terminal failed state;
- paid-preflight rejection for the terminal failed job;
- durable duplicate reuse without retrieval replay.

Dedicated A9 regression expectation:

`NO automatic paid fallback`

The regression asserts `paidCalls == 0`.

## CI evidence

For VoiceBridge commit `1b46f15588840eda5b8f14f5206fd966b69c4887`:
- workflow `A9.7-F Cobalt Package Validate`: PASS;
- workflow `Validate`: PASS.

No repository merge was performed.

## ScrapeCreators boundary

ScrapeCreators code remains present as reserve/legacy compatibility code, but current MEDIA BETA policy does not offer or invoke it after Cobalt failure.

Historical paid-preflight/continuation Action operations may remain in schema version `0.4.0-a9.7-c` for compatibility. Their presence does not make them active.

Any future ScrapeCreators activation requires:
- a separate owner decision;
- explicit implementation/acceptance scope;
- fresh security/cost review;
- fresh tests and runtime acceptance.

No existing historical consent is sufficient.

## Private GPT Builder state

Repository Builder instructions already contain the corrected routing rule:
- Facebook -> `startManagedFacebookFallback`;
- Cobalt failure -> retrieval unavailable;
- stop media intake;
- do not call `preflightManagedFacebookRetrievalCredit`;
- do not call `continueManagedFacebookPaidRetrieval`;
- do not offer paid fallback.

The corrected policy has not yet been re-applied to the actual private GPT Builder runtime.

Authoritative marker:

`builder_policy_fix_runtime_applied = false`

Private-GPT Facebook A9.7-I E2E therefore remains pending.

## Next gate

1. Reapply the corrected Builder instructions to the actual private owner GPT.
2. Preserve the existing Action authentication and isolated beta server.
3. Run one fresh NEW-chat Facebook zero-client E2E.
4. Accept success only when the observed behavior matches one of these branches:
   - Cobalt success -> AssemblyAI -> durable KRCM transcript;
   - Cobalt failure -> retrieval unavailable -> STOP with zero paid retrieval calls.
5. Record Builder policy reapply and E2E evidence before changing any completion marker.

## Non-goals

This hardening does not:
- merge PR #8 or PR #28;
- change repository `main`;
- change production VoiceBridge;
- enable external tester rollout;
- enable ScrapeCreators;
- authorize private/authenticated media;
- authorize Telegram or local upload.
