# KRC №101 — P0 scholarly workflow readiness control

Date 2026-10-25. Target isolated checkout on krc-cobalt `/tmp/krc-p0-offline-20261025`, not production.

New module `src/krc_research/workflow_readiness.py` and seven tests `tests/test_p0_workflow_readiness.py`. It validates an approved CriticProfile flag, a 64-character hexadecimal SHA256 source manifest identifier, rejects an incoming scientific_approval=true, records input digest, and returns nine proposed workflow stage statuses. Four local gate labels are `LOCAL_GATE_AVAILABLE`; remaining five stages explicitly `NOT_IMPLEMENTED`. **Local gate label is not a completed research service operation**; none of the nine stages is claimed to be a fully deployed authenticated workflow.

Fresh isolated regression `PYTHONPATH=src .venv/bin/python -m pytest -q tests/`: **260/260 PASS**, 0 failures, 1.90 s, exit code 0, prior 253. Seven new tests include denial behavior and package digest stability.

No real K_Science scientific payload or measurements were sent, no full remote scholarly invocation carried out. Existing bounded signed dispatch `research.evidence.preflight`, `research.bibliography.audit`, `research.inspection.review` is separate from the nine future service operations; current integration accepts only a bounded read-only `krc_capabilities` route with replay rejection.

Caution: input SHA256 is a syntax-validated supplied manifest digest, **not** cryptographically verified against provided source-file bytes by this function. `verified_primary_sources` is caller-provided and must not be treated as independently verified evidence. Critic output is conservative `REVISE`, publication `NO_GO`, service_dispatch_ready=false.

Next P0: authenticated fail-closed service contracts and actual source custody; add standalone research_start/source_search/source_verify/methodology_review/novelty_review/critic_review/manuscript_build/publication_gate/research_export progressively with real bounded handler tests, durable replay, ACL and end-to-end authorized K_Science→KRC evidence receipts before claiming readiness.

FREE_ONLY; no production/MEDIA/public change. REF27 scientific NO_GO unchanged.