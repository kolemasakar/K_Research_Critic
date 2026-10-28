"""Offline staging-only launch entrypoint. Requires protected configuration and explicit operator start."""
import argparse,json,os,stat
from pathlib import Path
from .staging_service123c import make_staging_server

def load_config(path):
    p=Path(path)
    st=p.lstat()
    if not stat.S_ISREG(st.st_mode) or (st.st_mode & 0o077):
        raise ValueError("Config must be a private regular file mode 0600")
    if st.st_uid!=os.geteuid():
        raise ValueError("Config owner must match service uid")
    config=json.loads(p.read_text(encoding="utf-8"))
    required={"socket_path","state_root","peer_uid","principal","key_id","transport_key_file","science_key_file","client","repository","workflow_ref"}
    if set(config)!=required:raise ValueError("Config field mismatch")
    return config

def secret(path):
    p=Path(path)
    s=p.lstat()
    if not stat.S_ISREG(s.st_mode) or (s.st_mode & 0o077) or s.st_uid!=os.geteuid():
        raise ValueError("Secret must be private, owned, regular file")
    key=p.read_bytes()
    if len(key)<32:raise ValueError("Weak key")
    return key

def main(argv=None):
    parser=argparse.ArgumentParser()
    parser.add_argument("--config",required=True)
    args=parser.parse_args(argv)
    c=load_config(args.config)
    uid=int(c["peer_uid"])
    if uid<1 or uid==os.geteuid():
        raise ValueError("Peer must be a distinct unprivileged UID")
    sock=Path(c["socket_path"])
    if sock.exists() or sock.is_symlink():raise ValueError("Socket already exists")
    transport=secret(c["transport_key_file"])
    science=secret(c["science_key_file"])
    claims={(c["client"],c["principal"],c["repository"],c["workflow_ref"])}
    server=make_staging_server(sock,c["state_root"],peer_principals={uid:c["principal"]},
        uid_keys={uid:{c["key_id"]:transport}},claim_allowlist=claims,science_secret=science)
    try:
        os.chmod(sock,0o660)
        server.serve_forever(poll_interval=0.2)
    finally:
        server.server_close()
        sock.unlink(missing_ok=True)

if __name__=="__main__":main()
