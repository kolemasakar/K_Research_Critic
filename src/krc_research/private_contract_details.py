"""Draft nested schemas and safe error adapter for KRC-SCIENCE-1 (not deployed)."""
SHA = {"type":"string", "pattern":"^[a-f0-9]{64}$"}
EVIDENCE = {
    "type":"object", "additionalProperties":False,
    "required":["source_id","origin_id","access","support","inspected_methods_results","scope_matched","provenance_verified","primary_url"],
    "properties":{
        **{k:{"type":"string"} for k in ("source_id","origin_id","support","primary_url")},
        "access":{"enum":["FULL_TEXT","METHODS_RESULTS_EXCERPT","ABSTRACT_ONLY","METADATA_ONLY","INACCESSIBLE","UNKNOWN"]},
        **{k:{"type":"boolean"} for k in ("inspected_methods_results","scope_matched","provenance_verified")},
    },
}
CLAIM = {
    "type":"object", "additionalProperties":False,
    "required":["claim_id","required","evidence"],
    "properties":{"claim_id":{"type":"string","pattern":"^C[0-9]{2,}$"},
                  "required":{"type":"integer","minimum":1},
                  "evidence":{"type":"array","items":EVIDENCE}},
}
RECEIPT = {
    "type":"object", "additionalProperties":False,
    "required":["source_id","origin_id","doi","document_sha256","inspected_sections",
                "passage_locators","checked_at","inspector_id","method","evidence_relation","external_trace_id"],
    "properties":{
        **{k:{"type":"string","minLength":1} for k in ("source_id","origin_id","doi","inspector_id","external_trace_id")},
        "document_sha256":SHA,
        "inspected_sections":{"type":"array","minItems":1,"items":{"type":"string"}},
        "passage_locators":{"type":"array","minItems":1,"items":{"type":"string"}},
        "checked_at":{"type":"string","format":"date-time"},
        "method":{"enum":["FULL_TEXT","METHODS_RESULTS_EXCERPT"]},
        "evidence_relation":{"enum":["SUPPORTS","CONTRADICTS","INSUFFICIENT"]},
        "trace_verified":{"type":"boolean","default":False},
    },
}
ERROR_CODES=("INVALID_REQUEST","UNAUTHORIZED","OPERATION_DENIED","REPLAY_REJECTED","EXPIRED_REQUEST","HANDLER_ERROR")
ERROR_SCHEMA={"type":"object","additionalProperties":False,"required":["status","error"],
 "properties":{"status":{"const":"error"},"error":{"type":"object","additionalProperties":False,
 "required":["code","message"],"properties":{"code":{"enum":list(ERROR_CODES)},"message":{"type":"string"}}}}}
def sanitized_error(code):
    if code not in ERROR_CODES: code="HANDLER_ERROR"
    return {"status":"error","error":{"code":code,"message":"Request rejected"}}
def approval_evidence_status(profile, receipt):
    if not isinstance(profile,dict) or not isinstance(receipt,dict): return "MISSING"
    keys=("profile_id","profile_version","approved_at","author_id","trace_id","profile_sha256")
    if any(not isinstance(receipt.get(k),str) or not receipt[k] for k in keys): return "INCOMPLETE"
    if receipt["profile_id"]!=profile.get("profile_id") or receipt["profile_version"]!=profile.get("version"): return "PROFILE_MISMATCH"
    return "PRESENT_UNVERIFIED"
