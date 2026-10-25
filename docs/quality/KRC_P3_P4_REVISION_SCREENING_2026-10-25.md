# KRC №76 — P3/P4 execution report, 2026-10-25

Owner policy: automatic Critic now; genuine independent external reviewer mandatory only at final scientific acceptance. FREE_ONLY; no production/public/MEDIA changes.

## Executable updates
- `src/krc_research/revision_history.py`: 1–5 actual changed research packages; per-package SHA256, recomputed evidence, executed deterministic Critic, iteration issue log. Duplicate input digests and duplicate revision IDs rejected.
- `src/krc_research/scholar_screening.py`: reproducible bounded selection ledger; exact query/provider/timestamp, inclusion/exclusion reason, source origin/access, deterministic digest. A screening record cannot independently verify scientific evidence.
- 15 new tests, full isolated regression **161/161 PASS**.

## EXT-S04 live replay
Two actual revised K_Science source packages processed on krc-cobalt:
- Registry-only: input SHA256 `ce173ca1d6e5c55db38a3c05cada9023f089d4554e37e8559a43ce7443d6f344`; Critic REVISE, gate NO_GO.
- Original MDPI PDF SHA256 and page locators added, with NO independent reviewer attestation: input SHA256 `afa6a5b063ee1510a90496ea36555afd4b2c3808395b36a1346b6d2a182415da`; Critic REVISE, gate NO_GO.

Actual Critic executions: 2; manuscript publication_ready false. Remote evidence output: `/tmp/krc-ext-s04-acceptance/revision_history_2_real.json`.

## P3 owner registry selection
Curated three-source citation-chain set (NOT a worldwide systematic search): INCLUDE EXT-S04 and hash-verified RTU REF27; UNRESOLVED REF26 (canonical binary not obtained). Screening SHA256 `bbb55dfe8a79e3f3e0880f1cbc2fa15123d680ffb2e8cb41073a65b8e87a19e9`. Remote output `/tmp/krc-ext-s04-acceptance/screening_3_sources.json`.

## Acceptance and remaining work
Engineering regression PASS; systematic live free scholarly database discovery NOT YET implemented; manual/independent reviewer NOT RUN; raw data experimental validation NOT RUN. Final scientific acceptance NO_GO. Next P3 live Crossref/OpenAlex query provenance and P4 manuscript revisions with audited content diff.
