#!/usr/bin/env python3
"""KRC local infrastructure inspection. Run as root. Prints sanitized JSON; no content or secrets."""
import json, os, pathlib, pwd, grp, sqlite3, subprocess, tempfile, urllib.request
from urllib.error import URLError
def run(*args):
    try:
        x=subprocess.run(args,text=True,capture_output=True,timeout=12,check=False)
        return {"exit":x.returncode,"text":x.stdout.strip()[:500]}
    except Exception as e: return {"error":type(e).__name__}
out={"scope":"krc-cobalt","mode":"read-only","checks":{}}
c=out["checks"]
c["service"]=run("systemctl","show","krc-public-mcp.service","-p","ActiveState","-p","User","-p","Group","-p","MemoryMax","-p","CPUQuotaPerSecUSec","-p","TasksMax","-p","NRestarts","-p","MemoryPeak")
c["docker"]=run("systemctl","is-active","docker")
c["caddy"]=run("systemctl","is-active","caddy")
c["cobalt"]=run("/usr/local/sbin/krc-tier1-media-status")
p=pathlib.Path("/var/lib/krc-public-mcp")
d=p/"queue.sqlite3"
for k,path in (("app",pathlib.Path("/opt/krc-public-mcp")),("state",p),("database",d)):
    try:
        s=path.stat()
        c[k]={"exists":True,"uid":s.st_uid,"gid":s.st_gid,"mode":oct(s.st_mode & 0o777)}
    except OSError: c[k]={"exists":False}
if d.exists():
    try:
        # sqlite3 online backup from a read-only source to a separate snapshot;
        # never checkpoint or modify live data intentionally.
        with tempfile.TemporaryDirectory(prefix="krc-audit-") as tmp:
            src=sqlite3.connect(f"file:{d}?mode=ro",uri=True,timeout=3)
            dst=sqlite3.connect(str(pathlib.Path(tmp)/"snapshot.db"))
            source_journal_mode=src.execute("PRAGMA journal_mode").fetchone()[0]
            src.backup(dst,pages=100)
            dst.close()
            src.close()
            ck=sqlite3.connect(str(pathlib.Path(tmp)/"snapshot.db"))
            c["sqlite"]={"integrity":ck.execute("PRAGMA integrity_check").fetchone()[0],"source_journal_mode":source_journal_mode,"wal_file_present":pathlib.Path(str(d)+"-wal").exists(),"snapshot_only":True}
            ck.close()
    except Exception as e:
        c["sqlite"]={"status":"PARTIAL","error_type":type(e).__name__}
else:
    c["sqlite"]={"status":"FAIL","reason":"database_missing"}
try:
    v=os.statvfs(str(p))
    c["disk"]={"free_percent":round(100*v.f_bavail/v.f_blocks,2)}
except OSError: c["disk"]={"status":"UNKNOWN"}
try:
    u=urllib.request.Request("http://127.0.0.1:9000/",method="GET")
    with urllib.request.urlopen(u,timeout=3) as f:
        c["cobalt_http"]=f.status
except Exception as e: c["cobalt_http"]={"error_type":type(e).__name__}
# Journals: counts only, no raw journal lines containing possible guest content.
for svc in ("krc-public-mcp.service","caddy.service","docker.service"):
    q=run("journalctl","-u",svc,"--since=-1 hour","-p","err","--no-pager","-q","-o","cat")
    c["journal_errors_"+svc]={"exit":q.get("exit"),"count":len([v for v in q.get("text","").splitlines() if v.strip()])}
# Active Caddy config: count upstreams; never output config/secrets.
try:
    with urllib.request.urlopen("http://127.0.0.1:2019/config/apps/http/servers",timeout=3) as f:
        raw=f.read(1024*1024)
    cfg=json.loads(raw)
    serialized=json.dumps(cfg)
    c["active_caddy"]={"admin_api":True,"contains_9013":("127.0.0.1:9013" in serialized),"contains_9000":("127.0.0.1:9000" in serialized)}
except Exception as e:
    c["active_caddy"]={"admin_api":False,"error_type":type(e).__name__}
print(json.dumps(out,ensure_ascii=False,indent=2))
