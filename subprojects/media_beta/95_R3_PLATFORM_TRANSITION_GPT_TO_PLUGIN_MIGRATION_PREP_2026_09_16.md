# KRC MEDIA — R3 Platform Transition / GPT-to-Plugin Migration Prep — 2026-09-16
Зафіксовано зміну зовнішньої платформи OpenAI, яка впливає на подальшу інтеграцію KRC MEDIA та робить обхід Builder automation blocker недоцільним як основну стратегію.

Status: PLATFORM_TRANSITION_IDENTIFIED / GPT_BUILDER_PREVIEW_HOLD / PLUGIN_MIGRATION_PREP_READY / PUBLICATION_HOLD

## Trigger

OpenAI announced planned retirement of Custom GPTs and migration to Plugins.
Official migration guidance states that the transition affects all ChatGPT plans, while detailed dates currently describe the Enterprise rollout and other plans may vary.
Target migration experience date for affected Enterprise workspaces: 2026-09-17.
Existing GPTs remain usable until the applicable retirement date.

Official references:
- https://help.openai.com/en/articles/20001519
- https://help.openai.com/en/articles/20001256

## Migration semantics relevant to KRC

Planned migration behavior:
- GPT instructions become a skill in the replacement plugin.
- Connected apps can be added to the plugin as apps.
- Custom GPT Actions do NOT transfer automatically.
- Required integrations must be assessed and rebuilt using a supported connector or custom MCP app/server.
- The migrated plugin may behave differently and requires regression testing before users switch.

Therefore KRC must not assume that `gpt_store/actions/media_public_r3_openapi.yaml` will migrate automatically.

## KRC architectural mapping

Current KRC assets remain canonical preparation inputs:
- Core instructions: `prompts/GPT_STORE_INSTRUCTIONS.md`
- MEDIA addendum: `prompts/GPT_STORE_MEDIA_R3_PUBLIC_ADDENDUM.md`
- R3 Action contract: `gpt_store/actions/media_public_r3_openapi.yaml`
- regression plan: `subprojects/media_beta/91_R3_BUILDER_PREVIEW_REGRESSION_PLAN_2026_09_16.md`

Migration target concept:
```text
KRC Core instructions -> Plugin skill
KRC MEDIA routing/invariants -> Plugin skill + integration contract
VoiceBridge public MEDIA API -> supported app/connector or custom MCP-backed app
Cobalt remains backend-only infrastructure behind VoiceBridge
```

This is an architecture target, not an authorization to create, publish, migrate, or expose a plugin.

## Builder blocker reclassification

Checkpoint 94 remains valid:
```text
BROWSER_AUTOMATION_START=BLOCKED_BY_OPENAI_SAFETY_LAYER
AUTH_BLOCKER=CLOSED
BUILDER_MUTATION=NONE
```

Because OpenAI is actively transitioning Custom GPTs to Plugins, no further attempt should be made to bypass the browser automation safety layer.

## Required preparation before migration is available

1. Preserve authoritative Core instructions and MEDIA addendum.
2. Preserve reference material and representative Core/MEDIA test prompts.
3. Inventory the four accepted MEDIA routes and all free-only/fail-closed invariants.
4. Map each current Action operation to a future connector/MCP tool contract.
5. Preserve current VoiceBridge and Render runtime without mutation.
6. When migration becomes available for the owner account/workspace, inspect the generated plugin before changing the existing GPT.
7. Rebuild custom MEDIA integration explicitly; do not assume Action transfer.
8. Run Core + YouTube + Instagram + Facebook + Telegram regression on the replacement.
9. Keep the existing GPT available until the replacement is accepted and separately approved for switch-over.

## Current release boundary

```text
R3_REPOSITORY=READY
R3_PREVIEW_PAYLOAD=READY
R3_REGRESSION_PLAN=READY
SENTINEL_CHECKPOINT_92=ACCEPTED
BROWSER_AUTOMATION_START=BLOCKED_BY_OPENAI_SAFETY_LAYER
PLUGIN_MIGRATION_PREP=READY
PLUGIN_CREATION=NOT_AUTHORIZED
PLUGIN_PUBLICATION=NOT_AUTHORIZED
GPT_MIGRATION=NOT_AUTHORIZED
PUBLICATION=HOLD
MAIN_MUTATION=DENIED
RENDER_CHANGE=DENIED
PR22_MERGE=DENIED
PR45_MERGE=DENIED
```

## Next project step

Prepare a repository-side MEDIA Action -> MCP/app compatibility map and plugin regression inventory while waiting for the account-specific migration option. Do not perform Builder automation bypass attempts and do not migrate or publish without explicit owner authorization.
