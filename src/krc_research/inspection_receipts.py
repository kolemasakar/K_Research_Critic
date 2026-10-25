"""Tamper-evident source-inspection receipts. Hashing proves ledger integrity, NOT actual reading.
Require separately verified external artifact before counting an experiment.
"""
from dataclasses import dataclass, asdict
from datetime import datetime
import hashlib, json, re

SHA = re.compile(r"^[a-f0-9]{64}$")
@dataclass(frozen=True)
class InspectionReceipt:
    source_id: str
    origin_id: str
    doi: str
    document_sha256: str
    inspected_sections: tuple[str,...]
    passage_locators: tuple[str,...]
    checked_at: str
    inspector_id: str
    method: str
    evidence_relation: str
    external_trace_id: str
    trace_verified: bool = False

def audit_receipt(r: InspectionReceipt) -> dict:
    reasons=[]
    if not SHA.fullmatch(r.document_sha256): reasons.append("document_hash_missing")
    if not all([r.source_id,r.origin_id,r.doi,r.inspector_id,r.external_trace_id]):
        reasons.append("identity_or_trace_missing")
    if not r.inspected_sections or not r.passage_locators:
        reasons.append("inspected_passages_missing")
    if r.evidence_relation not in {"SUPPORTS","CONTRADICTS","INSUFFICIENT"}:
        reasons.append("invalid_relation")
    try:
        date=datetime.fromisoformat(r.checked_at.replace("Z","+00:00"))
        if date.utcoffset() is None: reasons.append("timestamp_unzoned")
    except (TypeError,ValueError): reasons.append("timestamp_invalid")
    if r.method not in {"FULL_TEXT","METHODS_RESULTS_EXCERPT"}:
        reasons.append("insufficient_access")
    if not r.trace_verified: reasons.append("external_trace_not_verified")
    body=json.dumps(asdict(r),sort_keys=True,ensure_ascii=False,separators=(",",":")).encode("utf-8")
    return {"receipt_sha256":hashlib.sha256(body).hexdigest(),
            "eligible_for_independent_claim_review":not reasons,
            "shortfalls":reasons, "scientific_truth_verified":False}

def verify_chain(records: list[dict]) -> dict:
    prev="0"*64
    for row in records:
        if row.get("previous_sha256") != prev: raise ValueError("Broken prior hash")
        payload=row.get("payload")
        if not isinstance(payload,dict): raise ValueError("Missing receipt payload")
        h=hashlib.sha256(json.dumps({"previous_sha256":prev,"payload":payload},
                     sort_keys=True,ensure_ascii=False,separators=(",",":")).encode()).hexdigest()
        if row.get("entry_sha256")!=h: raise ValueError("Changed receipt payload")
        prev=h
    return {"count":len(records),"chain_tip_sha256":prev,"status":"INTEGRITY_OK_NOT_ATTESTED"}

def append_entry(records: list[dict], payload: dict) -> list[dict]:
    previous=verify_chain(records)["chain_tip_sha256"]
    h=hashlib.sha256(json.dumps({"previous_sha256":previous,"payload":payload},
                     sort_keys=True,ensure_ascii=False,separators=(",",":")).encode()).hexdigest()
    return [*records,{"previous_sha256":previous,"payload":payload,"entry_sha256":h}]
