# KRC MEDIA — R3-E2 credential rotation + probe disable / live canary ready

Date: 2026-09-19  
Status: **AUTHORITATIVE CHECKPOINT / R3-E2 CREDENTIAL ROTATION PASS / CONFIRMATION PROBE DISABLED / LIVE CANARY READY / EXECUTION NOT YET AUTHORIZED**

## Scope

This checkpoint records the bounded preparation performed after checkpoint 134 and before any real Instagram provider execution.

No real `media_instagram_start` was executed during this preparation.

## Credential rotation

A fresh route-scoped R3-E2 bearer was generated and installed server-side only on both sides of the R3-E2 binding:

```text
VoiceBridge service:
  service=voicebridge-krc-media-beta-kolemasakar
  service_id=srv-da1kic5bedkc73d6fk60
  env=KRC_MEDIA_R3E2_ACTION_TOKEN

R3-E2 MCP service:
  service=krc-mcp-r3e2-instagram-sentinel-v2
  service_id=srv-dan7vsijnfac73fmrtl0
  env=KRC_VOICEBRIDGE_BEARER
```

The secret value was not written to repository documentation, model-visible output, or tool arguments exposed to the user.

```text
R3E2_SCOPED_CREDENTIAL_ROTATION=PASS
SECRET_SERVER_SIDE_ONLY=true
```

## Confirmation probe cleanup

The zero-side-effect confirmation acceptance mode used for checkpoint 134 was disabled:

```text
KRC_R3E2_CONFIRMATION_PROBE_ONLY=false
```

Post-deploy R3-E2 health:

```text
status=ok
surface=r3e2_instagram_execution
tool_count=5
non_execution_tool_count=4
execution_tool_count=1
instagram_execution_enabled=true
other_execution_tools=not_enabled
voicebridge_binding_configured=true
confirmation_probe_only=false
confirmation_probe_invocation_count=0
provider_work_started=false
```

The invocation counter reset to zero because the service process restarted during the environment update.

## VoiceBridge health

Post-rotation VoiceBridge health:

```text
status=ok
service=voicebridge-cloud
version=0.6.0
```

No Instagram provider work was started as part of this health verification.

## Deploys

```text
VoiceBridge rotation deploy=dep-dana1aad0e5s73e351a0
R3-E2 rotation/probe-disable deploy=dep-dana1av40ujc73b7jba0
```

Both updated runtimes were observed serving successful health responses after the rotation.

## OAuth consequence

R3-E2 OAuth registration, authorization codes, access tokens and refresh tokens remain in-memory.

Therefore the R3-E2 service restart caused by the environment update invalidates the prior ChatGPT OAuth session:

```text
OAUTH_STATE_PERSISTENCE=NOT_IMPLEMENTED
restart/redeploy=>fresh_DCR/reconnect_required
```

Before the live canary, the owner ChatGPT account must establish a fresh R3-E2 OAuth/DCR connection.

## Gate status

```text
R3_E2_CHATGPT_CONFIRMATION_UI=PASS
R3_E2_CANCEL_PATH=PASS
R3_E2_APPROVE_PATH=PASS
R3_E2_SCOPED_CREDENTIAL_ROTATION=PASS
R3_E2_CONFIRMATION_PROBE_ONLY=false
R3_E2_RUNTIME_HEALTH=PASS
VOICEBRIDGE_RUNTIME_HEALTH=PASS
R3_E2_PROVIDER_WORK=false
R3_E2_REAL_MEDIA_START=false

R3_E2_LIVE_CANARY=READY_BUT_NOT_AUTHORIZED
```

## Next bounded gate

```text
1. fresh DCR/reconnect private R3-E2 MCP in owner ChatGPT
2. verify the authenticated 5-tool surface after reconnect
3. obtain explicit owner authorization for exactly one bounded live media_instagram_start
4. owner confirms the consequential action with Allow once
5. verify job creation and terminal state in Neon
6. verify free-only route / no paid fallback
7. restart/replay and duplicate-start idempotency acceptance
8. close R3-E2 and return runtime to a clean steady state
```

Target URL remains the bounded acceptance sample already used for the confirmation test:

```text
https://www.instagram.com/reel/DF1CIrPSVmf/
```

This checkpoint does not authorize step 3 or later.

## Preserved boundaries

```text
PROJECT_COST_POLICY=FREE_ONLY
PAID_DATABASE_UPGRADE=DENIED
PAID_HOSTING_FALLBACK=DENIED
PAID_PROVIDER_FALLBACK=DENIED
PUBLIC_GPT_MUTATION=NO
PLUGIN_PUBLICATION=NO
PLUGIN_SHARING=NO
MAIN_MUTATION=NO
PR22_MERGE=NO
PR45_MERGE=NO
R3_E3_E4=HOLD
R4=HOLD
```

Terminal marker:

`KRC_MEDIA_CHECKPOINT_135_R3E2_CREDENTIAL_ROTATION_PROBE_DISABLED_LIVE_CANARY_READY_2026_09_19`
