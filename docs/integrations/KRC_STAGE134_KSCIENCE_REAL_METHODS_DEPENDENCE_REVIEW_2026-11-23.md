# KRC Stage134 - K_Science real-paper methods and dependency handoff

Date: 2026-11-23
Status: CROSS_PROJECT_READONLY_RESEARCH_EVIDENCE_RECEIVED /
STAGE134_SOURCE_ONLY / NO_PROVIDER_CALL / NO_CONSENT / NOT_INSTALLED /
EXPERIMENTAL_INDEPENDENCE_NOT_VERIFIED / PRODUCTION_NO_GO.

## K_Science canonical review records

- K_Science draft PR17:
  https://github.com/kolemasakar/K_Science/pull/17
- Four-study machine-readable methods/lineage evidence:
  https://github.com/kolemasakar/K_Science/blob/science/stage134-real-corpus-20261123/literature/source_register/STAGE134_METHODS_SAMPLES_DEPENDENCIES_2026-11-23.json
- Source-backed critical report with source locators:
  https://github.com/kolemasakar/K_Science/blob/science/stage134-real-corpus-20261123/literature/reviews/STAGE134_METHODS_SAMPLES_INDEPENDENCE_REVIEW_2026-11-23.md
- Earlier real-file identity attestations (4/4) and negative tests (3/3):
  https://github.com/kolemasakar/K_Science/blob/science/stage134-real-corpus-20261123/literature/reviews/STAGE134_REAL_PDF_VALIDATION_2026-11-23.json
- No local owner disk access was used for this new methods inquiry.
  Previous temporary Stage134-generated files were moved to GitHub
  with exact verification and removed under owner direction.
  Three repositories have mandatory no-local-disk-without-direct-authorization
  policies.

## Four study categories and statistical unit correction

1. Schabowicz 2014, 10.1016/j.acme.2013.10.006:
   two reported lab specimens (simulated stepped defect, varying thickness)
   and a field member; ultrasonic tomography/defect geometry,
   NOT a strength-regression independent calibration.
   Published evidence tier: publisher abstract and figure snippets only.
2. Jain et al. 2013, 10.1016/j.proeng.2013.03.022:
   approx. 288 cast 150 mm concrete cubes across cement, aggregate,
   mix grades and curing; four per experimental condition, three NDT,
   one destructive reference. UPV, rebound and strength correlation.
   Batch and condition-level independence/held-out structure not proved.
   Evidence tier: author-uploaded public full-text transcription.
3. Volker and Shokouhi 2015, 10.1016/j.ndteint.2015.01.003:
   ONE 30 cm thick reinforced concrete slab with THREE artificial
   honeycombs, tested by IE/US/GPR, Hadamard and Dempster-Shafer
   fusion, same-specimen ROC reference. Three channels, many grid
   cells and three defects do NOT constitute three independent datasets.
   Evidence tier: author-uploaded public full-text transcription.
4. Breysse 2012, 10.1016/j.conbuildmat.2011.12.103:
   historical critical review, secondary reanalysis of prior
   experimental data and synthetic simulations; NOT a new fourth
   independent experimental campaign. Evidence tier: publisher
   abstract and summary only.

The machine graph records SIX pairwise relationships and FOUR
external method/source dependency edges. No directly shared original
data between these four articles was verified; no pairwise independence
of their original data was verified. Reported primary empirical
papers=3, secondary review papers=1, independent experimentally
verified datasets=0.

Important edges: Volker/Shokouhi to Wiggenhauser 2009 specimen-related
reference [7] (citation confirmed, raw-data reuse unknown); same
authors' later clustering paper (possible repeated specimen, not
proved); Breysse to earlier unenumerated author datasets (derived
data confirmed, source IDs unresolved); Jain to IS 13311 tests
(methodological standard, not duplicate raw data).

## KRC engine acceptance implications

- Stage134 metadata-provenance graph must retain SCIENTIFIC_INDEPENDENCE
  = NOT_ESTABLISHED and verified_origin_count=0. Do NOT promote
  separate journals, author affiliations, DOI IDs, sensor modalities,
  voxels, cubes or review papers into independent research counts.
- Real document hash and DOI published page are bibliographic
  identity checks, not cryptographically authenticated provider
  HTTP captures.
- Authentic original raw dataset IDs, repeated-data checks and
  separately verified reference/source-page receipts are future
  tasks. KRC provider metadata (Crossref / Europe PMC) requires
  separate explicit one-owner FREE_ONLY_METADATA approval and
  network budget. None was requested or executed here.
- Installed Stage133 route is not changed. KRC bibliography.audit
  operation remains NOT_INSTALLED and CANNOT execute from this
  source-only report.
- Existing source tests 1349 PASS/24 SKIPPED and focused Stage134
  82 PASS are not re-run here; this is a research evidence handoff.
  KRC review must not claim production or scientific acceptance.

Next gates: authenticated provider receipts, original page-specific
methods/results claims, independent raw data provenance, separate
consent, accepted Stage134 external contracts and multi-project
negative E2E, then human Critic.
