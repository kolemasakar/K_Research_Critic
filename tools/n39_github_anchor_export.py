"""Prepare an N39 GitHub anchor PR payload from a *locally verified* audit.

Read-only/export only. Does not issue consent, publish, merge, or bypass rules.
Separate trusted GitHub publication and independent witness are mandatory.
"""
import argparse
import hashlib
import json
import os
import re
import sqlite3
import stat
from pathlib import Path

def _canon(value):
    return json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode()

def audit_head(db_path):
    p=Path(db_path)
    if not p.is_absolute() or p.is_symlink():
        raise ValueError("UNSAFE_AUDIT_DB")
    st=p.stat()
    if not stat.S_ISREG(st.st_mode) or st.st_mode & 0o077:
        raise ValueError("UNSAFE_AUDIT_DB")
    conn=sqlite3.connect("file:"+str(p)+"?mode=ro",uri=True)
    try:
        prev="0"*64
        count=0
        for seq,raw,previous,digest in conn.execute("SELECT seq,event_json,prev_hash,entry_hash FROM events ORDER BY seq"):
            count+=1
            if seq!=count or previous!=prev:
                raise ValueError("AUDIT_CHAIN_MISMATCH")
            obj=json.loads(raw)
            if _canon(obj).decode()!=raw:
                raise ValueError("AUDIT_CHAIN_MISMATCH")
            actual=hashlib.sha256(_canon({"seq":seq,"prev_hash":prev,"event":obj})).hexdigest()
            if digest!=actual:
                raise ValueError("AUDIT_CHAIN_MISMATCH")
            prev=digest
        return count,prev
    finally:
        conn.close()

def manifest(path, *, journal_id, prior_commit_sha, source_commit_sha, phase, demo_only):
    if not re.fullmatch("[a-z0-9][a-z0-9_-]{3,62}",journal_id):
        raise ValueError("INVALID_JOURNAL_ID")
    for label,ref in (("PRIOR",prior_commit_sha),("SOURCE",source_commit_sha)):
        if not re.fullmatch("[0-9a-f]{40}",ref):
            raise ValueError("INVALID_"+label+"_SHA")
    if phase not in ("INTENT","OUTCOME"):
        raise ValueError("INVALID_PHASE")
    if not demo_only:
        raise ValueError("REAL_ANCHOR_NEEDS_APPROVED_ISSUER_AND_WITNESS")
    seq,head=audit_head(path)
    if seq<1:
        raise ValueError("EMPTY_JOURNAL")
    data={"schema_version":"KRC_N39_GITHUB_ANCHOR_V1","journal_id":journal_id,
          "sequence":seq,"chain_head_sha256":head,"previous_anchor_commit_sha":prior_commit_sha,
          "source_commit_sha":source_commit_sha,"phase":phase,
          "synthetic_test_only":True,"no_science_consent_or_grant":True,
          "immutable_witness_not_established":True}
    name=f"audit/n39/anchors/{journal_id}/{seq:08d}-{head}.json"
    return name,data

def main():
    ap=argparse.ArgumentParser()
    for k in ("db","journal-id","prior-commit-sha","source-commit-sha","phase"):
        ap.add_argument("--"+k,required=True)
    ap.add_argument("--synthetic-test-only",action="store_true")
    args=ap.parse_args()
    name,data=manifest(args.db,journal_id=args.journal_id,
      prior_commit_sha=args.prior_commit_sha,source_commit_sha=args.source_commit_sha,
      phase=args.phase,demo_only=args.synthetic_test_only)
    print(json.dumps({"path":name,"payload":data},sort_keys=True,indent=2))

if __name__=="__main__":
    main()
