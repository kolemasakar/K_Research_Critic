"""Real revision replay for frozen research packages, not self-reported Critic rounds.

Each revision is a new package; all evidence/receipts/search/manuscript gates are
recomputed and the rule Critic executes again. A repeated content digest is
rejected rather than being presented as a new iteration.
"""
from __future__ import annotations
import hashlib
import json
from .research_pipeline_v2 import run_review_cycle

MAX_REVISIONS=5

def digest_package(package:dict)->str:
    if not isinstance(package,dict):
        raise ValueError("Revision must contain a research package object")
    return hashlib.sha256(json.dumps(package,sort_keys=True,separators=(",",":"),
                                   ensure_ascii=False,allow_nan=False).encode("utf-8")).hexdigest()

def execute_revision_history(revisions:list[dict], *,
                             trusted_reviewer_keys=None,researcher_id=None,now=None)->dict:
    if not isinstance(revisions,list) or not 1<=len(revisions)<=MAX_REVISIONS:
        raise ValueError("1..5 research revisions required")
    seen_hashes=set()
    seen_ids=set()
    history=[]
    last=None
    for index,revision in enumerate(revisions,1):
        if not isinstance(revision,dict) or set(revision)!={"revision_id","package","attestations","change_note"}:
            raise ValueError("Revision schema mismatch")
        rid=revision["revision_id"]
        note=revision["change_note"]
        if not isinstance(rid,str) or not rid.strip() or rid in seen_ids:
            raise ValueError("Revision identity reused")
        if not isinstance(note,str) or not note.strip():
            raise ValueError("Revision change note required")
        seen_ids.add(rid)
        package=revision["package"]
        sha=digest_package(package)
        if sha in seen_hashes:
            raise ValueError("Revision does not change research package bytes")
        seen_hashes.add(sha)
        attestations=revision["attestations"]
        if not isinstance(attestations,list):
            raise ValueError("Attestation envelopes must be a list")
        result=run_review_cycle(package,attestations=attestations,
                                trusted_reviewer_keys=trusted_reviewer_keys,
                                researcher_id=researcher_id,now=now)
        critic=result["critic"]["history"][-1]["result"]
        row={"iteration":index,"revision_id":rid,"input_sha256":sha,
             "change_note":note,"critic_execution":"EXECUTED",
             "critic_verdict":critic["verdict"],
             "critic_input_sha256":critic["input_sha256"],
             "critic_issues":critic["issues"],
             "claim_verdicts":[{"claim_id":v["claim_id"],"verdict":v["verdict"]}
                              for v in result["research"]["claim_verdicts"]],
             "unresolved_conflicts":result["unresolved_conflicts"],
             "final_gate":result["final_gate"],
             "publication_ready":False}
        history.append(row)
        last=result
    return {"schema":"KRC-REVISION-HISTORY-1","rounds_executed":len(history),
            "history":history,"last_critic_verdict":history[-1]["critic_verdict"],
            "requires_new_revision":history[-1]["critic_verdict"]=="REVISE",
            "scientific_peer_review_completed":False,"publication_ready":False}
