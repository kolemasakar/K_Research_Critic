from krc_research.private_contract_schemas import contracts,approval_receipt_status
def test_four_contracts():
 c=contracts()
 assert len(c["operations"])==4 and not c["deployed"]
def test_output_fail_closed():
 for op in contracts()["operations"].values():
  assert op["outputSchema"]["properties"]["scientific_approval"]["const"] is False
def test_error_codes():
 assert "REPLAY_REJECTED" in contracts()["errorSchema"]["properties"]["error"]["properties"]["code"]["enum"]
def test_no_receipt():
 assert approval_receipt_status(None,{})=="MISSING_OR_INVALID"
def test_receipt_missing():
 assert approval_receipt_status({"profile_id":"p"},{"profile_id":"p"})=="INCOMPLETE"
def test_receipt_wrong_profile():
 p={"profile_id":"p","version":"1"}
 r={"profile_id":"different","profile_version":"1","approved_at":"2026-10-25T12:00:00Z","author_id":"a","trace_id":"t"}
 assert approval_receipt_status(r,p)=="PROFILE_MISMATCH"
def test_receipt_not_verified_by_shape():
 p={"profile_id":"p","version":"1"}
 r={"profile_id":"p","profile_version":"1","approved_at":"2026-10-25T12:00:00Z","author_id":"a","trace_id":"t"}
 assert approval_receipt_status(r,p)=="PRESENT_UNVERIFIED"
