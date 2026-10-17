# KRC Public MCP + Cobalt stability audit — 2026-10-17

**Mode:** OCI `krc-cobalt`, FREE_ONLY, read-only Cobalt probes, no Caddy/Docker/MEDIA changes, no external MCP exposure. Executed through authorized Desktop Commander.

## Baseline
- `krc-public-mcp.service`: systemd active; PID 76826; systemd `MemoryMax=201326592` bytes (192 MiB), `CPUQuotaPerSecUSec=500ms` (50%), `NRestarts=0`.
- Starting memory.current 42,500,096 bytes. MemoryPeak ~40.8 MiB before load.
- Cobalt `127.0.0.1:9000/` HTTP 200. Docker and Caddy active.
- Production MCP `/opt/krc-public-mcp/server.py` SHA256 `b280b686c4538ddb4c9c1e36801fd484b7d8ab369464e44fa88627b7160fa227`, same SHA as test GitHub checkout at start.
- `GET http://127.0.0.1:9013/mcp` returned 406 without MCP-specific Accept header; not a failure, only transport check.

## 74-second repeated load test
Using official MCP SDK on the actual local service, 12 rounds of 10 concurrently started guests (120 completed calls). Each guest: `initialize`, `guest_session`, submit `claim_evidence_audit` with three origins (including a duplicate), retrieve completed result by capability, acknowledge delivery. Four seconds spacing between rounds.
- **120/120 PASS**; total scripted duration `74.01 s`, worst round `2.404 s`.
- MemoryCurrent before: `42,500,096 B`; after: `42,479,616 B`; maximum of end-of-round samples: `42,799,104 B`. systemd MemoryPeak at post-check: `43,028,480 B` (~41.03 MiB), comfortably under 192 MiB.
- CPU cgroup deltas: `usage_usec +7,558,702`, `nr_periods +424`, `nr_throttled +110`, `throttled_usec +4,167,048`. CPU throttling occurred (110 / 424 periods); no observed request failures.
- memory.events deltas all zero: low/high/max/oom/oom_kill/oom_group_kill/sock_throttled.
- `NRestarts=0` after test; service remains active.
- Cobalt `GET /` checked once after each round: 12/12 HTTP 200, latency from `2.24` to `57.76 ms`; no detected degradation *of this health route*.
- Docker/Caddy/MCP all remain active.
- Isolated regression tests: `12/12 PASS` under `-W error::ResourceWarning`. They cover FIFO, restart preservation, guest isolation, document content, ACK retention, TTL cleanup, 10% free-disk admission, concurrent submissions. These use isolated ephemeral SQLite, NOT destructive production DB writes.

## Evaluation by requirement
| Requirement | Verdict | Caveat |
|---|---|---|
| Sustained concurrent MCP with Cobalt HTTP | **PASS limited** | 74 seconds, 120 short jobs, Cobalt health only |
| FIFO / concurrent submissions | **PASS limited** | unit regressions and end-to-end job retrieval; strict order under huge concurrent pressure not independently traced |
| SQLite WAL and restart recovery | **PASS offline only** | isolated unit DB, no production crash/restart imposed |
| Delivery, 10h TTL and temp cleanup | **PASS offline only** | artificial timestamps; no actual 10h soak |
| MemoryCurrent/Peak, CPU throttling, memory.events, restart count | **PASS measured** | CPU throttled; no OOM or restart |
| No degradation of MEDIA | **NOT VERIFIED** | no actual media extraction/transcription started, per owner no-change rule |
| Overall unconditional production readiness | **HOLD** | media co-load, long soak and adversarial/queue-storage scenarios remain |

## Open findings
1. A 74-second stress test is not a long endurance test; do not claim hours-long validation.
2. Actual Cobalt MEDIA pipeline was not exercised. HTTP 200 does not establish video function continuity.
3. The queue/DB cleanup passed isolated tests, but direct production SQLite was not manipulated; production WAL was not inspected due least-privilege `krcops` ownership restrictions. K_Sentinel can complete authorized read-only database integrity/operational inspection.
4. `10%` disk guard is checked at admission, not guaranteed against disk writes by other services.
5. Observed 110 throttled CPU periods under load, approximately 25.9% of measured cgroup periods. Not a failure at tested load, but monitor tail latency at larger payloads.
6. New public access needs anti-abuse controls and direct ChatGPT client acceptance.

## Handoff to K_Sentinel
Please confirm controlled read-only container health/status; evaluate real MEDIA co-load in a separately approved non-destructive scenario; review SQLite WAL integrity without modifying the live database; run extended monitoring and queue backpressure; preserve systemd limits and no public MCP exposure. Release gate remains HOLD until acceptance.

## Artifacts
Runtime JSON evidence: `/tmp/krc-mcp-stability-report.json` on `krc-cobalt`. Test harness: `/tmp/krc_mcp_stability_readonly_cobalt.py`. Both contain synthetic request metadata only, not guest capabilities or sensitive content; temporary files, not committed. This Markdown report captures aggregate facts permanently.
