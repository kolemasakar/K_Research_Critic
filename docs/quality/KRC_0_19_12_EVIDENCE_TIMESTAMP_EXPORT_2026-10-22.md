# KRC 0.19.12 — Evidence, approval time and export acceptance
Date: 2026-10-22. Scope: private plugin, no production/MEDIA/public changes.

## Current release
Plugin ID `plugin_bb3595f295708191a3f9e145ba1ff2d5`.
Private USER release `pluginrel_6ada5b660e188191a65080aa5762eeef` version `0.19.12`.
Canonical GitHub Core update: `0b04e9357bc11db0469febd163f36f99e14db8ba`.
Post-release read of `skills/instructions/SKILL.md`: evidence matrix, approval event capture, export contract, four-choice menu and NO_MCP/FREE_ONLY present (STATIC PASS).

## Inspected vs summary-only evidence
The user-provided example `KRC_SiC_vs_Graphite_Report_2026-10-22.md` labels:
S1: abstract + figure description; S2: abstract; S3: article text; S4: abstract; S5: abstract (research connection to S3).
Future KRC claim verification MUST NOT count abstract-only sources toward independently verified performance, quantitative, safety or mechanistic claims. Abstracts may substantiate only the narrower attributed reporting claim. Full-text/access-limited status must be visible per source, with a per-claim counted/excluded source matrix and provenance reasoning. This is a rules change; older report counts were NOT retrospectively verified from primary full texts.

## Timestamp contract
Record user selection event time before research begins with an actually accessible trusted clock. Keep one approval event record (profile version, choice, timezone, source, timestamp). If unavailable, store APPROVAL_TIME_UNAVAILABLE; never backdate using report time. Static instruction checks PASS; actual event timestamp availability still NOT VERIFIED by live plugin run.

## Export proof from supplied Markdown
Generated: `KRC_SiC_vs_Graphite_Export_VERIFIED.docx` and `KRC_SiC_vs_Graphite_Export_VERIFIED.pdf`, local artifacts, not committed as binary files to GitHub.
Rendered DOCX to 4 PDF pages and inspected contact sheet visually. DOCX: 5 tables, 1 inline figure. PDF: 4 pages, text extracted, claim IDs C1-C5 found, DOI and SHORTFALL text found.
Figure is reconstructed from the report's 2 PASS and 3 SHORTFALL table. Original Markdown had no embedded images; do not misrepresent the figure as original UI export. PDF/DOCX are prototype off-plugin exports, not evidence that installed KRC can itself generate files in every session.

## Remaining acceptance
- Live M02 case with new private release to verify source eligibility, claim tallies, and timing.
- Full provider inspection/provenance graph beyond instruction-level requirements.
- Automatic in-plugin DOCX/PDF generation in ordinary ChatGPT conversations has not been established.
