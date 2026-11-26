"""Explicit STAGING runtime candidate, never imported by the existing service.

Root must install reviewed immutable source, role-separated relay keys, a
durable relay nonce DB and marker. No automatic migration or state repair.
"""
import argparse
import os
import signal
import stat
import threading
from pathlib import Path
from contextlib import closing
from krc_research.stage132_project_post_relay import RelayClient, RelayAuthority, RelayServer, attach_pilot

CONF=Path("/etc/krc-stage132-post")
MARKER=CONF/"enable-reviewed-staging-post"
STAGE133_MARKER=CONF/"enable-reviewed-stage133-offline"
STAGE134_MARKER=CONF/"enable-reviewed-stage134-bibliography"
RELAY=Path("/run/krc-project-n39-post/backend.sock")
NONCE=Path("/var/lib/krc-project-n39-post/relay.sqlite")
OWNER_STATE=Path("/home/krcops/krc-project-n39-staging/state")
OLD_CONFIG=Path("/etc/krc-research-v2/staging.json")
OLD_SOCKET=Path("/run/krc-research-v2/backend.sock")
OLD_STATE=Path("/var/lib/krc-research-v2")
GID=984

from krc_research.stage132_project_post_wire import DEFAULT_OPS, OFFLINE_OPS, BIBLIOGRAPHY

def reviewed_offline_operations(requested=False, *, stage134_requested=False):
    # Keep the installed Stage133 gate unchanged by default. A separate
    # root-owned 0600 Stage134 marker and explicit CLI flag are required.
    if stage134_requested and not requested:
        raise ValueError("STAGE134_REQUIRES_STAGE133")
    if not requested:
        return DEFAULT_OPS
    st=STAGE133_MARKER.lstat()
    if not stat.S_ISREG(st.st_mode) or (st.st_uid,stat.S_IMODE(st.st_mode),st.st_nlink)!=(0,0o600,1):
        raise ValueError("STAGE133_MARKER_CUSTODY")
    if not stage134_requested:
        return OFFLINE_OPS
    st=STAGE134_MARKER.lstat()
    if not stat.S_ISREG(st.st_mode) or (st.st_uid,stat.S_IMODE(st.st_mode),st.st_nlink)!=(0,0o600,1):
        raise ValueError("STAGE134_MARKER_CUSTODY")
    return OFFLINE_OPS | {BIBLIOGRAPHY}

def marker_check():
    st=CONF.lstat()
    if not stat.S_ISDIR(st.st_mode) or (st.st_uid,st.st_gid,stat.S_IMODE(st.st_mode))!=(0,GID,0o750):
        raise ValueError("RELAY_CONFIG_DIRECTORY")
    st=MARKER.lstat()
    if not stat.S_ISREG(st.st_mode) or (st.st_uid,stat.S_IMODE(st.st_mode),st.st_nlink)!=(0,0o600,1):
        raise ValueError("RELAY_MARKER")

def read_key(path,uid):
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC|os.O_NONBLOCK)
    with os.fdopen(fd,"rb") as f:
        st=os.fstat(f.fileno())
        if not stat.S_ISREG(st.st_mode) or (st.st_uid,st.st_gid,stat.S_IMODE(st.st_mode),st.st_nlink)!=(uid,GID,0o400,1):
            raise ValueError("RELAY_KEY_CUSTODY")
        key=f.read(33)
    if len(key)!=32:raise ValueError("RELAY_KEY_LENGTH")
    return key

def serve(server,path,*,stop,ready=None):
    # Only unlink the socket created by this server instance.
    try:
        os.chmod(path,0o660)
        st=path.lstat()
        if not stat.S_ISSOCK(st.st_mode) or (st.st_uid,st.st_gid,stat.S_IMODE(st.st_mode))!=(os.geteuid(),os.getegid(),0o660):
            raise ValueError("SOCKET_CUSTODY")
        if ready is not None:ready()
        server.timeout=.2
        while not stop.is_set():server.handle_request()
    finally:
        server.server_close()
        if "st" in locals():
            try:
                current=path.lstat()
                if (current.st_dev,current.st_ino)==(st.st_dev,st.st_ino):path.unlink()
            except FileNotFoundError:pass

def compose_gateway(c,*,transport,science,relay):
    # Run this with the exact pre-existing legacy gateway source first in the
    # package resolution path excluding the new Stage132-only overlay.
    from krc_research.staging_service123c import make_staging_server
    uid=int(c["peer_uid"])
    claims={(c["client"],c["principal"],c["repository"],c["workflow_ref"])}
    server=make_staging_server(c["socket_path"],c["state_root"],
        peer_principals={uid:c["principal"]},uid_keys={uid:{c["key_id"]:transport}},
        claim_allowlist=claims,science_secret=science)
    return attach_pilot(server,relay)

def gateway(stop, *, enabled_operations=DEFAULT_OPS):
    from krc_research.staging_entrypoint124 import load_config,secret
    if (os.geteuid(),os.getegid())!=(988,GID):raise ValueError("GATEWAY_UID_GID")
    marker_check()
    c=load_config(OLD_CONFIG)
    if (c["socket_path"],c["state_root"],c["peer_uid"],c["principal"],c["client"],c["repository"],c["workflow_ref"],c["key_id"])!=(str(OLD_SOCKET),str(OLD_STATE),987,"K_Science","K_Science","kolemasakar/K_Science","refs/heads/main","stage126-v1"):
        raise ValueError("LEGACY_CONFIG_PARITY")
    if os.path.lexists(OLD_SOCKET):raise ValueError("OLD_SOCKET_ALREADY_EXISTS")
    key=read_key(CONF/"gateway.key",988)
    transport=secret(c["transport_key_file"])
    science=secret(c["science_key_file"])
    if key==transport or key==science:raise ValueError("KEY_SEPARATION")
    relay=RelayClient(RELAY,key=key,expected_uid=1002,expected_gid=GID,enabled_operations=enabled_operations,
                      enable_stage134=(BIBLIOGRAPHY in enabled_operations))
    serve(compose_gateway(c,transport=transport,science=science,relay=relay),OLD_SOCKET,stop=stop)

def broker(stop, *, enabled_operations=DEFAULT_OPS):
    from krc_research.stage132_project_post_contract import ProjectPostBoundary
    from krc_research.stage131_project_read_lifecycle import existing_nonce,producer_preflight,notify_ready,retrieval_key
    from krc_research.stage131_project_signed_read import ro,KEY_PATH
    if (os.geteuid(),os.getegid())!=(1002,GID):raise ValueError("BROKER_UID_GID")
    marker_check()
    st=RELAY.parent.lstat()
    if not stat.S_ISDIR(st.st_mode) or (st.st_uid,st.st_gid,stat.S_IMODE(st.st_mode))!=(1002,GID,0o750):
        raise ValueError("RELAY_RUNTIME_DIRECTORY")
    key=read_key(CONF/"broker.key",1002)
    if key==retrieval_key(KEY_PATH):raise ValueError("KEY_SEPARATION")
    producer_preflight(OWNER_STATE)
    for name,table in (("consent.sqlite","project_profiles"),("science-replay.sqlite","requests")):
        with closing(ro(OWNER_STATE/name)) as db:db.execute("SELECT * FROM "+table+" LIMIT 0")
    registry=existing_nonce(NONCE)
    boundary=ProjectPostBoundary(OWNER_STATE,enabled=True,enabled_operations=enabled_operations,
                                 enable_stage134=(BIBLIOGRAPHY in enabled_operations))
    authority=RelayAuthority(boundary=boundary,registry=registry,key=key,peer_uid=988,peer_gid=GID)
    server=RelayServer(RELAY,authority=authority)
    if not os.environ.get("NOTIFY_SOCKET"):
        server.server_close();RELAY.unlink(missing_ok=True);raise ValueError("NOTIFY_SOCKET_REQUIRED")
    serve(server,RELAY,stop=stop,ready=lambda:notify_ready(os.environ["NOTIFY_SOCKET"]))

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("role",choices=("broker","gateway"))
    parser.add_argument("--enable-reviewed-staging-post",action="store_true")
    parser.add_argument("--enable-stage133-offline-operations",action="store_true")
    parser.add_argument("--enable-stage134-bibliography",action="store_true")
    a=parser.parse_args()
    if not a.enable_reviewed_staging_post:raise SystemExit("DISABLED")
    os.umask(0o077)
    stop=threading.Event()
    signal.signal(signal.SIGTERM,lambda *_:stop.set())
    signal.signal(signal.SIGINT,lambda *_:stop.set())
    (broker if a.role=="broker" else gateway)(
        stop,enabled_operations=reviewed_offline_operations(
            a.enable_stage133_offline_operations,
            stage134_requested=a.enable_stage134_bibliography))

if __name__=="__main__":main()
