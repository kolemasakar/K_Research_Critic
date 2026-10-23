# KRC P0.4–P0.7 — Implementation and acceptance specification
Date: 2026-10-23. Status: DESIGN + ONE DEMONSTRATION DRAFT; full runtime acceptance NOT ACHIEVED.

## P0.4 Research methodology gate
Inputs: approved Scholarly CriticProfile, scope, approved research question, accessible sources, study-level provenance.
Artifacts: search_run ledger (providers, precise queries, UTC executed times, filters, result counts, duplicate/exclusion trail), method protocol, scope/type of review; data extraction (experiment, specimen, sample size, controls, test conditions, statistics, uncertainties, ethics / funding).
Reject or label NOT_VERIFIED whenever missing search trace, method access, numeric baseline, independent source inspection or conflicts.
If systematic review claimed, map to PRISMA 2020 (https://www.prisma-statement.org/prisma-2020-checklist) and PRISMA-S as applicable; no compliance claim from narrative search alone.

## P0.5 Manuscript workflow gate
Approved outline -> sections drafted -> claim citation matrix -> method/results boundary check -> technical reviewer/author revisions -> journal-target format -> appendix provenance.
For figures, store input table and rendering method; never recreate unavailable original publisher figures and present them as originals. Every substantive conclusion maps to claim_id / inspected S-code / origin.
Use demonstration draft at `docs/p0/KRC_P0_SCHOLARLY_SAMPLE_SIC_MANUSCRIPT_DRAFT_2026-10-23.md` solely as review fixture; it relies on user-provided KRC report rather than independently reverified studies.

## P0.6 Authorship, integrity and detector gate
For every final manuscript: similarity/plagiarism tool results with actual run provenance (or explicit NOT_RUN); inspect quote/citation integrity, image rights and author contribution/AI disclosure; verify current target-journal AI policy (journal unselected => UNKNOWN). Authorized external AI detectors: capture provider, model/version if disclosed, score and its scale, classification, input scope, timestamp, error, limitations and transcript/file hash; do not average incompatible provider scores or treat detector as authorship proof. In absence of permission or free tool, mark NOT_RUN/UNAVAILABLE; never upload unpublished manuscript without authorization.
COPE publication-ethics position: https://publicationethics.org/guidance/cope-position/authorship-and-ai-tools ; ICMJE's AI authorship guidance (nonbinding outside journals that adopt it): https://icmje.org/recommendations/browse/artificial-intelligence/ai-use-by-authors.html

## P0.7 Acceptance gate
At least one reproducible full sample manuscript with explicit source inspection, scientifically supportable claims, valid bibliographic metadata, verified methods, novelty check, revision trail, suitable target journal policy, rights/AI disclosure and **recorded human-author approval**. Actual detector results to be reported if service accessible/authorized; no guaranteed detector outcome.
The current sample is a **working draft only**: no independent source reread, reproducible search corpus, selected journal, author approval, permission to submit to third-party detector or detector results. Thus P0.7 = NOT_READY. Do not make up an approval merely because owner asked to continue implementation.

## Planned controlled checks now vs PZ
Ordinary P0 bounded acceptance checks (missing DOI, metadata-only, wrong cell scope, contradictory same-origin and incomplete journal policy) can be implemented as unit fixtures during P0, without fault injection or mutating any external system.
**PZ NEGATIVE CAMPAIGN remains LAST** after P0, P1 and P2 acceptance as mandated by canonical roadmap. PZ will cover destructive/isolated malformed payloads, resource exhaustion, worker cancellation, disk/TTL/queue failure and rate-limit attacks only in isolated test copies. Do not execute now merely because the owner requested sequence 1+2+3; step 3 is planned and gated on completion of P0, P1, P2.
No production/MEDIA/public changes. Free-only, NO_MCP.
