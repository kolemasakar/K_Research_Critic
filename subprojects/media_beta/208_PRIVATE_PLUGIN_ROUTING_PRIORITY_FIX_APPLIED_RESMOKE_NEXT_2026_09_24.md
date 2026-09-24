# KRC MEDIA — Private Plugin routing-priority fix applied; re-smoke next

Date: 2026-09-24  
Status: **AUTHORITATIVE CHECKPOINT / DIRECT_R3C_PASS / PLUGIN_APP_EXPOSURE_PASS / ROUTING_PRIORITY_FIX_APPLIED / PRIVATE_RESMOKE_NEXT / ZERO_PROVIDER / FREE_ONLY**

## Isolation result

Direct R3C call outside the Plugin:

```text
media_get_capabilities=PASS
configured=true
provider_work=0
```

Explicit R3C call **inside the private Plugin** also passed.

Therefore:

```text
PLUGIN_BUNDLED_APP_EXPOSURE=PASS
R3C_CALLABLE_IN_PLUGIN_CONTEXT=PASS
UNDERLYING_APP_HEALTH=PASS
FAILED_S3_ROOT_CAUSE=MODEL_ROUTING_PRIORITY / FALLBACK_SELECTION
```

The earlier failed S3 used TinyFish without first attempting KRC MEDIA.

## Plugin fix applied

```text
plugin_id=plugin_bb3595f295708191a3f9e145ba1ff2d5
previous_version=0.19.3+apps.20260924
current_version=0.19.4+routingfix.20260924
current_release=pluginrel_6ab578661cbc81918222878502316a6c
scope=USER
discoverability=PRIVATE
```

A mandatory `MEDIA ROUTING PRIORITY` section was added to the migrated Skill.

Key invariants:

```text
supported_media_after_profile_approval -> KRC MEDIA first
R3C -> all non-execution MEDIA operations
E1 -> youtube start only
E2 -> instagram start only
E3 -> facebook start only
E4 -> telegram start only

youtube order:
media_youtube_preflight -> media_youtube_lookup -> reuse/status/segments as applicable
new provider work -> data-use notice + explicit consent -> execution App

TinyFish/web before KRC read-only attempt = FORBIDDEN
claim KRC tools unavailable without actual KRC call = FORBIDDEN
TinyFish/web fallback after actual KRC failure = ALLOWED
web fact-check after transcript acquisition = ALLOWED
```

The five canonical app refs were preserved unchanged.

## Readback

```text
plugin_version=0.19.4+routingfix.20260924
apps=5/5 unchanged
Skill routing section=PRESENT
transport normalization=PRESENT
provider_work=0
publication/share=unchanged PRIVATE
```

## Next gate — private re-smoke

Use a **fresh Chat** from the updated private Plugin.

1. Submit the YouTube fact-check request.
2. Expect CriticProfile gate.
3. Reply `1`.
4. Expected next path:
   - KRC R3C read-only tool call(s), not TinyFish;
   - YouTube preflight/lookup;
   - if no reusable transcript, show Gemini Free Tier data-use notice and request explicit consent;
   - do not approve the consequential execution confirmation yet.
5. Capture tool-call trace.

## Hard boundary

```text
PLUGIN_PUBLICATION=NO
PLUGIN_SHARING_CHANGE=NO
MEDIA_EXECUTION_CONFIRMATION_APPROVAL=NO
PROVIDER_WORK=NO
PR22_MERGE=NO
PR45_MERGE=NO
MAIN_MUTATION=NO
```

## Resume

```text
RESUME_FROM=CHECKPOINT_208_PRIVATE_PLUGIN_ROUTING_PRIORITY_FIX_APPLIED
NEXT_GATE=PRIVATE_PLUGIN_S2_S3_RESMOKE
```

Terminal marker:

`KRC_MEDIA_CHECKPOINT_208_PRIVATE_PLUGIN_ROUTING_PRIORITY_FIX_APPLIED_RESMOKE_NEXT_2026_09_24`
