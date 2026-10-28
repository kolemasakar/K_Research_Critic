"""Stage131 draft response schema: deterministic offline tests."""
import json
from pathlib import Path
from jsonschema import Draft202012Validator

SCHEMA=Path(__file__).resolve().parents[1]/"schemas/stage131/science_response_v1.schema.json"
RID="KS-"+"1"*32

def test_schema_and_denial():
    schema=json.loads(SCHEMA.read_text())
    Draft202012Validator.check_schema(schema)
    v=Draft202012Validator(schema)
    assert v.is_valid({"request_id":RID,"status":"ERROR","error_code":"CONSENT_REQUIRED","scientific_approval":False})
    assert not v.is_valid({"request_id":RID,"status":"ERROR","error_code":"CONSENT_REQUIRED","scientific_approval":True})
    assert not v.is_valid({"request_id":RID,"status":"ERROR","error_code":"UNKNOWN","scientific_approval":False})
    assert not v.is_valid({"request_id":RID,"status":"ERROR","error_code":"INVALID_REQUEST","scientific_approval":False,"raw_jwt":"secret"})

def test_success_requires_scientific_flag():
    v=Draft202012Validator(json.loads(SCHEMA.read_text()))
    good={"request_id":RID,"status":"OK","operation":"research.profile.validate","result":{},"scientific_approval":False}
    assert v.is_valid(good)
    assert not v.is_valid({k:value for k,value in good.items() if k!="scientific_approval"})
