"""Stage131 isolated backend entrypoint: manual, fail-closed, private config only.

Does not mutate or launch Stage126. This module is source-only until reviewed,
pinned, installed and explicitly started in a disposable isolated environment.
"""
import argparse
import json
import os
import stat
from pathlib import Path
from .staging_service123c import make_staging_server
from .staging_entrypoint124 import secret

class Stage131ConfigurationError(ValueError):
    pass

REQUIRED = {
    "socket_path", "state_root", "peer_uid", "principal", "key_id",
    "transport_key_file", "science_key_file", "client", "repository",
    "workflow_ref", "enable_internal_science_signing",
}
FORBIDDEN_EXISTING = {
    "/run/krc-research-v2/backend.sock",
    "/var/lib/krc-research-v2",
    "/etc/krc-research-v2",
}

def _private_dir(path, uid, *, allow_group_traverse=False):
    p = Path(path)
    if not p.is_absolute() or p.is_symlink():
        raise Stage131ConfigurationError("UNSAFE_DIRECTORY")
    try:
        s = p.lstat()
    except OSError as exc:
        raise Stage131ConfigurationError("UNSAFE_DIRECTORY") from exc
    if not stat.S_ISDIR(s.st_mode) or s.st_uid != uid or s.st_mode & (0o027 if allow_group_traverse else 0o077):
        raise Stage131ConfigurationError("UNSAFE_DIRECTORY")
    return p

def load_stage131_config(path):
    p = Path(path)
    if not p.is_absolute() or p.is_symlink():
        raise Stage131ConfigurationError("UNSAFE_CONFIG")
    st = p.lstat()
    if not stat.S_ISREG(st.st_mode) or st.st_uid != os.geteuid() or st.st_mode & 0o077:
        raise Stage131ConfigurationError("UNSAFE_CONFIG")
    c = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(c, dict) or set(c) != REQUIRED:
        raise Stage131ConfigurationError("INVALID_CONFIG_FIELDS")
    if type(c["enable_internal_science_signing"]) is not bool:
        raise Stage131ConfigurationError("INVALID_SIGNING_FLAG")
    if c["enable_internal_science_signing"]:
        raise Stage131ConfigurationError("SCIENCE_SIGNING_REQUIRES_SEPARATE_REVIEWED_ENTRYPOINT")
    if not all(isinstance(c[k], str) and c[k] for k in (
        "socket_path", "state_root", "principal", "key_id",
        "transport_key_file", "science_key_file", "client", "repository", "workflow_ref"
    )):
        raise Stage131ConfigurationError("INVALID_CONFIG_VALUE")
    try:
        if type(c["peer_uid"]) is not int:
            raise ValueError("Peer UID must be an integer")
        uid = c["peer_uid"]
    except (ValueError, TypeError):
        raise Stage131ConfigurationError("INVALID_PEER_UID") from None
    if uid < 1 or uid == os.geteuid():
        raise Stage131ConfigurationError("INVALID_PEER_UID")
    if c["socket_path"] != "/run/krc-stage131/backend.sock":
        raise Stage131ConfigurationError("ISOLATED_SOCKET_REQUIRED")
    if c["state_root"] != "/var/lib/krc-stage131":
        raise Stage131ConfigurationError("ISOLATED_STATE_REQUIRED")
    if any(c[k].startswith(v) for k in ("socket_path", "state_root") for v in FORBIDDEN_EXISTING):
        raise Stage131ConfigurationError("EXISTING_SERVICE_PATH_DENIED")
    sock = Path(c["socket_path"])
    if sock.exists() or sock.is_symlink():
        raise Stage131ConfigurationError("SOCKET_ALREADY_EXISTS")
    for key in ("transport_key_file", "science_key_file"):
        secret_path = Path(c[key])
        if (not secret_path.is_absolute() or
                secret_path.parent != Path("/etc/krc-stage131") or
                secret_path.name in (".", "..") or
                secret_path.is_symlink()):
            raise Stage131ConfigurationError("ISOLATED_SECRET_PATH_REQUIRED")
    _private_dir(sock.parent, os.geteuid(), allow_group_traverse=True)
    _private_dir(c["state_root"], os.geteuid())
    return c

def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--config", required=True)
    args = p.parse_args(argv)
    c = load_stage131_config(args.config)
    uid = int(c["peer_uid"])
    transport = secret(c["transport_key_file"])
    science = secret(c["science_key_file"])
    server = make_staging_server(
        c["socket_path"], c["state_root"],
        peer_principals={uid: c["principal"]},
        uid_keys={uid: {c["key_id"]: transport}},
        claim_allowlist={(c["client"], c["principal"], c["repository"], c["workflow_ref"])},
        science_secret=science,
        bibliography_fn=None,
        enable_internal_science_signing=False,
    )
    sock = Path(c["socket_path"])
    try:
        os.chmod(sock, 0o660)
        server.serve_forever(poll_interval=0.2)
    finally:
        server.server_close()
        sock.unlink(missing_ok=True)

if __name__ == "__main__":
    main()
