"""Text manuscript revision audit, independently replayed research package per revision.

A new package without an actual text modification is not a manuscript revision.
No automatic scientific claim can be upgraded from a textual diff alone.
"""
from __future__ import annotations
import hashlib
import difflib
from .revision_history import execute_revision_history

def _hash(text:str)->str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def audit_manuscript_revisions(steps:list[dict],**review_kwargs)->dict:
    if not isinstance(steps,list) or not 2<=len(steps)<=5:
        raise ValueError("Manuscript revision requires 2..5 versions")
    revisions=[]
    documents=[]
    last=None
    for i,step in enumerate(steps,1):
        if not isinstance(step,dict) or set(step)!={"revision_id","manuscript","package","attestations","change_note"}:
            raise ValueError("Invalid manuscript step")
        manuscript=step["manuscript"]
        if not isinstance(manuscript,str) or not manuscript.strip() or len(manuscript)>200_000:
            raise ValueError("Invalid manuscript size")
        if last is not None and manuscript==last:
            raise ValueError("No actual manuscript change")
        digest=_hash(manuscript)
        if last is None:
            delta={"added_lines":0,"removed_lines":0,"changed":False}
        else:
            a=last.splitlines()
            b=manuscript.splitlines()
            changes=list(difflib.SequenceMatcher(a=a,b=b,autojunk=False).get_opcodes())
            removed=sum(j-i for tag,i,j,k,l in changes if tag in {"replace","delete"})
            added=sum(l-k for tag,i,j,k,l in changes if tag in {"replace","insert"})
            delta={"added_lines":added,"removed_lines":removed,"changed":True}
        documents.append({"revision_id":step["revision_id"],"manuscript_sha256":digest,
                          "characters":len(manuscript),"diff":delta,
                          "scientific_truth_verified":False})
        revisions.append({k:step[k] for k in ("revision_id","package","attestations","change_note")})
        last=manuscript
    research=execute_revision_history(revisions,**review_kwargs)
    return {"schema":"KRC-MANUSCRIPT-REVISION-1",
            "manuscripts":documents,"research_review":research,
            "actual_manuscript_revisions":len(documents)-1,
            "scientific_peer_review_completed":False,"publication_ready":False}
