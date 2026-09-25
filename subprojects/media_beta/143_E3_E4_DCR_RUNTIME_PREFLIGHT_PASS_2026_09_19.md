# KRC MEDIA — R3-E3 / R3-E4 live DCR preflight PASS

Date: 2026-09-19
Status: **DCR_RUNTIME_PASS / AUTHORIZATION_FORM_PASS / SECRET_NOT_SUBMITTED / MCP_NOT_CALLED / ZERO_SIDE_EFFECT_PASS**

## Scope

A real OAuth discovery and Dynamic Client Registration preflight was executed against the live Render Free E3/E4 sentinels from the dedicated KRC `krc-cobalt` control host.

No owner authorization code was transmitted. No access token was issued. No MCP method was called. No MEDIA execution tool was invoked.

## E3 result

```text
surface=R3-E3 Facebook
POST /oauth/register=201
GET /oauth/authorize=200
grant_types=authorization_code,refresh_token
response_types=code
token_endpoint_auth_method=none
owner_authorization_configured=true
secret_submitted=false
token_issued=false
mcp_called=false
```

## E4 result

```text
surface=R3-E4 Telegram
POST /oauth/register=201
GET /oauth/authorize=200
grant_types=authorization_code,refresh_token
response_types=code
token_endpoint_auth_method=none
owner_authorization_configured=true
secret_submitted=false
token_issued=false
mcp_called=false
```

## Zero-side-effect proof after DCR

```text
E3_CONFIRMATION_PROBE_ONLY=true
E3_CONFIRMATION_PROBE_INVOCATIONS=0
E3_PROVIDER_WORK_STARTED=false

E4_CONFIRMATION_PROBE_ONLY=true
E4_CONFIRMATION_PROBE_INVOCATIONS=0
E4_PROVIDER_WORK_STARTED=false

NEON_TOTAL_JOBS=1
NEON_FACEBOOK_JOBS=0
NEON_TELEGRAM_JOBS=0
```

## Next bounded gate

The remaining acceptance step requires the actual owner/ChatGPT OAuth path so the owner authorization secret is entered only in the authorization form rather than exposed through shell/process history.

1. Connect E3/E4 as private custom MCP surfaces in ChatGPT.
2. Complete owner OAuth authorization.
3. Confirm authenticated `tools/list` and read-only discovery.
4. Validate ChatGPT Cancel and Allow-once while confirmation-probe-only remains enabled.
5. Keep real Facebook/Telegram execution on HOLD until separate owner approval.

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

`KRC_MEDIA_CHECKPOINT_143_E3_E4_DCR_RUNTIME_PREFLIGHT_PASS_2026_09_19`
