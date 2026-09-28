# KRC MEDIA — R3-E3 ChatGPT OAuth connection PASS

Date: 2026-09-20
Status: **R3_E3_CHATGPT_OAUTH_CONNECTED / AUTHENTICATED_MCP_TRANSPORT_PASS / CONFIRMATION_TEST_PENDING / ZERO_SIDE_EFFECT_PASS**

## User-visible result

ChatGPT reports the private plugin/account:

```text
MCP E3 Facebook 1
account connected
```

## Runtime evidence

Render logs for `krc-mcp-r3e3-facebook-sentinel` show the successful owner authorization sequence:

```text
GET  /oauth/authorize -> 200
POST /oauth/authorize -> 302
POST /oauth/token     -> 200
POST /mcp             -> 401
GET  /.well-known/oauth-protected-resource -> 200
GET  /.well-known/oauth-authorization-server -> 200
POST /mcp             -> 200
POST /mcp             -> 200
```

The initial 401 is part of the expected protected-resource discovery flow before ChatGPT retries with the issued access token. Subsequent authenticated MCP requests succeeded.

## Zero-side-effect proof

Immediately after successful connection:

```text
E3_HEALTH=status=ok
E3_CONFIRMATION_PROBE_ONLY=true
E3_CONFIRMATION_PROBE_INVOCATIONS=0
E3_PROVIDER_WORK_STARTED=false
E3_VOICEBRIDGE_BINDING=true
NEON_TOTAL_JOBS=1
NEON_FACEBOOK_JOBS=0
POST_CONNECT_ERROR_LEVEL_LOGS=0
```

Therefore the connection caused no Facebook execution and no durable Facebook job.

## Remaining E3 gate

1. Verify the ChatGPT tool surface is available for the connected private MCP.
2. Request exactly one `media_facebook_start` while confirmation-probe-only remains enabled.
3. Validate Cancel path first.
4. Repeat and validate Allow-once path.
5. Confirm exactly one probe invocation, provider work=false, and Neon facebook_jobs=0.
6. Keep real Facebook execution on HOLD pending separate owner approval.

## Preserved boundaries

```text
PROJECT_COST_POLICY=FREE_ONLY
LIVE_FACEBOOK_START=NO
LIVE_TELEGRAM_START=NO
PUBLIC_GPT_MUTATION=NO
PLUGIN_PUBLICATION=NO
PLUGIN_SHARING=NO
MAIN_MUTATION=NO
PR22_MERGE=NO
PR45_MERGE=NO
R4=HOLD
```

Terminal marker:

`KRC_MEDIA_CHECKPOINT_144_R3E3_CHATGPT_OAUTH_CONNECTED_ZERO_SIDE_EFFECT_2026_09_20`
