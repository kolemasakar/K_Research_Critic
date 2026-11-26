"""Source-only prepared request read. No listener, credentials or live state."""
import hashlib
import hmac
import json
import os
import re
import sqlite3
import stat
import time
from contextlib import closing
from pathlib import Path

VERSION = "krc-prepared-read/2"
OPERATION = "prepared_request.read"
KEY_ID = "stage135-prepared-read-v1"
LIMIT = 262144
IDENTITY_FIELDS = {"principal", "repository", "workflow_ref", "workflow_file_ref", "run_id", "run_attempt"}

class Denied(ValueError):
    def __init__(self, status, code):
        self.status, self.code = status, code
        super().__init__(code)

def deny(status=403, code="FORBIDDEN"):
    raise Denied(status, code)

def hexstr(value, n):
    return isinstance(value, str) and re.fullmatch("[0-9a-f]{%d}" % n, value) is not None

def rid_ok(value):
    return isinstance(value, str) and re.fullmatch("KS-[0-9a-f]{32}", value) is not None

def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")

def strict_json(raw):
    def pairs(items):
        result = {}
        for k, v in items:
            if k in result:
                raise ValueError("duplicate key")
            result[k] = v
        return result
    def bad_constant(_):
        raise ValueError("nonfinite")
    return json.loads(raw.decode("utf-8"), object_pairs_hook=pairs, parse_constant=bad_constant)

def identity_ok(i):
    return (isinstance(i, dict) and set(i) == IDENTITY_FIELDS
            and i["principal"] == "K_Science"
            and i["repository"] == "kolemasakar/K_Science"
            and i["workflow_ref"] == "refs/heads/main"
            and isinstance(i["workflow_file_ref"], str)
            and re.fullmatch(r"kolemasakar/K_Science/\.github/workflows/[A-Za-z0-9_.-]+\.ya?ml@refs/heads/main", i["workflow_file_ref"]) is not None
            and isinstance(i["run_id"], str) and re.fullmatch("[1-9][0-9]{0,19}", i["run_id"]) is not None
            and type(i["run_attempt"]) is int and i["run_attempt"] == 1)

def signing_bytes(m):
    return canonical(dict(m, auth={k:v for k,v in m["auth"].items() if k != "mac_sha256"}))

def digest(data):
    return hashlib.sha256(data).hexdigest()

def verify(raw, *, key, peer_uid, expected_uid, allowed_workflow, claim, now):
    if peer_uid != expected_uid:
        deny()
    if not isinstance(raw, bytes) or not 0 < len(raw) <= 4096:
        deny(413, "REQUEST_TOO_LARGE")
    try:
        m = strict_json(raw)
        if not isinstance(m, dict) or set(m) != {"version","operation","request_id","identity","auth"}:
            raise ValueError()
        a, i = m["auth"], m["identity"]
        if not isinstance(a, dict) or set(a) != {"key_id","issued_at_epoch","nonce","mac_sha256"}:
            raise ValueError()
        if not rid_ok(m["request_id"]) or not identity_ok(i) or not hexstr(a["nonce"],32) or not hexstr(a["mac_sha256"],64) or type(a["issued_at_epoch"]) is not int:
            raise ValueError()
    except (ValueError, TypeError, KeyError, RecursionError):
        deny(400, "INVALID_REQUEST")
    if m["version"] != VERSION or m["operation"] != OPERATION or a["key_id"] != KEY_ID or i["workflow_file_ref"] != allowed_workflow:
        deny()
    if not isinstance(key, bytes) or len(key) != 32:
        deny(503,"BACKEND_UNAVAILABLE")
    if abs(now - a["issued_at_epoch"]) > 60:
        deny()
    if not hmac.compare_digest(hmac.new(key,signing_bytes(m),hashlib.sha256).hexdigest(),a["mac_sha256"]):
        deny()
    if claim(KEY_ID,i["principal"],a["nonce"],now) is not True:
        deny()
    return m["request_id"], i

class Registry:
    """Private isolated SQLite; trusted administrative callers only."""
    def __init__(self, root):
        self.root = Path(root)
        s = self.root.lstat()
        if not stat.S_ISDIR(s.st_mode) or s.st_uid != os.geteuid() or s.st_mode & 0o077:
            raise ValueError("unsafe state")
        self.path = self.root / "prepared.sqlite"
        fd = os.open(self.path, os.O_CREAT|os.O_RDWR|os.O_NOFOLLOW, 0o600)
        try:
            s = os.fstat(fd)
            if not stat.S_ISREG(s.st_mode) or s.st_uid != os.geteuid() or s.st_mode & 0o077 or s.st_nlink != 1:
                raise ValueError("unsafe database")
        finally:
            os.close(fd)
        with closing(self.db()) as db:
            db.executescript("""CREATE TABLE IF NOT EXISTS grants (
              rid TEXT PRIMARY KEY, identity TEXT NOT NULL, profile_hash TEXT NOT NULL,
              body_hash TEXT NOT NULL, size INTEGER NOT NULL, status TEXT NOT NULL,
              expires INTEGER NOT NULL, decision TEXT NOT NULL);
              CREATE TABLE IF NOT EXISTS nonces (key_id TEXT, principal TEXT, nonce TEXT,
              created INTEGER NOT NULL, PRIMARY KEY(key_id,principal,nonce));""")

    def db(self):
        db = sqlite3.connect(self.path, timeout=3, isolation_level=None)
        db.execute("PRAGMA synchronous=FULL")
        return db

    def claim(self, key_id, principal, nonce, now):
        with closing(self.db()) as db:
            db.execute("BEGIN IMMEDIATE")
            try:
                db.execute("DELETE FROM nonces WHERE created < ?",(now-900,))
                db.execute("INSERT INTO nonces VALUES(?,?,?,?)",(key_id,principal,nonce,now))
                db.execute("COMMIT")
                return True
            except sqlite3.IntegrityError:
                db.execute("ROLLBACK")
                return False

    def prepare(self, rid, identity, profile_hash, body_hash, size):
        if not rid_ok(rid) or not identity_ok(identity) or not hexstr(profile_hash,64) or not hexstr(body_hash,64) or type(size) is not int or not 0<size<=LIMIT:
            raise ValueError("invalid descriptor")
        with closing(self.db()) as db:
            db.execute("INSERT INTO grants VALUES(?,?,?,?,?,'PREPARED',0,'')",(rid,canonical(identity).decode(),profile_hash,body_hash,size))

    def authorize(self, rid, *, decision, now, ttl):
        if not isinstance(decision,str) or not decision.strip() or type(now) is not int or type(ttl) is not int or not 0<ttl<=900:
            raise ValueError("invalid decision")
        with closing(self.db()) as db:
            if db.execute("UPDATE grants SET status='AUTHORIZED',expires=?,decision=? WHERE rid=? AND status='PREPARED'",(now+ttl,decision,rid)).rowcount != 1:
                deny()

    def revoke(self, rid):
        with closing(self.db()) as db:
            db.execute("UPDATE grants SET status='REVOKED' WHERE rid=?",(rid,))

    def descriptor(self, rid, identity, now):
        with closing(self.db()) as db:
            row = db.execute("SELECT identity,profile_hash,body_hash,size,status,expires,decision FROM grants WHERE rid=?",(rid,)).fetchone()
        if not row or row[0] != canonical(identity).decode() or row[4] != "AUTHORIZED":
            deny()
        if now >= row[5]:
            deny(410,"GONE")
        return row

class Reader:
    def __init__(self, registry, *, key, peer_uid, allowed_workflow, profile_lookup, enabled=False, clock=time.time):
        self.registry,self.key,self.peer_uid,self.allowed_workflow = registry,key,peer_uid,allowed_workflow
        self.profile_lookup,self.enabled,self.clock = profile_lookup,enabled is True,clock

    def read(self, raw, *, peer_uid):
        if not self.enabled:
            deny(404,"NOT_FOUND")
        try:
            rid,i = verify(raw,key=self.key,peer_uid=peer_uid,expected_uid=self.peer_uid,allowed_workflow=self.allowed_workflow,claim=self.registry.claim,now=int(self.clock()))
            d = self.registry.descriptor(rid,i,int(self.clock()))
            # Trusted read-only adapter must return authoritative profile and consent state.
            profile,state = self.profile_lookup(rid)
            if state not in ("PROPOSED","APPROVED"):
                deny()
            if digest(canonical(profile)) != d[1]:
                deny(502,"UPSTREAM_INVALID_RESPONSE")
            expected = canonical({"request_id":rid,"operation":profile["operation"],"payload":profile["payload"]})
            path = self.registry.root / (rid+".json")
            fd = os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
            with os.fdopen(fd,"rb") as f:
                s = os.fstat(f.fileno())
                if not stat.S_ISREG(s.st_mode) or s.st_uid != os.geteuid() or s.st_mode & 0o077 or s.st_nlink != 1 or s.st_size != d[3]:
                    deny(502,"UPSTREAM_INVALID_RESPONSE")
                body = f.read(LIMIT+1)
                t = os.fstat(f.fileno())
                if (s.st_size,s.st_mtime_ns,s.st_ctime_ns) != (t.st_size,t.st_mtime_ns,t.st_ctime_ns):
                    deny(502,"UPSTREAM_INVALID_RESPONSE")
            if len(body)!=d[3] or digest(body)!=d[2] or body!=expected:
                deny(502,"UPSTREAM_INVALID_RESPONSE")
            if self.registry.descriptor(rid,i,int(self.clock())) != d:
                deny()
            latest, state = self.profile_lookup(rid)
            if state not in ("PROPOSED","APPROVED") or digest(canonical(latest)) != d[1]:
                deny()
            return body
        except Denied:
            raise
        except (OSError,sqlite3.Error):
            deny(503,"BACKEND_UNAVAILABLE")
        except (ValueError,TypeError,KeyError,RecursionError):
            deny(502,"UPSTREAM_INVALID_RESPONSE")
