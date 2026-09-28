# KRC MEDIA — Failed S3 trace shows TinyFish only; direct R3C App diagnostic next

Date: 2026-09-24  
Status: **AUTHORITATIVE CHECKPOINT / PRIVATE_S3_FAIL_CONFIRMED / TINYFISH_ONLY / KRC_APP_CALLS_ZERO / DIRECT_R3C_DIAGNOSTIC_NEXT / ZERO_PROVIDER**

## Failed S3 tool trace

Expanded ChatGPT tool-call traces from the failed private Plugin S3 turn show exactly:

```text
TinyFish / Fetch content
TinyFish / Fetch content
```

Observed requests:

```text
1. Fetch the YouTube page itself.
2. Fetch public YouTube timedtext endpoints for ru / ru&kind=asr.
```

No KRC MEDIA App/tool name appears in the visible trace.

## Correlation

This matches the server-side evidence already recorded in checkpoint 204:

```text
R3C POST /mcp = 0
E1 requests = 0
provider_work = 0
```

Therefore:

```text
PRIVATE_S3_MEDIA_ROUTING=FAIL_CONFIRMED
KRC_APP_CALL_ATTEMPT=NO_EVIDENCE
FALLBACK_TOOL_USED=TinyFish
FAILURE_LAYER=PLUGIN_BUNDLED_APP_EXPOSURE_OR_SELECTION
BACKEND_FAILURE=NOT_REACHED
```

## Package state

The current private Plugin package still contains:

```text
apps="./.app.json"
.app.json canonical refs=5/5
UI Apps render=5/5
Plugin version=0.19.3+apps.20260924
```

Thus UI/package reference presence alone is insufficient evidence that the bundled app tools are exposed to the chat runtime.

## Next isolation test

Before mutating the Plugin, test the underlying R3C App independently of the Plugin bundle.

In a fresh Chat conversation, explicitly invoke:

```text
@KRC MCP R3C Readonly

Виконай лише media_get_capabilities.
Не виконуй інших MEDIA tools.
Не запускай provider work.
Покажи structured result.
```

Acceptance:

```text
DIRECT_R3C_APP_CALL -> tool visible + invocation result
Render R3C POST /mcp -> 200
provider_work -> 0
```

Interpretation:

- if direct R3C PASS: underlying App is healthy; defect is Plugin bundling/runtime exposure or tool selection;
- if direct R3C FAIL: repair R3C app connection/access first.

## Hard boundary

```text
PLUGIN_MUTATION=HOLD
APP_REBIND_MUTATION=HOLD
PLUGIN_PUBLICATION=NO
PLUGIN_SHARING_CHANGE=NO
MEDIA_PROVIDER_WORK=NO
PR22_MERGE=NO
PR45_MERGE=NO
MAIN_MUTATION=NO
```

## Resume

```text
RESUME_FROM=CHECKPOINT_205_FAILED_S3_TOOL_TRACE_TINYFISH_ONLY
NEXT_GATE=DIRECT_R3C_APP_DIAGNOSTIC
```

Terminal marker:

`KRC_MEDIA_CHECKPOINT_205_FAILED_S3_TOOL_TRACE_TINYFISH_ONLY_DIRECT_R3C_APP_DIAGNOSTIC_NEXT_2026_09_24`
