# KRC P0: Executed Critic + frozen 12-claim audit — 2026-10-25

## Verified engineering
- Added `src/krc_research/independent_critic.py`: deterministic second-path rule auditor, does not trust the previously reported Critic verdict; explicitly distinguishes rule checking from scientific peer review.
- Added `src/krc_research/research_pipeline_v2.py`: links fail-closed integrated research preflight and actually executed rule Critic.
- Added `src/krc_research/artifact_attestation.py`: reads approved-local-root plaintext files, hashes actual bytes, checks quoted passage locators; never claims to independently verify science or source authorship.
- Added `tests/test_p0_execution_v2.py` with seven tests.
- Actual `pytest` on krc-cobalt isolated repo fixture: **80 passed in 0.54 s**, no failures. Earlier baseline: 73 PASS.

## Frozen corpus, exact owner file
Read `KRC_P07_claim_ledger_20261023_v1_4.json` from the current workspace, SHA256 `820f17b84f97e88c2d729323139044d1d4169ec6f4b17d48140aba1cc75cd764`, with 12 C-claims. The file is NOT committed into GitHub.
Legacy claim statuses: **7 reported PASS / 5 reported SHORTFALL**.
In a new conservative local rule-Critic recheck, lacking freshly verified full-text inspection receipts, all 12 are **UNVERIFIED => 0 new PASS / 12 new SHORTFALL**. This does not disprove earlier research; it prevents recycling unverifiable historical acceptance.
The deterministic rule-Critic was actually executed and repeated with identical output: **REVISE**, not publication ready.
The frozen output file `KRC_P0_12claim_frozen_critic_20261025.json` was generated in the chat workspace; SHA256 `8434a05ca5fe2ebe5206fd31b4879cdd831132f3a983a62e72995be92657746e`.

## Manuscript/report exports
Created a Ukrainian scientific-methodological review of the evidence status (not an original experimental paper), exported from the same v1.4 corpus as:
- `KRC_P0_SiC_12claim_review_20261025.md`
- `KRC_P0_SiC_12claim_review_20261025.docx`
- `KRC_P0_SiC_12claim_review_20261025.pdf`.
The DOCX was rendered to PDF and PNG and visually reviewed. Scientific content remains confined to the source ledger; no new claims, measurements or experimental validation.

## Limitations and next gates
- Hashing file bytes + finding passage locators is **not independent scientific attestation**. A separate reviewer/attestation issuer and provenance-controlled source records are not implemented.
- Rule Critic checks evidence counts, source-gate consistency and manuscript shape; **actual scientific peer review / literature judgment / experimental re-analysis are not done**.
- DOI editorial history still needs full primary-document verification, including the `10.1038/nmat2725` / `10.1038/nmat2749` editorial update.
- AI detector results: **NOT_RUN**; source-text copyright, permission and individual journal disclosure checks still PENDING.
- Author signoff and journal gate: **PENDING**; publication status remains **NO_GO**.
- No media, public exposure, production `9013` or private ChatGPT plugin `0.19.14` changes.

Status: `RULE_CRITIC_EXECUTED_PASS / FROZEN_CORPUS_REVISE / DOCUMENT_EXPORT_PASS / SCIENTIFIC_END_TO_END_NO_GO`.
