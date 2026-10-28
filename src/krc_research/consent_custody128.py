"""KRC consent verification: root-owned immutable grant files + separate replay state.

The running KRC service MUST NOT be able to issue or edit grants. Grant
provisioning is an out-of-band, root-authorized operator action.
"""
import hashlib,json,os,sqlite3,stat,time
from pathlib import Path

def fingerprint(context):
    body={k:v for k,v in context.items() if k!="consent_ref"}
    return hashlib.sha256(json.dumps(body,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode()).hexdigest()

class ConsentCustody128:
    def __init__(self,replay_path,*,approvals_dir="/etc/krc-research-v2/approvals"):
        self.dir=Path(approvals_dir)
        st=self.dir.lstat()
        if not stat.S_ISDIR(st.st_mode) or st.st_uid!=0 or st.st_mode & 0o022:
            raise ValueError("UNTRUSTED_APPROVAL_DIRECTORY")
        p=Path(replay_path)
        if not p.is_absolute() or p.is_symlink():
            raise ValueError("UNSAFE_REPLAY_DB")
        s=p.parent.stat()
        if not stat.S_ISDIR(s.st_mode) or s.st_mode & 0o077:
            raise ValueError("UNSAFE_REPLAY_DB")
        self.path=str(p)
        old=os.umask(0o077)
        try:
            with sqlite3.connect(self.path) as db:
                db.execute("CREATE TABLE IF NOT EXISTS consumed (ref TEXT PRIMARY KEY, consumed_at INTEGER NOT NULL)")
            os.chmod(self.path,0o600)
        finally:os.umask(old)

    def __call__(self,context):
        if not isinstance(context,dict):
            return False
        ref=context.get("consent_ref")
        if not isinstance(ref,str) or len(ref)<16 or len(ref)>128 or not ref.isascii() or not all(c.isalnum() or c in "-_" for c in ref):
            return False
        try:
            # Fixed name from validated opaque reference. Never follow symlinks.
            path=self.dir/(ref+".json")
            fd=os.open(str(path),os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC)
            try:
                st=os.fstat(fd)
                if not stat.S_ISREG(st.st_mode) or st.st_uid!=0 or st.st_mode & 0o022 or st.st_size>4096:
                    return False
                raw=os.read(fd,4097)
            finally: os.close(fd)
            grant=json.loads(raw)
            if (not isinstance(grant,dict) or set(grant)!={"consent_ref","context_sha256","approver","approved_at","expires_at"}
                or grant["consent_ref"]!=ref or grant["context_sha256"]!=fingerprint(context)
                or not isinstance(grant["approver"],str) or not grant["approver"].strip()
                or type(grant["approved_at"]) is not int or type(grant["expires_at"]) is not int
                or not grant["approved_at"]<=int(time.time())<grant["expires_at"]):
                return False
            with sqlite3.connect(self.path,timeout=3,isolation_level=None) as db:
                db.execute("BEGIN IMMEDIATE")
                try:
                    db.execute("INSERT INTO consumed(ref,consumed_at) VALUES(?,?)",(ref,int(time.time())))
                    db.execute("COMMIT")
                    return True
                except sqlite3.IntegrityError:
                    db.execute("ROLLBACK")
                    return False
        except (OSError,ValueError,TypeError,KeyError,sqlite3.Error):
            return False
