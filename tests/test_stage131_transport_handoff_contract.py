import json
from pathlib import Path
from jsonschema import Draft202012Validator
from tools.stage131_source_error_fixtures import fixtures
ROOT=Path(__file__).resolve().parents[1]/"schemas/stage131"
E=Draft202012Validator(json.loads((ROOT/"uds_source_errors_v1.schema.json").read_text()))
G=Draft202012Validator(json.loads((ROOT/"artifact_get_signed_uds_envelope_candidate_v1.schema.json").read_text()))
def test_emitted_source_errors_match_schema():
    rows=fixtures()
    assert len(rows)==5
    for row in rows: assert E.is_valid(row["body"]),row
    codes={r["case"]:r["http_status"] for r in rows}
    assert codes["HANDLER_ERROR"]==409 and codes["RESPONSE_TOO_LARGE"]==507
    assert rows[0]["body"]=={"status":"rejected","error":{"code":"INVALID_REQUEST"}}
    assert rows[1]["body"]["status"]=="pending_reconciliation"
def test_get_contract_field_negative():
    body={"version":"krc-artifact-get/1","operation":"artifact.read","request_id":"R","artifact_id":"a"*48,"identity":{"principal":"K_Science","repository":"kolemasakar/K_Science","workflow_ref":"refs/heads/main"},"auth":{"key_id":"k","issued_at_epoch":1,"nonce":"x"*16,"mac_sha256":"b"*64}}
    assert G.is_valid(body)
    for key in body:
        candidate={k:v for k,v in body.items() if k!=key}
        assert not G.is_valid(candidate),key
    assert not G.is_valid({**body,"artifact_id":"bad"})
    assert not G.is_valid({**body,"auth":{**body["auth"],"mac_sha256":"bad"}})
    assert not G.is_valid({**body,"identity":{**body["identity"],"principal":""}})
