import unittest
from krc_research.science_signer127 import KRCInternalScienceSigner,ScienceAuthorizationDenied

class SignerTests(unittest.TestCase):
    def setUp(self):
        self.context=[]
        self.dispatch=[]
        self.signer=KRCInternalScienceSigner(science_key=b"K"*32,
            authorizer=lambda c:self.context.append(c) or c["consent_ref"]=="approved",
            dispatcher=lambda op,p,principal:self.dispatch.append((op,p,principal)) or {"status":"synthetic"})
        self.req=dict(request_id="KS-"+"1"*32,task_id="ks126-"+"2"*32,
          operation="research.profile.validate",
          payload={"critic_profile":{"profile_id":"p","version":"1","protocol":"core","topic":"test"}},
          principal="K_Science",profile_ref="p",evidence_refs=[],consent_ref="approved")
    def test_internal_signature_binds_context(self):
        self.assertEqual(self.signer.execute(**self.req)["status"],"synthetic")
        self.assertEqual(self.context[0]["task_id"],self.req["task_id"])
        self.assertEqual(self.context[0]["request_id"],self.req["request_id"])
        self.assertEqual(self.context[0]["profile_ref"],"p")
        self.assertIn("science_signature",self.dispatch[0][1])
    def test_unapproved_ref_denied(self):
        req=dict(self.req,consent_ref="unapproved")
        with self.assertRaises(ScienceAuthorizationDenied):self.signer.execute(**req)
        self.assertEqual(self.dispatch,[])
    def test_bad_payload_denied(self):
        req=dict(self.req,payload={})
        with self.assertRaises(ScienceAuthorizationDenied):self.signer.execute(**req)
        self.assertEqual(self.context,[])
    def test_bibliography_denied_by_default(self):
        req=dict(self.req,operation="research.bibliography.audit",payload={"dois":["10.1/example"]})
        with self.assertRaises(ScienceAuthorizationDenied):self.signer.execute(**req)
        self.assertEqual(self.context,[])
    def test_missing_authorizer_denied(self):
        with self.assertRaises(ScienceAuthorizationDenied):
            KRCInternalScienceSigner(science_key=b"K"*32,authorizer=None,dispatcher=lambda *_:None)
if __name__=="__main__": unittest.main()
