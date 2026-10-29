import json
from pathlib import Path
from jsonschema import Draft202012Validator
from krc_research.uds_stage123 import Stage123Handler

def test_healthz_schema_matches_actual_handler_source():
    source=Path(__file__).resolve().parents[1]/"src/krc_research/uds_stage123.py"
    body=source.read_text()
    assert 'self.path=="/healthz"' in body
    assert '{"status":"staging","production":False}' in body
    schema=json.loads((source.parents[2]/"schemas/stage131/uds_healthz_response_v1.schema.json").read_text())
    Draft202012Validator.check_schema(schema)
    validator=Draft202012Validator(schema)
    assert validator.is_valid({"status":"staging","production":False})
    assert not validator.is_valid({"status":"staging","production":True})
    assert not validator.is_valid({"status":"staging"})
