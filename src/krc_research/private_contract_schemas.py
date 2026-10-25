"""Machine-readable private KRC operation contracts, v1 draft, offline only."""
OPERATIONS=("research.profile.validate","research.evidence.preflight",
 "research.bibliography.audit","research.inspection.review")
def contracts():
    base={"type":"object","additionalProperties":False,
          "required":["task_id","operation","status","engine_result","scientific_approval"],
          "properties":{"task_id":{"type":"string"},"operation":{"enum":list(OPERATIONS)},
                        "status":{"enum":["REVISE","PENDING"]},
                        "engine_result":{"type":"object"},
                        "scientific_approval":{"const":False}}}
    return {"schema_version":"KRC-SCIENCE-CONTRACT-1-DRAFT",
      "operations":{
       "research.profile.validate":{"inputSchema":{"type":"object","required":["critic_profile"],
           "properties":{"critic_profile":{"type":"object","required":["profile_id","version","protocol","topic"]},
                         "user_profile_approved":{"type":"boolean"}}},"outputSchema":base},
       "research.evidence.preflight":{"inputSchema":{"type":"object","required":["user_profile_approved","manuscript_gate"],
           "properties":{"user_profile_approved":{"const":True},"manuscript_gate":{"type":"object"},
                         "claims":{"type":"array"},"search_runs":{"type":"array"}}},"outputSchema":base},
       "research.bibliography.audit":{"inputSchema":{"type":"object","required":["dois"],
           "properties":{"dois":{"type":"array","minItems":1,"maxItems":24,"items":{"type":"string"}}}},"outputSchema":base},
       "research.inspection.review":{"inputSchema":{"type":"object","required":["receipt"],
           "properties":{"receipt":{"type":"object"}}},"outputSchema":base}},
      "errorSchema":{"type":"object","additionalProperties":False,"required":["status","error"],
          "properties":{"status":{"const":"error"},"error":{"type":"object","required":["code","message"],
          "properties":{"code":{"enum":["INVALID_REQUEST","UNAUTHORIZED","OPERATION_DENIED",
            "REPLAY_REJECTED","EXPIRED_REQUEST","HANDLER_ERROR"]},"message":{"type":"string"}}}}},
      "deployed":False}
def approval_receipt_status(receipt, profile):
    """Never interpret unverified receipt claims as verified owner approval."""
    if not isinstance(receipt,dict) or not isinstance(profile,dict):
        return "MISSING_OR_INVALID"
    for field in ("profile_id","profile_version","approved_at","author_id","trace_id"):
        if not isinstance(receipt.get(field),str) or not receipt[field].strip():
            return "INCOMPLETE"
    if receipt["profile_id"]!=profile.get("profile_id") or receipt["profile_version"]!=profile.get("version"):
        return "PROFILE_MISMATCH"
    return "PRESENT_UNVERIFIED"
