"""Synthetic owner-grant fixtures: mock root ownership solely in these tests."""
import json,os,tempfile,time,unittest
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch
from krc_research.consent_custody128 import ConsentCustody128,fingerprint

_REAL_LSTAT=Path.lstat
_REAL_FSTAT=os.fstat

def root_dir_stat(path):
    st=_REAL_LSTAT(path)
    if str(path).endswith("approvals"):return os.stat_result((st.st_mode,st.st_ino,st.st_dev,st.st_nlink,0,st.st_gid,st.st_size,st.st_atime,st.st_mtime,st.st_ctime))
    return st
def root_file_stat(fd):
    st=_REAL_FSTAT(fd)
    return os.stat_result((st.st_mode,st.st_ino,st.st_dev,st.st_nlink,0,st.st_gid,st.st_size,st.st_atime,st.st_mtime,st.st_ctime))

class ConsentCustodyTests(unittest.TestCase):
 def setUp(self):
  self.t=tempfile.TemporaryDirectory();self.addCleanup(self.t.cleanup)
  self.root=Path(self.t.name);self.d=self.root/"approvals";self.d.mkdir()
  self.ctx=dict(consent_ref="owner-approval-0001",request_id="KS-"+"1"*32,task_id="ks126-"+"2"*32,operation="research.profile.validate",principal="K_Science",profile_ref="P1",evidence_refs=[],payload_sha256="a"*64)
  self.p1=patch.object(Path,"lstat",root_dir_stat);self.p2=patch("os.fstat",root_file_stat)
  self.p1.start();self.p2.start();self.addCleanup(self.p1.stop);self.addCleanup(self.p2.stop)
  self.store=ConsentCustody128(str(self.root/"replay.sqlite"),approvals_dir=str(self.d))
 def grant(self,ctx=None,expires=None):
  c=ctx or self.ctx
  p=self.d/(c["consent_ref"]+".json")
  p.write_text(json.dumps(dict(consent_ref=c["consent_ref"],context_sha256=fingerprint(c),approver="SYNTHETIC_OWNER_FIXTURE",approved_at=int(time.time())-1,expires_at=expires or int(time.time())+120)))
  p.chmod(0o644)
 def test_no_grant(self):self.assertFalse(self.store(self.ctx))
 def test_positive_then_replay(self):
  self.grant();self.assertTrue(self.store(self.ctx));self.assertFalse(self.store(self.ctx))
 def test_replay_after_restart(self):
  self.grant();self.assertTrue(self.store(self.ctx))
  other=ConsentCustody128(self.store.path,approvals_dir=str(self.d));self.assertFalse(other(self.ctx))
 def test_wrong_request(self):
  self.grant();self.assertFalse(self.store(dict(self.ctx,request_id="KS-"+"3"*32)))
 def test_wrong_digest(self):
  self.grant();self.assertFalse(self.store(dict(self.ctx,payload_sha256="b"*64)))
 def test_wrong_principal(self):
  self.grant();self.assertFalse(self.store(dict(self.ctx,principal="attacker")))
 def test_wrong_profile(self):
  self.grant();self.assertFalse(self.store(dict(self.ctx,profile_ref="P2")))
 def test_expired(self):
  self.grant(expires=int(time.time())-1);self.assertFalse(self.store(self.ctx))
 def test_symlink_grant(self):
  self.grant();p=self.d/(self.ctx["consent_ref"]+".json")
  p2=self.d/"other.json";p.rename(p2);p.symlink_to(p2)
  self.assertFalse(self.store(self.ctx))
 def test_writable_grant(self):
  self.grant();(self.d/(self.ctx["consent_ref"]+".json")).chmod(0o666);self.assertFalse(self.store(self.ctx))
 def test_wrong_ref(self):
  self.grant();self.assertFalse(self.store(dict(self.ctx,consent_ref="../evil")))
if __name__=="__main__":unittest.main()
