# KRC MEDIA — MEDIA rebind prebuild PASS; native migration execution decision next

Date: 2026-09-24  
Status: **AUTHORITATIVE CHECKPOINT / MEDIA_REBIND_PREBUILD_PASS / FIVE_APPS_FOUND / 13_OPERATION_CONTRACT_PRESERVED / FINAL_NATIVE_MIGRATION_DECISION_NEXT / FREE_ONLY**

## Preconditions

```text
PUBLIC_R39_ACCEPTED=YES
PUBLIC_GPT=PUBLISHED_AND_EDITABLE
NATIVE_MIGRATION_PREFLIGHT=PASS
INSTRUCTIONS_AND_FILES_MIGRATION_SURFACE=PASS
CUSTOM_ACTIONS_TRANSFER=NO
MIGRATED_PLUGIN_INITIAL_VISIBILITY=PRIVATE
SOURCE_GPT_AFTER_COMPLETED_MIGRATION=READ_ONLY
```

## Five-app availability — current account read-only verification

All canonical registered app IDs from `plugins/krc_r4_candidate/.app.json` were resolved successfully:

```text
R3C = asdk_app_6aaaf8ca113c8191a4ac53f8793833a4
      KRC MCP R3C Readonly
      status=FOUND

E1  = asdk_app_6ab26b061fb4819180fa096638f1e4df
      KRC MCP R3E1 YouTube Sentinel
      status=FOUND

E2  = asdk_app_6aaeae197c9081918b90e46f5bb09615
      KRC MCP R3E2 Instagram Sentinel-v5
      status=FOUND

E3  = asdk_app_6aaf262767d8819199146dc84b8e1ee8
      MCP E3 Facebook 1
      status=FOUND

E4  = asdk_app_6aaf292e653481918c75767dea004c5c
      MCP E4 Telegram 1
      status=FOUND
```

Current permission baseline for all five:

```text
global_permission=Allow read actions
app_specific=Use my default
read_without_confirmation=YES
changes_require_confirmation=YES
```

This permission baseline is compatible with the intended read/execution separation. Actual consequential confirmation for the four execution tools must still be smoke-tested after native migration/app attachment.

## MEDIA rebind mapping

The frozen plugin contract preserves:

```text
R3C -> 9 non-execution/read operations
E1  -> media_youtube_start
E2  -> media_instagram_start
E3  -> media_facebook_start
E4  -> media_telegram_start

READ_OPERATIONS=9
EXECUTION_OPERATIONS=4
TOTAL_OPERATIONS=13
READ_ONLY_EXECUTION_LEAKAGE=0
```

FREE_ONLY remains mandatory:

```text
paid_retrieval_fallback=false
paid_stt_fallback=false
paid_proxy_fallback=false
supadata_public_active=false
scrapecreators_public_active=false
cookie_login_fallback=false
automatic_retry_loop=false
```

## Exact post-migration rebind sequence

If native migration is separately authorized:

1. migrate the GPT to a private Plugin;
2. do not change sharing/publication;
3. inspect generated Skill and reference files before app attachment;
4. attach/rebind the five canonical Apps using the exact existing IDs above;
5. verify 9 read + 4 execution = 13 tools;
6. verify read operations execute without consequential confirmation;
7. verify each execution start produces the expected confirmation boundary;
8. cancel the first consequential confirmation during smoke;
9. verify provider work=0 during smoke;
10. only after private acceptance consider any user-switch or distribution decision.

The source public GPT remains the operational fallback, but after completed native migration it is expected to be read-only.

## P2 result

```text
MEDIA_REBIND_PREBUILD=PASS
FIVE_APPS_CURRENTLY_AVAILABLE=5/5
APP_IDS_UNCHANGED=PASS
MEDIA_CONTRACT_STATIC_PARITY=PASS
PERMISSION_BASELINE=PASS
FINAL_NATIVE_MIGRATION_EXECUTION=NOT_YET_AUTHORIZED
```

## Hard boundary

```text
PUBLIC_GPT_STATE=R39_ACCEPTED / CURRENTLY_EDITABLE
NATIVE_PLUGIN_MIGRATION_EXECUTION=NO
PLUGIN_PUBLICATION=NO
PLUGIN_SHARING_CHANGE=NO
MEDIA_PROVIDER_WORK=NO
PR22_MERGE=NO
PR45_MERGE=NO
MAIN_MUTATION=NO
```

## Resume

```text
RESUME_FROM=CHECKPOINT_195_MEDIA_REBIND_PREBUILD_PASS
NEXT_GATE=NATIVE_PLUGIN_MIGRATION_EXECUTION_DECISION
```

Terminal marker:

`KRC_MEDIA_CHECKPOINT_195_MEDIA_REBIND_PREBUILD_PASS_NATIVE_MIGRATION_EXECUTION_DECISION_NEXT_2026_09_24`
