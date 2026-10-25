# KRC №98 — REF-27 final evidence admission ledger (2026-10-25)

Canonical author PDF SHA-256 **4bca8f7614ea2cf4681524edb39220dc52fd871203c225a19957e060e623289c** (8 pages), DOI 10.2478/cons-2013-0011. Physical PDF page 3 Table I, page 4 two embedded figure images, page 2 UK-1401 instrument claims.

Eleven evidence controls in the local machine-readable `evidence_registry.json`:
- E01 PDF custody/hash PASS
- E02 nine Table I specimen numbers PASS as *published source literals*
- E03 group UPV mean arithmetic PASS
- E04 source percentage aggregation MIXED / authors original method unresolved; two plausible methods reproduce printed summaries, previously rounded percent method fails K
- E05 Figure 1 / Figure 2 embedded raster existence PASS
- E06 unique Fig1 plotted-to-specimen/aggregation attribution SHORTFALL
- E07 270 m/s UPV fall in first 2 hours SOURCE_REPORTED (source p3/p7), graph-level replication SHORTFALL
- E08 UK-1401 stated ±1% accuracy SOURCE_REPORTED, not verified original device calibration
- E09 chart tick/pixel position total uncertainty SHORTFALL (±5 px earlier was hypothetical)
- E10 external human peer review PENDING until final owner-authorized gate
- E11 full KRC regression PASS, **fresh execution** on isolated `krc-cobalt`: `cd /tmp/krc-p0-offline-20261025 && PYTHONPATH=src .venv/bin/python -m pytest -q tests/`: **253 passed / 0 failures / 2.00s / exit code 0**.

Current automated Critic ledger: `REVISE`. Publication/scientific acceptance: **NO_GO**. Admitted original source numbers and arithmetic do not imply independent experimental validation. Do not use estimated graph point locations to fill unavailable source data or assert figure/table correlation. No source PDF or original experimental observations modified.

Artifacts generated outside repository in isolated local work directory: `stage98/build_registry.py`, `stage98/evidence_registry.json`; these are not asserted to be deployed code. FREE_ONLY; production, MEDIA, public access unchanged.
