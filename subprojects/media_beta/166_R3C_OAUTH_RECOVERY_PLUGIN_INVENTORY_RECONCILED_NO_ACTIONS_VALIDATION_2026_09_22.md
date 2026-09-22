# KRC MEDIA — R3C OAuth recovery + Plugin inventory reconciliation + no-Actions validation checkpoint

Date: 2026-09-22  
Status: **AUTHORITATIVE CHECKPOINT / R3C_OAUTH_RECOVERY_PASS / READONLY_RUNTIME_PASS / PLUGIN_INVENTORY_DRIFT_CLOSED / DOC_SYNC_IN_PROGRESS / R4_CUTOVER_HOLD**

## Scope

This checkpoint records the bounded recovery work performed after checkpoint 165.

No public GPT mutation, Plugin install/remove, Plugin publication/share change, PR merge, `main` mutation, or MEDIA `*_start` execution was performed.

GitHub Actions are currently unavailable and were **not** used as a gate for this recovery.

## Exact runtime/code authority

```text
KRC repo=kolemasakar/K_Research_Critic
KRC branch=agent/krc-public-media-r3-integration
PR22=OPEN / DRAFT / UNMERGED

R3C_RUNTIME_VALIDATED_CODE_HEAD=27585c0ce924c78529b90aaadbfbeee841d0d249
R3C_RENDER_SERVICE=krc-mcp-auth-sentinel
R3C_RENDER_DEPLOY=dep-dap55aegekts73fr0960
R3C_RENDER_DEPLOY_STATUS=LIVE

VoiceBridge repo=kolemasakar/VoiceBridge
VoiceBridge branch=agent/krc-media-gemini-migration
PR45=OPEN / DRAFT / UNMERGED
VOICEBRIDGE_DEPLOYED_HEAD=db9fb62c57fc731732f88ff5b417a0f15be178b6
```

## Validation mode — GitHub Actions unavailable

```text
GITHUB_ACTIONS_CURRENTLY_AVAILABLE=NO
NEW_GITHUB_ACTIONS_RUN=NO
CURRENT_GATE=EXACT_COMMIT_RENDER_BUILD + LIVE_READONLY_RUNTIME
HISTORICAL_CI_RESULTS=REFERENCE_ONLY
```

The exact R3C runtime head was validated through:

- Render build of commit `27585c0ce924c78529b90aaadbfbeee841d0d249`;
- successful service startup;
- `/healthz` read-only health response;
- real OAuth authorization-code flow;
- real ChatGPT R3C `media_get_capabilities` invocation;
- Render-side `POST /mcp -> 200` correlation.

## OAuth failure and remediation

Observed failure:

```text
Invalid authorization request
```

Root cause:

- the original R3C OAuth DCR client was process-memory state;
- after Render restart the legacy ChatGPT `client_id` remained in ChatGPT but no longer existed in server state;
- ChatGPT reconnect reused the legacy client instead of performing a new `POST /oauth/register`.

Accepted remediation:

```text
RESTART_SAFE_OAUTH=ENABLED
KRC_MCP_OAUTH_SIGNING_KEY=SERVER_SIDE_ONLY
LEGACY_COMPATIBILITY=EXACT_PAIR_ONLY
LEGACY_CLIENT_ID=SERVER_CONFIGURED
LEGACY_REDIRECT_URI=SERVER_CONFIGURED
```

The compatibility bridge is fail-closed: both the legacy public client identifier and the exact registered ChatGPT callback URI must match.

One intermediate deploy at commit `ec004ce23c135cb9e113dad371991adb7814b7c2` failed because the legacy redirect validator was referenced during module initialization before its function definition. The ordering bug was fixed, import-time regression coverage was added, and commit `27585c0ce924c78529b90aaadbfbeee841d0d249` deployed successfully.

## OAuth live acceptance

Observed successful flow:

```text
GET  /oauth/authorize -> 200
POST /oauth/authorize -> 302
POST /oauth/token     -> 200
ChatGPT connection    -> CONNECTED
```

R3C health after recovery:

```json
{
  "status": "ok",
  "surface": "r3c_readonly",
  "tool_count": 9,
  "voicebridge_binding_configured": true,
  "execution_tools": "not_enabled",
  "mutation": false,
  "provider_work": false
}
```

## Controlled read-only runtime acceptance

After waking both free-tier Render services, the owner invoked exactly:

```text
media_get_capabilities
```

No other MEDIA operation was called and provider work was not started.

Accepted result highlights:

```text
configured=true
mode=zero_client_managed_beta
durable_store=postgres
restart_resilient_jobs=true

automatic_paid_fallback=false
paid_retrieval_fallback=false
paid_stt_fallback=false
supadata_public_active=false

youtube_retrieval_provider=gemini_youtube_url
youtube_retrieval_credits=0
youtube_gemini_free_tier_only=true
youtube_stt_provider=gemini

instagram_retrieval_provider=cobalt
instagram_retrieval_credits=0
instagram_stt_provider=assemblyai

facebook_free_retrieval_provider=cobalt
facebook_stt_provider=assemblyai

telegram_retrieval_provider=telegram_public_web
telegram_retrieval_credits=0
telegram_stt_provider=assemblyai
```

Render correlation:

```text
R3C POST /mcp -> 200
MEDIA_GET_CAPABILITIES_LIVE=PASS
R3C_TO_VOICEBRIDGE_BINDING=PASS
PROVIDER_WORK_STARTED=NO
```

## Free-tier cold-start note

A retryable `429` was observed while the VoiceBridge free service was cold/asleep. A direct read-only health wake produced an initial `503`, then `/api/v1/health -> 200` after service start.

The final controlled invocation passed after both R3C and VoiceBridge were confirmed awake.

```text
FREE_TIER_COLD_START_EDGE=KNOWN
FINAL_RUNTIME_RESULT=PASS
```

## Plugin inventory reconciliation

Checkpoint 164 was a UI snapshot that visibly included both older and newer private connection artifacts.

Current required surfaces are present:

```text
KRC MCP Canary Sentinel=FOUND
KRC MCP Auth Sentinel R3B=FOUND
KRC MCP R3C Readonly=FOUND
KRC MCP R3D Confirmation Sentinel=FOUND
KRC MCP R3E2 Instagram Sentinel-v5=FOUND
MCP E3 Facebook 1=FOUND
MCP E4 Telegram 1=FOUND
```

Current legacy entries:

```text
KRC MCP Auth Sentinel=NOT_INSTALLED
KRC MCP R3E2 Instagram Sentinel=NOT_INSTALLED
```

Authoritative project history identifies the accepted R3-B connection as `KRC MCP Auth Sentinel R3B` and documents repeated R3-E2 recreate/reconnect cycles after DCR/redeploy resets. The older entries are therefore not required operational surfaces.

```text
PLUGIN_REQUIRED_SURFACES=PASS
LEGACY_PLUGIN_ENTRIES=NOT_REQUIRED
FUNCTIONAL_INVENTORY_DRIFT=NO
RECOVERY_CONSISTENCY_WARNING=CLOSED
REINSTALL_REQUIRED=NO
```

No Plugin installation, removal, permission change, publication, or sharing mutation was performed during this reconciliation.

## Current formal state

```text
R3_A_TO_H=COMPLETE

R3C_OAUTH_RECOVERY=PASS
R3C_READONLY_RUNTIME=PASS
VOICEBRIDGE_BINDING=PASS
MEDIA_GET_CAPABILITIES=PASS
PLUGIN_REQUIRED_SURFACES=PASS
RECOVERY_CONSISTENCY_WARNING=CLOSED

PROJECT_COST_POLICY=FREE_ONLY
GITHUB_ACTIONS_CURRENTLY_AVAILABLE=NO
R4_CUTOVER=HOLD
R4_CUTOVER_AUTHORIZED=NO
```

## Hard boundary

```text
PUBLIC_GPT_MUTATION=NO
PLUGIN_INSTALLATION_OR_CHANGE=NO
PLUGIN_PUBLICATION=NO
PLUGIN_SHARING_CHANGE=NO
MAIN_MUTATION=NO
PR22_MERGE=NO
PR45_MERGE=NO
ADDITIONAL_LIVE_MEDIA_STARTS=NO
```

## Next gate

Synchronize the canonical documentation to this checkpoint. After synchronization, R4 remains on HOLD until a separate explicit owner cutover decision with an exact mutation and rollback package.

Terminal marker:

`KRC_MEDIA_CHECKPOINT_166_R3C_OAUTH_RECOVERY_PLUGIN_INVENTORY_RECONCILED_NO_ACTIONS_VALIDATION_2026_09_22`
