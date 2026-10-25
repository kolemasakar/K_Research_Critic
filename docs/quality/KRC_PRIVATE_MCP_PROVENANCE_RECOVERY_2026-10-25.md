# KRC P0 private MCP — 4-track checkpoint, 2026-10-25

## Owner approval and scope
Owner ordered (1) inspection receipts, (2) DOI/editorial audit, (3) private MCP restart management, (4) private ChatGPT MCP integration. FREE_ONLY. Existing Research MCP on 127.0.0.1:9013 and public/MEDIA infrastructure untouched. Private MCP on 127.0.0.1:19014 and private plugin v0.19.14 remain separate.

## 1. Receipt mechanism
- Added `src/krc_research/inspection_receipts.py`: inspection receipt includes source+origin, DOI, SHA-256 of source content, inspected sections/locators, clock+reviewer, relation and verified external trace requirement.
- SHA-256 hash-chain detects changed records in the serialized ledger. It is **tamper-evident, not authenticated truth**: a forged complete chain is possible; source inspection and trace still need independent verification. `trace_verified=False` causes fail-closed; no scientific truth is granted by a hash.
- Exposed `krc_inspection_receipt_review` via MCP: invalid/missing external trace => rejected for independent acceptance.

## 2. Crossref / Europe PMC
- Metadata HTTP adapter now retries **once only** on transient 429/5xx/timeout (0.6 s delay) and remains bounded by 2 MB, per-request timeout, allowlisted provider URLs.
- New 18-DOI exact corpus rerun finished: **12 TWO_PROVIDER_MATCH / 6 PARTIAL**, **1 erratum** for original DOI `10.1038/nmat2725` with correction `10.1038/nmat2749`. Prior 3 editorial update request errors are now zero in the new run; no retraction clearance is asserted.
- Result file `/tmp/krc-p0-offline-20261025/krc_bibliography_live18_20261025.json`, SHA256 `49bc1ac165d918eec1882633db24de13fa7ded95be244843e38af9a27534ba23`.
- No full-text/scientific verification gained merely by metadata match. 6 PARTIAL records were not found in EuropePMC at exact DOI in this run.

## 3. User-space recovery
- New nonprivileged supervisor `deploy/private_mcp_user_supervisor.sh` deployed as `/home/krcops/krc-research-private/private_mcp_supervisor.sh`. It uses `flock`, checks loopback listener and already-running process, executes private venv on port 19014 only; does not affect 9013.
- Current user crontab contains only two new entries (prior user crontab was empty): `@reboot` launch and `*/5 * * * *` guarded restart checks. cron daemon reported active+enabled.
- Actual local restart drill: stopped prior private PID 97300, ran supervisor, observed new PID 97608 and listener 127.0.0.1:19014; MCP SDK smoke passed afterward.
- Reboot survival **NOT TESTED**. Cron checks every five minutes and is not a sub-second watchdog or systemd supervision. Process has no external network listener.

## 4. MCP + ChatGPT route
- Live official MCP SDK smoke tested **SIX** tools: `krc_capabilities`, `krc_scholarly_preflight`, `krc_doi_metadata`, `krc_doi_updates`, `krc_bibliography_audit`, `krc_inspection_receipt_review`. Result `PRIVATE_MCP_SDK_SMOKE=PASS TOOLS=6 NO_GO=PASS BATCH=PASS RECEIPT=FAIL_CLOSED`.
- Installed personal plugin `0.19.14` is still skill-only and has no app mapping; cannot invoke the loopback listener automatically in ChatGPT. Plugin Management cannot resolve a private personal plugin through its global-public dependency lookup. No supported account-level custom-MCP registration action is available in the connected tools. Therefore **PLUGIN_TO_MCP=NOT_CONNECTED**; do not claim the product step succeeded.
- Avoid exposing a unauthenticated tool via public Caddy reverse proxy to solve a connection failure. Use the connected Remote Desktop Commander app as an *engineering access bridge* in this chat until owner has an eligible secure custom MCP connector route.

## Executed tests
On KRC server, actual `pytest` in dedicated `/home/krcops/krc-research-private/.venv` (Python 3.12.3, pytest 9.1.1): **47 PASSED in 0.29s** after adding 5 inspection receipt tests. Supervisor no-op while listener live: PASS. Stop-and-restart private process: PASS. Six-tool official MCP SDK live call: PASS.
No production/publishing/approval claim. Retraction clearance=NOT_ESTABLISHED; AI detectors NOT_RUN; P0-D end-to-end ChatGPT plugin acceptance NO-GO.

## Priority after this checkpoint
Secure real custom MCP connection registration/binding via eligible ChatGPT product tooling, when available; supply external attestable read traces and dated search exports; finish independent retractions and scientific review; test private cron at an authorized reboot window without risking production.
