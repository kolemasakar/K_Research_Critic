# KRC MEDIA — R3-E2 live canary attempt 1 transient failure / cold-start remediation PASS

Date: 2026-09-19  
Status: **AUTHORITATIVE CHECKPOINT / R3-E2 LIVE CANARY ATTEMPT 1 PRE-PROVIDER FAILURE / COLD-START REMEDIATION PASS / RECONNECT REQUIRED**

## Incident

The first owner-approved live R3-E2 Instagram canary invoked only:

```text
media_instagram_start
url=https://www.instagram.com/reel/DF1CIrPSVmf/
```

The ChatGPT-side result was:

```text
HTTP 429
code=voicebridge_http_error
retryable=true
```

## Failure boundary

Evidence showed the request reached the R3-E2 MCP service, but no durable Instagram job was created in Neon.

```text
R3_E2_MCP_POST=200
VOICEBRIDGE_SERVICE_STOPPING=SIGTERM
VOICEBRIDGE_HEALTH_DURING_INCIDENT=503
NEON_JOB_FOR_TARGET_URL=NONE
COBALT_WORK=false
ASSEMBLYAI_WORK=false
PROVIDER_CHARGE=false
```

Because the public Cobalt engine reserves the durable job before retrieval/STT provider work, absence of the Neon job proves that provider execution did not begin.

The failure is therefore classified:

```text
R3_E2_LIVE_CANARY_ATTEMPT_1=FAILED_TRANSIENT
FAILURE_STAGE=PRE_PROVIDER
RETRY_SAFE_WITH_NEW_CONFIRMATION=true
```

## Root-cause remediation

Two bounded changes were implemented.

### VoiceBridge health / rate-limit isolation

Repository:

```text
kolemasakar/VoiceBridge
branch=agent/krc-media-gemini-migration
PR=45
```

Changes:
- `GET /api/v1/health` now executes before the global fixed-window request limiter.
- health/readiness probes therefore remain observable even when the request limiter is saturated.
- regression test added for repeated health requests with a one-request-per-minute global limit.

Commits:

```text
817d191ced675403d33ea84eb63cc2af149616ea
e7b8ebb2803f46656ed07483f87beb31b740f436
```

Validation:

```text
Validate #822=SUCCESS
deploy=dep-danac9btqb8s73b77h40
deploy_status=LIVE
runtime_health=HTTP 200 / status=ok
repeated_health_200=PASS
```

### R3-E2 cold-start-safe consequential start

Repository:

```text
kolemasakar/K_Research_Critic
branch=agent/krc-public-media-r3-integration
PR=22
```

The R3-E2 HTTP surface now performs only side-effect-free VoiceBridge health wake/retry before the consequential POST:

```text
GET /api/v1/health
-> bounded retry only for 429/502/503/504 or transient connectivity
-> health=200
-> exactly one POST /api/v1/media/managed/transcriptions
```

Important safety property:

```text
AUTO_RETRY_CONSEQUENTIAL_POST=false
WARMUP_PROVIDER_WORK=false
WARMUP_EXTERNAL_MUTATION=false
LIVE_POST_COUNT_MAX_PER_CONFIRMED_TOOL_CALL=1
```

Cold-start warmup budget:

```text
budget=45s
per_health_request_timeout<=5s
retry_delay=2s
```

Commits:

```text
e5511bfe48a01ccbfe435d0fbf69665088a163c2
e0cf1b1c0c46f936df7524c2906b5f7be0b96f6a
```

Validation:

```text
Tests #1717:
  Python 3.13=SUCCESS
  Python 3.14=SUCCESS
  Quality gates=SUCCESS
deploy=dep-danace8ae00c73e3e940
deploy_status=LIVE
R3E2_health=HTTP 200 / status=ok
confirmation_probe_only=false
provider_work_started=false
```

## OAuth consequence

The R3-E2 service redeploy resets the current in-memory OAuth/DCR state.

```text
OAUTH_STATE_PERSISTENCE=NOT_IMPLEMENTED
fresh_DCR_reconnect_required=true
```

The previously connected ChatGPT plugin instance must therefore be recreated/reconnected before retrying the live canary.

## Next gate

```text
1. fresh DCR/reconnect R3-E2 private MCP in owner ChatGPT
2. verify authenticated 5-tool surface
3. retry exactly one bounded media_instagram_start for the same target URL
4. owner selects Allow once in ChatGPT confirmation UI
5. verify Neon job creation and terminal state
6. verify zero paid fallback
7. restart/replay and duplicate-start idempotency acceptance
```

No provider work is authorized by this checkpoint itself.

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

`KRC_MEDIA_CHECKPOINT_136_R3E2_ATTEMPT1_TRANSIENT_COLD_START_REMEDIATION_PASS_RECONNECT_REQUIRED_2026_09_19`
