# KRC R4 — E1 v0.6 scope-aligned read-only surface acceptance (2026-10-14)

## Decision and reason
Earlier E1 v0.5.0 advertised all nine R3C read-only tools in addition to its YouTube start, but E1-scoped bearer cannot authenticate Instagram Cobalt or generic managed non-YouTube reads. In the private composite R4, E1 Instagram preflight/lookup gave HTTP 401. Changing authorization scope would weaken isolation; choose versioned *surface reduction* while keeping R3C complete and E2/E3/E4 their own operations.

## Source implementation
Private repo `kolemasakar/K_Research_Critic`, branch `agent/krc-public-media-r3-integration`, exact HEAD `dfdfff8ae12b3ecdb219d0f5d5c9a9644f885ec8`.
- `plugins/krc_migration_candidate/mcp_canary/r3e1.py`: bump E1 server version **0.5.0 -> 0.6.0**, declare `R3E1_READ_TOOL_NAMES` five authorized names: `media_get_capabilities`, `media_youtube_preflight`, `media_youtube_lookup`, `media_youtube_status`, `media_youtube_segments`; append only `media_youtube_start`. Filter descriptors from original R3C canonical list; no change to R3C descriptors, backend routes or token access.
- `tests/test_krc_mcp_r3e1.py`: update six-tool/5-read contract and health assertions, add regression that all four excluded cross-route read names are absent and rejected locally with `-32602 Unknown tool`.
- Source commit `4cbbccca5bfa71827b95f727276db42665467311`. Tests commit `dfdfff8ae12b3ecdb219d0f5d5c9a9644f885ec8`.

## Actual execution evidence
On authorized `krc-cobalt`, detached worktree from **exact GitHub HEAD** `dfdfff8...`.
- Cross-component MCP suites `test_krc_mcp_r3c.py`, `test_krc_mcp_r3e1.py`, `test_krc_mcp_r3e2.py`, `test_krc_mcp_r3e3.py`, `test_krc_mcp_r3e4.py`, `test_krc_mcp_r3f_local_parity.py`: **59 PASS**, 0 failures, ~1.32s.
- Whole `pytest -q` repository suite: **496 PASS, 17 SKIPPED, 0 FAIL**, exit 0, ~22.61s; log `/tmp/krc_e1_v06_exact_full_pytest_20261014.log`. The 17 skipped tests are opt-in and NOT proof of full optional acceptance.

## Deployment and limitations
- **NOT deployed** to E1 MCP application or updated in registered app backend. Private R4 Plugin Creator package v0.1.1 was NOT rebuilt/published; live tool list remains old until approved E1 surface rollout.
- Existing R3C nine read-only tool surface stays untouched; E2/E3/E4 remain separate and present in private R4 mapping.
- E1 YouTube start still requires explicit Gemini Free data use acknowledgment and consequential confirmation. No provider work, Telegram start, paid fallback or Render deploy.
- Current Neon check returned **one nonexpired FAILED job, zero nonexpired COMPLETED**; thus no unexpired successful transcript to test readback without fresh approved MEDIA work. Do not manufacture a readback PASS.
- This is a versioned contract breaking change to E1's read descriptors (10 tools → 6). Before rollout, check consumer expectations and connector mapping; versioned coordination of E1 MCP server and plugin tool metadata may be necessary.

## Next gate
1. Review E1 clients and existing consumers for legacy nine-read dependencies. Do not silently publish changed tool list.
2. Owner-controlled E1 MCP v0.6 deployment only after compatibility check, then read-only verify tool count six and approved YouTube preflight.
3. For real job readback, wait for an eligible unexpired COMPLETED job or explicitly approve one short FREE_ONLY test and immediately read status+segments before 3600s TTL.
4. R4 public/general release remains HOLD; E4 LIVE BLOCKED by policy.
