# KRC — OpenAI retirement research integration / migration acceptance hardening — 2026-09-16

Status: ACCEPTANCE_HARDENING_PREPARED / PLUGIN_FIRST_UNCHANGED / PUBLICATION_HOLD

## Trigger

Owner requested that KRC development explicitly incorporate:

`kolemasakar/AI_general/docs/openai-custom-gpts-retirement-to-plugins-2026-09-16.md`

The document consolidates current OpenAI migration guidance and project-level implications for published and in-development Custom GPTs.

## Compatibility with existing KRC direction

The research **does not reverse** P99/P100 or the Plugin-first strategy. It confirms them.

Already present before this checkpoint:

```text
PLUGIN_FIRST_STRATEGY=ACCEPTED
LEGACY_MEDIA_ACTION_CREATION=HOLD
CUSTOM_ACTIONS_AUTO_TRANSFER=FALSE
REPLACEMENT_PLUGIN_INITIAL_ACCESS=PRIVATE
CONVERSATION_STARTERS_TRANSFER_GUARANTEED=FALSE
PREVIOUS_CHATS_TRANSFER_GUARANTEED=FALSE
SELECTED_MODEL_TRANSFER_GUARANTEED=FALSE
MIGRATION_IS_STATE_CHANGING=TRUE
MEDIA_OPERATION_PARITY_COUNT=13
```

## New hardening introduced from the research

A new contract is added:

`plugins/krc_migration_candidate/contracts/migration_acceptance.yaml`

New acceptance requirements:

1. **Plan-specific timing discipline**
   - Enterprise target dates must not be silently applied to Plus/personal plans.
   - Account/workspace in-product migration notice is authoritative for execution timing.
   - Planned dates may change.

2. **Model independence**
   - Selected model is not assumed portable.
   - Core correctness must not depend on a GPT-selected model surviving migration.

3. **No required state only in chat history**
   - Previous chats are not assumed portable.
   - Required cross-chat state must be recoverable through explicit checkpoint artifacts.

4. **Conversation starter independence**
   - Starters are optional UX, not Core correctness dependencies.
   - Representative starter prompts must remain regression fixtures.
   - Replacement entry points/starters must be checked post-migration.

5. **Reference asset validation**
   - Reference files/templates/examples are not assumed to transfer perfectly.
   - Required assets must be enumerated and validated before cutover.
   - Optional asset loss must not silently alter Core semantics.

6. **Sharing/access reset**
   - Replacement Plugin starts private.
   - Public GPT sharing/access is not assumed inherited.
   - Intended user access must be explicitly validated before cutover.

7. **Store distribution is non-portable unless proven**
   - Ratings, reviews, usage counters, ranking and Store position are not assumed to transfer.
   - Migration acceptance must not depend on those metrics transferring.

8. **Legacy GPT link behavior must be observed, not assumed**
   - Redirect to replacement may occur when supported and the user has access.
   - Redirect is not a release prerequisite because it is not guaranteed.
   - Its actual behavior must be recorded after activation.

9. **Migration remains a state-changing action**
   - Migration makes the original GPT read-only under the described flow.
   - Read-only inspection must stop before `Migrate`.
   - Migration requires separate owner approval.

## New automated guards

`tests/test_krc_migration_acceptance.py`

CI now rejects regressions that:

- universalize Enterprise dates to personal plans;
- make selected model a runtime dependency;
- rely on previous chat history for required state;
- assume starters or reference assets migrate perfectly;
- assume Custom Actions transfer automatically;
- assume public sharing or Store metrics transfer;
- assume legacy-link redirect is guaranteed;
- treat migration as preview/read-only;
- permit cutover without Core+MEDIA regression, audience validation and separate owner approval.

## Updated cutover acceptance baseline

```text
CORE_SKILL_SEMANTIC_PARITY=REQUIRED
MODEL_AGNOSTIC_BEHAVIOR=REQUIRED
CHAT_HISTORY_INDEPENDENCE=REQUIRED
CHECKPOINT_RECOVERY=REQUIRED
REFERENCE_ASSET_VALIDATION=REQUIRED_IF_ANY
STARTER_OR_EQUIVALENT_ENTRY_POINT_VALIDATION=REQUIRED
MEDIA_13_OPERATION_PARITY=REQUIRED
MEDIA_FREE_ONLY_FAIL_CLOSED=REQUIRED
MEDIA_FAILURE_CORE_ISOLATION=REQUIRED
SHARING_AND_AUDIENCE_VALIDATION=REQUIRED
STORE_METRIC_TRANSFER=NOT_REQUIRED
LEGACY_LINK_BEHAVIOR=RECORD_AFTER_ACTIVATION
OWNER_APPROVAL_BEFORE_USER_SWITCH=REQUIRED
```

## Boundary

No migration, install, connection, publication, Render change, main mutation or PR merge is authorized by this checkpoint.

```text
PUBLIC_GPT=UNCHANGED
MIGRATION_EXECUTION=DENIED
PLUGIN_INSTALLATION=DENIED
APP_CONNECTION=DENIED
CUSTOM_MCP_UPLOAD=DENIED
PLUGIN_PUBLICATION=DENIED
RENDER_CHANGE=DENIED
MAIN_MUTATION=DENIED
PR22_MERGE=DENIED
PR45_MERGE=DENIED
```

## Next executable step

The next runtime-facing step remains the account-specific **read-only migration/plugin surface inspection**. When that surface appears, classify it against:

- `surface_decision_matrix.yaml`;
- `auth_transport_binding.yaml`;
- `migration_acceptance.yaml`;
- Core + MEDIA regression packs.

Do not migrate/install/connect until the owner separately authorizes the state-changing phase.
