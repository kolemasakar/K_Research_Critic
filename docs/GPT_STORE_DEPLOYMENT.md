# GPT_STORE_DEPLOYMENT
Модель розгортання public Core та окремого приватного MEDIA BETA.

Version: 1.3
Status: CORE_PUBLISHED / MEDIA_BETA_RELEASE_HOLD
Updated: 2026-08-27

## 1. Public Core Decision

K-Research & Critic is GPT Store-first. The public Core is already published and remains the production baseline.

Core runtime policy:

```text
channel: chatgpt_store
model_policy: user_plan
developer_api_key_required: false
external_backend_required: false
recommended_model: null
publication_state: published
```

The public text workflow does not require the MEDIA BETA backend.

## 2. Private MEDIA BETA Deployment Profile

The private media test product is separate:

```text
name: K-Research & Critic - MEDIA BETA
channel: chatgpt_private_beta
publication_state: private_owner_only
KRC branch: agent/video-url-research
VoiceBridge branch: agent/krc-media-transcript
backend: voicebridge-krc-media-beta-kolemasakar
```

Current Builder package:

```text
instructions: prompts/GPT_STORE_MEDIA_BETA_BUILDER_INSTRUCTIONS.md
canonical reference: prompts/GPT_STORE_MEDIA_MANAGED_BETA_INSTRUCTIONS.md
Action schema: gpt_store/actions/media_managed_beta_openapi.yaml
Builder version: 0.9.1-beta-a10
Action schema version: 0.6.0-a9.10
```

The Action uses bearer authentication. The bearer, owner admission value, and provider credentials remain server-side.

## 3. Accepted Private Runtime

Owner-only runtime acceptance exists for:
- YouTube;
- Instagram Reel;
- Facebook free Cobalt path;
- supported public Telegram video posts;
- one local current-conversation audio/video attachment.

A9/A9.10 media ingestion and A10 copy-safe report output are accepted for the private owner runtime.

## 4. Core vs Media Secret Boundary

Public Core requires no developer secret for its normal text workflow.

Private media ingestion requires developer-managed external-service credentials, but users are never asked for those credentials. The private Action bearer and provider keys must not appear in prompts, Knowledge, checkpoints, screenshots, logs, or user-facing reports.

## 5. Release Hold

Current release decision:

```text
merge media feature to main = HOLD
production VoiceBridge promotion = HOLD
external media testers = HOLD
public/Store media rollout = HOLD
```

Green private-beta CI or runtime acceptance does not authorize any of those transitions.

## 6. Later Merge Gate

A future merge decision means accepting the media feature changes into the KRC `main` codebase. Merge alone does not authorize production backend promotion or public access.

## 7. Later Production Promotion Gate

A future production promotion decision must separately validate production environment/secrets, persistence, quotas, health checks, logging, monitoring, rollback, and real smoke tests. The current isolated Render service must not be treated as an automatic production target.

## 8. Later External Tester Gate

External tester onboarding requires an explicit owner decision plus access-control, privacy, error-reporting, quota, and feedback procedures appropriate to additional users.

## 9. Later Public Rollout Gate

Before public sharing/Store rollout, re-verify current OpenAI Custom GPT/Action publication requirements, privacy-policy requirements, provider terms/data handling, scaling/resource controls, monitoring, support, and rollback.

No historical platform assumption is a permanent release waiver.

## 10. Persistence and Recovery

Core cross-chat continuation retains the explicit `K_SUPERVISOR_CHECKPOINT` schema where applicable. Full media transcripts and reusable credentials are not stored in KRC checkpoints.

Managed media jobs use durable KRCM backend state; normal users are not shown those internal Job IDs.

## 11. Validation

After repository package changes, keep the deterministic CI matrix green. Manual ChatGPT Builder/runtime verification is required only when an actual Builder package changes or when a release gate is opened.

The documentation-only audit does not require re-applying the already accepted Builder package.
