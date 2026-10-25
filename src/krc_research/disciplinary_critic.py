"""Structured disciplinary review: reproducible gap analysis, not automatic truth judgment.

Required scientific dimensions are tied to verifiable source IDs/locators.
Reviewer assessments are reported as claims, not assumed scientific validity.
"""
from __future__ import annotations
import hashlib,json

DIMENSIONS=("research_question","study_design","measurement_validity",
            "statistical_analysis","uncertainty","external_validity",
            "novelty","limitations","counterevidence","citation_trace")
VERDICTS={"ADEQUATE","SHORTFALL","NOT_ASSESSED"}

def scientific_review(review:dict,*,verified_source_ids=frozenset(), reviewer_authenticated=False)->dict:
    if not isinstance(review,dict) or set(review)!={"claim_id","reviewer_id","dimensions","conclusion"}:
        raise ValueError("Scientific review schema mismatch")
    if not review["claim_id"] or not review["reviewer_id"]:
        raise ValueError("Review identity required")
    dimensions=review["dimensions"]
    if not isinstance(dimensions,dict) or set(dimensions)!=set(DIMENSIONS):
        raise ValueError("All ten methodological dimensions required")
    findings=[]
    for name in DIMENSIONS:
        row=dimensions[name]
        if not isinstance(row,dict) or set(row)!={"verdict","rationale","source_ids","passage_locators"}:
            raise ValueError("Review dimension missing fields")
        if row["verdict"] not in VERDICTS:
            raise ValueError("Invalid dimension verdict")
        if not isinstance(row["rationale"],str) or not row["rationale"].strip():
            raise ValueError("Rationale is mandatory")
        sources=row["source_ids"]
        locators=row["passage_locators"]
        if not isinstance(sources,list) or any(not isinstance(x,str) or not x for x in sources):
            raise ValueError("Source IDs invalid")
        if not isinstance(locators,list) or any(not isinstance(x,str) or not x for x in locators):
            raise ValueError("Passage locators invalid")
        supported=(bool(sources) and bool(locators)
                   and all(s in verified_source_ids for s in sources))
        missing=row["verdict"]!="ADEQUATE" or not supported
        findings.append({"dimension":name,"reported_verdict":row["verdict"],
                         "evidence_trace_verified":supported,
                         "status":"SHORTFALL" if missing else "TRACEABLE_REVIEWER_ASSESSMENT",
                         "rationale":row["rationale"]})
    consistent=review["conclusion"] in {"REVISE","CONDITIONAL_PASS"}
    if not consistent:
        raise ValueError("Invalid conclusion")
    all_traceable=all(x["status"]=="TRACEABLE_REVIEWER_ASSESSMENT" for x in findings)
    if review["conclusion"]=="CONDITIONAL_PASS" and (not all_traceable or not reviewer_authenticated):
        conclusion="REVISE"
    else:
        conclusion="CONDITIONAL_REVIEW_PASS" if all_traceable and reviewer_authenticated else "REVISE"
    digest=hashlib.sha256(json.dumps(review,sort_keys=True,
            ensure_ascii=False,separators=(",",":")).encode()).hexdigest()
    return {"schema":"KRC-DISCIPLINARY-CRITIC-1","review_sha256":digest,
            "reviewer_authenticated":bool(reviewer_authenticated),
            "dimensions":findings,"verdict":conclusion,
            "scientific_truth_verified":False,"publication_ready":False,
            "shortfalls":[x["dimension"] for x in findings if x["status"]=="SHORTFALL"]}
