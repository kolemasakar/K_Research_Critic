import json
from pathlib import Path
from jsonschema import Draft202012Validator
from krc_research.artifact_exchange import deliver_result

PATH=Path(__file__).resolve().parents[1]/"schemas/stage131/uds_response_transport_v2.schema.json"

def test_actual_uds_response_matches_transport_v2_schema():
    schema=json.loads(PATH.read_text())
    Draft202012Validator.check_schema(schema)
    validator=Draft202012Validator(schema)
    class Exchange:
        def _assert_scope(self,principal,request_id):
            assert principal=="K_Science"
    rid="KS-"+"1"*32
    response=deliver_result({"status":"synthetic"},exchange=Exchange(),principal="K_Science",request_id=rid)
    assert validator.is_valid(response)
    assert validator.is_valid({"status":"rejected","request_id":rid,"error":{"code":"UNAUTHORIZED"}})
    assert validator.is_valid({"status":"pending_reconciliation","request_id":rid,"error":{"code":"AMBIGUOUS_REQUEST"}})
    assert not validator.is_valid({"status":"OK","request_id":rid,"result":{}})
    assert not validator.is_valid({"version":"krc-transport/2","request_id":rid,"status":"completed","delivery":"artifact","artifact":{"artifact_id":"bad","sha256":"bad","size_bytes":1}})
