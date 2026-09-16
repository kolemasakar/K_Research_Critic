# KRC — Sentinel cross-project Plugin rebase checkpoint — 2026-09-16

Status: **CROSS-PROJECT REBASE RECORDED / NO RELEASE MUTATION**

## Context

Sentinel Remote synchronized the OpenAI Custom GPT retirement impact across the projects it coordinates. KRC had already advanced further and established checkpoints 95–98, including migration preparation, Action→Plugin/MCP compatibility mapping, migration inventory, and a design-only Plugin migration skeleton.

This checkpoint does not replace those records. It records the cross-project architecture decision and confirms KRC alignment with the shared direction.

Source context: `kolemasakar/AI_general/docs/openai-custom-gpts-retirement-to-plugins-2026-09-16.md`.

## Canonical KRC direction

```text
PRIMARY_TARGET = KRC Plugin
LEGACY_TARGET  = existing Custom GPT until retirement
BUILDER_PREVIEW = optional legacy maintenance only
BUILDER_BLOCKS_PLUGIN_WORK = FALSE
```

Mapping remains:

- Core instructions → Plugin skill/workflow;
- R3 MEDIA routing/invariants → Plugin MEDIA skill/workflow policy;
- R3 OpenAPI Custom Action → App / Connector / custom MCP integration specification;
- VoiceBridge backend → preserve where compatible with the supported integration surface;
- regression plan → Plugin acceptance/regression suite.

## Cross-project coordination

Sentinel Remote is the private control-plane source for access metadata and cross-project platform-transition decisions. Public KRC repository evidence must remain non-secret and must not include browser profile identifiers, cookies, session material, API keys, bearer tokens, or credentials.

## Existing KRC migration package remains authoritative

The KRC-specific checkpoints 95–98 and associated `plugins/krc_migration_candidate/` design-only skeleton remain the detailed implementation baseline. This checkpoint adds no competing architecture and introduces no live Plugin/App/MCP deployment.

## Boundary

```text
PROJECT=ACTIVE
PLUGIN_MIGRATION_PREP=READY
PLUGIN_CANDIDATE_SKELETON=READY
LEGACY_PUBLIC_GPT=UNCHANGED
PUBLICATION=HOLD
PLUGIN_PUBLICATION=HOLD
MAIN_MUTATION=DENIED
RENDER_CHANGE=DENIED
PR22_MERGE=DENIED
PR45_MERGE=DENIED
```

No GPT publication/update/delete, Plugin installation/publication, Render mutation, main merge, PR #22 merge, or PR #45 merge is authorized by this checkpoint.
