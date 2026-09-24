# KRC MEDIA — Five Apps render in Plugin UI; E2 reconnect pending

Date: 2026-09-24  
Status: **AUTHORITATIVE CHECKPOINT / FIVE_APPS_UI_RENDER_PASS / E2_RECONNECT_PENDING / PRIVATE_PLUGIN / ZERO_PROVIDER**

## UI evidence

The private native Plugin UI renders all five canonical app references.

```text
PLUGIN_VERSION=0.19.3+apps.20260924
PLUGIN_VISIBILITY=PRIVATE

R3C=VISIBLE / KRC MCP R3C Readonly
E1=VISIBLE / asdk_app_6ab26b061fb4819180fa096638f1e4df
E2=VISIBLE / asdk_app_6aaeae197c9081918b90e46f5bb09615 / RECONNECT_REQUIRED
E3=VISIBLE / asdk_app_6aaf262767d8819199146dc84b8e1ee8
E4=VISIBLE / asdk_app_6aaf292e653481918c75767dea004c5c
```

Structural rebind is therefore confirmed 5/5. E2 Instagram authentication/connection is not currently ready because the UI explicitly shows **Повторно підключити**.

## Result

```text
FIVE_APP_UI_RENDER=PASS
APP_REFERENCE_COUNT=5/5
E2_CONNECTION=BLOCKED_RECONNECT_REQUIRED
PRIVATE_PLUGIN_SMOKE=HOLD
PROVIDER_WORK=0
```

The raw app IDs shown for E1/E2/E3/E4 match the canonical IDs in the frozen mapping. Display-name resolution is not treated as a blocker by itself.

## Next gate

Reconnect only E2:

```text
E2=asdk_app_6aaeae197c9081918b90e46f5bb09615
NAME=KRC MCP R3E2 Instagram Sentinel-v5
```

Do not invoke MEDIA tools during reconnection. After E2 is connected, refresh the Plugin page and verify the reconnect warning is gone. Then proceed to private zero-provider smoke.

## Hard boundary

```text
OTHER_APP_CHANGES=NO
PLUGIN_PUBLICATION=NO
PLUGIN_SHARING_CHANGE=NO
MEDIA_PROVIDER_WORK=NO
PR22_MERGE=NO
PR45_MERGE=NO
MAIN_MUTATION=NO
```

## Resume

```text
RESUME_FROM=CHECKPOINT_201_FIVE_APPS_UI_RENDER_PASS
NEXT_GATE=RECONNECT_E2_INSTAGRAM
AFTER_GATE=PRIVATE_PLUGIN_SMOKE_ZERO_PROVIDER
```

Terminal marker:

`KRC_MEDIA_CHECKPOINT_201_FIVE_APPS_UI_RENDER_PASS_E2_RECONNECT_PENDING_2026_09_24`
