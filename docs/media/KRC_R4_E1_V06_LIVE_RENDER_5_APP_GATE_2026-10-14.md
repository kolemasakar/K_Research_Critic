# KRC R4 Private — E1 v0.6 Render release and five-app acceptance matrix
Date: 2026-10-14. Owner ordered steps 1+2+3+4. No paid fallbacks, no consequential MEDIA start, no Telegram LIVE, no public publication.

## 1. E1 client compatibility and repo gate
- E1 v0.5 publicly exposed nine R3C read tools plus E1 YouTube start. New E1 v0.6 narrows advertised tools to five capable read-only actions (get_capabilities, youtube_preflight, youtube_lookup, youtube_status, youtube_segments) and one YouTube start. Other four cross-platform reads remain on canonical R3C.
- Search of KRC code/tests showed explicit E1 count dependencies in tests/test_krc_mcp_r3e1.py; updated and regression checked; union-of-canonical-tools parity across R3C and E1-E4 maintained.
- Exact source HEAD `dfdfff8ae12b3ecdb219d0f5d5c9a9644f885ec8`: 59/59 MCP tests PASS; whole suite 496 PASS, 17 SKIPPED, zero FAIL. Deployment HEAD `66bb67b701cfcb383f6922b086a651d848b5b9cd` added only an audit document after those tested source changes.
- Live Render previous E1 SHA `c7b7f9c9a8d168ce63d1f1efbc5fb8e1dd5bdebe` (2026-10-10). GitHub comparison to deployment HEAD: ahead_by=72, behind_by=0. Although most additions are docs and tests, runtime changes include E1, scoped R3C HTTP diagnostics, feature-gated P0 relay client and related server code. Full 496/17 test results are not equivalent to clearing skipped opt-in tests.

## 2. Owner-directed E1 v0.6 deployment
- Render workspace `tea-d9dsqdjrjlhs73ba1ga0`, service `srv-dall4qv40ujc73ednpqg` (`krc-mcp-r3e1-youtube-sentinel`), FREE plan, autoDeploy=no, branch `agent/krc-public-media-r3-integration`.
- Render deploy `dep-db7g8pqvcj2c73dhs1vg`, exact commit `66bb67b701cfcb383f6922b086a651d848b5b9cd`, finished `2026-10-14T04:26:58.927996Z`, status **LIVE**.
- Fresh unauthenticated read-only `GET https://krc-mcp-r3e1-youtube-sentinel.onrender.com/healthz` returned status ok, surface r3e1_youtube_execution, **tool_count=6, non_execution_tool_count=5, execution_tool_count=1, voicebridge_binding_configured=true, provider_work_started=false**. Other unsupported `/health` returned 404, not a defect.
- Live via E1 connector `media_get_capabilities`: PASS, request `82fcf9e4-67ce-44c4-baf7-2ee1d661bb7b`, postgres durable, paid fallbacks disabled, Gemini free tier true, consent required, Gemini model `gemini-3.8-flash`.
- Live E1 `media_youtube_preflight`: PASS, request `8e96e228-4f34-42e3-9087-8d9dd72b776b`, can_continue true, zero estimated retrieval credits, consent_required=true, model Gemini-3.8-flash. No processing initiated.
- MCP tool-list from a *new* ChatGPT session after release should be checked for full app registration refresh; current session may cache tool declarations. /healthz count proves service-side enumeration, not UI registry cache state.

## 3. Retained-job status/segments gate
- Neon project `plain-snow-71973546` read-only query at `2026-10-14T04:27:20.293Z`: one unexpired job, status FAILED, **zero nonexpired COMPLETED jobs**. Earlier at 04:14:58 and 04:24:49 the result was the same.
- No suitable complete transcript exists for readback. Therefore do **NOT** claim full status+segments success on actual nonexpired COMPLETED job. A new short FREE_ONLY provider start was NOT made solely for acceptance and no Telegram LIVE was started.
- Use an independently created eligible short nonexpired COMPLETED job when available, or seek separately explicit consent for one new FREE_ONLY start with specified source and provider data-use terms. Act before job TTL.

## 4. Updated five-surface acceptance matrix
| Surface | Registration in private 0.1.1 | Relevant read-only smoke | Real unexpired completed-job readback | Status |
|---|---|---|---|---|
| R3C | PASS | PASS, capabilities request c8ffeb34-5d5f-471b-b0af-4bdf73da2a7c; postgres and fallbacks off | NOT TESTED | PARTIAL overall |
| E1 YouTube v0.6 | PASS | PASS, Render live, healthz 6 tools and postdeploy capabilities/preflight | NOT TESTED | PARTIAL overall |
| E2 Instagram | PASS | PASS, preflight request bba2a07f-e78b-417c-8a67-823ea7447412; E2 401->404 absent job correction previously LIVE | NOT TESTED | PARTIAL overall |
| E3 Facebook | PASS | Missing-ID status read gives expected HTTP 404, request 54fecf9c-200e-42fa-a3b4-e49acffeef05 | NOT TESTED | PARTIAL |
| E4 Telegram | PASS | Missing-ID status read gives expected HTTP 404, request c447b3d3-c980-4c80-9a41-efe4ff594c88 | NOT TESTED; LIVE BLOCKED | PARTIAL |
- Missing syntactically valid job HTTP 404 confirms route reachability, NOT successful persistent job reading.
- Private Plugin Creator current release remains v0.1.1 and includes five mappings. Package has policy prompt NEVER call media_telegram_start but NOT independently demonstrated server-side disable. Telegram LIVE BLOCKED by owner policy, global/public R4 HOLD.
- Full acceptance remains **PARTIAL**. Next: new-chat composite E1 six-tool list verification and opportunistic unexpired completed-job status+segments through proper scoped surface.
