# KRC MEDIA — CI release / R3-E3 E4 runtime staging acceptance checkpoint

Date: 2026-09-19
Status: **CI_PASS / R3_E3_DEPLOY_HEALTH_PASS / R3_E4_DEPLOY_HEALTH_PASS / OAUTH_DISCOVERY_PASS / AUTHENTICATED_ACCEPTANCE_PENDING / LIVE_CANARY_HOLD / FREE_ONLY**

## GitHub Actions correction

Both project repositories are public and the validated workflows use standard GitHub-hosted Ubuntu runners. The previously recorded 2000/2000 included-minutes exhaustion did not block these public-repository PR workflows.

Validation was intentionally triggered by documentation-only staging commits without `[skip ci]`:

```text
KRC_HEAD=4c834382e18dfce1bea86dee26614a38a3428817
KRC_RUN=35466720921
KRC_PYTHON_3_13=PASS
KRC_PYTHON_3_14=PASS
KRC_QUALITY=PASS

VOICEBRIDGE_HEAD=751f83f2b1aca79f58e9a5f615296404836ada06
VOICEBRIDGE_RUN=35466722002
VOICEBRIDGE_CLOUD=PASS
VOICEBRIDGE_IMAGE_PARITY=PASS
VOICEBRIDGE_BROWSER_EXTENSION=PASS
VOICEBRIDGE_REPOSITORY_DOCS=PASS
```

No paid Actions usage was authorized or required.

## VoiceBridge runtime

```text
service=voicebridge-krc-media-beta-kolemasakar
service_id=srv-da1kic5bedkc73d6fk60
plan=free
branch=agent/krc-media-gemini-migration
deployed_head=751f83f2b1aca79f58e9a5f615296404836ada06
deploy=dep-danerkrbc2fs73e60du0
deploy_status=live
health=HTTP_200 / status=ok / version=0.6.0
```

Server-side R3-E3 and R3-E4 route-scoped bearer configuration is present. Secret values are not recorded in repository documentation.

## R3-E3 Facebook sentinel

```text
service=krc-mcp-r3e3-facebook-sentinel
service_id=srv-danerqmgekts738oejsg
plan=free
auto_deploy=no
branch=agent/krc-public-media-r3-integration
deployed_head=4c834382e18dfce1bea86dee26614a38a3428817
deploy=dep-danes16eod7s73aa748g
deploy_status=live
surface=r3e3_facebook_execution
tool_count=3
non_execution_tool_count=2
execution_tool_count=1
voicebridge_binding_configured=true
confirmation_probe_only=true
confirmation_probe_invocation_count=0
provider_work_started=false
health=PASS
```

The only execution tool is `media_facebook_start`. It was not invoked.

## R3-E4 Telegram sentinel

```text
service=krc-mcp-r3e4-telegram-sentinel
service_id=srv-danertv40ujc73bn9hog
plan=free
auto_deploy=no
branch=agent/krc-public-media-r3-integration
deployed_head=4c834382e18dfce1bea86dee26614a38a3428817
deploy=dep-danes2tii2qc73brpcm0
deploy_status=live
surface=r3e4_telegram_execution
tool_count=3
non_execution_tool_count=2
execution_tool_count=1
voicebridge_binding_configured=true
confirmation_probe_only=true
confirmation_probe_invocation_count=0
provider_work_started=false
health=PASS
```

The only execution tool is `media_telegram_start`. It was not invoked.

## OAuth discovery

Both E3 and E4 expose valid protected-resource and authorization-server metadata.

```text
bearer_method=header
required_read_scope=krc.mcp.read
pkce=S256
grant_types=authorization_code,refresh_token
dcr=advertised
token_endpoint_auth_method=none
restart_safe_signing_key=deployed_server_side
```

Authenticated owner authorization/token exchange and authenticated MCP `tools/list` are still pending. No secret was moved through an unsafe shell/process-history path.

## Runtime error scan

Post-deploy Render scan across VoiceBridge, E3 and E4:

```text
error_level_logs=0
http_5xx_request_logs=0
```

## Neon safety invariant

Read-only Neon audit after deployment:

```text
managed_jobs=1
instagram_jobs=1
facebook_jobs=0
telegram_jobs=0
```

Therefore the deployment and discovery work caused no Facebook or Telegram provider execution or durable job creation.

## Gate state

```text
R3_E1=PASS / COMPLETE
R3_E2=PASS / COMPLETE
R3_E3=CI_PASS / DEPLOY_HEALTH_PASS / OAUTH_DISCOVERY_PASS / AUTHENTICATED_CONFIRMATION_PENDING
R3_E4=CI_PASS / DEPLOY_HEALTH_PASS / OAUTH_DISCOVERY_PASS / AUTHENTICATED_CONFIRMATION_PENDING
R3_F=LOCAL_PASS / CI_PASS / RUNTIME_ACCEPTANCE_PENDING
R3_G_OAUTH=DEPLOYED / DISCOVERY_PASS / TOKEN_RESTART_ACCEPTANCE_PENDING
R3_H=HOLD
R4=HOLD
```

## Next bounded gate

1. Complete authenticated OAuth/DCR and MCP discovery for E3/E4 through a secret-safe ChatGPT/custom-MCP connection path.
2. Validate ChatGPT Cancel and Allow-once while `CONFIRMATION_PROBE_ONLY=true`.
3. Require separate owner authorization before any real `media_facebook_start` or `media_telegram_start`.
4. After such authorization only, run one bounded live canary per platform and verify Neon persistence/restart/idempotency/zero-paid-fallback.
5. Close E3/E4, then complete R3-F and R3-G runtime acceptance.

## Preserved boundaries

```text
PROJECT_COST_POLICY=FREE_ONLY
PAID_ACTIONS_USAGE=DENIED
PUBLIC_GPT_MUTATION=NO
PLUGIN_PUBLICATION=NO
PLUGIN_SHARING=NO
MAIN_MUTATION=NO
PR22_MERGE=NO
PR45_MERGE=NO
LIVE_FACEBOOK_START=NO
LIVE_TELEGRAM_START=NO
R4=HOLD
```

Terminal marker:

`KRC_MEDIA_CHECKPOINT_142_CI_E3_E4_DEPLOY_HEALTH_OAUTH_DISCOVERY_PASS_2026_09_19`
