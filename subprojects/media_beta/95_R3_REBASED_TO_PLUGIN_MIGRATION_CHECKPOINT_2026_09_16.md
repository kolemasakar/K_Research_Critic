# KRC MEDIA — R3 rebased to Plugin migration — 2026-09-16

Status: **R3 MIGRATION SOURCE PACKAGE READY / BUILDER NO LONGER STRATEGIC BLOCKER / PUBLICATION HOLD**

## Trigger

OpenAI has announced retirement of Custom GPTs and migration toward Plugins. The existing KRC R3 repository package is therefore reclassified from a long-term Custom GPT Builder target into a migration source package for a future KRC Plugin.

Source context: `kolemasakar/AI_general/docs/openai-custom-gpts-retirement-to-plugins-2026-09-16.md`.

## Strategic rebase

```text
PRIMARY_TARGET = KRC Plugin
LEGACY_TARGET  = existing Custom GPT until retirement

GPT Core instructions
-> Plugin Core skill/workflow

R3 MEDIA addendum
-> Plugin MEDIA skill/workflow policy

R3 OpenAPI Custom Action
-> App / Connector / custom MCP integration specification

Builder regression plan
-> Plugin regression / acceptance suite
```

The existing public/legacy GPT may remain operational while useful, but Builder integration is no longer a blocker for continued KRC product development.

## Assets preserved as migration inputs

- `prompts/GPT_STORE_INSTRUCTIONS.md` — canonical Core behavior source;
- `prompts/GPT_STORE_MEDIA_R3_PUBLIC_ADDENDUM.md` — MEDIA routing/policy source;
- `gpt_store/actions/media_public_r3_openapi.yaml` — integration contract/source specification; do not assume automatic Action migration;
- `subprojects/media_beta/91_R3_BUILDER_PREVIEW_REGRESSION_PLAN_2026_09_16.md` — regression matrix to be reused/adapted for Plugin acceptance;
- `subprojects/media_beta/92_R3_BUILDER_PREVIEW_SENTINEL_EXECUTION_PACKAGE_2026_09_16.md` — retained as historical bounded Builder execution package, no longer the strategic next step;
- current VoiceBridge backend/runtime evidence — preserve independently of the ChatGPT deployment wrapper.

## New migration workstream

1. Inventory current KRC GPT instructions, knowledge/reference assets, Actions/auth and sharing assumptions.
2. Extract Core into Plugin skill/workflow without changing CriticProfile, evidence, cross-check or traceability invariants.
3. Extract MEDIA behavior into a Plugin-compatible workflow layer.
4. Map each R3 OpenAPI operation to supported App / Connector / custom MCP primitives.
5. Preserve the VoiceBridge backend where compatible; change only the ChatGPT-facing integration layer where necessary.
6. Adapt regression plan 91 for Plugin testing: Core, YouTube, Instagram, Facebook, Telegram.
7. Build a private Plugin candidate.
8. Validate legacy GPT vs Plugin behavior in parallel.
9. Configure sharing/publication only after separate owner approval.

## Builder status after rebase

```text
AUTH_BLOCKER=CLOSED
BUILDER_UI_CONTROL=PARTIAL
BROWSER_AUTOMATION_START=PRESTART_BLOCKED_IN_SENTINEL_ATTEMPT
BUILDER_PREVIEW=OPTIONAL_LEGACY_MAINTENANCE
BUILDER_BLOCKS_PLUGIN_WORK=FALSE
```

Do not spend disproportionate engineering effort bypassing Builder/browser restrictions unless needed to keep the legacy GPT operational before retirement.

## Release / mutation boundary

```text
R3_REPOSITORY=READY
R3_MIGRATION_SOURCE_PACKAGE=READY
PLUGIN_DESIGN=NEXT_STRATEGIC_WORKSTREAM
PUBLICATION=HOLD
MAIN_MUTATION=DENIED
RENDER_CHANGE=DENIED
PR22_MERGE=DENIED
PR45_MERGE=DENIED
LEGACY_GPT_DELETE=DENIED
PLUGIN_PUBLICATION=HOLD
```

This checkpoint changes strategic direction only. It does not publish/migrate the GPT, merge PR #22, merge PR #45, mutate Render, or change production runtime.
