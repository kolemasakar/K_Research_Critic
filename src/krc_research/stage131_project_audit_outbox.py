"""N39 personal project audit outbox. Only hashes leave the private server.

A snapshot records OBSERVED persisted state, not retroactively minted approval
events. Local journal and publication receipt are kept separately from consent.
Existing accepted GitHub branch is the external checkpoint, not WORM.
"""
import argparse
import hashlib
import json
import os
import re
import secrets
import sqlite3
import stat
from contextlib import closing
from datetime import datetime,timezone
from pathlib import Path
from .stage131_n39_single_owner_chat_consent import canonical,profile_hash
from .stage131_project_signed_read import ro,checked

ZERO="0"*64
SCHEMA="KRC_N39_PROJECT_CHECKPOINT_V1"
BRANCH="audit/n39-anchor-ledger"

def sha(value):return hashlib.sha256(canonical(value)).hexdigest()
def hexlen(value,n):return isinstance(value,str) and re.fullmatch("[0-9a-f]{"+str(n)+"}",value) is not None

def snapshot(root):
    root=Path(root)
    checked(root,directory=True)
    with closing(ro(root/"consent.sqlite")) as db:
        db.execute("BEGIN")
        approvals=db.execute("""SELECT a.request_id,a.profile_sha256,a.status,a.event_ref,a.approved_at,
          a.expires_at,a.consumed_at,a.cancelled_at,a.completed_at,p.profile_json
          FROM approvals a JOIN project_profiles p USING(request_id) ORDER BY a.request_id""").fetchall()
        links=db.execute("SELECT request_id,artifact_id FROM artifacts ORDER BY request_id,artifact_id").fetchall()
        total=db.execute("SELECT COUNT(*) FROM approvals").fetchone()[0]
        if total!=len(approvals):raise ValueError("MISSING_PROFILE")
    with closing(ro(root/"requests.sqlite")) as db:
        requests=db.execute("SELECT principal,request_id,digest,state,result FROM requests ORDER BY principal,request_id").fetchall()
    with closing(ro(root/"artifacts"/"index.sqlite3")) as db:
        artifacts=db.execute("SELECT id,principal,request_id,size,sha256,expires FROM objects ORDER BY id").fetchall()
    # Do not persist original profile text or returned artifact contents.
    rows=[]
    for a in approvals:
        if profile_hash(json.loads(a[-1]))!=a[1]:raise ValueError("PROFILE_MISMATCH")
        rows.append([*a[:3],sha(a[3]) if a[3] is not None else None,*a[4:-1]])
    return {"approvals":rows,"links":links,"requests":[list(x[:4])+[sha(x[4]) if x[4] is not None else None] for x in requests],"artifacts":artifacts}

class ProjectAuditOutbox:
    def __init__(self,path):
        p=Path(path)
        if not p.is_absolute() or p.is_symlink():raise ValueError("UNSAFE_OUTBOX")
        p.parent.mkdir(mode=0o700,parents=True,exist_ok=True)
        checked(p.parent,directory=True)
        if p.exists():checked(p)
        self.path=p
        with closing(self._db()) as db:
            db.execute("CREATE TABLE IF NOT EXISTS journal (seq INTEGER PRIMARY KEY, previous TEXT NOT NULL, event_json TEXT NOT NULL, head TEXT NOT NULL, manifest_json TEXT NOT NULL, published_commit TEXT)")
            db.execute("CREATE TABLE IF NOT EXISTS metadata (id INTEGER PRIMARY KEY CHECK(id=1),journal_id TEXT NOT NULL,salt TEXT NOT NULL)")
            db.execute("INSERT OR IGNORE INTO metadata VALUES(1,?,?)",("project-"+secrets.token_hex(16),secrets.token_hex(32)))
        os.chmod(p,0o600)
    def _db(self):
        db=sqlite3.connect(self.path,isolation_level=None,timeout=5)
        db.execute("PRAGMA synchronous=FULL")
        return db
    def _scan(self,db):
        jid,salt=db.execute("SELECT journal_id,salt FROM metadata WHERE id=1").fetchone()
        prior=ZERO; rows=[]
        for seq,prev,raw,head,manifest,published in db.execute("SELECT * FROM journal ORDER BY seq"):
            event=json.loads(raw); public=json.loads(manifest)
            expected=sha({"seq":seq,"previous":prior,"event":event,"salt":salt})
            if (seq!=len(rows)+1 or prev!=prior or head!=expected or
                canonical(event).decode()!=raw or public!=self._manifest(jid,seq,prev,head,event) or
                (published is not None and not hexlen(published,40)) or
                (rows and rows[-1][2] is None)):
                raise ValueError("AUDIT_CHAIN_MISMATCH")
            rows.append((event,public,published));prior=head
        return jid,salt,rows
    @staticmethod
    def _manifest(jid,seq,prev,head,event):
        return {"schema_version":SCHEMA,"journal_id":jid,"sequence":seq,
            "chain_head_sha256":head,"previous_chain_head_sha256":prev,
            "previous_anchor_commit_sha":event["base_commit"],"source_commit_sha":event["source_commit"],
            "recorded_at_utc":event["observed_at"],"phase":"STATE_CHECKPOINT"}
    @staticmethod
    def path_for(m):
        return "audit/n39/anchors/"+m["journal_id"]+"/"+format(m["sequence"],"08d")+"-"+m["chain_head_sha256"]+".json"
    def prepare(self,root,*,base_commit,source_commit,prior_sequence=0,prior_head=ZERO,prior_commit=None):
        if not hexlen(base_commit,40) or not hexlen(source_commit,40) or not hexlen(prior_head,64):
            raise ValueError("INVALID_PINS")
        # Stable repeated snapshots, no lock across provider work. A transient
        # intermediate state is an observed checkpoint, never new authorization.
        state=snapshot(root)
        if canonical(state)!=canonical(snapshot(root)):raise ValueError("STATE_CHANGED_RETRY")
        with closing(self._db()) as db:
            db.execute("BEGIN IMMEDIATE")
            jid,salt,rows=self._scan(db)
            last=rows[-1] if rows else None
            confirmed=rows[:-1] if last and last[2] is None else rows
            expected=(len(confirmed),confirmed[-1][1]["chain_head_sha256"],confirmed[-1][2]) if confirmed else (0,ZERO,None)
            if (prior_sequence,prior_head,prior_commit)!=expected:raise ValueError("PUBLISHED_PREFIX_MISMATCH")
            if last and last[2] is None:
                if last[1]["previous_anchor_commit_sha"]!=base_commit:raise ValueError("PENDING_BASE_CHANGED")
                return {"path":self.path_for(last[1]),"payload":last[1],"status":"PENDING"}
            state_hash=sha({"private_salt":salt,"state":state})
            if last and last[0]["state_sha256"]==state_hash:
                return {"status":"UNCHANGED","payload":last[1],"published_commit":last[2]}
            event={"base_commit":base_commit,"source_commit":source_commit,
                "observed_at":datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00","Z"),
                "state_sha256":state_hash}
            seq=len(rows)+1;prev=last[1]["chain_head_sha256"] if last else ZERO
            head=sha({"seq":seq,"previous":prev,"event":event,"salt":salt})
            m=self._manifest(jid,seq,prev,head,event)
            db.execute("INSERT INTO journal VALUES(?,?,?,?,?,NULL)",(seq,prev,canonical(event).decode(),head,canonical(m).decode()))
            db.execute("COMMIT")
            return {"status":"PENDING","path":self.path_for(m),"payload":m}
    def ack(self,*,sequence,head,commit):
        # Invoked by trusted publisher ONLY after merged GitHub file and commit
        # ancestry have been checked. Not a proof of publication by itself.
        if not hexlen(head,64) or not hexlen(commit,40):raise ValueError("INVALID_RECEIPT")
        with closing(self._db()) as db:
            db.execute("BEGIN IMMEDIATE")
            _,_,rows=self._scan(db)
            if not rows or sequence!=len(rows) or rows[-1][1]["chain_head_sha256"]!=head:
                raise ValueError("RECEIPT_MISMATCH")
            if rows[-1][2] not in (None,commit):raise ValueError("RECEIPT_CONFLICT")
            db.execute("UPDATE journal SET published_commit=? WHERE seq=?",(commit,sequence))
            db.execute("COMMIT")
    def status(self):
        with closing(self._db()) as db:
            _,_,rows=self._scan(db)
        if not rows:return {"status":"EMPTY"}
        _,m,c=rows[-1]
        return {"status":"PUBLISHED" if c else "PENDING","path":self.path_for(m),"payload":m,"published_commit":c}

def main():
    os.umask(0o077)
    p=argparse.ArgumentParser()
    p.add_argument("--outbox",required=True)
    sub=p.add_subparsers(dest="action",required=True)
    a=sub.add_parser("prepare")
    for key in ("state","base-commit","source-commit"):a.add_argument("--"+key,required=True)
    a.add_argument("--prior-sequence",type=int,default=0);a.add_argument("--prior-head",default=ZERO);a.add_argument("--prior-commit")
    a=sub.add_parser("ack");a.add_argument("--sequence",type=int,required=True);a.add_argument("--head",required=True);a.add_argument("--commit",required=True)
    sub.add_parser("status")
    a=p.parse_args();o=ProjectAuditOutbox(a.outbox)
    if a.action=="prepare":result=o.prepare(a.state,base_commit=a.base_commit,source_commit=a.source_commit,prior_sequence=a.prior_sequence,prior_head=a.prior_head,prior_commit=a.prior_commit)
    elif a.action=="ack":o.ack(sequence=a.sequence,head=a.head,commit=a.commit);result=o.status()
    else:result=o.status()
    print(json.dumps(result,sort_keys=True))

if __name__=="__main__":main()
