"""Source-only N39 historical scientific consent / independent retrieval grant.

Read authorization never consumes a scientific execution consent or dispatches work.
Writing provenance and retrieval grant is a separately trusted, offline operator
action, not exposed by UDS, HTTP, or untrusted science payload.
"""
import sqlite3
import time
from pathlib import Path
from .consent_custody128 import ConsentCustody128

class N39ConsentPolicy:
    def __init__(self, db_path, *, clock=time.time):
        self.path=Path(db_path)
        self.path.parent.mkdir(parents=True,exist_ok=True)
        self.clock=clock
        with self._db() as db:
            db.execute("CREATE TABLE IF NOT EXISTS origin (principal TEXT NOT NULL, request_id TEXT NOT NULL, consent_ref TEXT NOT NULL, revoked INTEGER NOT NULL DEFAULT 0, PRIMARY KEY(principal,request_id))")
            db.execute("CREATE TABLE IF NOT EXISTS retrieval (principal TEXT NOT NULL,request_id TEXT NOT NULL,artifact_id TEXT NOT NULL,grant_ref TEXT NOT NULL,expires REAL NOT NULL,revoked INTEGER NOT NULL DEFAULT 0,PRIMARY KEY(principal,request_id,artifact_id))")

    def _db(self):
        db=sqlite3.connect(self.path,timeout=5,isolation_level=None)
        db.execute("PRAGMA busy_timeout=5000")
        return db

    def record_original(self, *, custody, context):
        """Only pre-execution: independently verify and consume the source grant."""
        if not isinstance(custody,ConsentCustody128) or not isinstance(context,dict):
            return False
        principal=context.get("principal")
        request_id=context.get("request_id")
        ref=context.get("consent_ref")
        if not all(isinstance(x,str) and x for x in (principal,request_id,ref)):
            return False
        # An existing record is not equivalent to a fresh execution authorization.
        with self._db() as db:
            if db.execute("SELECT 1 FROM origin WHERE principal=? AND request_id=?",(principal,request_id)).fetchone():
                return False
        if custody(dict(context)) is not True:
            return False
        with self._db() as db:
            try:
                db.execute("INSERT INTO origin VALUES(?,?,?,0)",(principal,request_id,ref))
                return True
            except sqlite3.IntegrityError:
                return False

    def revoke_original(self, *, principal, request_id):
        """Operator-side test mutation only; no server route exposes this."""
        with self._db() as db:
            db.execute("UPDATE origin SET revoked=1 WHERE principal=? AND request_id=?",(principal,request_id))

    def record_read_grant(self, *, principal, request_id, artifact_id, grant_ref, expires):
        """Separate out-of-band retrieval permission: NEVER inferred from origin."""
        if not all(isinstance(x,str) and x for x in (principal,request_id,artifact_id,grant_ref)) or not isinstance(expires,(int,float)) or expires<=self.clock():
            raise ValueError("INVALID_RETRIEVAL_GRANT")
        with self._db() as db:
            db.execute("BEGIN IMMEDIATE")
            exists=db.execute("SELECT 1 FROM origin WHERE principal=? AND request_id=?",(principal,request_id)).fetchone()
            if not exists:
                db.execute("ROLLBACK")
                raise ValueError("ORIGINAL_CONSENT_PROVENANCE_MISSING")
            db.execute("INSERT OR REPLACE INTO retrieval VALUES(?,?,?,?,?,0)",(principal,request_id,artifact_id,grant_ref,expires))
            db.execute("COMMIT")

    def revoke_read_grant(self, *, principal, request_id, artifact_id):
        with self._db() as db:
            db.execute("UPDATE retrieval SET revoked=1 WHERE principal=? AND request_id=? AND artifact_id=?",(principal,request_id,artifact_id))

    def is_authorized(self, *, principal, request_id, artifact_id):
        """Atomic linearization point for READ; a later revoke affects later reads."""
        with self._db() as db:
            db.execute("BEGIN IMMEDIATE")
            row=db.execute("""SELECT o.consent_ref,r.grant_ref,r.expires,r.revoked
                FROM origin o JOIN retrieval r ON o.principal=r.principal AND o.request_id=r.request_id
                WHERE o.principal=? AND o.request_id=? AND r.artifact_id=?""",
                (principal,request_id,artifact_id)).fetchone()
            ok=bool(row and row[0] and row[1] and row[3]==0 and row[2]>self.clock())
            db.execute("COMMIT")
            return ok
