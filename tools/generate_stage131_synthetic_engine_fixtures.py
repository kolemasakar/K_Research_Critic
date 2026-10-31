"""Emit actual offline synthetic KRC engine results; no network/identity/consent."""
import json
from krc_research.profile_validator import validate_profile
from krc_research.offline_acceptance import evaluate_payload
from krc_research.bibliography_audit import audit_bibliography
from krc_research.inspection_receipts import InspectionReceipt,audit_receipt
from krc_research.stage131_science_semantic_contract import validate_operation_result

MANUSCRIPT={k:False for k in ("journal_policy_checked","search_audit_reproducible","primary_sources_inspected","novelty_reviewed","citations_validated","scientific_methods_audited","rights_and_ai_disclosure_done","human_author_approved")}
inputs={
"research.profile.validate": lambda:validate_profile({"critic_profile":{"profile_id":"P-SYN","version":"1","protocol":"KRC Core","topic":"Synthetic"},"user_profile_approved":False}),
"research.evidence.preflight":lambda:evaluate_payload({"claims":[],"search_runs":[],"manuscript_gate":MANUSCRIPT}),
"research.bibliography.audit":lambda:audit_bibliography(["10.1000/synthetic"],crossref_fetch=lambda url:{"message":{}},europepmc_fetch=lambda url:{"resultList":{"result":[]}},updates_fetch=lambda url:{"message":{}}),
"research.inspection.review":lambda:audit_receipt(InspectionReceipt("S1","origin-1","10.1000/synthetic","a"*64,(),(),"2026-10-31T00:00:00+00:00","synthetic-inspector","FULL_TEXT","INSUFFICIENT","TRACE-SYN",False))
}
out={}
for op,fn in inputs.items():
    try:
        e=fn()
        status="REVISE" if op=="research.evidence.preflight" and e["final_publication_status"]=="NO_GO" else "PENDING"
        obj={"task_id":"synthetic-task-no-dispatch","operation":op,"status":status,"engine_result":e,"scientific_approval":False}
        obj["semantic_decision"]=validate_operation_result(obj,task_id=obj["task_id"],operation=op)
        out[op]=obj
    except Exception as err:
        out[op]={"fixture_generation_error":type(err).__name__,"description":str(err)[:180]}
print(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2))
