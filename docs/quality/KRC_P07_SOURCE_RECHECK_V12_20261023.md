# KRC P0.7 — independent source-audit checkpoint v1.2 (2026-10-23)

Scope: Owner's silicon–carbon anode degradation manuscript, prior recheck v1.1 and the original claim ledger C01–C12. Private KRC plugin stays v0.19.14. No public/MEDIA/production changes.

## Acceptance outcome

| Claim | Status | Reason |
|---|---|---|
| C01 | SHORTFALL | Obrovac [1] original XRD experimental methods/results not independently reread in this pass |
| C02 | SHORTFALL | Liu [2] ~150 nm value from publisher abstract; no full methods reread |
| C03 | SHORTFALL | McDowell [3] amorphous contrast abstract only |
| C04 | SHORTFALL | McDowell [4] stress-dependent kinetics graphical abstract only |
| C05 | SHORTFALL | Liu [5] yolk-shell and 1000-cycle performance described in abstract; experiment procedure not independently inspected |
| C06 | SHORTFALL | Martín-Yerga [12] full-text SECCM/SHINERS supports dynamic SEI, but FEC-specific [6] methods not fully verified. Combined claim retained as SHORTFALL |
| C07 | SHORTFALL | Kim [7] SSRM results verified at abstract level only |
| C08 | PASS | Kirkaldy [8] commercial LG M50T 21700 cell, 40°C and 0–30% SOC, original study reports ~80% Si capacity loss after 4 kAh (~400 EFC), ~10% graphite. Open primary paper and original Zenodo experiment protocol. Both are ONE experimental origin |
| C09 | PASS | Existing verified [9], [10] primary original studies on Li redistribution in different cycle/storage conditions, two origins; not identical-protocol replication |
| C10 | PASS | Fang [11] original paper full-text, Si/LiCoO2 450 mAh pouch full cell; cryo-TEM/EELS, FTIR and microscopy; after 300 cycles porous SEI ~53.5% and up to ~2.5 micrometres; ONE origin |
| C11 | SHORTFALL | Dose [13] abstract and Kirkaldy [8] methods do not yet independently verify complete exact separation of LAM and LLI under one matched condition |
| C12 | SHORTFALL | Magasinski [14] abstract and Liu [5] abstract are not full methods/results verification, nor identical architecture |
 
**3 PASS / 9 SHORTFALL** under the scope of this audit, threshold 1; neither the source paper plus its dataset nor its mirror URLs are counted twice. Shortfall is a status of checked evidence, not disproof.

## Correction/metadata

Nature Materials, Magasinski et al. DOI 10.1038/nmat2725: publisher change history says the 2010 corrigendum corrects spelling of first-author surname in HTML/PDF, not published experimental values. This closes the prior correction-effect UNKNOWN issue, but does not qualify C12 by itself.

## Verified primary-source locations
- C08: https://pmc.ncbi.nlm.nih.gov/articles/PMC9709825/ and actual originating dataset https://zenodo.org/records/7235858 ; DOI https://doi.org/10.1021/acsaem.2c02047
- C09: https://www.nature.com/articles/s41467-021-22662-7 and https://pubs.rsc.org/en/content/articlehtml/2025/eb/d4eb00040d
- C10: https://www.iop.cas.cn/xwzx/kydt/202410/P020241010347214667846.pdf ; DOI https://doi.org/10.1039/D4EE01755B
- Dynamic-only part C06: https://pmc.ncbi.nlm.nih.gov/articles/PMC9543478/
- Corrigendum https://www.nature.com/articles/nmat2725

## Research process and limitations
Executed focused DOI/title/paper/full-text web searches with publisher, institutional author-copy, PubMed/PMC and Zenodo hits. This is a directed secondary checkpoint; no complete provider-by-provider exported hit counts, search result CSV, preregistration or PRISMA flow. Full bibliographic and novelty acceptance **remain OPEN**. No external AI detector or commercial plagiarism service was used; AI results NOT_RUN. No journal selected or author sign-off. P0.7 = REVISE / NO-GO.

## Local artifacts, not yet checked into GitHub
- `Si_C_anode_degradation_manuscript_UA_v1_2_REAUDIT.docx` (rendered 15 pages, visually inspected contact sheet).
- `KRC_P07_claim_ledger_20261023_v1_2.json`
- `KRC_P07_claim_ledger_20261023_v1_2.csv`
Internal deterministic consistency assertions over 12 rows: PASS, but these are not independently repeated plugin runtime tests.

## Next acceptance actions
Full-text primary reads [1]-[7],[13],[14]; use narrow claim-specific PASS whenever eligible, else explicit SHORTFALL. Complete DOI correction/retraction controls for each source, track journal and author review prerequisites, then repeat P0.7.
