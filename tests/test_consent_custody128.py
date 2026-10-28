import tempfile,unittest,time
from pathlib import Path
from krc_research.consent_custody128 import ConsentCustody128
class ConsentCustodyTests(unittest.TestCase):
 def setUp(self):
  self.t=tempfile.TemporaryDirectory();self.addCleanup(self.t.cleanup)
  self.store=ConsentCustody128(str(Path(self.t.name)/"consent.sqlite"))
  self.ctx=dict(consent_ref="owner-approval-0001",request_id="KS-"+"1"*32,task_id="ks126-"+"2"*32,operation="research.profile.validate",principal="K_Science",profile_ref="P1",evidence_refs=[],payload_sha256="a"*64)
 def approve(self):
  self.store.record_owner_approval(self.ctx,approver="owner-authorized-stage",expires_at=int(time.time())+120)
 def test_deny_without_owner_approval(self):self.assertFalse(self.store(self.ctx))
 def test_approve_then_single_use(self):
  self.approve();self.assertTrue(self.store(self.ctx));self.assertFalse(self.store(self.ctx))
 def test_replay_after_reopen(self):
  self.approve();self.assertTrue(self.store(self.ctx))
  other=ConsentCustody128(self.store.path);self.assertFalse(other(self.ctx))
 def test_changed_request_id(self):
  self.approve();self.assertFalse(self.store(dict(self.ctx,request_id="KS-"+"3"*32)))
 def test_changed_digest(self):
  self.approve();self.assertFalse(self.store(dict(self.ctx,payload_sha256="b"*64)))
 def test_changed_principal(self):
  self.approve();self.assertFalse(self.store(dict(self.ctx,principal="attacker")))
 def test_changed_profile(self):
  self.approve();self.assertFalse(self.store(dict(self.ctx,profile_ref="P2")))
 def test_unknown_receipt(self):
  self.approve();self.assertFalse(self.store(dict(self.ctx,consent_ref="owner-approval-9999")))
if __name__=="__main__":unittest.main()
