"""Private single-use KRC approval custody. Staging-only, never a user-facing grant API.

Approval is inserted exclusively by a separate owner-authorized administrative workflow;
the transport request may only reference an existing approval by its opaque receipt ID.
"""
import hashlib,json,os,sqlite3,stat,time
from pathlib import Path

def fingerprint(context):
    body={k:v for k,v in context.items() if k!="consent_ref"}
    return hashlib.sha256(json.dumps(body,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode()).hexdigest()

class ConsentCustody128:
    def __init__(self,path):
        p=Path(path)
        if not p.is_absolute() or p.is_symlink():
            raise ValueError("UNSAFE_CONSENT_STORE")
        s=p.parent.stat()
        if not stat.S_ISDIR(s.st_mode) or s.st_mode & 0o077:
            raise ValueError("UNSAFE_CONSENT_STORE")
        self.path=str(p)
        old=os.umask(0o077)
        try:
            with sqlite3.connect(self.path) as db:
                db.execute("CREATE TABLE IF NOT EXISTS approvals (ref TEXT PRIMARY KEY, digest TEXT NOT NULL, approved_at INTEGER NOT NULL, expires_at INTEGER NOT NULL, approver TEXT NOT NULL, consumed_at INTEGER)")
            os.chmod(self.path,0o600)
        finally:os.umask(old)
    def record_owner_approval(self,context,*,approver,expires_at):
        """Admin-only primitive; MUST NOT be routed from HTTP/UDS or client payload."""
        if not isinstance(approver,str) or not approver.strip() or not isinstance(expires_at,int) or expires_at<=int(time.time()):
            raise ValueError("INVALID_APPROVAL")
        ref=context.get("consent_ref")
        if not isinstance(ref,str) or len(ref)<16 or len(ref)>128:
            raise ValueError("INVALID_APPROVAL")
        with sqlite3.connect(self.path,timeout=3) as db:
            db.execute("INSERT INTO approvals(ref,digest,approved_at,expires_at,approver) VALUES(?,?,?,?,?)",
                       (ref,fingerprint(context),int(time.time()),expires_at,approver))
    def __call__(self,context):
        if not isinstance(context,dict) or not isinstance(context.get("consent_ref"),str):
            return False
        now=int(time.time())
        with sqlite3.connect(self.path,timeout=3,isolation_level=None) as db:
            try:
                db.execute("BEGIN IMMEDIATE")
                row=db.execute("SELECT digest,expires_at,consumed_at FROM approvals WHERE ref=?",
                               (context["consent_ref"],)).fetchone()
                if not row or row[0]!=fingerprint(context) or row[1]<=now or row[2] is not None:
                    db.execute("ROLLBACK")
                    return False
                db.execute("UPDATE approvals SET consumed_at=? WHERE ref=? AND consumed_at IS NULL",(now,context["consent_ref"]))
                db.execute("COMMIT")
                return True
            except (sqlite3.Error,ValueError,TypeError):
                db.execute("ROLLBACK")
                return False
