# KRC №104 — Parallel P0: offline scholarly cycle

Date: 2026-10-25. K_Sentinel private route not ready; no live transport test attempted.

New `offline_scholarly_cycle.py` composes four bounded *local* operations in sequence: source_search (existing log validation), source_verify (metadata review), critic_review (source-origin evidence count) and research_export (status receipt). Explicit injected callback acknowledges each step, with fail-closed exception on denial or wrong stage. Output always `NO_GO`, `REVISE`, `network_tested=false`, `scientific_approval=false`.

Seven new tests include successful synthetic sequence, missing transport, mismatched acknowledgement, transport denial, unapproved profile, claim evidence shortfall, and stop-on-stage-two. Fresh isolated `krc-cobalt` full suite: **281/281 PASS**, 0 failures, 1.86s, exit 0; previous 274.

Limits: this callback is a test stub without authentication, network transport or verified remote identity; it cannot substitute for K_Sentinel. The source manifest SHA is syntax-checked but not verified against raw source bytes in this workflow. No actual new Crossref request, independent experiment, manuscript authoring or real K_Science request was executed. The four local operations are not complete deployed research service operations, so the nine-stage scholarly workflow remains NO_GO. K_Sentinel dependency is WAITING_FOR_SENTINEL_READY.

Next independent KRC P0: add bounded methodology and novelty audit manifests, input source custody validation against actual approved file bytes, deterministic immutable multi-revision Critic evidence, and negative tamper/failure tests. Live private E2E only when K_Sentinel ready. FREE_ONLY; production/MEDIA/public paused.