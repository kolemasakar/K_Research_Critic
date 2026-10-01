# KRC E2 existing-service transition — 2026-10-01

Owner decision: use existing Instagram E2 (`srv-dan7vsijnfac73fmrtl0`) for controlled acceptance. Retire/delete extra isolated E2 (`srv-dav8r9ou01pc738ro880`) **after verification**. No new isolated OAuth credentials needed.

## Read-only live checks
- Existing E2 `krc-mcp-r3e2-instagram-sentinel-v2`: Render Free plan, Frankfurt, `agent/krc-public-media-r3-integration`, autoDeploy off, build `python -m compileall plugins/krc_migration_candidate/mcp_canary`, start `python -m plugins.krc_migration_candidate.mcp_canary.r3e2_http_server`.
- Existing E2 public `/healthz`: HTTP 200, `status:ok`, `surface:r3e2_instagram_execution`, `tool_count:5`, `execution_tool_count:1`, `voicebridge_binding_configured:true`, `confirmation_probe_only:true`, `provider_work_started:false`.
- Extra E2 has same branch/build/start, Free plan and autoDeploy off. No secrets were supplied to extra E2 at creation. No owner-provisioned credentials confirmed there.
- Existing E2 has previously passed warmed preflight for the chosen public Instagram URL and zero automatic paid fallback. A full provider E2E has NOT yet passed.

## Controlled transition
1. Capture redacted deployment configuration and latest live deploy SHA of existing E2, verify owner-only secret state without printing values.
2. Confirm actual VoiceBridge free-only capabilities and nonzero *available* STT free quota (zero retrieval credits estimate alone is insufficient).
3. Warm VoiceBridge health to avoid cold-start-correlated nested HTTP 429, then preflight exactly once.
4. Temporarily set `KRC_R3E2_CONFIRMATION_PROBE_ONLY=false` on existing E2 only during owner-approved maintenance acceptance; run exactly one free-only Instagram provider job and capture job ID/status/segments, then restore `true` unless owner explicitly chooses production mode. Do not change E3/E4.
5. Verify existing E2 returned to intended state and no paid provider work occurred. Only then delete the unused isolated service `srv-dav8r9ou01pc738ro880`.

## Deletion tool limitation
Current connected Render integration exposes no delete-service operation. Do not claim automated deletion. After verification, use Render dashboard service Settings > Delete Service or a separately authorized supported tool; deletion must be verified by subsequent Render list_services. Do not delete before owner-requested verification gate.
