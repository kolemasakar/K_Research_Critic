import pytest
from unittest.mock import patch
from plugins.krc_migration_candidate.mcp_canary import r3c

BINDING = r3c.VoiceBridgeBinding("https://voicebridge.invalid", "fixture-token")
class Health:
    status = 200
    def __enter__(self): return self
    def __exit__(self, *args): pass
    def read(self, size): return b'{"status":"ok"}'

@pytest.mark.parametrize("method,path", [
 ("GET","/api/v1/media/public-capabilities"),
 ("POST","/api/v1/media/managed/preflight"),
 ("POST","/api/v1/media/managed/lookup"),
 ("POST","/api/v1/media/youtube-gemini/preflight"),
 ("POST","/api/v1/media/youtube-gemini/lookup"),
 ("GET","/api/v1/media/managed/transcriptions/KRCM_12345678-1234-1234-1234-123456789012/segments"),
])
def test_read_recovery_after_health_once(method,path):
    failure = r3c.VoiceBridgeError("voicebridge_http_error", http_status=429, retryable=True)
    with patch.object(r3c,"_call_voicebridge_once", side_effect=[failure,{"status":"ok"}]) as once, patch.object(r3c,"urlopen",return_value=Health()) as health:
        assert r3c.call_voicebridge(BINDING,method,path,{}, {}) == {"status":"ok"}
    assert once.call_count == 2
    assert health.call_count == 1
    assert health.call_args.args[0].get_header("Authorization") is None

@pytest.mark.parametrize("path",["/api/v1/media/managed/transcriptions","/api/v1/media/youtube-gemini/transcriptions","/api/v1/media/unknown"])
def test_no_execution_replay(path):
    failure=r3c.VoiceBridgeError("voicebridge_http_error",http_status=429,retryable=True)
    with patch.object(r3c,"_call_voicebridge_once",side_effect=failure) as once, patch.object(r3c,"urlopen") as health:
        with pytest.raises(r3c.VoiceBridgeError):r3c.call_voicebridge(BINDING,"POST",path,{}, {})
    assert once.call_count==1
    health.assert_not_called()

@pytest.mark.parametrize("status",[400,401,403,404])
def test_terminal_read_errors_not_retried(status):
    failure=r3c.VoiceBridgeError("voicebridge_http_error",http_status=status)
    with patch.object(r3c,"_call_voicebridge_once",side_effect=failure) as once, patch.object(r3c,"urlopen") as health:
        with pytest.raises(r3c.VoiceBridgeError):r3c.call_voicebridge(BINDING,"GET","/api/v1/media/public-capabilities",None,{})
    assert once.call_count==1
    health.assert_not_called()

def test_unready_preserves_original_error():
    failure=r3c.VoiceBridgeError("voicebridge_http_error",http_status=429)
    with patch.object(r3c,"_call_voicebridge_once",side_effect=failure) as once, patch.object(r3c,"urlopen",side_effect=TimeoutError):
        with pytest.raises(r3c.VoiceBridgeError) as caught:r3c.call_voicebridge(BINDING,"GET","/api/v1/media/public-capabilities",None,{})
    assert caught.value is failure
    assert once.call_count==1

def test_second_failure_terminates_without_loop():
    failure=r3c.VoiceBridgeError("voicebridge_http_error",http_status=429)
    with patch.object(r3c,"_call_voicebridge_once",side_effect=failure) as once, patch.object(r3c,"urlopen",return_value=Health()) as health:
        with pytest.raises(r3c.VoiceBridgeError):r3c.call_voicebridge(BINDING,"GET","/api/v1/media/public-capabilities",None,{})
    assert once.call_count==2
    assert health.call_count==1
