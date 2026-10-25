"""Bind local Markdown manuscript revisions to concrete claim locators.

No inferred citations: supplied IDs must appear literally in a manuscript snapshot
and must exist in the research package. The returned map is a structural trace,
not scientific truth or journal suitability.
"""
from __future__ import annotations
import hashlib
from pathlib import Path
from .manuscript_revision import audit_manuscript_revisions

MAX_FILE=250_000

def audit_manuscript_files(items:list[dict],*,approved_root,**kwargs)->dict:
    root=Path(approved_root).resolve(strict=True)
    steps=[];paths=set();traces=[]
    if not isinstance(items,list) or not 2<=len(items)<=5:
        raise ValueError("2..5 manuscript files required")
    for item in items:
        if not isinstance(item,dict) or set(item)!={"revision_id","path","package","attestations","change_note","claim_anchors"}:
            raise ValueError("Invalid manuscript file input")
        p=Path(item["path"])
        if p.is_symlink():
            raise ValueError("Symlink manuscript prohibited")
        path=p.resolve(strict=True)
        if not path.is_relative_to(root) or path.suffix.lower()!=".md" or not path.is_file():
            raise ValueError("Manuscript must be Markdown inside approved root")
        if path in paths: raise ValueError("Same physical file reused")
        paths.add(path)
        if path.stat().st_size>MAX_FILE: raise ValueError("Manuscript too large")
        raw=path.read_bytes()
        manuscript=raw.decode("utf-8")
        anchors=item["claim_anchors"]
        if not isinstance(anchors,dict):
            raise ValueError("Claim anchors must be mapping")
        known={x["claim_id"] for x in item["package"]["claims"]}
        if not known or set(anchors)!=known:
            raise ValueError("Every research claim requires a manuscript anchor")
        lines=manuscript.splitlines()
        matches=[]
        for claim,locator in sorted(anchors.items()):
            if not isinstance(locator,str) or len(locator)<8:
                raise ValueError("Anchor must be an exact nontrivial phrase")
            locations=[idx+1 for idx,line in enumerate(lines) if locator in line]
            if len(locations)!=1:
                raise ValueError("Claim anchor must appear on exactly one line")
            matches.append({"claim_id":claim,"line":locations[0],
                            "locator_sha256":hashlib.sha256(locator.encode()).hexdigest()})
        traces.append({"revision_id":item["revision_id"],
                       "source_md_sha256":hashlib.sha256(raw).hexdigest(),
                       "claim_anchor_rows":matches,"scientific_truth_verified":False})
        steps.append({"revision_id":item["revision_id"],"manuscript":manuscript,
                      "package":item["package"],"attestations":item["attestations"],
                      "change_note":item["change_note"]})
    outcome=audit_manuscript_revisions(steps,**kwargs)
    return {"schema":"KRC-MANUSCRIPT-FILE-TRACE-1","file_traces":traces,
            "revision_audit":outcome,"publication_ready":False}
