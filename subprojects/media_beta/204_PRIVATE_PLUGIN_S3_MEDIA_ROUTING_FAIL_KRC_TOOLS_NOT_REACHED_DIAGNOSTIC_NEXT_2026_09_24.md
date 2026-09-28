# KRC MEDIA — Private Plugin S3 media routing FAIL; KRC tools not reached

Date: 2026-09-24  
Status: **AUTHORITATIVE CHECKPOINT / PRIVATE_S1_PASS / PRIVATE_S2_PASS / PRIVATE_S3_FAIL / KRC_APP_RUNTIME_NOT_REACHED / ZERO_PROVIDER / DIAGNOSTIC_NEXT**

## Private Plugin smoke evidence

Chat mode was used with the private `K-Research & Critic` Plugin.

```text
PRIVATE_S1_CORE_GATE=PASS
PRIVATE_S2_MEDIA_PREAPPROVAL_GATE=PASS
```

After the owner approved the CriticProfile with `1`, the Plugin did **not** follow the expected KRC MEDIA read-only route.

Instead, it produced a final report stating that KRC MEDIA YouTube tools were unavailable in the session and used non-KRC/public web evidence.

The final report therefore does not count as S3 acceptance.

## Server-side correlation

Read-only Render log checks for the private-smoke window showed:

```text
R3C_SERVICE=krc-mcp-auth-sentinel
R3C_POST_MCP_REQUESTS=0

E1_SERVICE=krc-mcp-r3e1-youtube-sentinel
E1_REQUESTS=0

PROVIDER_WORK=0
```

Therefore the failure occurred **before** any KRC MCP request reached R3C or E1.

This isolates the current failure layer to ChatGPT Plugin/App tool exposure, selection, or client-side app connection/routing rather than VoiceBridge/MEDIA backend execution.

## Current interpretation

```text
FIVE_APP_UI_RENDER=PASS
E2_RECONNECT=PASS
PRIVATE_S1=PASS
PRIVATE_S2=PASS
PRIVATE_S3_MEDIA_ROUTING=FAIL
FAILURE_LAYER=CHATGPT_PLUGIN_APP_TOOL_EXPOSURE_OR_SELECTION
BACKEND_FAILURE=NO_EVIDENCE
PROVIDER_WORK=0
```

No Plugin mutation is authorized yet. First inspect the two visible ChatGPT tool-call traces from the failed S3 turn to identify which tools were actually called and whether any app call failed client-side before Render.

## Next gate

1. Expand both `Здійснено виклик інструмента` entries in the failed S3 turn.
2. Capture tool/app names and any visible error/status.
3. If the calls are only Web/Search, diagnose Plugin tool exposure/routing.
4. If a KRC App call is shown with a client-side connection error, repair only that connection.
5. Do not proceed to Gemini consent/S4 until S3 is corrected.

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
RESUME_FROM=CHECKPOINT_204_PRIVATE_PLUGIN_S3_MEDIA_ROUTING_FAIL
NEXT_GATE=INSPECT_FAILED_S3_TOOL_TRACES
```

Terminal marker:

`KRC_MEDIA_CHECKPOINT_204_PRIVATE_PLUGIN_S3_MEDIA_ROUTING_FAIL_KRC_TOOLS_NOT_REACHED_DIAGNOSTIC_NEXT_2026_09_24`
