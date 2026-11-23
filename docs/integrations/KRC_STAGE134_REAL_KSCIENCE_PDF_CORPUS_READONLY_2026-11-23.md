# Stage134 real K_Science source pilot (document identity only)

Date: 2026-11-23
Status: REAL_LOCAL_PDF_IDENTITY_4_OF_4_PASS / DOI_SYNTAX_4_OF_4_PASS /
SOURCE_ONLY / NO KRC PROVIDER CAPTURE / NO EXECUTION / NO SCIENTIFIC APPROVAL /
NOT INSTALLED / PRODUCTION_NO_GO.

## External K_Science source-of-truth

- K_Science draft PR17: https://github.com/kolemasakar/K_Science/pull/17
- Real local original PDF manifest (byte size, SHA256, page count, DOI):
  https://github.com/kolemasakar/K_Science/blob/science/stage134-real-corpus-20261123/literature/source_register/STAGE134_REAL_PDF_CORPUS_2026-11-23.json
- Original PDFs are only on the authorized K_Science local PC; not copied to KRC
  VM, repository or a network provider.
- Original PDF hash and first-two-page DOI checks are reproducible with:
  https://github.com/kolemasakar/K_Science/blob/science/stage134-real-corpus-20261123/tools/stage134_verify_local_pdf_manifest.py

## Actual four papers

| Item | DOI | SHA256 of local PDF | Original PDF pages | Classification |
|---|---|---|---:|---|
| Schabowicz 2014 | 10.1016/j.acme.2013.10.006 | b8f152d24ca89b9b195d552206b4a345b5837199384a753b0dd71f64c76c1b70 | 9 | Research, ultrasonic tomography |
| Jain et al. 2013 | 10.1016/j.proeng.2013.03.022 | 5748da4c74054e04b5b3d51109ce6a93470699c02eef0c37e358a05cbe844c20 | 11 | Research, concrete strength from UPV/rebound |
| Volker and Shokouhi 2015 | 10.1016/j.ndteint.2015.01.003 | ecf814b67b8a14fe5fa24bd74673d85a244235afdb660cd469056f72f775c077 | 7 | Research, multi-sensor honeycombing |
| Breysse 2012 | 10.1016/j.conbuildmat.2011.12.103 | 43e737b6ec29ef5667d25a533c85ed710e250265891f2d2921f9fa11ac21ff32 | 25 | Critical review / historical data reanalysis |

All four full-file checksums, file lengths, PDF page counts and DOI printed
on the first two pages were independently recomputed by the K_Science
local read-only script: 4/4 PASS. Fault injection wrong SHA, DOI and file
length: 3/3 expected denials, no original files changed. Publisher pages
were separately matched for DOI and paper title through public web search;
those pages are bibliographic observations, not signed transfer receipts.

## Actual KRC integration result

- Existing Stage134 source-only normalize_stage134_doi accepted 4/4 exact DOI
  strings; no Crossref or Europe PMC request was sent by KRC.
- Existing K_Science Stage134 source-only candidate client accepted the same
  list and source profile, with sent=false, provider_network=DISABLED,
  krc_external_contract=NOT_RATIFIED, profile SHA256:
  bfffa924925759774764ca61eb00d5e726d4e7d83245c8979d9589ed34fdfe60.
- The profile is not a KRC PROPOSED or APPROVED operation; no consent record,
  request ledger, artifact or new GitHub Actions execution was created.
- Installed KRC Stage133 cannot execute bibliography.audit and was not modified.
  Four unrelated active KRC/Sentinel services were independently observed
  ACTIVE / NRestarts=0 during this check.
- KRC Stage134 audit_stage134_provenance full provider-capture contract is NOT
  claimed to have been fulfilled by an offline local-PDF hash.

## Precisely what remains unverified

- KRC did not receive original article bytes or authenticated provider responses.
  A checksum of local PDF bytes proves their local identity, not publisher
  issuance or license status.
- Crossref and Europe PMC live API metadata, corrected retractions and
  publisher update records have not been fetched in the Stage134 execution.
- Methods, results, specimens, experiments and data reuse have NOT been
  independently verified; the actual count of verified independent original
  experimental sources remains ZERO. The Breysse historical review/reanalysis
  is explicitly NOT another independent experimental campaign.
- Local full-text extraction of a later page in the Volker PDF hit a pypdf
  token-budget limit; partial reading is not represented as full-text acceptance.
- K_Science recent translation drafts and standards in docs/standards/uk/_work
  are not new independent scientific articles, and several standard PDFs
  are incomplete previews.

## Next separate release and scientific gates

1. Page-specific full-text science evidence with provenance and actual
   hash-verified source custody, including model/experiment independence checks.
2. Authentic provider capture and bounded FREE_ONLY_METADATA HTTP policy
   with separate explicit owner approval and provider request budget.
3. Stage134 schema/route for bibliography.audit, independent
   KRC/Sentinel/Science verification, negative E2E and rollback.
4. No merge, service change, online provider request, grant or production
   promotion based on the four local-file identity checks alone.

Production NO-GO, scientific_approval=false.
