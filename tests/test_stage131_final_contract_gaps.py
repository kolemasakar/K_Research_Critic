import json
from pathlib import Path
from jsonschema import Draft202012Validator
schema=json.loads((Path(__file__).resolve().parents[1]/"schemas/stage131/uds_response_observed_bundle_v1.schema.json").read_text())
v=Draft202012Validator(schema)
BASE={"version":"krc-transport/2","request_id":"KS-"+"a"*32,"status":"completed"}
def test_missing_task_id_and_operation_fail_for_science():
    valid={**BASE,"delivery":"inline","result":{"task_id":"sample1","operation":"research.profile.validate","status":"PENDING","engine_result":{},"scientific_approval":False}}
    assert v.is_valid(valid)
    for k in ("task_id","operation","status","engine_result"):
        bad={**valid,"result":{a:b for a,b in valid["result"].items() if a!=k}}
        assert not v.is_valid(bad),k
def test_artifact_lifecycle_mandatory():
    artifact={"artifact_id":"a"*48,"sha256":"b"*64,"size_bytes":42,"filename":"result.json","media_type":"application/json","expires_at_epoch":1800000000}
    valid={**BASE,"delivery":"artifact","artifact":artifact}
    assert v.is_valid(valid)
    for k in ("filename","media_type","expires_at_epoch"):
        assert not v.is_valid({**valid,"artifact":{a:b for a,b in artifact.items() if a!=k}})
