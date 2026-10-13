import io
from unittest.mock import patch
from urllib.error import HTTPError
import json
from plugins.krc_migration_candidate.mcp_canary.r3c import VoiceBridgeBinding, _wait_for_voicebridge_health
from plugins.krc_migration_candidate.p0_wake_relay_client import attempt_external_wake
from plugins.krc_migration_candidate import p0_wake_relay_client

B = VoiceBridgeBinding("https://voicebridge.example", "private-token")

class Reply:
    status = 200
    def __enter__(self): return self
    def __exit__(self, *_): pass
    def read(self, n): return b'{"status":"ok"}'

def failed(req, *, application=False):
    headers = {"Server":"cloudflare"}
    if application: headers["Retry-After"]="30"
    return HTTPError(req.full_url,429,"rate",headers,io.BytesIO(b"blocked"))

def test_no_wake_by_default():
    with patch.dict("os.environ", {}, clear=True):
        assert attempt_external_wake() == "disabled"

def test_invalid_relay_config_stays_disabled():
    with patch.dict("os.environ", {"KRC_WAKE_RELAY_ENABLED":"1",
              "KRC_WAKE_RELAY_URL":"http://127.0.0.1/krc-wake/v1",
              "KRC_WAKE_RELAY_HOST":"127.0.0.1",
              "KRC_WAKE_RELAY_TOKEN":"a"*40}, clear=True):
        assert attempt_external_wake()=="disabled"

def test_proxy_failure_wakes_at_most_once():
    calls=[]; wakes=[]
    def mock_get(req, timeout):
        calls.append(req)
        if len(calls)<3: raise failed(req)
        return Reply()
    with patch("plugins.krc_migration_candidate.mcp_canary.r3c.urlopen", mock_get),\
         patch("plugins.krc_migration_candidate.mcp_canary.r3c.attempt_external_wake", side_effect=lambda: wakes.append(1) or "relay_success"),\
         patch("plugins.krc_migration_candidate.mcp_canary.r3c.sleep"):
        assert _wait_for_voicebridge_health(B)==(True,3)
    assert len(wakes)==1
    assert all(req.method=="GET" and req.get_header("Authorization") is None for req in calls)

def test_real_application_limit_does_not_wake():
    wakes=[]
    def mock_get(req,timeout):
        raise failed(req, application=True)
    with patch("plugins.krc_migration_candidate.mcp_canary.r3c.urlopen",mock_get),\
         patch("plugins.krc_migration_candidate.mcp_canary.r3c.attempt_external_wake",side_effect=lambda: wakes.append(1) or "relay_success"),\
         patch("plugins.krc_migration_candidate.mcp_canary.r3c._READONLY_HEALTH_ATTEMPTS",2),\
         patch("plugins.krc_migration_candidate.mcp_canary.r3c.sleep"):
        assert _wait_for_voicebridge_health(B)==(False,2)
    assert not wakes

def test_relay_failure_is_fail_closed():
    calls=[]; wakes=[]
    def mock_get(req, timeout):
        calls.append(req)
        raise failed(req)
    with patch("plugins.krc_migration_candidate.mcp_canary.r3c.urlopen",mock_get),\
         patch("plugins.krc_migration_candidate.mcp_canary.r3c.attempt_external_wake",side_effect=lambda: wakes.append(1) or "relay_unavailable"),\
         patch("plugins.krc_migration_candidate.mcp_canary.r3c._READONLY_HEALTH_ATTEMPTS",2),\
         patch("plugins.krc_migration_candidate.mcp_canary.r3c.sleep"):
        assert _wait_for_voicebridge_health(B)==(False,2)
    assert len(wakes)==1 and len(calls)==2

def test_no_redirect_credentials_to_third_party():
    class MockOpener:
        def open(self, request, timeout):
            assert request.full_url=="https://wake.example/krc-wake/v1"
            assert request.get_header("Authorization") == "Bearer " + "a"*40
            assert request.data==b'{"action":"wake_voicebridge"}'
            assert request.method=="POST"
            assert timeout==12
            return type("Response",(),{"status":200,"__enter__":lambda self:self,"__exit__":lambda self,*a:None,"read":lambda self,n:b'{"status":"woken"}'})()
    with patch.dict("os.environ",{"KRC_WAKE_RELAY_ENABLED":"1",
          "KRC_WAKE_RELAY_URL":"https://wake.example/krc-wake/v1",
          "KRC_WAKE_RELAY_HOST":"wake.example",
          "KRC_WAKE_RELAY_TOKEN":"a"*40},clear=True),\
         patch.object(p0_wake_relay_client,"build_opener",return_value=MockOpener()):
        assert attempt_external_wake()=="relay_success"
