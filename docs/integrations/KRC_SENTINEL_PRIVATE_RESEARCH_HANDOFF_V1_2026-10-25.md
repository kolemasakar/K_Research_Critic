# KRC → K_Sentinel integration handoff v1 — 2026-10-25

Source-reviewed isolation: `/tmp/krc-p0-offline-20261025/src/krc_research/{interproject_contract,science_dispatch,offline_acceptance,bibliography_audit,inspection_receipts}.py`. This is not a live MCP tools/list schema and **not** a deployed private service API.

## Operation matrix

| Contract operation | Implementation | Input contract | Output type | Side effects |
|---|---|---|---|---|
| `research.profile.validate` | NOT_IMPLEMENTED | Envelope accepts name, no actual handler schema | raises ValueError | none |
| `research.evidence.preflight` | OFFLINE_ONLY | payload: user_profile_approved=true; manuscript_gate with eight boolean fields; optional claims[], search_runs[] | dispatcher {task_id,operation,status,engine_result,scientific_approval:false}; engine_result KRC-P0D-1 | claims may be processed; durable replay claim if registry provided; no provider |
| `research.bibliography.audit` | OFFLINE_DISPATCH_CAN_TRIGGER_PROVIDER | payload.dois: list of 1..24 distinct normalizable DOIs | engine_result KRC-BIB-1; dispatcher wrapper | Crossref / Europe PMC network calls (if default audit used), replay claim |
| `research.inspection.review` | OFFLINE_ONLY | payload.receipt: InspectionReceipt dataclass fields | {receipt_sha256,eligible_for_independent_claim_review,shortfalls,scientific_truth_verified:false} in dispatcher wrapper | replay claim only; hash is not evidence that inspector genuinely inspected text |

## Mandatory envelope (KRC-SCIENCE-1)
Exactly 8 JSON members: version='krc-science/1', task_id (ASCII regex ^[a-zA-Z0-9][a-zA-Z0-9_.:-]{7,119}$), client='K_Science', provider='K_Research_Critic', operation (one of four above), created_at timezone-aware ISO datetime, payload JSON object (canonical encoding <=262144 bytes), payload_sha256 computed from canonical JSON with sorted keys, no NaN. Separate HMAC-SHA256 signature over complete envelope; key must be >=32 bytes; max absolute age 600 seconds; exact route ACL and time/replay checks; durable registry required in deployment.

`research.evidence.preflight` requires a `manuscript_gate` with booleans journal_policy_checked, search_audit_reproducible, primary_sources_inspected, novelty_reviewed, citations_validated, scientific_methods_audited, rights_and_ai_disclosure_done, human_author_approved. Optional detector_check_status=NOT_RUN/UNAVAILABLE/COMPLETED; detector_authorized boolean; detector_run_records array of {provider, checked_at, input_hash} for completed or recorded checks. Claims are evidence ledger entries with claim_id, required, and Evidence dataclass list. search_runs are SearchRun dataclass entries.

`research.inspection.review`: receipt includes source_id,origin_id,doi,document_sha256,inspected_sections,passage_locators,checked_at,inspector_id,method,evidence_relation,external_trace_id, optional trace_verified=false. Audit does not verify scientific truth or source bytes by itself.

## Error boundary
Internal exceptions are ValueError/TypeError etc., **no confirmed stable machine error code/HTTP mapping**. K_Sentinel must explicitly implement structured errors, restrict exposed details, and not infer HTTP 200 from internal function returns. Do not equate the public MCP tool `research_profile_validate` (FIFO) with private `research.profile.validate` (currently not implemented).

## Zero test and blocked dependences
- Read-only public MCP `tools/list` is safest zero test, but only checks public tools. On-host source identified 7 tools: guest_session, research_submit, research_status, research_document_upload, research_profile_validate, claim_evidence_audit, research_report_validate. Live tools/list schema still **NOT_VERIFIED** this stage.
- Previous K_Science `krc_capabilities` bounded read-only with replay denial is separate, not four-operation proof.
- Private K_Sentinel live route `WAITING_FOR_SENTINEL_READY`.
- No tokens, keys or private documents included.
- FREE_ONLY, production/MEDIA/public unchanged; science approval NO_GO.

## Current QA
Stage105 isolated suite rerun on krc-cobalt **288/288 PASS**, 2.12s, exit code 0. Stage105 missing GitHub test/docs synchronization resolved.
