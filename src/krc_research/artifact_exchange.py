"""Private staging artifact exchange. Do not expose without trusted auth transport."""
import hashlib
import json
import os
import secrets
import sqlite3
import stat
import tempfile
import time
from pathlib import Path

MIB = 1024 * 1024
INLINE_TARGET = 900 * 1024
MAX_ARTIFACT = 200 * MIB
MAX_TOTAL = 2 * 1024 * MIB
TTL = 7 * 24 * 3600

class ExchangeError(Exception):
    def __init__(self, code):
        self.code = code
        super().__init__(code)

class ArtifactExchange:
    def __init__(self, root, *, max_artifact=MAX_ARTIFACT, max_total=MAX_TOTAL, ttl=TTL, clock=time.time):
        self.root = Path(root)
        self.root.mkdir(mode=0o700, parents=True, exist_ok=True)
        if self.root.is_symlink() or self.root.stat().st_mode & 0o077:
            raise ExchangeError("INSECURE_STORE")
        self.data = self.root / "objects"
        self.data.mkdir(mode=0o700, exist_ok=True)
        if self.data.is_symlink() or self.data.stat().st_mode & 0o077:
            raise ExchangeError("INSECURE_STORE")
        self.dbpath = self.root / "index.sqlite3"
        if not (isinstance(max_artifact,int) and isinstance(max_total,int) and 0 < max_artifact <= max_total and isinstance(ttl,int) and ttl > 0):
            raise ExchangeError("INVALID_CONFIGURATION")
        self.max_artifact,self.max_total,self.ttl,self.clock = max_artifact,max_total,ttl,clock
        self._init()

    def _connect(self):
        db = sqlite3.connect(self.dbpath,timeout=10,isolation_level=None)
        db.execute("PRAGMA busy_timeout=10000")
        return db

    def _init(self):
        with self._connect() as db:
            db.execute("PRAGMA journal_mode=WAL")
            db.execute("CREATE TABLE IF NOT EXISTS objects (id TEXT PRIMARY KEY, principal TEXT NOT NULL, request_id TEXT NOT NULL, filename TEXT NOT NULL, media_type TEXT NOT NULL, size INTEGER NOT NULL, sha256 TEXT NOT NULL, expires REAL NOT NULL)")
            db.execute("CREATE INDEX IF NOT EXISTS object_owner ON objects(principal,request_id)")
        os.chmod(self.dbpath,0o600)

    @staticmethod
    def _assert_scope(principal,request_id):
        if not isinstance(principal,str) or not principal.strip() or len(principal)>512:
            raise ExchangeError("UNAUTHORIZED")
        if not isinstance(request_id,str) or not request_id.strip() or len(request_id)>128:
            raise ExchangeError("INVALID_REQUEST")

    def store_bytes(self,payload,*,principal,request_id,filename,media_type="application/octet-stream"):
        self._assert_scope(principal,request_id)
        if not isinstance(payload,bytes) or not isinstance(filename,str) or not filename or len(filename)>160 or "/" in filename or "\\" in filename or filename in (".",".."):
            raise ExchangeError("INVALID_REQUEST")
        if not isinstance(media_type,str) or not media_type or len(media_type)>128:
            raise ExchangeError("INVALID_REQUEST")
        size=len(payload)
        if size>self.max_artifact:
            raise ExchangeError("ARTIFACT_TOO_LARGE")
        digest=hashlib.sha256(payload).hexdigest()
        identifier=secrets.token_hex(24)
        fd,temp=tempfile.mkstemp(prefix=".pending-",dir=self.data)
        committed=False
        expires=self.clock()+self.ttl
        try:
            with os.fdopen(fd,"wb") as f:
                os.fchmod(f.fileno(),0o600)
                f.write(payload)
                f.flush()
                os.fsync(f.fileno())
            with self._connect() as db:
                db.execute("BEGIN IMMEDIATE")
                occupied=db.execute("SELECT COALESCE(SUM(size),0) FROM objects").fetchone()[0]
                if occupied+size>self.max_total:
                    db.execute("ROLLBACK")
                    raise ExchangeError("STORAGE_QUOTA_EXCEEDED")
                os.replace(temp,self.data/identifier)
                db.execute("INSERT INTO objects VALUES (?,?,?,?,?,?,?,?)",(identifier,principal,request_id,filename,media_type,size,digest,expires))
                db.execute("COMMIT")
                committed=True
            return {"artifact_id":identifier,"filename":filename,"media_type":media_type,"size_bytes":size,"sha256":digest,"expires_at_epoch":expires}
        finally:
            if not committed:
                if os.path.exists(temp): os.unlink(temp)
                if (self.data/identifier).exists(): os.unlink(self.data/identifier)

    def get_bytes(self,artifact_id,*,principal,request_id):
        self._assert_scope(principal,request_id)
        if not isinstance(artifact_id,str) or len(artifact_id)!=48 or any(c not in "0123456789abcdef" for c in artifact_id):
            raise ExchangeError("NOT_FOUND")
        with self._connect() as db:
            record=db.execute("SELECT principal,request_id,size,sha256,expires FROM objects WHERE id=?",(artifact_id,)).fetchone()
        if record is None or record[0]!=principal or record[1]!=request_id:
            raise ExchangeError("NOT_FOUND")
        if record[4]<=self.clock():
            raise ExchangeError("ARTIFACT_EXPIRED")
        try:
            fd=os.open(self.data/artifact_id,os.O_RDONLY|getattr(os,"O_NOFOLLOW",0))
            if not stat.S_ISREG(os.fstat(fd).st_mode):
                os.close(fd)
                raise ExchangeError("ARTIFACT_UNAVAILABLE")
            with os.fdopen(fd,"rb") as f:
                data=f.read(self.max_artifact+1)
        except OSError:
            raise ExchangeError("ARTIFACT_UNAVAILABLE") from None
        if len(data)!=record[2] or hashlib.sha256(data).hexdigest()!=record[3]:
            raise ExchangeError("ARTIFACT_CORRUPTED")
        return data

    def iter_chunks(self,artifact_id,*,principal,request_id,chunk_size=256*1024):
        """Chunked output; buffers full content for preflight verification; staging only."""
        if not isinstance(chunk_size,int) or not 0 < chunk_size <= MIB:
            raise ExchangeError("INVALID_REQUEST")
        data=self.get_bytes(artifact_id,principal=principal,request_id=request_id)
        for offset in range(0,len(data),chunk_size):
            yield data[offset:offset+chunk_size]

    def reconcile_orphans(self):
        """Manual single-process maintenance only. Never run during concurrent writes."""
        with self._connect() as db:
            known={row[0] for row in db.execute("SELECT id FROM objects")}
        count=0
        for path in self.data.iterdir():
            if path.name.startswith(".pending-") or (len(path.name)==48 and path.name not in known):
                if path.is_file() or path.is_symlink():
                    path.unlink()
                    count+=1
        return count

    def cleanup_expired(self):
        with self._connect() as db:
            db.execute("BEGIN IMMEDIATE")
            ids=[r[0] for r in db.execute("SELECT id FROM objects WHERE expires<=?",(self.clock(),))]
            for identifier in ids:
                (self.data/identifier).unlink(missing_ok=True)
                db.execute("DELETE FROM objects WHERE id=?",(identifier,))
            db.execute("COMMIT")
        return len(ids)

def deliver_result(result,*,exchange,principal,request_id,filename="research-result.json"):
    exchange._assert_scope(principal,request_id)
    wire={"version":"krc-transport/2","request_id":request_id,"status":"completed","delivery":"inline","result":result}
    try:
        encoded=json.dumps(wire,ensure_ascii=False,separators=(",",":"),allow_nan=False).encode("utf-8")
    except (TypeError,ValueError):
        raise ExchangeError("INVALID_RESULT") from None
    if len(encoded)<=MIB:
        return wire
    body=json.dumps(result,ensure_ascii=False,separators=(",",":"),allow_nan=False).encode("utf-8")
    artifact=exchange.store_bytes(body,principal=principal,request_id=request_id,filename=filename,media_type="application/json")
    return {"version":"krc-transport/2","request_id":request_id,"status":"completed","delivery":"artifact","artifact":artifact}
