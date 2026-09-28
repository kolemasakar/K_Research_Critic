# KRC MEDIA — R3-E2 isolated Instagram sentinel + authenticated preflight PASS / confirmation pending

Date: 2026-09-19  
Status: **AUTHORITATIVE CHECKPOINT / R3-E2 IMPLEMENTATION PASS / AUTHENTICATED PREFLIGHT PASS / CONFIRMATION UI PENDING / LIVE START HOLD**

## Scope

This checkpoint records the implementation and deployment of the isolated R3-E2 Instagram execution surface, the dedicated route-scoped VoiceBridge bearer contract, and the authenticated no-provider-work Instagram preflight/lookup acceptance.

No live `media_instagram_start` was executed.

## VoiceBridge R3-E2 scoped bearer

Repository:

```text
repository=kolemasakar/VoiceBridge
branch=agent/krc-media-gemini-migration
PR=45 OPEN / DRAFT / UNMERGED
head=e640900bfddd367680badcc8e7cf349e471e2d8a
Validate #820=SUCCESS
```

Implementation adds `KRC_MEDIA_R3E2_ACTION_TOKEN` and accepts it only on the public Cobalt handler under an Instagram-only scope.

Scope rules:

```text
Instagram preflight=allowed
Instagram lookup=allowed
Instagram job/status/segments=allowed only when stored source_url is Instagram
Instagram start route=addressable through the scoped Cobalt handler
YouTube through R3-E2 bearer=DENIED
Facebook through R3-E2 bearer=DENIED
Telegram through R3-E2 bearer=DENIED
general MEDIA action token behavior=UNCHANGED
```

Regression coverage verifies an R3-E2 credential cannot be used to widen the execution surface to YouTube.

Current VoiceBridge deployment:

```text
service=voicebridge-krc-media-beta-kolemasakar
service_id=srv-da1kic5bedkc73d6fk60
deploy=dep-dan7s4e8n08c73apmd8g
commit=e640900bfddd367680badcc8e7cf349e471e2d8a
status=LIVE
plan=free
```

## Isolated R3-E2 MCP surface

Repository:

```text
repository=kolemasakar/K_Research_Critic
branch=agent/krc-public-media-r3-integration
PR=22 OPEN / DRAFT / UNMERGED
implementation_head=7a09b857033a791a7dd6d10d7c41ed182f227e09
Tests #1678=SUCCESS
```

Surface:

```text
surface=r3e2_instagram_execution
tool_count=5
non_execution_tool_count=4
execution_tool_count=1
```

Exposed tools:

```text
media_instagram_preflight
media_instagram_lookup
media_non_youtube_status
media_non_youtube_segments
media_instagram_start
```

Not exposed:

```text
media_youtube_start
media_facebook_start
media_telegram_start
```

The `media_instagram_start` descriptor is write-style / consequential:

```text
readOnlyHint=false
destructiveHint=false
idempotentHint=false
openWorldHint=true
description_requires_confirmation=true
automatic_paid_fallback_forbidden=true
```

This proves the server-side confirmation contract but does not by itself prove that the current ChatGPT UI presents and enforces the confirmation dialog for this newly connected private surface.

## Active R3-E2 runtime

Accepted service:

```text
service=krc-mcp-r3e2-instagram-sentinel-v2
service_id=srv-dan7vsijnfac73fmrtl0
plan=free
region=frankfurt
autoDeploy=no
deploy=dep-dan800dii2qc73bm47k0
commit=7a09b857033a791a7dd6d10d7c41ed182f227e09
status=LIVE
surface=r3e2_instagram_execution
```

Health:

```text
HTTP=200
status=ok
tool_count=5
non_execution_tool_count=4
execution_tool_count=1
instagram_execution_enabled=true
other_execution_tools=not_enabled
voicebridge_binding_configured=true
provider_work_started=false
```

## Authenticated Instagram preflight + durable lookup

The active R3-E2 runtime executed only:

```text
media_instagram_preflight
media_instagram_lookup
```

Result:

```text
status=PASS
provider=cobalt
platform=instagram
stt_provider=assemblyai
estimated_retrieval_credits=0
automatic_paid_fallback=false
lookup=pass_empty
lookup_http_status=404
provider_work_started=false
start_called=false
error_logs=0
```

The 404 is the expected durable lookup result when no reusable Instagram job exists.

Neon after the probe:

```text
managed_jobs=0
instagram_jobs=0
cobalt_jobs=0
```

Therefore the authenticated preflight did not create a durable Instagram job and did not start Cobalt or AssemblyAI provider work.

## Provisioning artifact

The first Render service attempt:

```text
service=krc-mcp-r3e2-instagram-sentinel
service_id=srv-dan7s6egekts7381bbj0
```

was created without `KRC_MCP_BIND_HOST=0.0.0.0` on its initial deploy. It remained in Render port-detection/update state and is **NOT ACCEPTED / NOT USED** for R3-E2 evidence.

The accepted replacement is `krc-mcp-r3e2-instagram-sentinel-v2`.

Cleanup of the failed provisioning artifact is operational housekeeping and must not be confused with the accepted runtime.

## Credential status

The R3-E2 preflight uses a dedicated temporary test-only scoped credential stored only in Render environment configuration. It is not committed to Git and is not written to project documentation.

Before any live Instagram provider execution:

```text
R3E2_SCOPED_CREDENTIAL_ROTATION=REQUIRED
R3E2_OWNER_CODE_ROTATION=RECOMMENDED
```

The fresh live-acceptance credential must remain server-side.

## Confirmation gate

Current evidence:

```text
R3_D_GENERIC_CONFIRMATION=PASS
R3_E2_CONFIRMATION_CONTRACT=PASS
R3_E2_CHATGPT_CONFIRMATION_UI=PENDING
```

The next acceptance action must connect the private R3-E2 MCP surface to ChatGPT and verify the consequential-action confirmation UI, preferably beginning with the CANCEL path so that `media_instagram_start` cannot reach VoiceBridge or providers.

## Gate status

```text
R3_E2_SCOPED_BEARER_CODE=PASS
R3_E2_SCOPED_BEARER_RUNTIME=PASS
R3_E2_ISOLATED_SURFACE=PASS
R3_E2_REPOSITORY_CI=PASS
R3_E2_RUNTIME_HEALTH=PASS
R3_E2_AUTHENTICATED_PREFLIGHT=PASS
R3_E2_DURABLE_LOOKUP=PASS_EMPTY
R3_E2_PROVIDER_WORK=false
R3_E2_START_CALLED=false
R3_E2_CONFIRMATION_CONTRACT=PASS
R3_E2_CHATGPT_CONFIRMATION_UI=PENDING
R3_E2_CREDENTIAL_ROTATION_BEFORE_LIVE=REQUIRED

R3_E2_EXECUTION=HOLD
```

## Preserved boundaries

```text
PROJECT_COST_POLICY=FREE_ONLY
PAID_DATABASE_UPGRADE=DENIED
PAID_HOSTING_FALLBACK=DENIED
PAID_PROVIDER_FALLBACK=DENIED
R3C_USED=NO
media_instagram_start=NOT_CALLED
PUBLIC_GPT_MUTATION=NO
PLUGIN_PUBLICATION=NO
PLUGIN_SHARING=NO
MAIN_MUTATION=NO
PR22_MERGE=NO
PR45_MERGE=NO
R3_E3_E4=HOLD
R4=HOLD
```

## Next bounded work

```text
1. rotate the temporary R3-E2 scoped credential before live acceptance
2. connect/reconnect the private R3-E2 MCP surface in the owner ChatGPT account
3. verify ChatGPT confirmation UI with CANCEL first
4. verify APPROVE reaches exactly one media_instagram_start only after explicit owner authorization
5. then run one bounded free-only Instagram live acceptance
6. prove Neon persistence / restart replay / duplicate-start idempotency
7. close R3-E2 and return the sentinel to a clean non-probe runtime
```

Terminal marker:

`KRC_MEDIA_CHECKPOINT_132_R3E2_ISOLATED_SENTINEL_AUTHENTICATED_PREFLIGHT_PASS_CONFIRMATION_PENDING_2026_09_19`
