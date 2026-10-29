import json
from pathlib import Path
from jsonschema import Draft202012Validator
p=Path(__file__).resolve().parents[1]/"schemas/stage131/uds_response_observed_bundle_v1.schema.json"
s=json.loads(p.read_text())
v=Draft202012Validator(s)
def test_health_is_in_uds_bundle():
    assert v.is_valid({"status":"staging","production":False})
    assert not v.is_valid({"status":"staging","production":True})
def test_inline_explicit_scientific_approval_false_only():
    base={"version":"krc-transport/2","request_id":"KS-"+"1"*32,"status":"completed","delivery":"inline"}
    assert v.is_valid({**base,"result":{"task_id":"case","scientific_approval":False}})
    assert not v.is_valid({**base,"result":{"task_id":"case","scientific_approval":True}})
    assert not v.is_valid({**base,"result":{"engine_result":{"scientific_approval":True}}})
    assert v.is_valid({**base,"result":{"engine_result":{"scientific_approval":False}}})
