# KRC MEDIA — Work-mode App exposure PASS; VoiceBridge cold 429; wake complete; retry next

Date: 2026-09-24  
Status: **AUTHORITATIVE CHECKPOINT / WORK_MODE_APP_EXPOSURE_PASS / R3C_REACHED / DOWNSTREAM_429 / VOICEBRIDGE_WOKEN / ZERO_PROVIDER / RETRY_NEXT**

## Work-mode canonical test

Private Plugin:

```text
version=0.19.6+portable.20260924
surface=ChatGPT Work
```

Fresh Work conversation used `@K-Research & Critic`, submitted the YouTube fact-check request, and approved the CriticProfile.

Observed user-visible result:

```text
analysis not completed
two transcription-service attempts returned HTTP 429
Gemini Free Tier processing did not start
provider work did not start
```

## Server correlation

R3C Render logs during the Work test:

```text
POST /oauth/token -> 200
POST /mcp -> 200
POST /mcp -> 200
```

E1 logs:

```text
requests=0
```

Therefore:

```text
WORK_MODE_BUNDLED_APP_EXPOSURE=PASS
R3C_RUNTIME_CALLABILITY=PASS
R3C_AUTH=PASS
R3C_MCP=PASS
FAILURE_LAYER=DOWNSTREAM_VOICEBRIDGE_429
E1_BEFORE_CONSENT=0
PROVIDER_WORK=0
```

This distinguishes Work from standard Chat, where the same bundled App tools were unavailable in runtime.

## VoiceBridge wake

VoiceBridge had been stopped/slept before the Work attempt.

A read-only health wake was performed after the test:

```text
GET /api/v1/health -> 200
service=voicebridge-cloud
status=ok
version=0.6.0
```

No MEDIA provider work was started.

## Next gate

Retry the same Work-mode flow now that VoiceBridge is awake:

1. Fresh Work chat from the same private Plugin.
2. YouTube fact-check request.
3. Approve CriticProfile with `1`.
4. Expected: R3C preflight/lookup succeeds.
5. If no reusable transcript exists: show Gemini Free Tier data-use notice and request explicit consent.
6. Stop before approving consequential E1 execution confirmation.

## Hard boundary

```text
PLUGIN_MUTATION=NO
APP_MAPPING_MUTATION=NO
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
RESUME_FROM=CHECKPOINT_213_WORK_MODE_APP_EXPOSURE_PASS
NEXT_GATE=WORK_MODE_RETRY_AFTER_VOICEBRIDGE_WAKE
```

Terminal marker:

`KRC_MEDIA_CHECKPOINT_213_WORK_MODE_APP_EXPOSURE_PASS_VOICEBRIDGE_COLD_429_WOKEN_RETRY_NEXT_2026_09_24`
