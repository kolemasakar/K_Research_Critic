import json
from pathlib import Path
import pytest
from jsonschema import Draft202012Validator
SCHEMA=json.loads((Path(__file__).resolve().parents[1]/"schemas/stage131/inner_science_success_v1.schema.json").read_text())
V=Draft202012Validator(SCHEMA)
OPS=("research.profile.validate","research.evidence.preflight","research.bibliography.audit","research.inspection.review")
@pytest.mark.parametrize("op",OPS)
def test_four_science_operations_success_shape(op):
    assert V.is_valid({"task_id":"KS-task","operation":op,"status":"PENDING","engine_result":{},"scientific_approval":False})
@pytest.mark.parametrize("key",["task_id","operation","status","engine_result","scientific_approval"])
def test_missing_fields_denied(key):
    x={"task_id":"KS-task","operation":OPS[0],"status":"PENDING","engine_result":{},"scientific_approval":False}
    x.pop(key)
    assert not V.is_valid(x)
def test_invalid_approval_revise_and_unknown_op():
    base={"task_id":"KS-task","operation":OPS[0],"status":"PENDING","engine_result":{},"scientific_approval":False}
    assert not V.is_valid({**base,"scientific_approval":True})
    assert not V.is_valid({**base,"status":"REVISE"})
    assert not V.is_valid({**base,"operation":"unlisted"})
    assert not V.is_valid({**base,"engine_result":[]})
    assert V.is_valid({**base,"operation":OPS[1],"status":"REVISE"})
def test_error_variant_not_claimed_as_observed():
    assert not V.is_valid({"task_id":"KS-task","operation":OPS[0],"status":"ERROR","error":{"code":"X"},"scientific_approval":False})
