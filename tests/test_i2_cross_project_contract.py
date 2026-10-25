import sys, pathlib, unittest
from datetime import datetime, timezone, timedelta
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/"src"))
from krc_research.cross_project_contract import sign_request,verify_request,not_ready_gate

KEY=b"synthetic-contract-test-only-not-a-real-secret-key!"
NOW=datetime(2026,10,25,11,0,tzinfo=timezone.utc)
ID="KS-"+"a"*32

def fixture(operation="krc_scholarly_preflight",payload=None):
    return sign_request(operation=operation,payload=payload or {"claims":[]},
      request_id=ID,issued_at=NOW.isoformat(),signing_key=KEY)

class ContractChecks(unittest.TestCase):
    def test_valid_scoped_request(self):
        e=fixture()
        v=verify_request(e,signing_key=KEY,now=NOW,seen_ids=set())
        self.assertTrue(v["authorized"])
        self.assertEqual(v["caller"],"K_Science")
    def test_tampered_payload(self):
        e=fixture()
        e["payload"]["claims"].append({"forged":True})
        with self.assertRaises(ValueError): verify_request(e,signing_key=KEY,now=NOW,seen_ids=set())
    def test_replay_fails(self):
        e=fixture();seen=set()
        verify_request(e,signing_key=KEY,now=NOW,seen_ids=seen)
        with self.assertRaisesRegex(ValueError,"Replay"): verify_request(e,signing_key=KEY,now=NOW,seen_ids=seen)
    def test_wrong_project_fails(self):
        e=fixture();e["caller"]="K_Tr ader"
        with self.assertRaises(ValueError): verify_request(e,signing_key=KEY,now=NOW,seen_ids=set())
    def test_wrong_key_fails(self):
        with self.assertRaises(ValueError): verify_request(fixture(),signing_key=b"b"*40,now=NOW,seen_ids=set())
    def test_future_timestamp_fails(self):
        with self.assertRaises(ValueError): verify_request(fixture(),signing_key=KEY,now=NOW-timedelta(seconds=301),seen_ids=set())
    def test_unknown_operation_fails(self):
        with self.assertRaises(ValueError): fixture(operation="krc_admin")
    def test_unsupported_expansion_fails(self):
        with self.assertRaises(ValueError): fixture(operation="research_start")
    def test_gate_not_silently_active(self):
        self.assertFalse(not_ready_gate()["cross_project_live_calls_enabled"])
    def test_max_body(self):
        with self.assertRaises(ValueError):fixture(payload={"s":"x"*300000})

if __name__=="__main__":unittest.main()
