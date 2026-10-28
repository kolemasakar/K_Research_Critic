import json,os
import pytest
from krc_research.staging_entrypoint124 import load_config,secret

def test_reject_public_config(tmp_path):
 p=tmp_path/"config.json"
 p.write_text("{}")
 p.chmod(0o644)
 with pytest.raises(ValueError,match="private"):
  load_config(str(p))

def test_reject_public_secret(tmp_path):
 p=tmp_path/"key"
 p.write_bytes(b"x"*32)
 p.chmod(0o644)
 with pytest.raises(ValueError,match="private"):
  secret(str(p))

def test_accept_private_file(tmp_path):
 p=tmp_path/"config.json"
 p.write_text(json.dumps(dict.fromkeys(("socket_path","state_root","peer_uid","principal","key_id","transport_key_file","science_key_file","client","repository","workflow_ref"),"/tmp/sock")))
 p.chmod(0o600)
 assert load_config(str(p))["socket_path"]=="/tmp/sock"

def test_secret_minimum_length(tmp_path):
 p=tmp_path/"key"
 p.write_bytes(b"x"*16)
 p.chmod(0o600)
 with pytest.raises(ValueError,match="Weak"):
  secret(str(p))
