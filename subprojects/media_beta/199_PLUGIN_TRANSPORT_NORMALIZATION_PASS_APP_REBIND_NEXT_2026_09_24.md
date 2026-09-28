# KRC MEDIA — Plugin transport normalization PASS; five-App rebind next

Date: 2026-09-24  
Status: **AUTHORITATIVE CHECKPOINT / PRIVATE_PLUGIN_UPDATED / TRANSPORT_NORMALIZATION_PASS / APPS_EMPTY / FIVE_APP_REBIND_NEXT / FREE_ONLY**

## Exact Plugin identity

```text
plugin_id=plugin_bb3595f295708191a3f9e145ba1ff2d5
scope=USER
discoverability=PRIVATE
old_release=pluginrel_32dc077fd5988191973f9e5bf35dfcbf
new_release=pluginrel_6ab563faebe48191ac77f4df8c705581
old_version=0.19.1+bundle.537edef6e9b2291f8ee718897254ce9b
new_version=0.19.2+transportfix.20260924
```

## Applied Skill changes

Only the two legacy Custom Action transport phrases were normalized:

```text
OLD:
For supported public media URLs use the MEDIA Action; MEDIA failure never blocks Core.

NEW:
For supported public media URLs use the available KRC MEDIA apps/tools; MEDIA failure never blocks Core.
```

```text
OLD:
YouTube: preflight first; before new provider work show the returned Gemini Free data-use notice and require explicit approval; only then send the required gemini_free_consent object. No consent=no start.

NEW:
YouTube: preflight first; before new provider work show the returned Gemini Free data-use notice and require explicit approval; only then call the YouTube execution tool with the consent fields required by that tool. No consent=no start.
```

The manifest version was bumped because Plugin update requires a new version. No other functional settings were changed.

## Readback verification

```text
PLUGIN_UPDATE=PASS
SKILL_TRANSPORT_LINE_1=PASS
SKILL_TRANSPORT_LINE_2=PASS
CORE_OTHER_TEXT=UNCHANGED
DISCOVERABILITY=PRIVATE
APPS_ATTACHED=0
PROVIDER_WORK=0
```

## Next gate

Attach/rebind exactly the five canonical Apps:

```text
R3C = asdk_app_6aaaf8ca113c8191a4ac53f8793833a4
E1  = asdk_app_6ab26b061fb4819180fa096638f1e4df
E2  = asdk_app_6aaeae197c9081918b90e46f5bb09615
E3  = asdk_app_6aaf262767d8819199146dc84b8e1ee8
E4  = asdk_app_6aaf292e653481918c75767dea004c5c
```

Then verify 9 read + 4 execution = 13 operations and run private zero-provider smoke.

## Hard boundary

```text
PLUGIN_PUBLICATION=NO
PLUGIN_SHARING_CHANGE=NO
MEDIA_PROVIDER_WORK=NO
PR22_MERGE=NO
PR45_MERGE=NO
MAIN_MUTATION=NO
```

## Resume

```text
RESUME_FROM=CHECKPOINT_199_PLUGIN_TRANSPORT_NORMALIZATION_PASS
NEXT_GATE=ATTACH_FIVE_CANONICAL_APPS
AFTER_GATE=PRIVATE_PLUGIN_SMOKE_ZERO_PROVIDER
```

Terminal marker:

`KRC_MEDIA_CHECKPOINT_199_PLUGIN_TRANSPORT_NORMALIZATION_PASS_APP_REBIND_NEXT_2026_09_24`
