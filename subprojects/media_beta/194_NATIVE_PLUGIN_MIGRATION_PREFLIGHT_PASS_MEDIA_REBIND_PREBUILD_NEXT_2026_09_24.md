# KRC MEDIA — Native Plugin migration preflight PASS; MEDIA rebind prebuild next

Date: 2026-09-24  
Status: **AUTHORITATIVE CHECKPOINT / NATIVE_MIGRATION_PREFLIGHT_PASS / INSTRUCTIONS_FILES_OK / CUSTOM_ACTIONS_NOT_TRANSFERRED / PLUGIN_PRIVATE / SOURCE_GPT_READ_ONLY_AFTER_MIGRATION / MEDIA_REBIND_PREBUILD_NEXT / FREE_ONLY**

## Live migration UI evidence

Owner UI displayed the native **Перенести K-Research & Critic** dialog.

Observed migration contract:

```text
INSTRUCTIONS_AND_FILES=NO_PROBLEMS_DETECTED
CUSTOM_ACTIONS=UNSUPPORTED / WILL_NOT_WORK_IN_PLUGIN
APP_SEARCH_FOR_REPLACEMENT=SUPPORTED_BY_UI
PUBLIC_PLUGIN_SHARING=UNAVAILABLE
MIGRATED_PLUGIN=PRIVATE
SOURCE_GPT_AFTER_MIGRATION=NO_LONGER_EDITABLE
SOURCE_GPT_CAN_STILL_BE_UPDATED_AS_PLUGIN=YES
```

The owner did **not** press the final `Перенести в плагін` button.

```text
NATIVE_PLUGIN_MIGRATION_EXECUTION=0
SOURCE_GPT_STATE_CHANGE=0
PLUGIN_CREATION_BY_NATIVE_MIGRATION=0
```

## P1 result

```text
P1_NATIVE_MIGRATION_PREFLIGHT=PASS
CORE_TRANSFER_SURFACE=PASS / instructions+files accepted by UI
CUSTOM_ACTION_AUTO_TRANSFER=NO
PUBLIC_SHARING_AFTER_MIGRATION=NO
PLUGIN_INITIAL_VISIBILITY=PRIVATE
SOURCE_GPT_POST_MIGRATION=READ_ONLY
FINAL_MIGRATION_CONFIRMATION=NOT_AUTHORIZED
```

## MEDIA replacement architecture

The previously validated R4 Candidate already contains the accepted five app mappings:

```text
R3C / krc-media-readonly = asdk_app_6aaaf8ca113c8191a4ac53f8793833a4
E1  / krc-youtube       = asdk_app_6ab26b061fb4819180fa096638f1e4df
E2  / krc-instagram     = asdk_app_6aaeae197c9081918b90e46f5bb09615
E3  / krc-facebook      = asdk_app_6aaf262767d8819199146dc84b8e1ee8
E4  / krc-telegram      = asdk_app_6aaf292e653481918c75767dea004c5c
```

These app mappings are the preferred rebind target for the 13-operation MEDIA contract because the native GPT migration does not transfer custom Actions.

Expected functional split remains:

```text
READ_OPERATIONS=9
EXECUTION_OPERATIONS=4
TOTAL_OPERATIONS=13
READ_ONLY_EXECUTION_LEAKAGE=0
FREE_ONLY=REQUIRED
```

## Next gate — MEDIA rebind prebuild

Before final native migration:

1. verify the five registered app mappings are still available to the owner;
2. verify Core Skill parity against the accepted Unified R3.9 semantics;
3. prepare the exact post-migration app attachment/rebind sequence;
4. verify that read-only vs consequential operation classification remains preserved;
5. keep Plugin private;
6. do not start provider work;
7. do not complete native migration yet.

## Hard boundary

```text
PUBLIC_GPT_STATE=R39_ACCEPTED / KEEP_EDITABLE_AND_PUBLISHED
NATIVE_PLUGIN_MIGRATION_EXECUTION=NO
MEDIA_REBIND_PREBUILD=AUTHORIZED
PLUGIN_PUBLICATION=NO
PLUGIN_SHARING_CHANGE=NO
NEW_MEDIA_PROVIDER_WORK=NO
PR22_MERGE=NO
PR45_MERGE=NO
MAIN_MUTATION=NO
```

## Resume

```text
RESUME_FROM=CHECKPOINT_194_NATIVE_PLUGIN_MIGRATION_PREFLIGHT_PASS
NEXT_GATE=MEDIA_REBIND_PREBUILD
AFTER_GATE=NATIVE_PLUGIN_MIGRATION_EXECUTION_DECISION
```

Terminal marker:

`KRC_MEDIA_CHECKPOINT_194_NATIVE_PLUGIN_MIGRATION_PREFLIGHT_PASS_MEDIA_REBIND_PREBUILD_NEXT_2026_09_24`
