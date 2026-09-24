# KRC MEDIA — Direct R3C App call reached MCP; VoiceBridge cold-wake retry next

Date: 2026-09-24  
Status: **AUTHORITATIVE CHECKPOINT / DIRECT_R3C_APP_EXPOSURE_PASS / MCP_REACHED / BACKEND_429_COLD_EDGE / VOICEBRIDGE_WOKEN / ZERO_PROVIDER / DIRECT_RETRY_NEXT**

## Direct App diagnostic

A fresh Chat directly invoked:

```text
@KRC MCP R3C Readonly
media_get_capabilities only
```

Observed result:

```json
{
  "status": "error",
  "error": {
    "code": "voicebridge_http_error",
    "http_status": 429,
    "retryable": true
  }
}
```

No other MEDIA tool was called and no provider work was started.

## Server correlation

Render R3C logs confirm the direct app call reached the MCP runtime:

```text
POST /oauth/token -> 200
POST /mcp -> 200
```

Therefore:

```text
DIRECT_R3C_APP_TOOL_EXPOSURE=PASS
DIRECT_R3C_CONNECTION=PASS
DIRECT_R3C_MCP_INVOCATION=PASS
VOICEBRIDGE_BACKEND_RESPONSE=429 / retryable=true
```

This isolates the 429 to the downstream VoiceBridge/free-tier runtime edge rather than ChatGPT App discovery or R3C OAuth/tool exposure.

## VoiceBridge wake

A direct read-only health wake was then performed:

```text
GET /api/v1/health -> 200
service=voicebridge-cloud
status=ok
```

No MEDIA provider work was started.

## Implication for Plugin S3

The underlying R3C App itself is available and invocable outside the Plugin bundle. The private Plugin S3 failure remains specifically:

```text
PLUGIN_CONTEXT_KRC_TOOL_SELECTION_OR_EXPOSURE=UNRESOLVED
DIRECT_APP_HEALTH=PASS_TO_MCP
```

## Next gate

Retry only the direct R3C call now that VoiceBridge is awake:

```text
@KRC MCP R3C Readonly
Виконай лише media_get_capabilities.
Не виконуй інших MEDIA tools.
Не запускай provider work.
Покажи structured result.
```

Acceptance:

```text
media_get_capabilities=PASS
R3C POST /mcp=200
provider_work=0
```

After direct R3C success, return to the Plugin bundling/tool-selection defect.

## Hard boundary

```text
PLUGIN_MUTATION=HOLD
APP_REBIND_MUTATION=HOLD
MEDIA_PROVIDER_WORK=NO
PLUGIN_PUBLICATION=NO
PLUGIN_SHARING_CHANGE=NO
PR22_MERGE=NO
PR45_MERGE=NO
MAIN_MUTATION=NO
```

## Resume

```text
RESUME_FROM=CHECKPOINT_206_DIRECT_R3C_APP_CALL_REACHED_MCP
NEXT_GATE=RETRY_DIRECT_R3C_AFTER_VOICEBRIDGE_WAKE
AFTER_GATE=PLUGIN_KRC_TOOL_EXPOSURE_DIAGNOSTIC
```

Terminal marker:

`KRC_MEDIA_CHECKPOINT_206_DIRECT_R3C_APP_CALL_REACHED_MCP_VOICEBRIDGE_COLD_WAKE_RETRY_NEXT_2026_09_24`
