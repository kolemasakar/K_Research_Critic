"""Owner-approved personal chat research consent, source-only.

This module cannot identify a real ChatGPT user by itself. An independently
trusted chat gateway must verify the owner and sign event envelopes. Untrusted
chat text, caller booleans and original research prompts are never sufficient.
No installed service is changed; no free/paid provider work is initiated.
"""
import hashlib
import hmac
import json
import os
import secrets
import sqlite3
import stat
import time
from pathlib import Path

class ConsentDenied(ValueError):
    pass

def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(",",":"),allow_nan=False,ensure_ascii=False).encode("utf-8")

def profile_hash(profile):
    if not isinstance(profile,dict) or not profile:
        raise ConsentDenied("INVALID_PROFILE")
    return hashlib.sha256(canonical(profile)).hexdigest()

class SignedChatEventVerifier:
    """Verifier-only HMAC trust boundary; signing happens outside KRC.

    key must be provisioned privately by the authenticated chat gateway. A
    reference-only event is not authenticated without a valid gateway MAC.
    """
    def __init__(self, *, owner_ref, issuer, key, clock=time.time, max_skew_seconds=300):
        if not all(isinstance(v,str) and v for v in (owner_ref,issuer)) or not isinstance(key,bytes) or len(key)<32:
            raise ConsentDenied("INVALID_GATEWAY_TRUST")
        self.owner_ref=owner_ref
        self.issuer=issuer
        self._key=key
        self.clock=clock
        self.max_skew_seconds=max_skew_seconds

    def verify(self, event, *, request_id, chat_id, expected_profile_hash):
        required={"version","issuer","owner_ref","request_id","chat_id",
                  "profile_sha256","decision","event_ref","issued_at","mac_sha256"}
        if not isinstance(event,dict) or set(event)!=required:
            return False
        if (event.get("version")!=1 or event.get("issuer")!=self.issuer
            or event.get("owner_ref")!=self.owner_ref
            or event.get("request_id")!=request_id or event.get("chat_id")!=chat_id
            or event.get("profile_sha256")!=expected_profile_hash
            or event.get("decision") not in ("APPROVE","CANCEL")
            or not isinstance(event.get("event_ref"),str) or len(event["event_ref"])<16
            or type(event.get("issued_at")) is not int
            or abs(int(self.clock())-event["issued_at"])>self.max_skew_seconds
            or not isinstance(event.get("mac_sha256"),str)):
            return False
        try:
            mac=hashlib.sha256().hexdigest()
            if len(event["mac_sha256"])!=len(mac):
                return False
            signed={k:v for k,v in event.items() if k!="mac_sha256"}
            expected=hmac.new(self._key,canonical(signed),hashlib.sha256).hexdigest()
            return hmac.compare_digest(event["mac_sha256"],expected)
        except (TypeError,ValueError,OverflowError):
            return False

class SingleOwnerConsentLedger:
    MAX_SECONDS=86400
    def __init__(self, db_path, *, verifier, authorized_principal, clock=time.time):
        if not isinstance(verifier,SignedChatEventVerifier) and not (type(verifier).__name__=="ProjectChannelVerifier" and type(verifier).__module__=="krc_research.stage131_n39_project_channel_consent"):
            raise ConsentDenied("TRUSTED_CHAT_OR_PROJECT_CHANNEL_REQUIRED")
        if not isinstance(authorized_principal,str) or not authorized_principal:
            raise ConsentDenied("INVALID_AUTHORIZED_PRINCIPAL")
        self.verifier=verifier
        self.authorized_principal=authorized_principal
        self.clock=clock
        self.path=Path(db_path)
        if not self.path.is_absolute() or self.path.is_symlink():
            raise ConsentDenied("UNSAFE_CONSENT_DB")
        self.path.parent.mkdir(parents=True,mode=0o700,exist_ok=True)
        pst=self.path.parent.stat()
        if not stat.S_ISDIR(pst.st_mode) or pst.st_mode & 0o077:
            raise ConsentDenied("UNSAFE_CONSENT_DIRECTORY")
        if self.path.exists():
            st=self.path.lstat()
            if not stat.S_ISREG(st.st_mode) or st.st_mode & 0o077:
                raise ConsentDenied("UNSAFE_CONSENT_DB")
        with self._db() as db:
            db.execute("""CREATE TABLE IF NOT EXISTS approvals(
                request_id TEXT PRIMARY KEY,chat_id TEXT NOT NULL,profile_sha256 TEXT NOT NULL,
                status TEXT NOT NULL,event_ref TEXT UNIQUE,approved_at INTEGER,
                expires_at INTEGER, consumed_at INTEGER,cancelled_at INTEGER,
                completed_at INTEGER)""")
            db.execute("""CREATE TABLE IF NOT EXISTS artifacts(
                artifact_id TEXT PRIMARY KEY,request_id TEXT NOT NULL,
                FOREIGN KEY(request_id) REFERENCES approvals(request_id))""")
        os.chmod(self.path,0o600)

    def _db(self):
        db=sqlite3.connect(str(self.path),timeout=5,isolation_level=None)
        db.execute("PRAGMA busy_timeout=5000")
        db.execute("PRAGMA synchronous=FULL")
        db.execute("PRAGMA foreign_keys=ON")
        return db

    def propose(self, *, request_id, chat_id, profile):
        if not all(isinstance(x,str) and x for x in (request_id,chat_id)):
            return False
        digest=profile_hash(profile)
        with self._db() as db:
            try:
                db.execute("INSERT INTO approvals(request_id,chat_id,profile_sha256,status) VALUES(?,?,?,'PROPOSED')",
                           (request_id,chat_id,digest))
                return True
            except sqlite3.IntegrityError:
                return False

    def decide(self, *, request_id, chat_id, event):
        with self._db() as db:
            db.execute("BEGIN IMMEDIATE")
            row=db.execute("SELECT chat_id,profile_sha256,status FROM approvals WHERE request_id=?",(request_id,)).fetchone()
            if not row or row[0]!=chat_id or row[2] not in ("PROPOSED","APPROVED","RUNNING","COMPLETED"):
                db.execute("ROLLBACK")
                return False
            if not self.verifier.verify(event,request_id=request_id,chat_id=chat_id,expected_profile_hash=row[1]):
                db.execute("ROLLBACK")
                return False
            now=int(self.clock())
            if event["decision"]=="APPROVE":
                if row[2]!="PROPOSED":
                    db.execute("ROLLBACK")
                    return False
                expires=now+self.MAX_SECONDS
                db.execute("""UPDATE approvals SET status='APPROVED',event_ref=?,approved_at=?,expires_at=?
                    WHERE request_id=? AND status='PROPOSED'""",(event["event_ref"],now,expires,request_id))
            else:
                db.execute("""UPDATE approvals SET status='CANCELLED',cancelled_at=? WHERE request_id=?""",(now,request_id))
            db.execute("COMMIT")
            return True

    def claim_execution(self, request_id):
        """A one-shot claim; crash after claim never creates a second execution."""
        with self._db() as db:
            db.execute("BEGIN IMMEDIATE")
            now=int(self.clock())
            row=db.execute("SELECT status,expires_at FROM approvals WHERE request_id=?",(request_id,)).fetchone()
            if not row or row[0]!="APPROVED" or row[1]<=now:
                db.execute("ROLLBACK")
                return False
            db.execute("""UPDATE approvals SET status='RUNNING',consumed_at=?
                WHERE request_id=? AND status='APPROVED'""",(now,request_id))
            db.execute("COMMIT")
            return True

    def can_continue(self, request_id):
        """Workers must check before each new step; cancel or 24h expiry denies."""
        with self._db() as db:
            row=db.execute("SELECT status,expires_at FROM approvals WHERE request_id=?",(request_id,)).fetchone()
        return bool(row and row[0]=="RUNNING" and row[1]>int(self.clock()))

    def complete(self, request_id):
        with self._db() as db:
            db.execute("BEGIN IMMEDIATE")
            now=int(self.clock())
            result=db.execute("""UPDATE approvals SET status='COMPLETED',completed_at=?
                WHERE request_id=? AND status='RUNNING' AND expires_at>?""",(now,request_id,now))
            db.execute("COMMIT")
            return result.rowcount==1

    def register_artifact(self, *, request_id, artifact_id):
        if not isinstance(artifact_id,str) or not artifact_id:
            return False
        with self._db() as db:
            db.execute("BEGIN IMMEDIATE")
            row=db.execute("SELECT status FROM approvals WHERE request_id=?",(request_id,)).fetchone()
            if not row or row[0]!="COMPLETED":
                db.execute("ROLLBACK")
                return False
            try:
                db.execute("INSERT INTO artifacts VALUES(?,?)",(artifact_id,request_id))
                db.execute("COMMIT")
                return True
            except sqlite3.IntegrityError:
                db.execute("ROLLBACK")
                return False

    def is_authorized(self, *, principal, request_id, artifact_id):
        if principal!=self.authorized_principal:
            return False
        with self._db() as db:
            row=db.execute("""SELECT a.status FROM approvals a JOIN artifacts b
                ON a.request_id=b.request_id
                WHERE a.request_id=? AND b.artifact_id=?""",(request_id,artifact_id)).fetchone()
            return bool(row and row[0]=="COMPLETED")

    def status(self, request_id):
        with self._db() as db:
            row=db.execute("SELECT status,expires_at,completed_at FROM approvals WHERE request_id=?",(request_id,)).fetchone()
        if row is None:
            return "MISSING"
        if row[0]=="APPROVED" and row[1]<=int(self.clock()):
            return "EXPIRED"
        if row[0]=="RUNNING" and row[1]<=int(self.clock()):
            return "EXPIRED_RUNNING"
        return row[0]
