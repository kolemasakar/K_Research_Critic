"""Stage119 durable request ledger for staging. No network identity trust implied."""
import hashlib
import json
import sqlite3
from pathlib import Path

class LedgerError(Exception):
    def __init__(self,code):
        super().__init__(code)
        self.code=code

class RequestLedger:
    """Atomic request admission; ambiguous IN_PROGRESS never automatically redispatched."""
    def __init__(self,path):
        self.path=Path(path)
        self.path.parent.mkdir(mode=0o700,parents=True,exist_ok=True)
        with self._db() as db:
            db.execute("CREATE TABLE IF NOT EXISTS requests(principal TEXT NOT NULL,request_id TEXT NOT NULL,digest TEXT NOT NULL,state TEXT NOT NULL,result TEXT,PRIMARY KEY(principal,request_id))")

    def _db(self):
        db=sqlite3.connect(self.path,timeout=10,isolation_level=None)
        db.execute("PRAGMA busy_timeout=10000")
        db.execute("PRAGMA journal_mode=WAL")
        return db

    @staticmethod
    def digest(operation,payload):
        try:
            canonical=json.dumps({"operation":operation,"payload":payload},sort_keys=True,ensure_ascii=False,allow_nan=False,separators=(",",":")).encode("utf-8")
        except (TypeError,ValueError):
            raise LedgerError("INVALID_REQUEST") from None
        return hashlib.sha256(canonical).hexdigest()

    @staticmethod
    def scope(principal,request_id):
        if not isinstance(principal,str) or not principal.strip() or len(principal)>512:
            raise LedgerError("UNAUTHORIZED")
        if not isinstance(request_id,str) or not request_id.strip() or len(request_id)>128:
            raise LedgerError("INVALID_REQUEST")

    def admit(self,*,principal,request_id,operation,payload):
        self.scope(principal,request_id)
        digest=self.digest(operation,payload)
        with self._db() as db:
            db.execute("BEGIN IMMEDIATE")
            row=db.execute("SELECT digest,state,result FROM requests WHERE principal=? AND request_id=?",(principal,request_id)).fetchone()
            if row is None:
                db.execute("INSERT INTO requests VALUES(?,?,?,?,NULL)",(principal,request_id,digest,"IN_PROGRESS"))
                db.execute("COMMIT")
                return {"decision":"EXECUTE","digest":digest}
            db.execute("COMMIT")
            if row[0]!=digest: raise LedgerError("IDEMPOTENCY_CONFLICT")
            if row[1]=="COMPLETE":
                return {"decision":"REPLAY","result":json.loads(row[2]),"digest":digest}
            return {"decision":"AMBIGUOUS","digest":digest}

    def complete(self,*,principal,request_id,operation,payload,result):
        self.scope(principal,request_id)
        digest=self.digest(operation,payload)
        try:
            encoded=json.dumps(result,sort_keys=True,ensure_ascii=False,allow_nan=False,separators=(",",":"))
        except (TypeError,ValueError):
            raise LedgerError("INVALID_RESULT") from None
        with self._db() as db:
            db.execute("BEGIN IMMEDIATE")
            row=db.execute("SELECT digest,state FROM requests WHERE principal=? AND request_id=?",(principal,request_id)).fetchone()
            if row is None or row[0]!=digest:
                db.execute("ROLLBACK")
                raise LedgerError("IDEMPOTENCY_CONFLICT")
            if row[1]!="IN_PROGRESS":
                db.execute("ROLLBACK")
                raise LedgerError("ALREADY_COMPLETED")
            db.execute("UPDATE requests SET state='COMPLETE',result=? WHERE principal=? AND request_id=?",(encoded,principal,request_id))
            db.execute("COMMIT")
