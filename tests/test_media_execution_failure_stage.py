from unittest.mock import patch
from urllib.error import URLError
import pytest
from plugins.krc_migration_candidate.mcp_canary import r3e2_http_server as e2
from plugins.krc_migration_candidate.mcp_canary.r3c import VoiceBridgeBinding, VoiceBridgeError, call_voicebridge, _sanitized_backend_error
from plugins.krc_migration_candidate.mcp_canary.voicebridge_http_diagnostics import safe_error_diagnostics

BINDING = VoiceBridgeBinding("https://voicebridge.invalid", "fixture-token")

def test_warmup_failure_marks_unsent_and_never_posts():
    with patch.object(e2, "_warm_voicebridge", side_effect=VoiceBridgeError("voicebridge_http_error", http_status=429)), patch.object(e2, "call_voicebridge") as post:
        with pytest.raises(VoiceBridgeError) as caught:
            e2._cold_start_resilient_backend(BINDING, "POST", "/api/v1/media/managed/transcriptions", {}, {})
    post.assert_not_called()
    error = _sanitized_backend_error(caught.value)["error"]
    assert error["failure_stage"] == "warmup"
    assert error["consequential_post_attempted"] is False

def test_readiness_failure_marks_unsent():
    with patch("plugins.krc_migration_candidate.mcp_canary.r3c.urlopen", side_effect=URLError("private")) as send, patch("plugins.krc_migration_candidate.mcp_canary.r3c._READONLY_HEALTH_ATTEMPTS", 1):
        with pytest.raises(VoiceBridgeError) as caught:
            call_voicebridge(BINDING, "POST", "/api/v1/media/managed/transcriptions", {}, {})
    assert send.call_count == 1
    error = _sanitized_backend_error(caught.value)["error"]
    assert error["failure_stage"] == "readiness"
    assert error["consequential_post_attempted"] is False

def test_uncertain_post_marks_attempt_without_replay():
    class Ready:
        status = 200
        def __enter__(self): return self
        def __exit__(self, *args): pass
        def read(self, limit): return b'{"status":"ok"}'
    with patch("plugins.krc_migration_candidate.mcp_canary.r3c.urlopen", side_effect=[Ready(), URLError("private")]) as send:
        with pytest.raises(VoiceBridgeError) as caught:
            call_voicebridge(BINDING, "POST", "/api/v1/media/managed/transcriptions", {}, {})
    assert send.call_count == 2
    error = _sanitized_backend_error(caught.value)["error"]
    assert error["failure_stage"] == "start"
    assert error["consequential_post_attempted"] is True

def test_egress_rejects_untrusted_stage_and_inconsistent_attempt_flag():
    for values in [{"failure_stage": [], "consequential_post_attempted": False}, {"failure_stage":"secret"}, {"failure_stage":"warmup","consequential_post_attempted":True}, {"failure_stage":"start","consequential_post_attempted":False}]:
        assert safe_error_diagnostics(values) == {}
