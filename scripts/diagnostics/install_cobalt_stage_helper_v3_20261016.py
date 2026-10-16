#!/usr/bin/env python3
import hashlib,os,pathlib,tempfile,time
source=pathlib.Path("/tmp/krc-cobalt-instagram-stage-v3.js")
target=pathlib.Path("/usr/local/libexec/krc-cobalt-instagram-stage.js")
if os.geteuid()!=0: raise SystemExit("Administrator identity required")
fd=os.open(source,os.O_RDONLY|os.O_NOFOLLOW)
with os.fdopen(fd,"rb") as f: data=f.read(100001)
if len(data)>100000 or hashlib.sha256(data).hexdigest()!="306c49816b384385c38b3d54fcbd8741f5f19bd1a65088fb9f7ec3953477193b":
    raise SystemExit("Candidate hash mismatch; no changes")
if target.is_symlink() or target.stat().st_uid!=0:
    raise SystemExit("Unexpected target ownership; no changes")
backup=target.with_name(target.name+".backup-"+str(time.time_ns()))
backup.write_bytes(target.read_bytes())
os.chmod(backup,0o600)
fd,tmp=tempfile.mkstemp(prefix=".krc-stage-",dir=target.parent)
try:
    with os.fdopen(fd,"wb") as f: f.write(data)
    os.chown(tmp,0,0)
    os.chmod(tmp,0o644)
    os.replace(tmp,target)
finally:
    if os.path.exists(tmp): os.unlink(tmp)
print("KRC_STAGE_HELPER_V3_INSTALLED=PASS")
print("PRODUCTION_CONTAINER_CHANGED=NO")
