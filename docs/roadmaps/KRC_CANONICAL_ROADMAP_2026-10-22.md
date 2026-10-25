# KRC — Canonical Roadmap v2026-10-22
Status: OWNER PRIORITIES UPDATED; planning and repository documentation only. No production/publication/MEDIA changes.
Precedence: this document supersedes the execution priorities of KRC_OWNER_PRIORITIES_QUALITY_ACCEPTANCE_2026-10-22.md, not its historical observations.

## Principles and product boundary
- FREE_ONLY, Ukrainian by default, evidence traceability, CriticProfile approval, explicit risk floors, external-source cross-checking, Critic and revised final reports.
- Personal KRC remains PRIVATE. As of owner decision 2026-10-25, **private MCP execution is ALLOWED** where a supported, securely registered ChatGPT app exists; no public plugin distribution is intended. Public Research MCP and MEDIA remain distinct and frozen. Skill-only private release 0.19.14 has no bound private MCP app yet.
- The scientific-writing workflow aims for original, independently verifiable, publishable scholarly work in compliance with journals' AI disclosure/authorship rules. No promise to pass AI-text detectors, no deceptive human-authorship claims, no fabricated citations/data, no detector evasion as an acceptance metric. Detectors can be inaccurate and vary by provider; use editorial validation, provenance and reproducibility instead.
- Roadmap labels: P0 first priority; P1 implement after P0; P2 planned; HOLD paused; PZ last.
- GitHub and deployed SHA/version mapping maintained continuously when any executable code is changed, and verified during every chat handoff. No deployment requested now.

## P0 — FIRST PRIORITY: Scholarly research and publication authoring mechanism
P0.1 Requirements and ethics: workflow for original research, literature review, empirical article, systematic review, technical paper; author ownership, target journal requirements, journal-specific AI policy, permitted/required disclosure, contributors' roles, human review.
P0.2 Scientific question: scope, hypothesis/research question, novelty gap, definitions, inclusion/exclusion criteria, theoretical framework and preregistration where relevant.
P0.3 Source acquisition: scholarly database queries (where access exists), DOI/bibliography metadata and deduplication, evidence provenance, citation-to-claim traceability, dates and versions; record missing paywalled/unavailable sources.
P0.4 Research methods: replicable methodology, statistics and uncertainty review, data/material provenance, ethics approvals when applicable, results vs interpretation, tables/figures attribution and reproducibility checklist.
P0.5 Manuscript workflow: outline -> section drafts -> author review -> Critic -> revisions -> journal formatting (IMRaD, abstract, keywords, references, supplementary data, cover letter as needed). Reject unsupported claims and hallucinated citations. Preserve substantive author voice and choices through genuine editing, not style obfuscation.
P0.6 Originality/integrity gate: check attribution and quotation, plagiarism/similarity flags where licensed tools are available, reference consistency, journal AI assistance disclosures, authorship verification, coauthor approval and copyright/licensing. Treat AI detectors as unreliable signals requiring contextual review, not PASS/FAIL gates.
P0.7 Acceptance: >=1 full reproducible sample paper using clearly labeled synthetic/demo data or owner-provided authentic data; every nontrivial claim linked to inspected sources; no invented citations; journal policy checklist; evidence of human author approval; reviewer checklist and an auditable revision log. Report untested limits; do not claim journal acceptance or detector outcome.

## P1 — IMPLEMENT AFTER P0
P1.1 Analysis of scientific studies and publications: methods, bias, statistics, citation networks where available, conflicts of interest, limitations.
P1.2 Real independence of primary evidence: original-source graph, syndication chain, same press release/study recognition, DOI/statement identity and independence UNKNOWN status when not provable.
P1.3 Deep fact checking: atomic claims, contradictions, temporal qualification, source origins and calibrated verdicts.
P1.4 Audit of legal/technical/financial statements: risk-specific verification matrices and applicable jurisdiction/standards; no unsupported professional certainty.
P1.5 Long-document analysis with page/paragraph/fragment references, OCR only if necessary, page and version provenance.
P1 acceptance: representative traceable fixtures per domain, independent cross-checks, no fabricated quotes/citations.

## P2 — PLANNED (not immediate build)
P2.1 Independent systematic quality evaluation KRC Core with frozen gold corpus and expected verdicts, repeat runs, false-positive/unsupported verdict and evidence ledger metrics.
P2.2 Full-cycle CriticProfile -> Research -> Critic -> Report acceptance, profile gate correctness and revisions.
P2.3 Automated source independence verification (extend P1.2 to robust tests and automation).
P2.4 Standardized reliability/contradictions/completeness assessment, citeable evidence score and uncertainty methodology (not fictitious probabilities).
P2.5 Compare conflicting accounts of events (timeline, shared sources, unresolved evidence).
P2.6 Consolidate current version and non-public documentation. Public-facing legal/publishing documents stay HOLD.
P2 acceptance: frozen regression corpus, expected-vs-observed log, reproducible build/spec references and review approval. Continuous quality tests can be added during P0/P1 but formal independent test campaign is scheduled P2.

## Continuous engineering control — SHA/provenance (not public deployment)
During each code/prompt/package change, record repo branch, commit SHA, plugin version/release ID, on-disk file SHA256 if deployed, service PID/start time and whether code has been restarted; NEVER equate disk checksum with running code without proof.
At each new-chat transition, reconcile: current canonical roadmap version, open work, frozen tasks, branch/commit, plugin release/version, deployed host/service and unverified mismatches. No server restart solely to prove parity.

## HOLD — explicitly paused
- Public plugin distribution for Plus, eligibility, With MCP submission/moderation and third-party Plus installation.
- Public MCP abuse hardening, public HTTPS endpoint, security/load acceptance, complete production runtime attestation.
- All MEDIA YouTube/Instagram/Facebook/Telegram, retrieval and transcription end-to-end, video checks with timecodes.
- Public marketplace support/privacy/terms/website and other publication-facing legal files.
- Monitoring of changes to claims/sources over time.
- Production MEDIA/Cobalt/VoiceBridge and any paid provider/VM procurement.
Resume only by explicit owner decision.

## PZ — VERY END OF PLAN
PZ.1 Isolated negative behavior tests for research tools and API validation.
PZ.2 Fault injection (queue exhaustion, worker interruption, SQLite/disk faults, TTL/retention, malformed payloads, rate limit), on isolated copies only; no production experiments.
This is separate from ordinary safety checks and acceptance validation embedded in P0/P1/P2.

## Private MCP execution authorization — 2026-10-25
- Owner permitted `With MCP` for PRIVATE KRC; this supersedes earlier blanket NO_MCP preference for private execution only. Do not silently open HTTP endpoints to the public or treat an unauthenticated local service as cloud-accessible.
- Loopback test executor and dedicated virtual environment created under `/home/krcops/krc-research-private/` on `krc-cobalt`; localhost `127.0.0.1:19014`, separate from existing service `9013`. Live SDK tool calls passed; private plugin app binding/secure remote access remains NOT_CONNECTED.
- Use FREE_ONLY, user-controlled auth and least privilege for any future private app registration. Public catalog publication, MEDIA, load tests and public MCP remain HOLD.

## Immediate next checkpoint
Implement P0.1-P0.2 specification and one scientifically honest sample workflow first, then P0.3-P0.7. P1 only after P0 acceptance; P2 planned after P1. Mark tests PASS only when executed.
