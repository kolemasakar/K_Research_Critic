"""Strict source-derived Stage131 science semantics, source-only; never grants approval."""
from .stage131_consumer_boundary_checks import validate_science_result

class SemanticContractError(ValueError):
    pass

def _require(ok, code):
    if not ok: raise SemanticContractError(code)

def validate_operation_result(obj, *, task_id, operation):
    _require(validate_science_result(obj,expected_task_id=task_id,expected_operation=operation)=="VALID_SHAPE_ONLY","INVALID_ENVELOPE")
    e=obj["engine_result"]
    if operation=="research.evidence.preflight":
        _require(set(e)=={"schema","result","historical_report","final_publication_status"} and e["schema"]=="KRC-P0D-1","PREFLIGHT_FIELDS")
        r=e["result"]
        expected={"status","claim_ledger","search_logs","search_reproducibility","manuscript_gate","submission_ready","reason"}
        _require(isinstance(r,dict) and set(r)==expected,"PREFLIGHT_NESTED_FIELDS")
        ledger=r["claim_ledger"]; logs=r["search_logs"]; gate=r["manuscript_gate"]
        _require(isinstance(ledger,dict) and set(ledger)=={"count","pass","shortfall","status"},"INVALID_CLAIM_LEDGER")
        _require(all(type(ledger[k]) is int and ledger[k]>=0 for k in ("count","pass","shortfall")) and ledger["count"]==ledger["pass"]+ledger["shortfall"] and ledger["status"]=="PASS","LEDGER_COUNT_MISMATCH")
        _require(isinstance(logs,list) and all(isinstance(x,dict) and x.get("status") in ("REPRODUCIBLE_LOG","PARTIAL_LOG") and all(k in x for k in ("provider","query","hit_count")) for x in logs),"INVALID_SEARCH_LOG")
        _require(r["search_reproducibility"]==("PASS" if logs and all(x["status"]=="REPRODUCIBLE_LOG" for x in logs) else "SHORTFALL"),"SEARCH_STATUS_MISMATCH")
        _require(isinstance(gate,dict) and set(gate)=={"status","missing_gates","detector_status","detector_results_count"} and gate["status"] in ("READY_FOR_AUTHOR_REVIEW","REVISE") and isinstance(gate["missing_gates"],list) and type(gate["detector_results_count"]) is int and gate["detector_results_count"]>=0,"INVALID_MANUSCRIPT_GATE")
        _require(r["submission_ready"] is False and isinstance(r["reason"],str) and bool(r["reason"]),"UNSUPPORTED_SUBMISSION_APPROVAL")
        expected_status="REVISE" if ledger["shortfall"] or r["search_reproducibility"]!="PASS" or gate["status"]!="READY_FOR_AUTHOR_REVIEW" else "READY_FOR_AUTHOR_REVIEW"
        _require(r["status"]==expected_status,"PREFLIGHT_STATUS_MISMATCH")
        expected_publication="NO_GO" if expected_status=="REVISE" else "AWAIT_AUTHOR_JOURNAL_SIGNOFF"
        _require(e["final_publication_status"]==expected_publication and obj["status"]==("REVISE" if expected_status=="REVISE" else "PENDING"),"PUBLICATION_STATUS_MISMATCH")
        _require(e["historical_report"] is None or isinstance(e["historical_report"],dict),"INVALID_HISTORICAL_REPORT")
    elif operation=="research.bibliography.audit":
        _require(e.get("schema")=="KRC-BIB-1" and isinstance(e.get("records"),list),"INVALID_BIBLIOGRAPHY")
        rows=e["records"]; n=e.get("count")
        _require(type(n) is int and 1<=n<=24 and n==len(rows),"BIBLIOGRAPHY_COUNT_MISMATCH")
        required={"doi","metadata_status","has_recorded_updates","updates_status","retraction_clearance","methods_results_verified","experimental_origins_verified","providers"}
        _require(all(isinstance(row,dict) and set(row)==required and row["metadata_status"] in ("TWO_PROVIDER_MATCH","PARTIAL") and row["retraction_clearance"]=="NOT_ESTABLISHED" and row["methods_results_verified"] is False and row["experimental_origins_verified"]==0 and isinstance(row["providers"],dict) for row in rows),"INVALID_BIBLIOGRAPHY_RECORD")
        _require(e.get("retraction_clearance")=="NOT_ESTABLISHED" and e.get("full_texts_inspected")==0,"UNVERIFIED_BIBLIOGRAPHY_PROMOTION")
        _require(type(e.get("two_provider_metadata_matches")) is int and e["two_provider_metadata_matches"]==sum(x["metadata_status"]=="TWO_PROVIDER_MATCH" for x in rows),"METADATA_COUNT_MISMATCH")
        _require(type(e.get("updates_detected")) is int and e["updates_detected"]==sum(x["has_recorded_updates"] is True for x in rows),"UPDATE_COUNT_MISMATCH")
    elif operation=="research.inspection.review":
        _require(set(e)=={"receipt_sha256","eligible_for_independent_claim_review","shortfalls","scientific_truth_verified"},"RECEIPT_FIELDS")
        _require(isinstance(e["receipt_sha256"],str) and len(e["receipt_sha256"])==64 and all(c in "0123456789abcdef" for c in e["receipt_sha256"]),"RECEIPT_HASH")
        _require(type(e["eligible_for_independent_claim_review"]) is bool and e["scientific_truth_verified"] is False,"UNVERIFIED_INSPECTION_PROMOTION")
        _require(isinstance(e["shortfalls"],list) and all(isinstance(x,str) and x for x in e["shortfalls"]) and e["eligible_for_independent_claim_review"] == (not e["shortfalls"]),"RECEIPT_SHORTFALL_MISMATCH")
    elif operation=="research.profile.validate":
        _require(set(e)=={"schema","profile_id","profile_version","protocol","validation","approval_claimed","approval_independently_verified","scientific_approval"},"PROFILE_FIELDS")
        _require(e["schema"]=="KRC-CRITICPROFILE-1" and e["validation"]=="STRUCTURE_VALID" and e["approval_independently_verified"] is False and e["scientific_approval"] is False and type(e["approval_claimed"]) is bool,"PROFILE_APPROVAL_MISMATCH")
    return "SEMANTIC_SHAPE_VALID_ONLY_NOT_SCIENTIFIC_APPROVAL"
