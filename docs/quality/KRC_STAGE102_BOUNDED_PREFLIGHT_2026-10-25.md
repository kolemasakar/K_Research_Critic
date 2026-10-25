# KRC №102 — isolated signed scholarly preflight

Date: 2026-10-25. Isolated host krc-cobalt, directory `/tmp/krc-p0-offline-20261025`, no production deployment.

Added local module `src/krc_research/bounded_workflow.py` and tests `tests/test_p0_bounded_workflow.py`. The wrapper restricts execution to `research.evidence.preflight`, uses the existing signed envelope verification and SQLite replay registry, requires approved CriticProfile and source manifest SHA256 syntax, and returns Critic `REVISE`, publication `NO_GO`, scientific approval false. Source hash syntax alone does NOT verify source bytes or independent evidence.

One correctly signed, bounded request passed via local test and its repeated task ID was rejected after SQLite registry reopening. Six negative checks cover invalid signature, disallowed operation, unapproved profile, malformed digest, missing manuscript acceptance schema, and attempted self-approval. Fresh full isolated regression: **267/267 passed**, 0 failed, 1.89 s, exit 0; previous 260.

Limit: this is an isolated entrypoint only; not the complete nine-stage research service and NOT a real K_Science-to-KRC network E2E transaction. The local source/test changes have not yet been copied to the tracked GitHub branch. Publication and scientific acceptance remain NO_GO. FREE_ONLY, no production/MEDIA/public changes.
