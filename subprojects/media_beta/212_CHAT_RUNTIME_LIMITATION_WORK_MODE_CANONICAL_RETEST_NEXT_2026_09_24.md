# KRC MEDIA — Chat runtime limitation isolated; Work-mode canonical retest next

Date: 2026-09-24  
Status: **AUTHORITATIVE CHECKPOINT / CHAT_APP_RUNTIME_UNAVAILABLE / PACKAGE_VALID / DIRECT_APPS_HEALTHY / WORK_MODE_CANONICAL_TEST_NEXT / ZERO_PROVIDER**

## Evidence from Chat-mode test on 0.19.6

Private Plugin version:

```text
0.19.6+portable.20260924
```

After CriticProfile approval, the Skill correctly attempted the required KRC MEDIA read-only route.

The Chat runtime reported:

```text
media_youtube_preflight -> UNAVAILABLE_IN_RUNTIME
media_youtube_lookup -> UNAVAILABLE_IN_RUNTIME
media_get_capabilities -> UNAVAILABLE_IN_RUNTIME
```

Then the Skill used the allowed TinyFish/web fallback.

Render correlation:

```text
R3C requests=0
E1 requests=0
provider_work=0
```

Therefore the failure occurs before the KRC MCP backend.

## Package / App validation

Current package readback:

```text
root plugin.json=PRESENT
extensions.com.openai.apps=./.app.json
compatibility .codex-plugin/plugin.json=PRESENT
compatibility apps=./.app.json
canonical app refs=5/5
routing Skill=PRESENT
```

All five app-specific permission records resolve successfully and inherit the user's default "Allow read actions" setting.

A direct invocation of `KRC MCP R3C Readonly` returns capabilities successfully, proving the underlying registered App, OAuth, MCP surface, and VoiceBridge are healthy.

## Important ID validation

OpenAI's current Plugin Creator validator requires `.app.json` IDs in the form:

```text
asdk_app_...
connector_...
templated_apps_...
```

A diagnostic update using `plugin_asdk_app_...` in `.app.json` was rejected by schema validation. Therefore the current `asdk_app_...` mappings are correct and were not changed.

## Product-surface finding

Current official OpenAI Plugin quickstart explicitly instructs developers who create a **personal plugin with an MCP server** to test its tool in **ChatGPT Work**:

```text
ChatGPT homepage -> switch Chat to Work -> new Work chat -> @plugin -> invoke tool
```

The packaging guide also describes local/personal plugin authoring and testing through Work/Codex flows, while plugin/app capability availability can vary by surface.

This matches the observed behavior:

```text
direct App invocation=PASS
Chat Plugin Skill=PASS
Chat bundled App tools=UNAVAILABLE_IN_RUNTIME
```

Therefore standard Chat is not the canonical acceptance surface for this private personal MCP-backed Plugin.

## Next gate

Retest current `0.19.6+portable.20260924` in **Work**, not Chat.

Sequence:

1. Open Plugin -> `Спробувати в чаті`.
2. Select `Робота`.
3. Start a fresh Work conversation with `@K-Research & Critic`.
4. Send YouTube fact-check request.
5. Approve CriticProfile with `1`.
6. Expected: R3C `preflight -> lookup`.
7. If no reusable transcript: Gemini Free Tier data-use notice + explicit consent request.
8. Do not approve consequential E1 execution yet.

## Hard boundary

```text
PLUGIN_MUTATION=HOLD
APP_MAPPING_MUTATION=HOLD
PLUGIN_PUBLICATION=NO
PLUGIN_SHARING_CHANGE=NO
MEDIA_PROVIDER_WORK=NO
EXECUTION_CONFIRMATION_APPROVAL=NO
PR22_MERGE=NO
PR45_MERGE=NO
MAIN_MUTATION=NO
```

## Resume

```text
RESUME_FROM=CHECKPOINT_212_CHAT_RUNTIME_LIMITATION
NEXT_GATE=WORK_MODE_CANONICAL_S2_S3_RETEST_ON_0_19_6
```

Terminal marker:

`KRC_MEDIA_CHECKPOINT_212_CHAT_RUNTIME_LIMITATION_WORK_MODE_CANONICAL_RETEST_NEXT_2026_09_24`
