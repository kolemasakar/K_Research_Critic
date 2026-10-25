# KRC №105 — autonomous source custody and scholarly review controls

2026-10-25. Isolated research checkout at krc-cobalt only.

New module `src/krc_research/source_custody_gates.py` implements actual-file SHA-256 verification and fail-closed methodology/novelty completeness screening. Unlike prior digest-format-only check, the checksum was computed on real original REF-27 PDF at `/tmp/krc-ext-s04-acceptance/ref27_rtu_original_2013.pdf`: 230806 bytes; SHA256 `4bca8f7614ea2cf4681524edb39220dc52fd871203c225a19957e060e623289c`; PASS. This validates bytes, NOT scientific accuracy.

Seven new isolated negative and positive tests cover exact byte hash, content mutation, invalid digest, symlink denial, methodological shortfall, documented-methodology-without-proven-novelty, invalid input. Full research checkout: **288 passed, 0 failed, 2.00s**, exit 0; previous 281.

Existing `revision_history.py` has deterministic package digests, maximum five Critic iterations and duplicate package rejection. No additional new revision-history logic or new tests were implemented in this stage. The scientific and publication gate is NO_GO, external independent reviewer pending as previously agreed. FREE_ONLY; K_Sentinel WAITING_FOR_SENTINEL_READY; production/public/MEDIA unmodified.

GitHub code module commit `f0f81413`. The test file exists on isolated host; synchronization of its new test file remained blocked by tool safety and is **pending**. This document records that boundary rather than claiming the complete GitHub regression is 288/288.