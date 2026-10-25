# KRC P0 — EXT-S04 authentic publisher PDF acceptance, 2026-10-25

## Source selection and byte-level custody
Source: **K_Science EXT-S04**, Lencis et al., *Methodology for Determining the Correct Ultrasonic Pulse Velocity in Concrete*, Buildings 2024, 14(3), 720. DOI `10.3390/buildings14030720`.

Publisher PDF at `https://mdpi-res.com/d_attachment/buildings/buildings-14-00720/article_deploy/buildings-14-00720.pdf` downloaded directly on `krc-cobalt` using HTTPS, HTTP **200**, `application/pdf`, **2,130,661 bytes**, **15 pages**. Actual source file location (isolated; not committed to GitHub): `/tmp/krc-ext-s04-acceptance/buildings-14-00720.pdf`. PDF title and DOI in content correspond to registry entry.

**SHA-256:** `9a40186cdce051ce2b8f313ea87af3e7c1b30653658621f0e7130679580fc07a`. Recalculated again after test, identical. Prior `https://www.mdpi.com/2075-5309/14/3/720/pdf` returned **HTTP 403** from server; alternate publisher file distribution route resolved it.

## Executed actual-file source inspection
KRC module `source_file_inspection.inspect_source_file()` read real publisher PDF bytes using `pypdf` in a dedicated test venv with `approved_root=/tmp/krc-ext-s04-acceptance`, matched exact hash and 3 page/section descriptors:

| Physical page | Section descriptor | Exact phrase found? |
|---|---|---|
| 3 | METHODS, description of measurement equipment | YES |
| 12 | RESULTS, discussion of UPV changes | YES |
| 14 | LIMITATIONS, no new data declaration | YES |

Result: `TEXT_MATCH_WITH_METHODS_RESULTS`, pages 15, hash verified, 3/3 excerpts found, `scientific_truth_verified=False`, `independent_reviewer_attestation=False`.
Server-produced structured receipt: `/tmp/krc-ext-s04-acceptance/inspection.json` (not in source control). Sections were structurally matched; **full tabulated numbers, figures and raw laboratory data were not independently reanalyzed**.

## Real KRC scientific-cycle rerun
A revised runtime copy of the frozen real source fixture `tests/fixtures/kscience_ext_s04_real_article_pilot.json` gained a source-inspection receipt bound to exact PDF SHA and pages. Crucially, `trace_verified=False` and **NO reviewer signature** was issued: the tool operator is not a separately authorized scientific reviewer.

Actual `scientific_cycle_v3.run_scientific_cycle()` on server:
- source inspection structure `False` for claim admission due `external_trace_not_verified`;
- external attestation `False`, shortfall `independent_attestation_missing`;
- claims **C01 / C02 / C03 = SHORTFALL / SHORTFALL / SHORTFALL**;
- deterministic Critic = `REVISE`;
- final `NO_GO`; publication ready false.

Output: `/tmp/krc-ext-s04-acceptance/e2e_after_pdf.json`, SHA-256 `606684c9500134df7ef6b7564bd4e8d7257ace83dd4afdb62f6c96b75d0456f8`.

Recorded receipt hash `fcd0ba7bdd7a6e6fdda1a54d75a031a5e46e0c85424a060e1ef6379b26a297ce` is **not a verified attestation** and must not be presented as a signed scientific source.

## Evidence-origin audit
The 2024 paper calls itself a synthesis and states that no new data were created or analyzed. It cites earlier research by the **same** Lencis/Udris/Korjakins team:
- Ref 26: *Effect of elevated temperature environment on ultrasonic pulse velocity in curing concrete* (2013), Civil Engineering '13 Proceedings, pp. 11–18; RTU record `https://ortus0m.rtu.lv/science/en/publications/15928`. Source URL in 2024 paper timed out during this pass. Alternative entire 2013 proceedings is publicly indexed at `https://llufb.llu.lv/conference/Civil_engineering/2013/partII/Latvia_CivilEngineering2013Vol4Part2.pdf`; not yet binary-inspected in KRC.
- Ref 27: *Moisture Effect on the Ultrasonic Pulse Velocity in Concrete Cured under Normal Conditions and at Elevated Temperature* (2013), Construction Science 14:71–78, RTU record `https://ortus0m.rtu.lv/science/en/publications/16677`. The 2013 article's reported DOI `10.2478/cons-2013-0011` requires separate DOI metadata verification before admission.
- These are prior publication records with overlapping researchers, **not independent experimental origins merely because they have separate titles**.

## Test results and remaining acceptance gates
Added exact hash/page manifest `tests/fixtures/kscience_ext_s04_pdf_snapshot_manifest.json` and tests `tests/test_p0_ext_s04_pdf_integration.py` (3 new tests). Full isolated regression on `krc-cobalt`: **126/126 PASS, 0 FAIL, 0.93s**.

Publisher HTML version notes indicate file updates; no meaningful scientific alteration was established. Previous DOI audit remained `Crossref METADATA_ONLY`, `Europe PMC NOT_FOUND`, `editorial updates NO_UPDATES_RETURNED`, `retraction clearance NOT_ESTABLISHED`.

### Verdicts
- `PUBLISHER_PDF_OBTAINED=PASS`
- `PDF_SHA_AND_TEXT_METHODS_RESULTS=PASS`
- `CLAIM_AND_ORIGIN_SCOPING=PARTIAL`
- `INDEPENDENT_REVIEWER_SIGN_OFF=SHORTFALL`
- `PUBLISHED_PRIMARY_EXPERIMENTAL_DATA_REANALYSIS=SHORTFALL`
- `KRC_SCIENTIFIC_CYCLE_EXECUTED=PASS_WITH_SCIENTIFIC_NO_GO`
- `PUBLICATION_READINESS=NO_GO`

No new human independent reviewer credential issued, no fabricated scientific endorsement, no real claim promoted to independently proven. No production, media or public service changes.

## Next actions
Audit original cited 2013 studies' full text, identify datasets and overlap; compare equations/experimental tables and figure provenance; receive an authorized independent scientific reviewer decision; rerun signed source and disciplinary Critic. Retain original PDF by hash in approved repository storage under data policy if long-term persistence is needed; current copy is **temporary**.
