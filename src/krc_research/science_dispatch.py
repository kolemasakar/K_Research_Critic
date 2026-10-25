"""Sentinel-authorized K_Science → KRC dispatch, offline, no remote listener.
Use only behind authenticated transport and durable replay storage.
"""
from .interproject_contract import validate_envelope, check_replay
from .offline_acceptance import evaluate_payload
from .bibliography_audit import audit_bibliography
from .inspection_receipts import InspectionReceipt,audit_receipt

def handle_science_request(message:dict,*,secret:bytes,signature:str,seen:set,
                           permitted:set[str],now=None, bibliography_fn=audit_bibliography)->dict:
    auth=validate_envelope(message,key=secret,signature=signature,
                           allowed_operations=permitted,now=now)
    operation=auth["operation"]
    request=message["payload"]
    if not isinstance(request,dict): raise ValueError("Object payload required")
    if operation=="research.evidence.preflight":
        if request.get("user_profile_approved") is not True:
            raise ValueError("Explicit user profile approval required")
        if "manuscript_gate" not in request:
            raise ValueError("Missing canonical scientific acceptance schema")
    elif operation=="research.bibliography.audit":
        if "dois" not in request: raise ValueError("DOI list required")
    elif operation=="research.inspection.review":
        if "receipt" not in request: raise ValueError("Receipt required")
    else:
        raise ValueError("Not implemented in isolated dispatcher")
    # Durable ReplayRegistry is required for deployed gateways; set is test-only.
    if hasattr(seen, "claim"):
        seen.claim(message["client"], auth["task_id"])
    else:
        check_replay(auth["task_id"], seen)
    if operation=="research.evidence.preflight":
        result=evaluate_payload(request)
    elif operation=="research.bibliography.audit":
        result=bibliography_fn(request["dois"])
    else:
        result=audit_receipt(InspectionReceipt(**request["receipt"]))
    return {"task_id":auth["task_id"],"operation":operation,
            "status":"REVISE" if operation=="research.evidence.preflight" and result["final_publication_status"]=="NO_GO" else "PENDING",
            "engine_result":result,"scientific_approval":False}
