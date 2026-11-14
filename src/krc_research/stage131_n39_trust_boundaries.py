"""N39 isolated, fail-closed provenance journal and root-owned retrieval receipts.

No receipt issuer, HTTP administration, science execution or deployed changes live
here. Only the independent owner can provision trusted root-owned receipt files.
"""
import hashlib
import json
import os
import sqlite3
import stat
import time
from pathlib import Path

from .consent_custody128 import ConsentCustody128, fingerprint

def _canonical(value):
    return json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode("utf-8")

def _read_root_json(directory, filename):
    directory=Path(directory)
    st=directory.lstat()
    if not stat.S_ISDIR(st.st_mode) or st.st_uid!=0 or st.st_mode & 0o022:
        raise ValueError("UNTRUSTED_DIRECTORY")
    fd=os.open(str(directory/filename),os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC)
    try:
        st=os.fstat(fd)
        if not stat.S_ISREG(st.st_mode) or st.st_uid!=0 or st.st_mode & 0o022 or st.st_size>4096:
            raise ValueError("UNTRUSTED_RECEIPT")
        raw=os.read(fd,4097)
    finally:
        os.close(fd)
    if len(raw)>4096:
        raise ValueError("RECEIPT_OVERSIZE")
    obj=json.loads(raw)
    if not isinstance(obj,dict):
        raise ValueError("INVALID_RECEIPT")
    return obj,hashlib.sha256(raw).hexdigest()

def _name(value):
    return isinstance(value,str) and 16<=len(value)<=128 and value.isascii() and all(c.isalnum() or c in "-_" for c in value)

class N39ProvenanceJournal:
    """Write durable intent before consent consumption; reconcile fail-closed.

    Reconciliation validates both a root-owned receipt *and* consumed durable
    ConsentCustody evidence. It NEVER dispatches new science.
    """
    def __init__(self, path, custody):
        if not isinstance(custody,ConsentCustody128):
            raise ValueError("REAL_CUSTODY_REQUIRED")
        self.path=Path(path)
        if not self.path.is_absolute() or self.path.is_symlink():
            raise ValueError("UNSAFE_JOURNAL")
        self.path.parent.mkdir(mode=0o700,parents=True,exist_ok=True)
        if self.path.parent.stat().st_mode & 0o077:
            raise ValueError("INSECURE_JOURNAL_DIR")
        self.custody=custody
        with self._db() as db:
            db.execute("""CREATE TABLE IF NOT EXISTS provenance(
                principal TEXT NOT NULL,request_id TEXT NOT NULL,consent_ref TEXT NOT NULL,
                context_json TEXT NOT NULL,context_sha256 TEXT NOT NULL,
                state TEXT NOT NULL,receipt_sha256 TEXT,approver TEXT,consumed_at INTEGER,
                PRIMARY KEY(principal,request_id),UNIQUE(consent_ref))""")
        os.chmod(self.path,0o600)

    def _db(self):
        db=sqlite3.connect(str(self.path),timeout=5,isolation_level=None)
        db.execute("PRAGMA busy_timeout=5000")
        db.execute("PRAGMA synchronous=FULL")
        return db

    def prepare(self, context):
        if not isinstance(context,dict):
            return False
        principal=context.get("principal")
        request_id=context.get("request_id")
        ref=context.get("consent_ref")
        if not all(isinstance(x,str) and x for x in (principal,request_id)) or not _name(ref):
            return False
        raw=_canonical(context).decode("utf-8")
        digest=fingerprint(context)
        with self._db() as db:
            try:
                db.execute("BEGIN IMMEDIATE")
                db.execute("INSERT INTO provenance(principal,request_id,consent_ref,context_json,context_sha256,state) VALUES(?,?,?,?,?,'PENDING')",
                   (principal,request_id,ref,raw,digest))
                db.execute("COMMIT")
                return True
            except sqlite3.IntegrityError:
                db.execute("ROLLBACK")
                return False

    def reconcile(self, principal, request_id):
        """Recovery never reconsumes consent and never authorizes execution."""
        with self._db() as db:
            db.execute("BEGIN IMMEDIATE")
            row=db.execute("SELECT consent_ref,context_json,context_sha256,state,receipt_sha256 FROM provenance WHERE principal=? AND request_id=?",
                           (principal,request_id)).fetchone()
            if not row:
                db.execute("COMMIT")
                return "MISSING"
            if row[3]=="COMMITTED":
                db.execute("COMMIT")
                return "COMMITTED"
            context=json.loads(row[1])
            evidence=self.custody.inspect_consumed(context)
            if (not evidence or evidence["consent_ref"]!=row[0]
                or evidence["context_sha256"]!=row[2]):
                db.execute("COMMIT")
                return "HOLD_UNVERIFIED"
            db.execute("""UPDATE provenance SET state='COMMITTED',receipt_sha256=?,approver=?,consumed_at=?
                WHERE principal=? AND request_id=? AND state='PENDING'""",
                (evidence["receipt_sha256"],evidence["approver"],evidence["consumed_at"],principal,request_id))
            db.execute("COMMIT")
            return "RECOVERED"

    def consume_once(self, context):
        """Only the original trusted, pre-dispatch route may call this method."""
        if not self.prepare(context):
            return False
        if self.custody(dict(context)) is not True:
            # Keep durable PENDING for investigation; never retry consume.
            return False
        # A crash here leaves PENDING; reconcile() repairs with trusted evidence.
        return self.reconcile(context["principal"],context["request_id"])=="RECOVERED"

    def attestation(self, principal, request_id):
        """Fail closed if the root receipt or consumed evidence has since changed."""
        with self._db() as db:
            row=db.execute("SELECT consent_ref,context_json,context_sha256,receipt_sha256,approver,consumed_at FROM provenance WHERE principal=? AND request_id=? AND state='COMMITTED'",
                           (principal,request_id)).fetchone()
        if not row or not all((row[0],row[1],row[2],row[3],row[4])) or type(row[5]) is not int:
            return None
        observed=self.custody.inspect_consumed(json.loads(row[1]))
        if not observed or (observed["consent_ref"],observed["context_sha256"],
                           observed["receipt_sha256"],observed["approver"],observed["consumed_at"]) != (
                           row[0],row[2],row[3],row[4],row[5]):
            return None
        return observed

class N39RootRetrievalReceipts:
    """Read-only root-owned retrieval grant and revocation source.

    A revocation tombstone wins forever for that grant_ref. Regrant requires a
    NEW root-issued grant_ref and explicit supersedes of the revoked reference.
    """
    def __init__(self, approvals_dir, *, clock=time.time):
        self.dir=Path(approvals_dir)
        self.clock=clock

    def _read(self, name):
        try:
            return _read_root_json(self.dir,name)
        except (OSError,ValueError,TypeError,json.JSONDecodeError):
            return None

    def permit(self, *, principal, request_id, artifact_id, attestation, grant_ref):
        if not _name(grant_ref) or not isinstance(attestation,dict):
            return False
        result=self._read(grant_ref+".json")
        if result is None:
            return False
        grant,_=result
        required={"version","action","grant_ref","principal","request_id","artifact_id","issuer",
                  "issued_at","expires_at","origin_receipt_sha256","supersedes"}
        if (set(grant)!=required or grant.get("version")!=1 or grant.get("action")!="grant"
            or grant.get("grant_ref")!=grant_ref or grant.get("principal")!=principal
            or grant.get("request_id")!=request_id or grant.get("artifact_id")!=artifact_id
            or grant.get("origin_receipt_sha256")!=attestation.get("receipt_sha256")
            or not isinstance(grant.get("issuer"),str) or not grant["issuer"].strip()
            or type(grant.get("issued_at")) is not int or type(grant.get("expires_at")) is not int
            or not grant["issued_at"]<=int(self.clock())<grant["expires_at"]):
            return False
        # Even if an old grant is copied/reissued, immutable revocation wins.
        if self._read(grant_ref+".revoked.json") is not None:
            return False
        old=grant["supersedes"]
        if old is not None:
            if not _name(old):
                return False
            prev=self._read(old+".revoked.json")
            if prev is None:
                return False
            revoke=prev[0]
            if not (revoke.get("action")=="revoke" and revoke.get("grant_ref")==old
                    and revoke.get("principal")==principal and revoke.get("request_id")==request_id
                    and revoke.get("artifact_id")==artifact_id):
                return False
        return True

    def revoked(self, *, principal, request_id, artifact_id, grant_ref):
        item=self._read(grant_ref+".revoked.json")
        if item is None:
            return False
        rec=item[0]
        return (rec.get("action")=="revoke" and rec.get("grant_ref")==grant_ref
                and rec.get("principal")==principal and rec.get("request_id")==request_id
                and rec.get("artifact_id")==artifact_id and isinstance(rec.get("issuer"),str)
                and bool(rec["issuer"].strip()))

class N39ProtectedReadAuthorizer:
    """Independent root-issued active-grant pointer, never in-process issuer input."""
    def __init__(self, *, journal, receipts):
        if not isinstance(journal,N39ProvenanceJournal) or not isinstance(receipts,N39RootRetrievalReceipts):
            raise ValueError("TRUSTED_N39_DEPENDENCIES_REQUIRED")
        self.journal=journal
        self.receipts=receipts

    def __call__(self, *, principal, request_id, artifact_id):
        evidence=self.journal.attestation(principal,request_id)
        if evidence is None:
            return False
        scope={"principal":principal,"request_id":request_id,"artifact_id":artifact_id}
        selector=hashlib.sha256(_canonical(scope)).hexdigest()+".index.json"
        index_result=self.receipts._read(selector)
        if index_result is None:
            return False
        index=index_result[0]
        if (set(index)!={"version","principal","request_id","artifact_id","active_grant_ref"}
            or index["version"]!=1 or any(index.get(k)!=v for k,v in scope.items())):
            return False
        ref=index["active_grant_ref"]
        return self.receipts.permit(principal=principal,request_id=request_id,
                                    artifact_id=artifact_id,attestation=evidence,grant_ref=ref)
