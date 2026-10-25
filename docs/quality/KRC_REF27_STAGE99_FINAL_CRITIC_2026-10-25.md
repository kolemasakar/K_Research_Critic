# KRC №99 — REF-27 final internal Critic (2026-10-25)

Canonical reference: Lencis, Udris, Korjakins 2013 DOI 10.2478/cons-2013-0011; 8-page RTU PDF SHA256 `4bca8f7614ea2cf4681524edb39220dc52fd871203c225a19957e060e623289c`. Genuine primary source accepted as source of **reported** experimental findings, not independently validated experimental truth.

## Evidence final state (11 checks)
- E01 original PDF DOI/hash PASS.
- E02 9 published sample rows in Table I PASS.
- E03 source group mean arithmetic PASS; wet/dry (m/s): N 4817.00/4093.33; K 4725.67/4019.00; KV 4764.00/4011.00.
- E04 percentage derivation MIXED: two plausible aggregate calculations match; authors' exact rule unresolved.
- E05 authentic original Figure 1/2 raster existence PASS.
- E06 precise plotted Fig1 curve→source specimen mapping SHORTFALL.
- E07 270 m/s within first two hours SOURCE_REPORTED; independent graph derivation SHORTFALL.
- E08 UK-1401 maximum velocity/time error ±1% SOURCE_REPORTED; actual instrument calibration not documented.
- E09 full metrological/graph uncertainty SHORTFALL (assumed ±5px was a sensitivity test only).
- E10 independent human reviewer PENDING final acceptance by owner-approved policy.
- E11 full research checkout KRC suite rerun on isolated `krc-cobalt`: **253 passed, 0 failed, 1.78 seconds, exit 0**, command `PYTHONPATH=src .venv/bin/python -m pytest -q tests/`.

## Nonrecoverable from paper alone
Original repetitive measurements, calibration certificate, plot's data arrays with unique specimen/aggregate keys, exact original percentage algorithm, rigorously combined uncertainty and independent experimental replication. Do not claim these were verified.

## Critic
Automated internal determination: **REVISE**; publication/scientific acceptance **NO_GO**. Appropriate restricted admission: `CONDITIONAL_SOURCE_ACCEPTED / FIGURE_NUMERIC_SHORTFALL`. Full independent final approval requires additional source data and later external human review.

FREE_ONLY; production, MEDIA, public endpoints unchanged. Local complete UA report `KRC_REF27_STAGE99_FINAL_CRITIC.md` in conversation artifact (not automatically committed).