"""KRC P0 A–D: strict, deterministic integration of search, evidence, receipts and Critic.

This does not read scientific papers or infer facts. An independent attestor must
supply approved receipt SHA-256 digests; self-asserted trace_verified is insufficient.
"""
from __future__ import annotations
from dataclasses import replace
from hashlib import sha256
import json
from .canonical_evidence_ledger import Evidence, assess
from .inspection_receipts import InspectionReceipt, audit_receipt
from .source_search_ledger import SearchRun
from .manuscript_gates import ManuscriptGateInput
from .scholarly_preflight import scholarly_preflight

MAX_CLAIMS=100
MAX_ROUNDS=5

def execute_research(package:dict, *, attested_receipt_hashes=frozenset()) -> dict:
    if not isinstance(package,dict): raise ValueError("Research package must be object")
    claim_rows=package.get("claims")
    if not isinstance(claim_rows,list) or not 1<=len(claim_rows)<=MAX_CLAIMS:
        raise ValueError("Research requires 1..100 claims")
    if not isinstance(attested_receipt_hashes,(set,frozenset)):
        raise ValueError("Attestations must be a set")
    receipts={}
    checks=[]
    for raw in package.get("inspection_receipts",[]):
        receipt=InspectionReceipt(**raw)
        result=audit_receipt(receipt)
        if receipt.source_id in receipts: raise ValueError("Duplicate receipt source ID")
        independent=result["receipt_sha256"] in attested_receipt_hashes
        checks.append({"source_id":receipt.source_id, "receipt_sha256":result["receipt_sha256"],
                       "structure_valid":result["eligible_for_independent_claim_review"],
                       "external_attestation":independent,
                       "usable":result["eligible_for_independent_claim_review"] and independent,
                       "shortfalls":result["shortfalls"]+([] if independent else ["independent_attestation_missing"])})
        receipts[receipt.source_id]=(receipt,result,independent)
    assessments=[]
    for row in claim_rows:
        source_evidence=[]
        for source in row.get("evidence",[]):
            candidate=Evidence(**source)
            held=receipts.get(candidate.source_id)
            valid=(held is not None and held[0].origin_id==candidate.origin_id
                   and held[1]["eligible_for_independent_claim_review"] and held[2]
                   and held[0].evidence_relation=="SUPPORTS")
            # Neither source-provided provenance_verified nor a self-signed receipt suffices.
            source_evidence.append(replace(candidate,provenance_verified=valid and candidate.provenance_verified))
        assessments.append(assess(row["claim_id"],row["required"],source_evidence))
    raw_rounds=package.get("critic_rounds",[])
    if not isinstance(raw_rounds,list) or not 1<=len(raw_rounds)<=MAX_ROUNDS:
        raise ValueError("1..5 explicit Critic rounds required")
    previous=None
    cycle=[]
    for index,round_data in enumerate(raw_rounds,1):
        if not isinstance(round_data,dict) or round_data.get("round")!=index:
            raise ValueError("Critic round order invalid")
        revision=round_data.get("revision_id")
        if not isinstance(revision,str) or not revision.strip() or revision==previous:
            raise ValueError("Critic revision identity invalid")
        previous=revision
        if round_data.get("critic") not in {"REVISE","PASS"}:
            raise ValueError("Invalid Critic verdict")
        cycle.append({"round":index,"revision_id":revision,
                      "reported_critic":round_data["critic"],
                      "independent_execution":"NOT_RUN"})
    search_runs=[SearchRun(**r) for r in package.get("search_runs",[])]
    manuscript=ManuscriptGateInput(**package["manuscript_gate"])
    preflight=scholarly_preflight(claims=assessments,searches=search_runs,manuscript=manuscript)
    ready=(preflight["status"]=="READY_FOR_AUTHOR_REVIEW" and
           all(x["usable"] for x in checks) and
           bool(checks) and cycle[-1]["reported_critic"]=="PASS")
    # Reported Critic verdict does not count as an independently executed Critic.
    return {"schema":"KRC-P0-INTEGRATED-1",
            "status":"REVIEW_PENDING_INDEPENDENT_CRITIC" if ready else "REVISE",
            "publication_ready":False,"critic_independently_executed":False,
            "preflight":preflight,"inspection_audit":checks,"critic_iterations":cycle,
            "claim_verdicts":assessments,
            "gates":{"independent_attestation_required":True,
                     "independent_critic_required":True,"journal_approval_required":True}}
