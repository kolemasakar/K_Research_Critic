import json
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]
SCHEMA=json.loads((ROOT/"schemas/stage131/uds_response_observed_bundle_v1.schema.json").read_text())
def test_schema_itself_valid(): Draft202012Validator.check_schema(SCHEMA)
def test_all_observed_response_shapes():
    cases=[
      {"version":"krc-transport/2","request_id":"KS-"+"a"*32,"status":"completed","delivery":"inline","result":{}},
      {"version":"krc-transport/2","request_id":"KS-"+"a"*32,"status":"completed","delivery":"artifact","artifact":{"artifact_id":"a"*48,"sha256":"b"*64,"size_bytes":4}},
      {"status":"rejected","error":{"code":"OPERATION_DENIED"}},
      {"status":"pending_reconciliation","error":{"code":"AMBIGUOUS"},"request_id":"KS-"+"b"*32},
      {"error":"OPERATION_DENIED"},
      {"error":"INVALID_REQUEST"},
      {"status":"error","error":{"code":"RESPONSE_TOO_LARGE"}},
    ]
    for case in cases: Draft202012Validator(SCHEMA).validate(case)
def test_bad_shapes_rejected():
    invalid=[
      {"version":"krc-transport/2","status":"completed","delivery":"inline","result":{}},
      {"version":"krc-transport/2","request_id":"test","status":"completed","delivery":"artifact","artifact":{"artifact_id":"bad","sha256":"b"*64,"size_bytes":4}},
      {"status":"error","error":{"code":"WRONG"}},
      {"error":1},
    ]
    for case in invalid: assert not Draft202012Validator(SCHEMA).is_valid(case)
