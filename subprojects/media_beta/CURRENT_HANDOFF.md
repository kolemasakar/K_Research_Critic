# KRC MEDIA — CURRENT HANDOFF

Version: 18.5
Status: **ACTIVE_HANDOFF / R3-E1_PASS_COMPLETE / R3-E2_PASS_COMPLETE / R3-E3_CHATGPT_OAUTH_CONNECTED / R3-E4_CI_DEPLOY_DCR_PASS / R3-F_CI_PASS / R3-G_OAUTH_RUNTIME_ACTIVE / FREE_ONLY / PUBLICATION_HOLD**
Date: 2026-09-20

## Recovery command

`Віднови K-Research & Critic MEDIA з subprojects/media_beta/CURRENT_HANDOFF.md та checkpoint 144. R3-E1/E2 COMPLETE. R3-E3 Facebook: CI PASS, Render Free deploy+health PASS, OAuth discovery+DCR PASS, ChatGPT owner OAuth connection PASS, authenticated MCP transport PASS, confirmation-probe-only=true, provider work=false. Наступний gate — перевірити tool surface і ChatGPT Cancel/Allow-once для media_facebook_start у zero-side-effect probe mode. R3-E4 Telegram ще очікує ChatGPT OAuth connection. Live Facebook/Telegram start заборонено до окремого owner approval. PROJECT_COST_POLICY=FREE_ONLY.`

## Canonical current authority

1. `CURRENT_HANDOFF.md` — v18.5.
2. `144_R3E3_CHATGPT_OAUTH_CONNECTED_ZERO_SIDE_EFFECT_2026_09_20.md`.
3. `143_E3_E4_DCR_RUNTIME_PREFLIGHT_PASS_2026_09_19.md`.
4. `142_CI_E3_E4_DEPLOY_HEALTH_OAUTH_DISCOVERY_PASS_2026_09_19.md`.
5. `140_PROJECT_AUDIT_DOCS_RUNTIME_SYNC_2026_09_19.md`.
6. `02_ROADMAP.md` — v6.9.
7. current PR #22 / PR #45 heads and current runtime evidence.

## Repository / PR authority

```text
KRC repository=kolemasakar/K_Research_Critic
branch=agent/krc-public-media-r3-integration
PR=22
state=OPEN / DRAFT / UNMERGED
ci_validated_code_head=4c834382e18dfce1bea86dee26614a38a3428817
latest_runtime_checkpoint=dce5459279ef9322a62344e4d5c08a0d22d3719a

VoiceBridge repository=kolemasakar/VoiceBridge
branch=agent/krc-media-gemini-migration
PR=45
state=OPEN / DRAFT / UNMERGED
ci_validated_and_deployed_head=751f83f2b1aca79f58e9a5f615296404836ada06
```

Documentation commits after the validated KRC code head use `[skip ci]`.

## Phase state

```text
R3_A=PASS
R3_B=PASS
R3_C=PASS
R3_D=PASS
R3_E1=PASS / COMPLETE
R3_E2=PASS / COMPLETE
R3_E3=CI_PASS / DEPLOY_HEALTH_PASS / DCR_PASS / CHATGPT_OAUTH_CONNECTED / AUTHENTICATED_MCP_TRANSPORT_PASS / CONFIRMATION_UI_PENDING
R3_E4=CI_PASS / DEPLOY_HEALTH_PASS / DCR_PASS / CHATGPT_OAUTH_PENDING
R3_F=LOCAL_PASS / CI_PASS / RUNTIME_ACCEPTANCE_PENDING
R3_G_OAUTH=DEPLOYED / DCR_PASS / E3_TOKEN_FLOW_PASS / TOKEN_RESTART_ACCEPTANCE_PENDING
R3_H=HOLD
R4=HOLD
MEDIA_OPERATION_COUNT=13
NON_EXECUTION_COUNT=9
EXECUTION_COUNT=4
```

## CI acceptance

```text
KRC_RUN=35466720921
KRC_PYTHON_3_13=PASS
KRC_PYTHON_3_14=PASS
KRC_QUALITY=PASS

VOICEBRIDGE_RUN=35466722002
VOICEBRIDGE_CLOUD=PASS
VOICEBRIDGE_IMAGE_PARITY=PASS
VOICEBRIDGE_BROWSER_EXTENSION=PASS
VOICEBRIDGE_REPOSITORY_DOCS=PASS
```

Paid Actions usage was not required or authorized.

## Current runtime audit

```text
VOICEBRIDGE_SERVICE=voicebridge-krc-media-beta-kolemasakar
VOICEBRIDGE_SERVICE_ID=srv-da1kic5bedkc73d6fk60
VOICEBRIDGE_DEPLOYED_HEAD=751f83f2b1aca79f58e9a5f615296404836ada06
VOICEBRIDGE_HEALTH=HTTP_200 / status=ok / version=0.6.0

R3E3_SERVICE=krc-mcp-r3e3-facebook-sentinel
R3E3_SERVICE_ID=srv-danerqmgekts738oejsg
R3E3_PLAN=free
R3E3_HEALTH=PASS
R3E3_SURFACE=r3e3_facebook_execution
R3E3_TOOL_COUNT=3
R3E3_CONFIRMATION_PROBE_ONLY=true
R3E3_CONFIRMATION_PROBE_INVOCATIONS=0
R3E3_PROVIDER_WORK_STARTED=false
R3E3_VOICEBRIDGE_BINDING=true

R3E4_SERVICE=krc-mcp-r3e4-telegram-sentinel
R3E4_SERVICE_ID=srv-danertv40ujc73bn9hog
R3E4_PLAN=free
R3E4_HEALTH=PASS
R3E4_SURFACE=r3e4_telegram_execution
R3E4_TOOL_COUNT=3
R3E4_CONFIRMATION_PROBE_ONLY=true
R3E4_CONFIRMATION_PROBE_INVOCATIONS=0
R3E4_PROVIDER_WORK_STARTED=false
R3E4_VOICEBRIDGE_BINDING=true
```

No live Facebook or Telegram execution is authorized.

## R3-E3 ChatGPT OAuth acceptance

User-visible ChatGPT state:

```text
plugin=MCP E3 Facebook 1
account=connected
```

Render sequence:

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

The initial 401 is the protected-resource discovery step before retry with the issued token. Subsequent authenticated MCP requests succeeded.

Zero-side-effect invariant after connection:

```text
R3E3_CONFIRMATION_PROBE_INVOCATIONS=0
R3E3_PROVIDER_WORK_STARTED=false
NEON_TOTAL_JOBS=1
NEON_FACEBOOK_JOBS=0
POST_CONNECT_ERROR_LEVEL_LOGS=0
```

## R3-E4 OAuth state

R3-E4 DCR and authorization-form preflight are PASS, but the ChatGPT account connection has not yet been completed.

## Durable Neon state

```text
provider=Neon Free
project=krc-media-beta-neon
project_id=plain-snow-71973546
branch=production
branch_id=br-summer-union-b2qlszfv
database=krc_media_beta

managed_jobs=1
instagram_jobs=1
facebook_jobs=0
telegram_jobs=0
```

## R3-F state

The local contract verifies 13 operations: 9 read and 4 execution, with no execution leakage into R3-C and exactly one route-specific start tool per E1/E2/E3/E4 surface. Local and full CI are PASS. Runtime parity closure remains pending.

## Cost / infrastructure policy

```text
PROJECT_COST_POLICY=FREE_ONLY
RENDER_FREE_WEB_SERVICES=ACCEPTED
NEON_FREE_POSTGRES=PRIMARY_DURABLE_DATABASE
OCI_ALWAYS_FREE=ACCEPTED
SELF_HOSTED_COBALT_ON_OCI=ACCEPTED
PAID_HOSTING_FALLBACK=DENIED
PAID_PROVIDER_FALLBACK=DENIED
PAID_ACTIONS_USAGE=DENIED
```

## Storage rule

```text
HP_OMEN_LOCAL_DISK_AS_PROJECT_STORAGE=DENIED
AUTHORITATIVE_PROJECT_STATE=GITHUB_REPOSITORIES
LOCAL_WORKTREE_USE=TRANSIENT_ONLY
```

## Next gate

1. Verify the connected E3 ChatGPT tool surface.
2. Request exactly one `media_facebook_start` while `CONFIRMATION_PROBE_ONLY=true`; validate Cancel first.
3. Repeat and validate Allow-once; confirm exactly one probe invocation, provider work=false and Neon facebook_jobs=0.
4. Connect R3-E4 Telegram through the same secret-safe ChatGPT OAuth path.
5. Repeat E4 Cancel/Allow-once zero-side-effect acceptance.
6. Obtain separate owner approval before any real Facebook or Telegram live canary.
7. Complete R3-F runtime parity and R3-G token-restart acceptance.
8. Proceed to R3-H only after all prior gates pass.

## Hard release boundary

```text
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

`KRC_MEDIA_CURRENT_HANDOFF_V18_5_R3E3_CHATGPT_OAUTH_CONNECTED_CONFIRMATION_PENDING_2026_09_20`
