# KRC №90 — REF-27 acquisition retry and fail-closed source admission
Date: 2026-10-25

## Purpose
Acquire the original 2013 Lencis/Udris/Korjakins REF-27 source without altering production. DOI: 10.2478/cons-2013-0011.

## Verified source identifiers
- RTU institutional record: https://ortus.rtu.lv/science/en/publications/16677/fulltext
- Alternate RTU catalog listing: https://ortus0m.rtu.lv/science/en/publications/16677
- Expected SHA-256 from previous custody record: `4bca8f7614ea2cf4681524edb39220dc52fd871203c225a19957e060e623289c`.

## Actual new attempts
- RTU primary endpoint provided `application/octet-stream` to the browser tool and was not exposed as transferable original binary bytes.
- Separate binary download attempts from the primary RTU and alternate institutional endpoint were unsuccessful.
- Other online reproductions/search hits do not demonstrate bytewise identity with the institutional source and were excluded.
- The local extraction test suite ran again: `3 passed in 0.17s`, all synthetic; no original graph coordinate admission.
- Remote execution via Remote Desktop Commander previously returned host security-tool blocking. In this stage no production host action was executed.
- KRC 249/249 repository-level regression from №85 **not re-executed**.

## Evidence acceptance
- Verified original source PDF locally available: NO.
- SHA-256 comparison: NOT PERFORMED.
- Original Figure 1/2 raster extraction: NOT PERFORMED.
- Axis tick identification and calibrated curve values: NOT PERFORMED.
- Scientific graph/Table I agreement: SHORTFALL.
- Scientific approval: NO_GO.

## Next route
Acquire original RTU PDF bytes through an authorized host or user-provided exact source file; require SHA-256 match before extracting physical page 4. If the hash differs, preserve as a separate unverified candidate, do not treat as the canonical original. Continue FREE_ONLY; public, production and MEDIA unchanged.