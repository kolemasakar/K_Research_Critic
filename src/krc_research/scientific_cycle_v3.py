"""Run scientific-domain Critic only with a reviewer-signed assessment.

The independent key is loaded by trusted host injection, never research JSON.
Even a signed positive assessment is not scientific fact proof or journal approval.
"""
import hashlib
import hmac
from .reviewer_attestation import canonical
from .disciplinary_critic import scientific_review
from .research_pipeline_v2 import run_review_cycle
from .specimen_lineage import audit_specimen_overlap
from .review_policy import evaluate_review_policy

def sign_scientific_review(review, key):
    if not isinstance(key,bytes) or len(key)<32:
        raise ValueError("Invalid reviewer signing key")
    return hmac.new(key, canonical(review),hashlib.sha256).hexdigest()

def run_scientific_cycle(package, *, signed_reviews=(), trusted_reviewer_keys=None,
                         researcher_id=None, verified_source_ids=frozenset(),
                         source_attestations=(), now=None):
    baseline=run_review_cycle(package,attestations=source_attestations,
                              trusted_reviewer_keys=trusted_reviewer_keys,
                              researcher_id=researcher_id,now=now)
    counted_sources=set()
    for assessed in baseline['research']['claim_verdicts']:
        counted_sources.update(assessed['counted_sources'])
    trusted_sources=frozenset(verified_source_ids).intersection(counted_sources)
    reviews=[]
    if signed_reviews and (not trusted_reviewer_keys or not researcher_id):
        raise ValueError("Missing trusted reviewer configuration")
    claim_ids={c["claim_id"] for c in baseline["research"]["claim_verdicts"]}
    seen=set()
    for record in signed_reviews:
        if not isinstance(record,dict) or set(record)!={"review","signature"}:
            raise ValueError("Signed review structure invalid")
        body=record["review"]
        if not isinstance(body,dict):
            raise ValueError("Review required")
        reviewer=body.get("reviewer_id")
        if not reviewer or reviewer==researcher_id:
            raise ValueError("Self-review denied")
        if body.get("claim_id") not in claim_ids or body["claim_id"] in seen:
            raise ValueError("Unknown or duplicate reviewed claim")
        key=trusted_reviewer_keys.get(reviewer)
        if key is None:
            raise ValueError("Reviewer identity not trusted")
        signature=record["signature"]
        if not isinstance(signature,str) or not hmac.compare_digest(
                    sign_scientific_review(body,key),signature):
            raise ValueError("Invalid scientific review signature")
        seen.add(body["claim_id"])
        reviews.append(scientific_review(body,verified_source_ids=trusted_sources,
                                         reviewer_authenticated=True))
    lineage=audit_specimen_overlap(package['specimen_lineage']) if 'specimen_lineage' in package else None
    lineage_cleared=lineage is None or lineage['verdict']=='NO_ID_OVERLAP_DETECTED'
    all_complete=(lineage_cleared and baseline['research']['preflight']['status']=='READY_FOR_AUTHOR_REVIEW'
                  and baseline['verified_reviewer_attestations']>0
                  and len(reviews)==len(claim_ids) and bool(claim_ids)
                  and all(x["verdict"]=="CONDITIONAL_REVIEW_PASS" for x in reviews))
    review_policy=evaluate_review_policy(phase="INTERNAL_VALIDATION",
        automatic_critic=baseline['critic']['history'][-1]['result'])
    return {"schema":"KRC-SCIENTIFIC-CYCLE-V3","baseline":baseline,
            "disciplinary_reviews":reviews,
            "review_policy":review_policy,
            "specimen_lineage_audit":lineage,
            "all_claims_reviewed":len(seen)==len(claim_ids),
            "disciplinary_gate":"CONDITIONAL_REVIEW_COMPLETE" if all_complete
                       else "REVISE",
            "scientific_truth_verified":False,"publication_ready":False,
            "final_status":"AWAIT_EXPERIMENTAL_AND_AUTHOR_VALIDATION" if all_complete
                       else "NO_GO"}
