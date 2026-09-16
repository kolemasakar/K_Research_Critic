# KRC — Plugin-First Strategy Decision — 2026-09-16

Status: **PLUGIN_FIRST_ACCEPTED / LEGACY_ACTION_CREATION_HOLD / PUBLIC_GPT_UNCHANGED / PUBLICATION_HOLD**

## Trigger

OpenAI has announced the planned retirement of Custom GPTs and migration toward Plugins. Current official guidance states that:

- existing Custom GPTs remain usable until the applicable retirement date;
- GPT instructions are intended to migrate into a Plugin skill;
- Plugins combine reusable skills with connected apps/capabilities;
- Custom GPT Actions do **not** transfer automatically through migration;
- required integrations must be rebuilt through a supported connector/app or custom MCP server;
- migrated replacement plugins require explicit regression and access/sharing validation;
- account/workspace migration availability can vary by rollout.

Canonical external research input:
`kolemasakar/AI_general/docs/openai-custom-gpts-retirement-to-plugins-2026-09-16.md`

Official OpenAI references used by that research and revalidated on 2026-09-16:
- `https://help.openai.com/en/articles/20001519`
- `https://help.openai.com/en/articles/20001256`
- `https://help.openai.com/en/articles/8554407`

## Current KRC facts

The current public KRC is already published and remains unchanged.

Cloud Browser read-only inspection confirmed:

```text
WORK_CLOUD_BROWSER=PASS
CHATGPT_AUTH=PASS
KRC_BUILDER_ENTRY=PASS
READ_ONLY_SNAPSHOT=PASS
CURRENT_ACTIONS=NONE
```

Therefore there is no existing Action or bearer configuration that must be preserved for migration.

Repository-side migration preparation is already materially ahead of a legacy Action deployment:

```text
CORE_SKILL_CANDIDATE=READY
MEDIA_TOOL_CONTRACT_CANDIDATE=READY
MEDIA_OPERATION_PARITY_COUNT=13
CORE_REGRESSION_PACK=READY
MEDIA_NEGATIVE_REGRESSION_PACK=READY
MEDIA_ADAPTER_CONTRACT=READY
```

## Decision

Do **not** create a new MEDIA Custom GPT Action merely to complete the old R3 Builder Preview path.

Reason:

1. The current public GPT has no Action to preserve.
2. A newly created Custom Action would be a legacy integration layer with limited remaining lifetime.
3. OpenAI migration does not carry Custom Actions into Plugins automatically.
4. The same VoiceBridge integration would have to be rebuilt and retested against the supported Plugin/App/MCP surface.
5. KRC already has a transport-neutral 13-operation contract, Core skill candidate, regression packs and migration adapter.
6. Waiting for the account-specific migration/plugin surface avoids unnecessary duplicate configuration and secret handling in the retiring Builder Action UI.

## Architecture after this decision

```text
Current published KRC GPT
    -> keep operational / unchanged until migration acceptance

KRC Core
    -> Plugin skill candidate

KRC MEDIA semantics
    -> transport-neutral media adapter
    -> future supported Plugin App / Connector / MCP binding
    -> existing VoiceBridge MEDIA API

Cobalt / AssemblyAI / Gemini
    -> remain backend/provider implementation details behind VoiceBridge
```

## Status of former R3 Action assets

`gpt_store/actions/media_public_r3_openapi.yaml` remains valuable, but its role changes:

```text
OLD_ROLE=planned Custom GPT Action deployment payload
NEW_ROLE=canonical API/operation parity reference for Plugin/App/MCP binding and regression
```

`prompts/GPT_STORE_MEDIA_R3_PUBLIC_ADDENDUM.md` remains a semantic source for future skill/tool guidance, not an instruction to mutate the retiring public GPT now.

Checkpoint 91/92 Builder Preview plans remain historical/test assets and are superseded for implementation priority by the Plugin-first migration path.

## Exception / fallback

A temporary legacy MEDIA Action may be reconsidered only if all of the following become true:

- Plugin migration/app integration is materially delayed for this account;
- MEDIA capability is operationally required before retirement;
- owner explicitly authorizes temporary duplicate implementation;
- expected short-term value exceeds the duplicate setup/regression/migration cost.

Absent that exception, legacy Action creation remains on HOLD.

## Next executable steps

1. Keep the current public GPT unchanged.
2. Inspect the account-specific migration/plugin surface read-only when it appears.
3. Confirm which supported integration surface is available: connected app, connector, custom MCP, or another supported Plugin app binding.
4. Bind the existing transport-neutral MEDIA adapter to that supported surface without changing VoiceBridge semantics unless required.
5. Preserve server-side-only authentication; do not expose bearer/API secrets in skills, evidence, or model-visible configuration.
6. Run Core + MEDIA regression packs against the replacement plugin.
7. Validate sharing/access because replacement plugins start private unless separately configured.
8. Switch users only after replacement acceptance.
9. Keep public GPT publication/update and retirement transition behind separate owner approval.

## Canonical boundary

```text
CUSTOM_GPT_RETIREMENT_PREP=ACTIVE
PLUGIN_FIRST_STRATEGY=ACCEPTED
LEGACY_MEDIA_ACTION_CREATION=HOLD
R3_OPENAPI_ROLE=PARITY_REFERENCE
CURRENT_PUBLIC_GPT=UNCHANGED
PLUGIN_APP_BINDING=WAITING_FOR_ACCOUNT_SURFACE
CUSTOM_MCP_IMPLEMENTATION=NOT_STARTED
GPT_MIGRATION=NOT_STARTED
PLUGIN_INSTALLATION=NOT_STARTED
PLUGIN_PUBLICATION=NOT_AUTHORIZED
PUBLICATION=HOLD
MAIN_MUTATION=DENIED
RENDER_CHANGE=DENIED
PR22_MERGE=DENIED
PR45_MERGE=DENIED
```
