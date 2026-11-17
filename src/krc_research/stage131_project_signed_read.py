"""N39 source-only personal project artifact read/describe composition.

The service runs as the existing private state owner, krcops, never grants
Sentinel direct filesystem access, and never instantiates a research signer
or dispatcher. Authenticated AF_UNIX retrieval only. No live activation here.
"""
import argparse
import hashlib
import json
import os
import re
import sqlite3
import stat
import tempfile
import time
from contextlib import closing
from pathlib import Path
from .stage131_artifact_nonce_registry import ArtifactNonceRegistry
from .stage131_signed_artifact_read import verify_signed_read, ArtifactReadDenied
from .stage131_signed_artifact_uds import SignedArtifactUDSServer
from .stage131_consumer_boundary_checks import validate_artifact_descriptor

PRINCIPAL="K_Science"
IDENTITY={"principal":PRINCIPAL,"repository":"kolemasakar/K_Science",
 "workflow_ref":"refs/heads/main"}
STATE=Path("/home/krcops/krc-project-n39-staging/state")
SOCKET=Path("/run/krc-project-n39-read/backend.sock")
NONCE=Path("/var/lib/krc-project-n39-read/nonce.sqlite")
KEY_ID="stage131-project-read-v1"
KEY_PATH=Path("/etc/krc-project-n39-read/retrieval.key")
MAX_BYTES=200*1024*1024
class ReadDenied(ValueError):
    def __init__(self,status,code):
        self.status,self.code=status,code
        super().__init__(code)

def deny(status,code):
    raise ReadDenied(status,code)

def checked(path, *, directory=False, uid=None, private=True):
    st=Path(path).lstat()
    if not (stat.S_ISDIR(st.st_mode) if directory else stat.S_ISREG(st.st_mode)):
        deny(503,"BACKEND_UNAVAILABLE")
    if st.st_uid!=(os.geteuid() if uid is None else uid) or (private and st.st_mode & 0o077):
        deny(503,"BACKEND_UNAVAILABLE")
    return st

def ro(path):
    p=Path(path)
    checked(p)
    db=sqlite3.connect(p.as_uri()+"?mode=ro",uri=True,timeout=3)
    db.execute("PRAGMA query_only=ON")
    return db

class ProjectArtifactAuthority:
    def __init__(self,root,*,clock=time.time,limit=MAX_BYTES):
        self.root=Path(root)
        if not self.root.is_absolute(): raise ValueError("ABSOLUTE_STATE_REQUIRED")
        checked(self.root,directory=True)
        checked(self.root/"artifacts",directory=True)
        checked(self.root/"artifacts"/"objects",directory=True)
        if type(limit) is not int or not 0<limit<=MAX_BYTES:
            raise ValueError("INVALID_LIMIT")
        self.limit,self.clock=limit,clock

    def descriptor(self,scope):
        rid,aid,principal=scope["request_id"],scope["artifact_id"],scope["principal"]
        if principal!=PRINCIPAL or not re.fullmatch(r"KS-[0-9a-f]{32}",rid):
            deny(403,"FORBIDDEN")
        with closing(ro(self.root/"requests.sqlite")) as db:
            row=db.execute("SELECT state,result FROM requests WHERE principal=? AND request_id=?",(principal,rid)).fetchone()
        if not row or row[0]!="COMPLETE": deny(404,"NOT_FOUND")
        try:
            out=json.loads(row[1])
            a=out["artifact"]
            if (out["version"]!="krc-transport/2" or out["status"]!="completed" or
                out["delivery"]!="artifact" or out["request_id"]!=rid or
                validate_artifact_descriptor(a,now_epoch=0)!="DESCRIPTOR_VALID_NOT_AUTHORIZED"):
                deny(502,"UPSTREAM_INVALID_RESPONSE")
        except (KeyError,TypeError,ValueError) as exc:
            if isinstance(exc,ReadDenied):raise
            deny(502,"UPSTREAM_INVALID_RESPONSE")
        if a["artifact_id"]!=aid: deny(404,"NOT_FOUND")
        with closing(ro(self.root/"consent.sqlite")) as db:
            row=db.execute("""SELECT a.status FROM approvals a JOIN artifacts b USING(request_id)
                WHERE a.request_id=? AND b.artifact_id=?""",(rid,aid)).fetchone()
        if not row or row[0]!="COMPLETED": deny(403,"FORBIDDEN")
        # Retain the authoritative descriptor separately from response bytes.
        descriptor={k:a[k] for k in ("artifact_id","filename","media_type","size_bytes","sha256","expires_at_epoch")}
        with closing(ro(self.root/"artifacts"/"index.sqlite3")) as db:
            row=db.execute("SELECT filename,media_type,size,sha256,expires FROM objects WHERE id=? AND principal=? AND request_id=?",(aid,principal,rid)).fetchone()
        if not row:
            if descriptor["expires_at_epoch"]<=self.clock():deny(410,"GONE")
            deny(404,"NOT_FOUND")
        if tuple(descriptor[k] for k in ("filename","media_type","size_bytes","sha256","expires_at_epoch"))!=row:
            deny(502,"UPSTREAM_INVALID_RESPONSE")
        if descriptor["expires_at_epoch"]<=self.clock():deny(410,"GONE")
        if descriptor["size_bytes"]>self.limit:deny(413,"REQUEST_TOO_LARGE")
        return dict(descriptor,request_id=rid)

    def spool(self,scope):
        d=self.descriptor(scope)
        path=self.root/"artifacts"/"objects"/scope["artifact_id"]
        f=tempfile.TemporaryFile(mode="w+b")
        try:
            try:fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC)
            except FileNotFoundError:deny(404,"NOT_FOUND")
            except OSError:deny(502,"UPSTREAM_INVALID_RESPONSE")
            h=hashlib.sha256();count=0
            with os.fdopen(fd,"rb") as src:
                st=os.fstat(src.fileno())
                if not stat.S_ISREG(st.st_mode) or st.st_uid!=os.geteuid() or st.st_mode&0o077:
                    deny(502,"UPSTREAM_INVALID_RESPONSE")
                while True:
                    part=src.read(256*1024)
                    if not part:break
                    count+=len(part)
                    if count>d["size_bytes"] or count>self.limit:deny(502,"UPSTREAM_INVALID_RESPONSE")
                    h.update(part);f.write(part)
                end=os.fstat(src.fileno())
                if (st.st_size,st.st_mtime_ns,st.st_ctime_ns)!=(end.st_size,end.st_mtime_ns,end.st_ctime_ns):
                    deny(502,"UPSTREAM_INVALID_RESPONSE")
            if count!=d["size_bytes"] or h.hexdigest()!=d["sha256"]:deny(502,"UPSTREAM_INVALID_RESPONSE")
            # Linearization point: a cancellation before this final check denies.
            # An already authorized stream cannot retract transmitted bytes.
            if self.descriptor(scope)!=d:deny(502,"UPSTREAM_INVALID_RESPONSE")
            f.seek(0)
            return f,d
        except BaseException:
            f.close()
            raise

class ProjectSignedArtifactBoundary:
    def __init__(self,*,authority,nonce_registry,key,peer_uid,enabled=False,identity=None):
        if not isinstance(key,bytes) or len(key)<32 or type(peer_uid) is not int or peer_uid<1:
            raise ValueError("INVALID_SERVICE_TRUST")
        self.authority,self.nonce,self.key,self.peer_uid=authority,nonce_registry,key,peer_uid
        self.enabled=enabled is True
        self.identity=dict(IDENTITY if identity is None else identity)
    def _call(self,message,peer_uid,operation):
        def error(status,code):return {"http_status":status,"content_type":"application/json","body":{"error":code}}
        if not self.enabled:return error(404,"NOT_FOUND")
        if peer_uid!=self.peer_uid:return error(403,"FORBIDDEN")
        try:
            if message["auth"]["key_id"]!=KEY_ID:return error(403,"FORBIDDEN")
            scope=verify_signed_read(message,trusted_identity=self.identity,secret=self.key,
                nonce_claim=self.nonce.claim,expected_operation=operation)
            if operation=="artifact.describe":
                return {"http_status":200,"content_type":"application/json","body":self.authority.descriptor(scope)}
            spool,d=self.authority.spool(scope)
            return {"http_status":200,"content_type":"application/octet-stream","body_file":spool,
                "size_bytes":d["size_bytes"],"sha256":d["sha256"]}
        except ArtifactReadDenied as exc:return error(400 if str(exc)=="INVALID_REQUEST" else 403,
                                                      "INVALID_REQUEST" if str(exc)=="INVALID_REQUEST" else "FORBIDDEN")
        except ReadDenied as exc:return error(exc.status,exc.code)
        except (KeyError,TypeError):return error(400,"INVALID_REQUEST")
        except (OSError,sqlite3.Error):return error(503,"BACKEND_UNAVAILABLE")
        except Exception:return error(502,"UPSTREAM_INVALID_RESPONSE")
    def execute(self,message,*,peer_uid):return self._call(message,peer_uid,"artifact.read")
    def describe(self,message,*,peer_uid):return self._call(message,peer_uid,"artifact.describe")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--enable-reviewed-staging-read",action="store_true")
    a=p.parse_args()
    if not a.enable_reviewed_staging_read:
        raise SystemExit("DISABLED: no listener created")
    if os.geteuid()!=1002 or os.getegid()!=984:
        raise SystemExit("EXPECTED_KRCOPS_UID1002_GID984")
    os.umask(0o077)
    # Key is root-provisioned 0440 root:krc-sentinel-ipc. No other service uses it.
    fd=os.open(KEY_PATH,os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC)
    with os.fdopen(fd,"rb") as f:
        st=os.fstat(f.fileno())
        if not stat.S_ISREG(st.st_mode) or (st.st_uid,st.st_gid,stat.S_IMODE(st.st_mode))!=(0,984,0o440):
            raise SystemExit("KEY_CUSTODY_MISMATCH")
        key=f.read(65)
    if len(key)!=32:raise SystemExit("KEY_LENGTH_MISMATCH")
    # systemd creates these two dedicated directories; no private state ACL change.
    st=SOCKET.parent.lstat()
    if (st.st_uid,st.st_gid,stat.S_IMODE(st.st_mode))!=(1002,984,0o750) or not stat.S_ISDIR(st.st_mode):
        raise SystemExit("SOCKET_DIRECTORY_MISMATCH")
    checked(NONCE.parent,directory=True)
    if SOCKET.exists() or SOCKET.is_symlink():raise SystemExit("SOCKET_ALREADY_EXISTS")
    boundary=ProjectSignedArtifactBoundary(authority=ProjectArtifactAuthority(STATE),
        nonce_registry=ArtifactNonceRegistry(NONCE),key=key,peer_uid=987,enabled=True)
    server=SignedArtifactUDSServer(SOCKET,boundary=boundary)
    try:
        os.chmod(SOCKET,0o660)
        server.serve_forever(poll_interval=0.2)
    finally:
        server.server_close()
        SOCKET.unlink(missing_ok=True)

if __name__=="__main__":main()
