# KRC E2 isolated Free Render deployment — 2026-10-01

## Actual creation
- Render workspace: existing owner workspace.
- New isolated service: `krc-e2-instagram-isolated-acceptance` (`srv-dav8r9ou01pc738ro880`).
- Dashboard: https://dashboard.render.com/web/srv-dav8r9ou01pc738ro880
- Public URL: https://krc-e2-instagram-isolated-acceptance.onrender.com
- Plan `free`, region `frankfurt`, Python runtime, branch `agent/krc-public-media-r3-integration`, autoDeploy `no`.
- Build: `python -m compileall plugins/krc_migration_candidate/mcp_canary`.
- Start: `python -m plugins.krc_migration_candidate.mcp_canary.r3e2_http_server`.
- Initial deploy ID: `dep-dav8raou01pc738roch0`; deployment was in progress at the time of creation; do not claim deployed/healthy until verified.
- Non-secret env set: `KRC_MCP_AUTH_MODE=oauth`, `KRC_MCP_SURFACE=r3e2_instagram_execution`, `KRC_MCP_PUBLIC_BASE_URL=https://krc-e2-instagram-isolated-acceptance.onrender.com`, `KRC_VOICEBRIDGE_BASE_URL=https://voicebridge-krc-media-beta-kolemasakar.onrender.com`, `KRC_R3E2_CONFIRMATION_PROBE_ONLY=true`, `KRC_VOICEBRIDGE_TIMEOUT_SECONDS=30`.
- **No secrets** provisioned. This service must remain fail-closed for OAuth and VoiceBridge calls until owner provisions required credentials directly in Render dashboard. Never paste them into chat or GitHub.

## Owner-only secret gate (Render dashboard)
- `KRC_MCP_OWNER_CODE`: unique owner secret entered directly in Render.
- `KRC_MCP_OAUTH_SIGNING_KEY`: unique random 32+ character server-side secret entered directly in Render.
- `KRC_VOICEBRIDGE_BEARER` and any route-specific override: provision only using approved credential routing; do not copy credentials between surfaces blindly. Verify redacted health fingerprint and scope before real provider work.

## Next safe checks
1. Wait for deploy `live` and check public `/healthz` for `confirmation_probe_only:true`, surface and binding status without printing secrets.
2. After owner-only secret setup, verify OAuth and route-scoped binding using non-mutating preflight/lookup; verify free-only flags on canonical VoiceBridge.
3. Only after these gates, consider a controlled one-job test by switching the **isolated** service's probe flag to `false`, with explicit owner approval and verified free STT budget. Existing production E2/E3/E4 flags must remain unchanged.
