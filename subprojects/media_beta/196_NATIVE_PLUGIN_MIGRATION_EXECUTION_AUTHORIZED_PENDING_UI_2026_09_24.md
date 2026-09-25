# KRC MEDIA — Native Plugin migration execution authorized; UI execution pending

Date: 2026-09-24  
Status: **AUTHORITATIVE CHECKPOINT / NATIVE_MIGRATION_EXECUTION_AUTHORIZED / UI_EXECUTION_PENDING / MEDIA_REBIND_PREBUILD_PASS / FREE_ONLY**

## Owner authorization

The owner explicitly selected option:

```text
1 = APPROVE native migration execution
```

Therefore:

```text
NATIVE_PLUGIN_MIGRATION_EXECUTION_AUTHORIZED=YES
FINAL_MIGRATION_CONFIRMATION_AUTHORIZED=YES
PLUGIN_INITIAL_VISIBILITY=PRIVATE
MEDIA_REBIND_POST_MIGRATION_REQUIRED=YES
```

## Preconditions satisfied

```text
PUBLIC_R39_ACCEPTED=YES
PUBLIC_PRIVACY_POLICY_URL_RECONCILIATION=PASS
NATIVE_MIGRATION_PREFLIGHT=PASS
MEDIA_REBIND_PREBUILD=PASS
FIVE_CANONICAL_APPS_FOUND=5/5
STATIC_MEDIA_CONTRACT=9 read + 4 execution = 13
FREE_ONLY=PASS
```

## Expected migration effects

```text
INSTRUCTIONS_AND_FILES_TRANSFER=YES
CUSTOM_ACTIONS_TRANSFER=NO
PLUGIN_INITIAL_VISIBILITY=PRIVATE
PUBLIC_PLUGIN_SHARING=UNAVAILABLE
SOURCE_GPT_AFTER_COMPLETED_MIGRATION=READ_ONLY
SOURCE_GPT_USABLE_UNTIL_RETIREMENT=YES
```

The accepted public R3.9 GPT therefore remains the functional fallback after migration, but it is expected to become read-only.

## Execution sequence

1. Owner presses the native `Перенести в плагін` confirmation.
2. Capture resulting Plugin identity/state.
3. Verify generated Skill/instruction parity.
4. Verify no unexpected files/apps/permissions were introduced.
5. Attach/rebind the exact canonical Apps:
   - R3C = `asdk_app_6aaaf8ca113c8191a4ac53f8793833a4`
   - E1 = `asdk_app_6ab26b061fb4819180fa096638f1e4df`
   - E2 = `asdk_app_6aaeae197c9081918b90e46f5bb09615`
   - E3 = `asdk_app_6aaf262767d8819199146dc84b8e1ee8`
   - E4 = `asdk_app_6aaf292e653481918c75767dea004c5c`
6. Verify 13-operation parity and permission/confirmation boundaries.
7. Run private smoke with provider work=0.
8. Only after private acceptance consider any user-switch or distribution decision.

## Hard boundary

```text
PLUGIN_PUBLICATION=NO
PLUGIN_SHARING_CHANGE=NO
NEW_MEDIA_PROVIDER_WORK=NO
PR22_MERGE=NO
PR45_MERGE=NO
MAIN_MUTATION=NO
POST_MIGRATION_APP_IDS_MUST_MATCH=YES
```

## Resume

```text
RESUME_FROM=CHECKPOINT_196_NATIVE_PLUGIN_MIGRATION_EXECUTION_AUTHORIZED
NEXT_GATE=COMPLETE_NATIVE_MIGRATION_IN_UI_AND_CAPTURE_RESULT
```

Terminal marker:

`KRC_MEDIA_CHECKPOINT_196_NATIVE_PLUGIN_MIGRATION_EXECUTION_AUTHORIZED_PENDING_UI_2026_09_24`
