# KRC PRIVATE MCP — bibliography batch, 2026-10-25

## Execution scope
Owner authorized continued engineering development. Private MCP experimental executor remains loopback only on `krc-cobalt`, listening `127.0.0.1:19014/mcp` as user `krcops`. The earlier service on `127.0.0.1:9013` remains active/unchanged. No Caddy route, no public exposure, no deployment of private ChatGPT plugin, no payment/provider auth, no scientific manuscript upload.

## Implementation
- `src/krc_research/bibliography_audit.py` added, bounded 1..24 distinct normalized DOI records per batch, returns Crossref + Europe PMC metadata and Crossref editorial updates separately. Rejects duplicate DOI; errors isolated per provider, no blanket fail/false positive.
- `src/krc_research/mcp_private_server.py` updated with fifth tool `krc_bibliography_audit`. Existing four tools unchanged. Restarted *only the private process* using dedicated `/home/krcops/krc-research-private/.venv`, not public service.
- `tests/test_p0_bibliography_audit.py` added, 5 pytest cases.
- `tests/sdk_private_mcp_smoke.py` updated to inspect all FIVE live tools and exercise batch metadata call.

## Test execution
Python 3.12.3, pytest 9.1.1 (in project venv). Command: `python -m pytest -q tests/test_p0_*.py`; **42 passed in 0.21 seconds**, zero failed. Official MCP SDK client observed **PRIVATE_MCP_SDK_SMOKE=PASS TOOLS=5 NO_GO=PASS BATCH=PASS**.

## Actual 18-DOI bibliography corpus
Source: 14 primary and 4 novelty-check bibliographic DOIs in the Si–C manuscript.
Run via `/home/krcops/krc-research-private/bibliography_live18.py`; output file `/tmp/krc-p0-offline-20261025/krc_bibliography_live18_20261025.json`.
Output SHA-256: `e269fd9d56de08f5d3d79ad9b4b980c3936ee84bb09bf79c9054125365b4c796`.
- Input DOI count: 18; Crossref and Europe PMC TWO_PROVIDER_MATCH: **12**; PARTIAL: **6**, Europe PMC DID_NOT_FIND exact normalized DOI for these.
- Editorial updates: **1 found**, for `10.1038/nmat2725`, related `10.1038/nmat2749` erratum.
- Editorial update checks ERROR on **3** records (`10.1021/nl3044508`, `10.1039/d4eb00040d`, `10.1016/j.jpowsour.2026.240432`). Do NOT claim an all-clear for any citation.
- These are **METADATA checks only**, NOT 12 validated full texts, NOT scientific claim validation, and NOT proof of no retractions. `retraction_clearance=NOT_ESTABLISHED`. Primary source inspection and independent origins remain separate.

## Product boundary and open tasks
The private plugin version **0.19.14** is still skill-only, with no installed ChatGPT app binding to this loopback server; `PLUGIN_TO_MCP=NOT_CONNECTED`. Custom app registration/secure remote transport remains platform-eligibility constrained and requires the owner's permitted product route. Never portray the loopback URL as cloud-accessible. Tests run using Remote Desktop Commander for engineering QA, not user-facing app access.

Process runs as an interactive remote session, not systemd-managed. Persistence after reboot **NOT_VERIFIED**. FREE_ONLY respected.

## Next steps
1. Make a provenance-certified source-inspection ledger (reviewer/time/method reference, not self-attested), offline test and expose through private MCP with no fabricated credentials.
2. Continue full DOI correction/retraction audits and evaluate provider errors without retry storms; clear only validated citations.
3. Implement a permitted app binding/secure private transport when plan permits, and then E2E private ChatGPT plugin tests.
4. Add uptime/restart supervision after privilege review, keeping existing 9013 and public ingress unchanged.
5. P0-D manuscript author/journal approval and output parity remain NO_GO/PENDING.
