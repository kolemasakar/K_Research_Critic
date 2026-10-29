"""Read-only Stage131 installation prerequisites. Never reads secret contents."""
import argparse
import json
import os
import stat
from pathlib import Path

PATHS = ("/etc/krc-stage131", "/var/lib/krc-stage131", "/run/krc-stage131")
FILES = ("/etc/krc-stage131/staging.json", "/etc/krc-stage131/transport.key",
         "/etc/krc-stage131/science.key")

def inspect_path(path, uid, *, directory, expected_mode):
    p=Path(path)
    try:
        meta=p.lstat()
    except (FileNotFoundError,PermissionError):
        return {"path":path,"status":"NOT_READY"}
    kind=stat.S_ISDIR(meta.st_mode) if directory else stat.S_ISREG(meta.st_mode)
    mode=stat.S_IMODE(meta.st_mode)
    ok=kind and meta.st_uid==uid and mode==expected_mode
    return {"path":path,"status":"PASS" if ok else "DENIED",
            "uid":meta.st_uid,"mode":oct(mode)}

def audit(uid):
    return {"schema":"KRC-STAGE131-PREINSTALL-AUDIT-1",
      "read_only":True,
      "checks":[
        inspect_path(PATHS[0],uid,directory=True,expected_mode=0o700),
        inspect_path(PATHS[1],uid,directory=True,expected_mode=0o700),
        inspect_path(PATHS[2],uid,directory=True,expected_mode=0o750),
        *(inspect_path(p,uid,directory=False,expected_mode=0o600) for p in FILES)
      ]}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--service-uid",type=int,required=True)
    args=p.parse_args()
    if args.service_uid<1:p.error("service uid must be unprivileged")
    result=audit(args.service_uid)
    print(json.dumps(result,sort_keys=True))
    return 0 if all(r["status"]=="PASS" for r in result["checks"]) else 2

if __name__=="__main__":
    raise SystemExit(main())
