# KRC P0.7 — v1.4 follow-on audit, 2026-10-23

## Scope
Executed source verification for C01, C06, C07, C11 and C12 and bounded DOI/correction/novelty audit against the existing owner manuscript. Output is a manuscript appendix and machine-readable C01-C12 ledger v1.4. No public/MEDIA/production change and private plugin remains 0.19.14.

## Evidence decisions
| Claim | Status | Access and reason |
|---|---|---|
| C01 | SHORTFALL 0/1 | DOI 10.1149/1.1652421 XRD record plus abstract; original methods and results not independently reread |
| C06 | SHORTFALL 0/1 | Huang DOI 10.1016/j.matt.2019.09.020 publisher summary verifies cryo-EM/FEC mechanism at abstract/summary level, author PDF identified but full method/results inspection not established; combined claim includes Martin-Yerga methods and cannot simply promote both |
| C07 | SHORTFALL 0/1 | Kim DOI 10.1021/acsami.8b07012 publisher abstract gives SSRM and 300 cycles; original detailed methods paywalled |
| C11 | SHORTFALL 0/1 | Dose DOI 10.1039/C8CC00456K RSC/PubMed summary indicates LiFePO4 ref/counter and dQ/dV; article HTML access blocked; detailed LAM/LLI separation not inspected |
| C12 | SHORTFALL 0/1 | Magasinski DOI 10.1038/nmat2725 publisher abstract + original-paper metadata, full methods/result still not independently inspected; Liu 2012 architecture is not same experiment |

Carry-forward scoped claims C02 C03 C04 C05 C08 C09 C10 = PASS from v1.3, NOT re-executed as experiments in this turn. Audit overall remains **7 PASS / 5 SHORTFALL**, no assumption that duplicated URLs are independent origin.

## DOI and retractions
Limited targeted DOI metadata checked via publisher / PubMed pages for five open claims. Systematic machine Crossref/Crossmark/retraction audit of all fourteen primary and four review citations NOT COMPLETED, therefore no all-clear for every citation. Nature Materials linked erratum 10.1038/nmat2749 (2010) **corrects spelling of Magasinski surname** and is not a retraction or revision of conclusions. Verified at https://www.nature.com/articles/nmat2749 .

## Search and novelty
Searches executed 2026-10-23 for exact combinations of source titles, authors, original/full text PDF and methods for each open claim, via web; selected queries and locations documented in DOCX v1.4. No per-engine full hit counts, search export, time stamps for every query, exclusion flow, or independent duplicate screener. Reproducibility PARTIAL, not PRISMA. Existing competing review list from owner manuscript 2025-2026 not replaced by a new exhaustive full-text originality review. Positive claim of scientific novelty NOT VERIFIED.

## Acceptance and tools
Isolated ledger preflight assertion: 12 unique IDs, 7 PASS, 5 SHORTFALL, counts matching verdict, unique origin records used, PASS only if threshold met. DOCX v1.4 renders 19 pages; 19-page contact sheet visually inspected, no obvious clipping. External AI detectors, commercial similarity checker NOT RUN; no manuscript sent. Journal target and human author approval missing.

Artifacts retained as downloadable local files in this conversation: `Si_C_anode_degradation_manuscript_UA_v1_4_REAUDIT.docx`, `KRC_P07_claim_ledger_20261023_v1_4.json`, `KRC_P07_claim_ledger_20261023_v1_4.csv`. Not uploaded as binaries to repo.

**Final Critic: REVISE. P0.7 NO-GO.** Formal PZ negative/fault campaign on HOLD per Canonical Roadmap.
