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
    with patch.object(r3c,"_call_voicebridge_once",side_effect=failure) as once, patch.object(r3c,"_wait_for_readonly_health",return_value=(False, 4)):
        with pytest.raises(r3c.VoiceBridgeError) as caught:r3c.call_voicebridge(BINDING,"GET","/api/v1/media/public-capabilities",None,{})
    assert caught.value is failure
    assert once.call_count==1

def test_second_failure_terminates_without_loop():
    failure=r3c.VoiceBridgeError("voicebridge_http_error",http_status=429)
    with patch.object(r3c,"_call_voicebridge_once",side_effect=failure) as once, patch.object(r3c,"urlopen",return_value=Health()) as health:
        with pytest.raises(r3c.VoiceBridgeError):r3c.call_voicebridge(BINDING,"GET","/api/v1/media/public-capabilities",None,{})
    assert once.call_count==2
    assert health.call_count==1


class Clock:
    def __init__(self): self.now = 0.0
    def monotonic(self): return self.now
    def sleep(self, seconds): self.now += seconds


def test_health_polls_until_ready_without_credentials():
    from urllib.error import HTTPError
    clock = Clock()
    responses = [HTTPError("https://voicebridge.invalid/api/v1/health", 429, "warming", {}, None), TimeoutError(), Health()]
    with patch.object(r3c, "monotonic", clock.monotonic), patch.object(r3c, "sleep", clock.sleep), patch.object(r3c, "urlopen", side_effect=responses) as health:
        assert r3c._wait_for_readonly_health(BINDING) == (True, 3)
    assert clock.now == 4.0
    for call in health.call_args_list:
        request = call.args[0]
        assert request.method == "GET"
        assert request.full_url == "https://voicebridge.invalid/api/v1/health"
        assert request.get_header("Authorization") is None
        assert call.kwargs["timeout"] <= 5.0


def test_health_deadline_clamps_each_request_and_sleep():
    clock = Clock()
    timeouts = []
    def unavailable(request, timeout):
        timeouts.append(timeout)
        clock.now += timeout
        raise TimeoutError()
    with patch.object(r3c, "monotonic", clock.monotonic), patch.object(r3c, "sleep", clock.sleep), patch.object(r3c, "urlopen", side_effect=unavailable):
        ready, attempts = r3c._wait_for_readonly_health(BINDING)
    assert not ready
    assert attempts == len(timeouts)
    assert clock.now == 45.0
    assert timeouts[-1] <= 5.0


@pytest.mark.parametrize("status", [400, 401, 403, 404])
def test_health_terminal_http_stops_without_polling(status):
    from urllib.error import HTTPError
    with patch.object(r3c, "urlopen", side_effect=HTTPError("https://voicebridge.invalid", status, "terminal", {}, None)) as health, patch.object(r3c, "sleep") as sleep:
        assert r3c._wait_for_readonly_health(BINDING) == (False, 1)
    assert health.call_count == 1
    sleep.assert_not_called()


@pytest.mark.parametrize("diagnostics", [{"upstream_code":"RATE_LIMITED"}, {"upstream_code":"MEDIA_PUBLIC_FREE_TIER_RATE_LIMIT"}, {"upstream_code":"MEDIA_PUBLIC_CONCURRENCY_LIMIT"}, {"retry_after_seconds":10}])
def test_explicit_rate_limit_is_not_replayed(diagnostics):
    failure = r3c.VoiceBridgeError("voicebridge_http_error", http_status=429, diagnostics=diagnostics)
    with patch.object(r3c, "_call_voicebridge_once", side_effect=failure) as once, patch.object(r3c, "_wait_for_readonly_health") as health:
        with pytest.raises(r3c.VoiceBridgeError) as caught:
            r3c.call_voicebridge(BINDING, "GET", "/api/v1/media/public-capabilities", None, {})
    assert caught.value is failure
    assert once.call_count == 1
    health.assert_not_called()


def test_exhausted_recovery_diagnostics_survive_mcp_egress():
    failure = r3c.VoiceBridgeError("voicebridge_http_error", http_status=429)
    with patch.object(r3c, "_call_voicebridge_once", side_effect=failure), patch.object(r3c, "_wait_for_readonly_health", return_value=(False, 7)):
        with pytest.raises(r3c.VoiceBridgeError) as caught:
            r3c.call_voicebridge(BINDING, "GET", "/api/v1/media/public-capabilities", None, {})
    detail = r3c._sanitized_backend_error(caught.value)["error"]
    assert detail["readonly_health_ready"] is False
    assert detail["readonly_health_attempts"] == 7


@pytest.mark.parametrize("ready,attempts", [("true",1),(True,True),(True,25),(True,-1)])
def test_invalid_recovery_diagnostics_are_dropped(ready,attempts):
    detail = r3c._sanitized_backend_error(r3c.VoiceBridgeError("voicebridge_http_error", diagnostics={"readonly_health_ready":ready,"readonly_health_attempts":attempts}))["error"]
    assert "readonly_health_ready" not in detail
    assert "readonly_health_attempts" not in detail
