import json
from unittest.mock import patch
from urllib.error import URLError
import pytest
from plugins.krc_migration_candidate.mcp_canary.r3c import VoiceBridgeBinding, VoiceBridgeError, call_voicebridge

class Reply:
    def __init__(self, body, status=200):
        self.status = status
        self.body = json.dumps(body).encode()
    def __enter__(self): return self
    def __exit__(self, *args): pass
    def read(self, limit): return self.body[:limit]

BINDING = VoiceBridgeBinding("https://voicebridge.example", "private-token")

@pytest.mark.parametrize("path", ["/api/v1/media/managed/transcriptions", "/api/v1/media/youtube-gemini/transcriptions"])
def test_ready_checks_then_posts_once(path):
    calls = []
    def send(request, timeout):
        calls.append(request)
        return Reply({"status": "ok"} if request.method == "GET" else {"job_id": "fixture"})
    with patch("plugins.krc_migration_candidate.mcp_canary.r3c.urlopen", send):
        assert call_voicebridge(BINDING, "POST", path, {"url": "fixture"}, {}) == {"job_id": "fixture"}
    assert [c.method for c in calls] == ["GET", "POST"]
    assert calls[0].full_url == "https://voicebridge.example/api/v1/health"
    assert calls[0].get_header("Authorization") is None

@pytest.mark.parametrize("failure", ["timeout", "bad_status", "not_ready"])
def test_readiness_failure_never_posts(failure):
    calls = []
    def send(request, timeout):
        calls.append(request)
        if failure == "timeout": raise URLError("private diagnostic")
        return Reply({"status": "ok" if failure == "bad_status" else "starting"}, 503 if failure == "bad_status" else 200)
    with patch("plugins.krc_migration_candidate.mcp_canary.r3c.urlopen", send), patch("plugins.krc_migration_candidate.mcp_canary.r3c._READONLY_HEALTH_ATTEMPTS", 1):
        with pytest.raises(VoiceBridgeError) as result:
            call_voicebridge(BINDING, "POST", "/api/v1/media/managed/transcriptions", {}, {})
    assert result.value.code == "voicebridge_not_ready"
    assert result.value.retryable
    assert [c.method for c in calls] == ["GET"]

def test_readonly_has_no_extra_call_and_post_failure_is_not_retried():
    calls = []
    def send(request, timeout):
        calls.append(request)
        if request.method == "POST": raise URLError("uncertain send")
        return Reply({"status": "ok"})
    with patch("plugins.krc_migration_candidate.mcp_canary.r3c.urlopen", send):
        call_voicebridge(BINDING, "GET", "/api/v1/media/capabilities", None, {})
        with pytest.raises(VoiceBridgeError):
            call_voicebridge(BINDING, "POST", "/api/v1/media/managed/transcriptions", {}, {})
    assert [c.method for c in calls] == ["GET", "GET", "POST"]


@pytest.mark.parametrize("path", ["/api/v1/media/managed/transcriptions", "/api/v1/media/youtube-gemini/transcriptions"])
def test_delayed_health_never_replays_consequential_post(path):
    calls = []
    def send(request, timeout):
        calls.append(request)
        if len(calls) < 3:
            raise URLError("still warming")
        return Reply({"status":"ok"} if request.method == "GET" else {"job_id":"fixture"})
    with patch("plugins.krc_migration_candidate.mcp_canary.r3c.urlopen", send), patch("plugins.krc_migration_candidate.mcp_canary.r3c.sleep"):
        assert call_voicebridge(BINDING, "POST", path, {}, {}) == {"job_id":"fixture"}
    assert [c.method for c in calls] == ["GET", "GET", "GET", "POST"]
    assert all(c.get_header("Authorization") is None for c in calls[:-1])


def test_readiness_exhaustion_exposes_safe_attempt_count():
    with patch("plugins.krc_migration_candidate.mcp_canary.r3c._wait_for_voicebridge_health", return_value=(False, 9)), patch("plugins.krc_migration_candidate.mcp_canary.r3c.urlopen") as send:
        with pytest.raises(VoiceBridgeError) as error:
            call_voicebridge(BINDING, "POST", "/api/v1/media/youtube-gemini/transcriptions", {}, {})
    send.assert_not_called()
    from plugins.krc_migration_candidate.mcp_canary.r3c import _sanitized_backend_error
    detail = _sanitized_backend_error(error.value)["error"]
    assert detail["readiness_health_attempts"] == 9
    assert detail["consequential_post_attempted"] is False
