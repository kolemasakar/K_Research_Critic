# KRC MEDIA — Five canonical Apps rebound to private Plugin; UI verification next

Date: 2026-09-24  
Status: **AUTHORITATIVE CHECKPOINT / FIVE_APP_REBIND_APPLIED / PRIVATE_PLUGIN / UI_VERIFICATION_NEXT / FREE_ONLY**

## Plugin state

```text
plugin_id=plugin_bb3595f295708191a3f9e145ba1ff2d5
scope=USER
discoverability=PRIVATE
previous_release=pluginrel_6ab563faebe48191ac77f4df8c705581
current_release=pluginrel_6ab565dc1a788191b775aa8ddbc14042
previous_version=0.19.2+transportfix.20260924
current_version=0.19.3+apps.20260924
```

## App rebind

Native migrated Plugin was updated using the supported native-plugin reference pattern:

```text
.codex-plugin/plugin.json:
  apps="./.app.json"
```

and the root `.app.json` references exactly:

```text
R3C / krc-media-readonly = asdk_app_6aaaf8ca113c8191a4ac53f8793833a4
E1  / krc-youtube       = asdk_app_6ab26b061fb4819180fa096638f1e4df
E2  / krc-instagram     = asdk_app_6aaeae197c9081918b90e46f5bb09615
E3  / krc-facebook      = asdk_app_6aaf262767d8819199146dc84b8e1ee8
E4  / krc-telegram      = asdk_app_6aaf292e653481918c75767dea004c5c
```

Readback from Plugin Creator confirms:

```text
.app.json=PRESENT
apps_field=PRESENT
canonical_app_refs=5/5
Skill=UNCHANGED_FROM_0.19.2_TRANSPORTFIX
Plugin=PRIVATE
```

## Important UI note

The Plugin page button `Додати застосунок` opens the **create-new custom MCP app** form. That form is not the correct path for attaching the already registered canonical Apps.

Existing Apps are referenced through `.app.json` in the Plugin package.

## Next gate

1. close the create-new custom app dialog without saving;
2. refresh/reopen the private Plugin page;
3. verify the Apps section renders the five referenced Apps;
4. if 5/5 render, proceed to 13-operation/private zero-provider smoke;
5. if the UI does not show them, stop and inspect app availability/rendering before any smoke.

## Hard boundary

```text
NEW_CUSTOM_APP_CREATION=NO
PLUGIN_PUBLICATION=NO
PLUGIN_SHARING_CHANGE=NO
MEDIA_PROVIDER_WORK=NO
PR22_MERGE=NO
PR45_MERGE=NO
MAIN_MUTATION=NO
```

## Resume

```text
RESUME_FROM=CHECKPOINT_200_FIVE_CANONICAL_APPS_REBOUND
NEXT_GATE=VERIFY_FIVE_APPS_IN_PLUGIN_UI
AFTER_GATE=PRIVATE_PLUGIN_SMOKE_ZERO_PROVIDER
```

Terminal marker:

`KRC_MEDIA_CHECKPOINT_200_FIVE_CANONICAL_APPS_REBOUND_PRIVATE_PLUGIN_VERIFY_UI_NEXT_2026_09_24`
