# KRC MEDIA — Direct R3C capabilities PASS; explicit in-Plugin App call next

Date: 2026-09-24  
Status: **AUTHORITATIVE CHECKPOINT / DIRECT_R3C_PASS / UNDERLYING_APP_HEALTHY / PLUGIN_ROUTING_UNRESOLVED / EXPLICIT_IN_PLUGIN_APP_CALL_NEXT / ZERO_PROVIDER**

## Direct R3C acceptance

After VoiceBridge wake, a fresh direct App invocation executed only:

```text
@KRC MCP R3C Readonly
media_get_capabilities
```

Result:

```text
status=PASS
configured=true
mode=zero_client_managed_beta
platforms=youtube,instagram,facebook,telegram
youtube_gemini_free_tier_only=true
youtube_gemini_consent_required=true
paid_retrieval_fallback=false
paid_stt_fallback=false
automatic_paid_fallback=false
owner_access_injected_server_side=true
provider_work=0
start_tools=0
```

This proves:

```text
UNDERLYING_R3C_APP=HEALTHY
R3C_AUTH=PASS
R3C_MCP=PASS
VOICEBRIDGE_BINDING=PASS
FREE_ONLY=PASS
```

## Remaining ambiguity

Private Plugin S3 previously used TinyFish only, despite five referenced Apps rendering in the Plugin UI.

Two possibilities remain:

1. bundled KRC Apps are available in the Plugin runtime but model routing/tool selection did not choose them;
2. bundled KRC Apps render in Plugin metadata/UI but are not exposed as callable tools in that chat context.

## Next isolation test

In a **fresh Chat using the private K-Research & Critic Plugin**, explicitly request only:

```text
Виконай лише media_get_capabilities через KRC MCP R3C Readonly.
Не використовуй TinyFish, веб-пошук або інші MEDIA tools.
Не запускай provider work.
Покажи structured result.
```

Acceptance:

- if R3C tool executes and returns capabilities: Plugin app exposure PASS; defect is routing/instruction priority;
- if R3C cannot be called or another tool is substituted: Plugin app exposure/binding FAIL.

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
RESUME_FROM=CHECKPOINT_207_DIRECT_R3C_CAPABILITIES_PASS
NEXT_GATE=EXPLICIT_R3C_CALL_INSIDE_PRIVATE_PLUGIN
```

Terminal marker:

`KRC_MEDIA_CHECKPOINT_207_DIRECT_R3C_CAPABILITIES_PASS_PLUGIN_EXPLICIT_APP_CALL_NEXT_2026_09_24`
