# GPT_STORE_PACKAGE
Опис public Core пакета та окремого private MEDIA BETA пакета.

Version: 2.1
Status: CORE_PUBLISHED / MEDIA_BETA_OWNER_ACCEPTED_RELEASE_HOLD
Updated: 2026-08-27

## 1. Package Separation

K-Research & Critic has two intentionally separate package scopes.

### Public Core

```text
gpt_store/manifest.yaml
prompts/GPT_STORE_INSTRUCTIONS.md
gpt_store/checkpoint.py
gpt_store/checkpoint_example.json
```

The public Core is published and remains the production baseline. Its normal text workflow has no mandatory external backend or developer API key.

### Private MEDIA BETA

```text
gpt_store/media_beta_manifest.yaml
prompts/GPT_STORE_MEDIA_BETA_BUILDER_INSTRUCTIONS.md
prompts/GPT_STORE_MEDIA_MANAGED_BETA_INSTRUCTIONS.md
gpt_store/actions/media_managed_beta_openapi.yaml
docs/PRIVACY_POLICY.md
```

Current private package versions:

```text
Builder package: 0.9.1-beta-a10
Action schema:   0.6.0-a9.10
```

Private Action server:

```text
https://voicebridge-krc-media-beta-kolemasakar.onrender.com
```

## 2. Private Builder Configuration

Name:

```text
K-Research & Critic - MEDIA BETA
```

Capabilities:

```text
Web search: enabled
Code Interpreter & Data Analysis: enabled
Actions: enabled
Apps: disabled
Image generation: disabled
```

Authentication:

```text
bearer/API-key secret configured in Builder and isolated backend
```

Never place the secret in repository content or user-visible output.

## 3. Accepted Private Media Inputs

```text
prerecorded YouTube
Instagram Reel
public Facebook Video/Reel through free Cobalt
supported public Telegram video post
one current-conversation local audio/video attachment
```

Public/private platform credentials are not part of the accepted flow.

## 4. Current Action Contract

Primary operation families:

```text
getManagedMediaCapability
preflightManagedMediaCredits
startManagedMediaNativeTranscription
startManagedFacebookFallback
startManagedTelegramPublicTranscription
startManagedAttachmentTranscription
probeManagedAttachmentTransport
getManagedMediaTranscriptionStatus
getManagedMediaTranscriptSegments
preflightManagedMediaAiCredits
startManagedMediaAiTranscription
```

Reserved Facebook paid-retrieval compatibility operations remain present in the schema for historical compatibility but are not active or offerable by the current Builder contract.

## 5. Cost/Consent Rules

- Supadata native billable work requires preflight and explicit user approval.
- Instagram AI generation requires a separate quote and a new approval.
- Facebook active retrieval is free Cobalt only; failure is unavailable/STOP.
- Telegram retrieval credits are zero and there is no paid fallback.
- Local attachment retrieval credits are zero; AssemblyAI STT accounting is separate.
- Uncertain-charge operations are never automatically replayed.

## 6. Workflow Mapping

```text
supported media input
 -> transcript acquisition
 -> material claim inventory
 -> CriticProfile draft
 -> explicit user approval/edit/cancel
 -> independent Research
 -> Critic
 -> bounded revision
 -> final report + protocol
```

The transcript is source content for what was said, not independent proof of truth.

## 7. Claim-Level Output Contract

For every material factual claim:
- exactly one verdict;
- timestamp/segment when relevant;
- visible evidence;
- confidence;
- required/achieved cross-check result;
- visible SHORTFALL when the requirement is not met.

A10 also requires both a normal four-column summary table and an identical fenced copy-safe table.

## 8. Persistence and Privacy

Managed media jobs and segments are durable backend state. The private GPT does not expose KRCM Job IDs. Full transcripts and reusable credentials are not stored in KRC checkpoints.

The privacy-policy source is `docs/PRIVACY_POLICY.md` and must reflect the active private-beta routing before any future public rollout.

## 9. Validation

Static package validation and the full repository CI suite protect the package. Actual ChatGPT UI behavior is validated separately when Builder/runtime changes are made.

Current runtime acceptance is documented in `subprojects/media_beta/` acceptance records and current-state/checkpoint files.

## 10. Current Release Boundary

```text
private owner runtime = ACCEPTED
merge to main = HOLD
production promotion = HOLD
external testers = HOLD
public rollout = HOLD
```

Do not convert private acceptance into production/public package state without a separate explicit owner release decision.
