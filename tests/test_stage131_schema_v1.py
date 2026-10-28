"""Read-only draft contract checks; never starts a service."""
import json
from pathlib import Path
from copy import deepcopy
from jsonschema import Draft202012Validator

SCHEMA=Path(__file__).resolve().parents[1]/"schemas/stage131/science_request_envelope_v1.schema.json"

def test_stage131_schema_is_valid_and_closed():
    s=json.loads(SCHEMA.read_text())
    Draft202012Validator.check_schema(s)
    assert s["additionalProperties"] is False

def test_stage131_rejects_untrusted_extensions_and_operations():
    validator=Draft202012Validator(json.loads(SCHEMA.read_text()))
    valid={"request_id":"KS-"+"1"*32,"task_id":"ks131-"+"2"*32,
           "operation":"research.profile.validate","principal":"K_Science",
           "profile_ref":"p1","evidence_refs":[],"consent_ref":"consent-synthetic-1",
           "science_payload":{"critic_profile":{}}}
    assert validator.is_valid(valid)
    for change in ({"principal":"other"},{"operation":"os.execute"},
                   {"raw_jwt":"not-allowed"},{"consent_ref":""},
                   {"request_id":"bad"}):
        candidate=deepcopy(valid)
        candidate.update(change)
        assert not validator.is_valid(candidate)
