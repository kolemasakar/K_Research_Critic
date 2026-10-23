# KRC P0.7 – primary experimental full-text audit v1.3 (2026-10-23)
Scope: owner manuscript `Si_C_anode_degradation_manuscript_UA_v1_2_REAUDIT.docx` and C01–C12 ledger. Risk: incomplete source access. Results refer to narrow source-specific propositions, not cross-lab replication or a systematic review.

## 1. Source audit
- **C02 PASS (1/1):** Liu et al. ACS Nano 2012, https://doi.org/10.1021/nn204476h — original corresponding-author full PDF `https://www.zhugroup.gatech.edu/paper/AN12.pdf`; methods and Results/Figs 1–6, TEM on crystalline SiNPs, reported critical D ≈150±10 nm under their setups. This diameter is NOT a universal rule for all Si–C.
- **C03 PASS (1/1):** McDowell et al. Nano Lett 2013, https://doi.org/10.1021/nl3044508 — `https://web.stanford.edu/group/cui_group/papers/McDowell_aSi.pdf`; in situ TEM on amorphous Si spheres, experimental methods/results, no cracking in studied examples as large as 870 nm; not identical system to C02.
- **C04 PASS (1/1), narrowly scoped:** McDowell et al. Adv Mater 2012, https://doi.org/10.1002/adma.201202744 — `https://web.stanford.edu/group/cui_group/papers/Matt_AM2012.pdf`; measured reaction-front velocity decreases during lithiation, Figs 1–2; mechanical-stress **explanation is an interpretation**, not an independent direct measurement of stress. Same broader research group as C03 but distinct experimental series, no double counting within one claim.
- **C05 PASS (1/1), narrowly scoped:** Liu et al. Nano Lett 2012, https://doi.org/10.1021/nl3014814 — `https://web.stanford.edu/group/cui_group/papers/Liu_NLett_2012.pdf`; authors' fabrication methods (sacrificial silica, polydopamine carbon), Si@void@C structure, TEM/XPS and capacity data; **only the studied design**. No guarantee of industrial performance.
- Carried forward (previous full-text audit): **C08, C09, C10 PASS**. This checkpoint did not repeat their original experiments.
- **C01, C06, C07, C11, C12 SHORTFALL (0/1)** because required narrow methods/results remain insufficiently verified here. In particular C06 combines heterogeneous dynamic SEI and FEC subclaims, so partial support cannot mark combined proposition PASS.

## 2. Totals
One expected verified independent experimental origin per narrow claim, no count of multiple URLs or supporting material as extra origins: **7 PASS / 5 SHORTFALL, 12 total.** Underlying papers do not create a new independent lab replication merely because a review exists.

## 3. Files and integrity
Produced local `Si_C_anode_degradation_manuscript_UA_v1_3_REAUDIT.docx` with a new additive audit appendix (17 rendered pages), corresponding v1.3 JSON/CSV claim ledgers, and performed deterministic assertion tests: 12 unique C IDs, exact 7/5 count, origin counts consistent, verdicts consistent. Rendered DOCX and inspected 17-page visual contact sheet. Historical audit appendices in main document remain unchanged; the LAST appendix is authoritative. No binaries committed to repository during this checkpoint.

## 4. Open gates
Reproducible full search log and results/hit counts, bibliographic DOI correction/retraction check for all source references, proof of novelty, approved target-journal policy, author signoff and licensed similarity/authorized AI detector runs remain NOT COMPLETE/NOT RUN. No confidential manuscript was uploaded to third-party detectors. **P0.7 REVISE / NO-GO**. Private plugin 0.19.14 and public/MEDIA/production environments unchanged. PZ fault-injection campaign remains frozen per canonical roadmap.
