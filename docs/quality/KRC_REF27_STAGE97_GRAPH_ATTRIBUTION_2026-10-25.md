# KRC №97 — REF-27 curve-to-table attribution gate (2026-10-25)

## Primary source
Owner-uploaded RTU original PDF (DOI 10.2478/cons-2013-0011), SHA-256 `4bca8f7614ea2cf4681524edb39220dc52fd871203c225a19957e060e623289c` verified locally. Original Fig1/2 rasters present; physical page 3 Table I inspected.

## Actual new checks
1. Recomputed dry and saturated group mean UPV m/s directly from the 9 published Table I specimen rows:
   - N wet 4817.00 / dry 4093.33
   - K wet 4725.67 / dry 4019.00
   - KV wet 4764.00 / dry 4011.00
2. Compared previous exploratory Fig1 x~0% graph readings (N 4029.6, K 3931.0, KV 4049.3 m/s) to table dry **group** averages; diagnostic differences approx N -63.7, K -88.0, KV +38.3 m/s. A sampled individual value (e.g. K-12.28 dry 3931 m/s) can resemble a plotted marker. These coincidences do **not** prove sample identity, group averaging rule, or graph mispublication.
3. Fig2 axis is an already accumulated **decrease in UPV** from 200 to 400 m/s, not absolute UPV or a zero-based change. Initial displayed points near time 0 are already ~220–250 m/s; readings near 2h are around ~270–290 m/s. The author's “270 m/s during first two hours” can refer to decline from an earlier saturated reference, but source plot has no independently established baseline/point attribution. Status SOURCE_REPORTED, not independently verified.
4. Local reproducible script `stage97_audit.py` produced `stage97_audit.json`, Critic REVISE / scientific NO_GO. Local earlier suite rerun: **11/11 PASS**.
5. Fresh **full KRC isolated** suite on `krc-cobalt`: `PYTHONPATH=src .venv/bin/python -m pytest -q tests/` from `/tmp/krc-p0-offline-20261025` → **253/253 PASS**, 1.80s, process exit 0.

## Claim admissibility
Table I primary printed source and exact arithmetic PASS. Fig1 numerical identification of individual specimens and interpolation rule SHORTFALL. Fig2 270-m/s/2-hour graphical replication SHORTFALL. No independent second human chart annotation. Do not admit approximate image-to-table agreement as independent science evidence. Automated Critic outcome REVISE; scientific publication gate NO_GO.

FREE_ONLY; production, MEDIA, public endpoints not changed.