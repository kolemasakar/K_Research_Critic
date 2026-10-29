import json
from pathlib import Path
from jsonschema import Draft202012Validator
BASE=Path(__file__).resolve().parents[1]/"schemas/stage131"
def validate(name,obj):
    schema=json.loads((BASE/name).read_text())
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema).is_valid(obj)
def test_signed_uds_accept_and_reject():
    msg={"version":"krc-transport/2","request_id":"KS-"+"a"*32,"operation":"research.profile.validate","identity":{"client":"K_Sentinel","principal":"K_Science","repository":"kolemasakar/K_Science","workflow_ref":"staging-disabled"},"payload":{},"transport_auth":{"alg":"HMAC-SHA256","key_id":"stage131-local-v1","issued_at":"2026-10-29T00:00:00Z","mac":"a"*64}}
    assert validate("uds_signed_request_observed_v1.schema.json",msg)
    for field in ["transport_auth","identity","version"]:
        broken=dict(msg);broken.pop(field)
        assert not validate("uds_signed_request_observed_v1.schema.json",broken)
    assert not validate("uds_signed_request_observed_v1.schema.json",{**msg,"transport_auth":{**msg["transport_auth"],"mac":"bad"}})
def test_external_minimal_not_internal():
    msg={"request_id":"KS-"+"b"*32,"operation":"research.profile.validate","payload":{}}
    assert validate("sentinel_external_request_candidate_v1.schema.json",msg)
    assert not validate("sentinel_external_request_candidate_v1.schema.json",{**msg,"transport_auth":{"mac":"x"}})
    assert not validate("sentinel_external_request_candidate_v1.schema.json",{**msg,"request_id":"bad"})
