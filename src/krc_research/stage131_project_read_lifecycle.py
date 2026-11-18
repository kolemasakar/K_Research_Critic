"""Continuous STAGING read lifecycle candidate; no scientific execution.

Distinct from the installed temporary lease. Only an explicitly installed
systemd unit with a root-owned permanent marker can invoke this entrypoint.
No network listener, writes to producer DB, identity change or POST dependency.
"""
import argparse
import os
import signal
import socket
import stat
import threading
from contextlib import closing
from pathlib import Path

from .stage131_project_signed_read import (
    STATE, SOCKET, NONCE, KEY_PATH, ProjectArtifactAuthority,
    ProjectSignedArtifactBoundary, checked, ro,
)
from .stage131_artifact_nonce_registry import ArtifactNonceRegistry
from .stage131_signed_artifact_uds import SignedArtifactUDSServer

MARKER=Path("/etc/krc-project-n39-read/enable-reviewed-continuous")
TABLES={
    "consent.sqlite": ("approvals", "artifacts"),
    "requests.sqlite": ("requests",),
    "artifacts/index.sqlite3": ("objects",),
}

def notify_ready(address):
    """systemd readiness only, not a health/authentication bypass."""
    if not isinstance(address,str) or not address or address[0] not in ("/","@"):
        raise ValueError("NOTIFY_SOCKET_REQUIRED")
    target="\0"+address[1:] if address.startswith("@") else address
    with socket.socket(socket.AF_UNIX,socket.SOCK_DGRAM) as s:
        s.settimeout(2)
        s.connect(target)
        s.sendall(b"READY=1\nSTATUS=Scoped signed artifact reader listening")

def marker_check(path):
    st=Path(path).lstat()
    if (not stat.S_ISREG(st.st_mode) or st.st_uid!=0 or
        stat.S_IMODE(st.st_mode)!=0o600 or st.st_nlink!=1):
        raise ValueError("CONTINUOUS_RELEASE_MARKER_DENIED")

def producer_preflight(root):
    """Check actual schema access before READY; bounded DB lock waits, no writes."""
    authority=ProjectArtifactAuthority(root)
    for name,tables in TABLES.items():
        with closing(ro(Path(root)/name)) as db:
            for table in tables:
                db.execute(f"SELECT * FROM {table} LIMIT 0").fetchall()
    return authority

def existing_nonce(path):
    """A restart must reuse the original registry, never create a missing one."""
    p=Path(path)
    checked(p.parent,directory=True)
    st=checked(p)
    if stat.S_IMODE(st.st_mode)!=0o600 or st.st_nlink!=1:
        raise ValueError("NONCE_CUSTODY_MISMATCH")
    with closing(ro(p)) as db:
        cols=db.execute("PRAGMA table_info(used)").fetchall()
        if [(r[1],r[5]) for r in cols]!=[
                ("key_id",1),("nonce",2),("principal",3),("created",0)]:
            raise ValueError("NONCE_SCHEMA_MISMATCH")
    return ArtifactNonceRegistry(p)

def retrieval_key(path):
    p=Path(path);parent=p.parent.lstat()
    if (not stat.S_ISDIR(parent.st_mode) or
        (parent.st_uid,parent.st_gid,stat.S_IMODE(parent.st_mode))!=(0,984,0o750)):
        raise ValueError("KEY_DIRECTORY_MISMATCH")
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC|os.O_NONBLOCK)
    with os.fdopen(fd,"rb") as f:
        st=os.fstat(f.fileno())
        if (not stat.S_ISREG(st.st_mode) or st.st_nlink!=1 or
            (st.st_uid,st.st_gid,stat.S_IMODE(st.st_mode))!=(0,984,0o440)):
            raise ValueError("KEY_CUSTODY_MISMATCH")
        key=f.read(33)
    if len(key)!=32:raise ValueError("KEY_LENGTH_MISMATCH")
    return key

def run_reader(path,boundary,*,ready,stop):
    """Bind, set verified socket custody, notify, and serve until stop.

    The runtime directory must be private to its designated service/group.
    Never unlink a preexisting socket (including stale/foreign paths).
    systemd owns runtime directory removal between service invocations.
    """
    path=Path(path)
    if path.exists() or path.is_symlink():raise ValueError("SOCKET_ALREADY_EXISTS")
    server=SignedArtifactUDSServer(path,boundary=boundary)
    try:
        os.chmod(path,0o660)
        st=path.lstat()
        if (not stat.S_ISSOCK(st.st_mode) or
            (st.st_uid,st.st_gid,stat.S_IMODE(st.st_mode))!=(os.geteuid(),os.getegid(),0o660)):
            raise ValueError("SOCKET_CUSTODY_MISMATCH")
        if stop.is_set():return
        ready()
        server.timeout=.2
        while not stop.is_set():
            server.handle_request()
    finally:
        server.server_close()
        path.unlink(missing_ok=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--enable-reviewed-continuous",action="store_true")
    a=p.parse_args()
    if not a.enable_reviewed_continuous:raise SystemExit("DISABLED")
    if (os.geteuid(),os.getegid())!=(1002,984):raise SystemExit("EXPECTED_UID_GID")
    os.umask(0o077)
    marker_check(MARKER)
    address=os.environ.get("NOTIFY_SOCKET")
    if not address or address[0] not in ("/","@"):
        raise SystemExit("NOTIFY_SOCKET_REQUIRED")
    st=SOCKET.parent.lstat()
    if (not stat.S_ISDIR(st.st_mode) or
        (st.st_uid,st.st_gid,stat.S_IMODE(st.st_mode))!=(1002,984,0o750)):
        raise SystemExit("SOCKET_DIRECTORY_MISMATCH")
    key=retrieval_key(KEY_PATH)
    authority=producer_preflight(STATE)
    registry=existing_nonce(NONCE)
    boundary=ProjectSignedArtifactBoundary(authority=authority,
        nonce_registry=registry,key=key,peer_uid=987,enabled=True)
    stop=threading.Event()
    def terminate(*_):stop.set()
    signal.signal(signal.SIGTERM,terminate)
    signal.signal(signal.SIGINT,terminate)
    run_reader(SOCKET,boundary,ready=lambda:notify_ready(address),stop=stop)

if __name__=="__main__":main()
