# KRC private MCP executor — executed acceptance checkpoint, 2026-10-25

## Owner decisions
- Install pytest when needed — APPROVED and completed.
- PRIVATE KRC With MCP is permitted; public publication is no longer a project objective. FREE_ONLY remains.
- Do not make an existing Caddy service or public Research MCP more open merely to enable a cloud client.

## Server state and isolation
- Host: krc-cobalt; account: krcops.
- Existing production experimental service: /opt/krc-public-mcp, 127.0.0.1:9013, active/running, NOT MODIFIED.
- New independent executor files: /home/krcops/krc-research-private/src/krc_research/ (fetched from branch).
- New independent Python venv: /home/krcops/krc-research-private/.venv, Python 3.12.3, mcp==1.30.0, pytest==9.1.1.
- Listener bound ONLY to 127.0.0.1:19014. No Caddy/public reverse-proxy route, no external auth/third-party access. Process started in an interactive remote session, not installed as a persistent managed systemd service; restart survival is UNVERIFIED.
- No production system Python modification, no paid provider, no global package installation.

## Pytest execution
The earlier 37/37 success used a custom runner. This turn installed real pytest in isolated venv, removed the local 'pytest.py' stub and ran:
`cd /tmp/krc-p0-offline-20261025 && .venv/bin/python -m pytest -q tests/test_p0_*.py`
**37 passed**, then re-ran from independent private venv:
`PYTHONPATH=src /home/krcops/krc-research-private/.venv/bin/python -m pytest -q /tmp/krc-p0-offline-20261025/tests/test_p0_*.py`
**37 passed in 0.52s**. These checks prove offline code behavior for scoped fixtures, NOT the full plugin integration.

## New isolated MCP tool service
Source: `src/krc_research/mcp_private_server.py`; transport SDK FastMCP streamable-http, local URL `http://127.0.0.1:19014/mcp`.
Four tool names:
1. `krc_capabilities`
2. `krc_scholarly_preflight`
3. `krc_doi_metadata`
4. `krc_doi_updates`

Private MCP SDK ClientSession established, enumerated four tools, called all four successfully. `krc_scholarly_preflight` returned fail-closed NO_GO on incomplete data. Crossref/Europe PMC DOI metadata response succeeded; Crossref correction detection found 10.1038/nmat2749 for 10.1038/nmat2725. Full scientific source inspection, retraction clearance and author approval NOT IMPLIED. SDK test source: `tests/sdk_private_mcp_smoke.py`.

## Integration constraint, accurately recorded
The currently installed private ChatGPT plugin **0.19.14** has a skill-only package (`plugin.json` and SKILL.md); no App binding / registered app mapping to this new MCP server. Updating instructions cannot create an independently callable ChatGPT tool. An app/connector must be registered and explicitly connected by the owner before the private plugin can invoke the endpoint.

The current loopback listener is not reachable by a ChatGPT cloud MCP client. To make it usable by a ChatGPT app, create a securely authenticated remote transport with host mapping and allowlisted access, register a private ChatGPT app connector, connect it, and bind to plugin. Only after this should a *real plugin chat-to-MCP* acceptance test be marked PASS. Neither private app registration nor secure remote route was performed in this checkpoint; **PLUGIN_TO_MCP = NOT_CONNECTED**. Existing public Research MCP must not be repurposed without review.

## Result
- pytest installed in project-specific venv: PASS.
- GitHub code unit tests via real pytest: 37/37 PASS.
- PRIVATE MCP server active at loopback + SDK 4 tool calls: PASS.
- Existing production 9013 unchanged: PASS.
- True ChatGPT private plugin tool invocation: NOT CONNECTED.
- P0-D end-to-end journal manuscript: NO_GO.
- Next step: supported secure private app registration / binding and E2E plugin test (requires platform app connection action), or use the current Desktop Commander connector as an authorized execution bridge in chats outside the plugin.
