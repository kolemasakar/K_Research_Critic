"""Isolated N39 fail-closed audit for out-of-band grant operations.

This is NOT an authenticated human approval or a production issuer. Callers must
bring independently validated authorization and an externally anchored digest.
The SQLite hash chain detects changes only when checked against a trusted anchor.
"""
import hashlib
import hmac
import json
import os
import sqlite3
import stat
import time
from pathlib import Path

class AuditDenied(ValueError):
    pass

def canonical(item):
    return json.dumps(item,sort_keys=True,separators=(",",":"),allow_nan=False,ensure_ascii=False).encode("utf-8")

class N39AuditJournal:
    def __init__(self, path, *, anchor_checker, clock=time.time):
        self.path=Path(path)
        if not self.path.is_absolute() or self.path.is_symlink():
            raise AuditDenied("UNSAFE_AUDIT_PATH")
        self.path.parent.mkdir(parents=True,mode=0o700,exist_ok=True)
        st=self.path.parent.stat()
        if not stat.S_ISDIR(st.st_mode) or st.st_mode & 0o077:
            raise AuditDenied("UNSAFE_AUDIT_DIRECTORY")
        if not callable(anchor_checker):
            raise AuditDenied("INDEPENDENT_ANCHOR_REQUIRED")
        self.anchor_checker=anchor_checker
        self.clock=clock
        with self._db() as db:
            db.execute("""CREATE TABLE IF NOT EXISTS events(
                seq INTEGER PRIMARY KEY,event_json TEXT NOT NULL,prev_hash TEXT NOT NULL,
                entry_hash TEXT NOT NULL UNIQUE)""")
        os.chmod(self.path,0o600)

    def _db(self):
        db=sqlite3.connect(str(self.path),timeout=5,isolation_level=None)
        db.execute("PRAGMA busy_timeout=5000")
        db.execute("PRAGMA journal_mode=WAL")
        db.execute("PRAGMA synchronous=FULL")
        return db

    def _scan(self,db):
        prior="0"*64
        count=0
        for seq,event_json,previous,digest in db.execute(
                "SELECT seq,event_json,prev_hash,entry_hash FROM events ORDER BY seq"):
            count+=1
            if seq!=count or previous!=prior:
                raise AuditDenied("AUDIT_CHAIN_MISMATCH")
            try:
                record=json.loads(event_json)
            except (ValueError,TypeError):
                raise AuditDenied("AUDIT_CHAIN_MISMATCH") from None
            if canonical(record).decode()!=event_json:
                raise AuditDenied("AUDIT_CHAIN_MISMATCH")
            expected=hashlib.sha256(canonical({"seq":seq,"prev_hash":prior,"event":record})).hexdigest()
            if not hmac.compare_digest(expected,digest):
                raise AuditDenied("AUDIT_CHAIN_MISMATCH")
            prior=digest
        return count,prior

    def verify(self):
        with self._db() as db:
            count,head=self._scan(db)
        try:
            if self.anchor_checker(count,head) is not True:
                raise AuditDenied("AUDIT_ANCHOR_UNVERIFIED")
        except AuditDenied:
            raise
        except Exception:
            raise AuditDenied("AUDIT_ANCHOR_UNVERIFIED") from None
        return {"seq":count,"head_sha256":head}

    def record_intent(self, *, ticket_digest, operator_id, action, principal,
                      request_id, artifact_id, grant_ref, event_id):
        if action not in ("issue","revoke","regrant"):
            raise AuditDenied("INVALID_AUDIT_ACTION")
        values=(ticket_digest,operator_id,principal,request_id,artifact_id,grant_ref,event_id)
        if not all(isinstance(x,str) and x for x in values):
            raise AuditDenied("INVALID_AUDIT_CONTEXT")
        if len(ticket_digest)!=64 or any(c not in "0123456789abcdef" for c in ticket_digest):
            raise AuditDenied("INVALID_TICKET_DIGEST")
        state=self.verify() # independently anchored preceding state
        record={"kind":"INTENT","event_id":event_id,"ticket_sha256":ticket_digest,
                "operator_id":operator_id,"action":action,"principal":principal,
                "request_id":request_id,"artifact_id":artifact_id,"grant_ref":grant_ref,
                "time_epoch":int(self.clock())}
        encoded=canonical(record).decode("utf-8")
        with self._db() as db:
            db.execute("BEGIN IMMEDIATE")
            count,head=self._scan(db)
            if count!=state["seq"] or head!=state["head_sha256"]:
                db.execute("ROLLBACK")
                raise AuditDenied("AUDIT_CONCURRENT_CHANGE")
            if db.execute("SELECT 1 FROM events WHERE event_json LIKE ?",('%' + event_id + '%',)).fetchone():
                db.execute("ROLLBACK")
                raise AuditDenied("AUDIT_DUPLICATE_EVENT")
            seq=count+1
            digest=hashlib.sha256(canonical({"seq":seq,"prev_hash":head,"event":record})).hexdigest()
            db.execute("INSERT INTO events VALUES(?,?,?,?)",(seq,encoded,head,digest))
            db.execute("COMMIT")
        # Operator MUST anchor the new head outside this journal BEFORE file issuance.
        return {"seq":seq,"head_sha256":digest,"event_id":event_id}

    def check_anchored_intent(self, *, seq, event_id):
        state=self.verify()
        if state["seq"]!=seq:
            raise AuditDenied("AUDIT_INTENT_NOT_HEAD")
        with self._db() as db:
            row=db.execute("SELECT event_json FROM events WHERE seq=?",(seq,)).fetchone()
        if row is None:
            raise AuditDenied("AUDIT_MISSING_INTENT")
        record=json.loads(row[0])
        if record.get("kind")!="INTENT" or record.get("event_id")!=event_id:
            raise AuditDenied("AUDIT_INTENT_MISMATCH")
        return True
