# Stage131 bibliography adapter and E2E contract checkpoint — 2026-10-29

## Source-only adapter
Commit `1db5671861565a7af0e775af021c9f380b32788a` includes `src/krc_research/stage131_bibliography_adapter.py` and tests. Offline/injected-fake test run on krc-cobalt RD: **9/9 PASS** (adapter plus classifier). This is **NOT** live Stage131 deployed parity or HTTP integration: installed release remains immutable `49f8b857b46ebdf45636deffe90f8a4ee578bddf`; service remains running. No production changes.

Features: default fail-closed no network, opt-in explicit `allow_network` and injected fetcher, DOI validation, timeout 0-10s, separate provider statuses, no fulltext/independence promotion. Not yet implemented: production HTTPS fetcher, 429/503-specific structured errors, retry budgets and provider headers, external provider/network dispatch integration. This adapter must not be advertised as an E2E bibliography PASS.

## Consumer integration alignment
K_Science PR #7 preliminary 28 scientific E2E cases NOT_RUN, scope paper DOI `10.1088/1757-899X/365/3/032058`, FULL_TEXT in its library claimed but independently checking PDF SHA/figure not yet completed. Crossref+Europe PMC same DOI is only metadata reconciliation, not experiment independence.
KRC actual UDS `krc-transport/2` schema requires partner ACK; draft science_response_v1 is not wire.
Backend stage131 entrypoint remains `enable_internal_science_signing=False`, and user grant never fabricated.
KRC Stage127 transport ACK_WITH_LIMITATIONS remains CLOSED; no added ingress.

## Next gating
1. K_Science + K_Sentinel cross-project schema mapping signed ACK, including 403 preledger and 409/reconciliation and artifact transfer.
2. Scoped owner consent issue/verify/revoke and separately reviewed signer-enabled entrypoint.
3. Bibliography live provider integration with 429/503 behavior and field-level reconciliation, copyright/licensing and proof scope; only then E2E-01..05.
