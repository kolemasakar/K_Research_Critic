"""Isolated tests; no network calls or production integration."""
import pytest
from plugins.krc_migration_candidate.mcp_canary.proxy_peer_diagnostics import observe_peer

K1 = b"a" * 32
K2 = b"b" * 32

def test_same_peer_same_window():
    assert observe_peer("192.0.2.1", None, K1).peer_tag == observe_peer("192.0.2.1", "1.2.3.4", K1).peer_tag

def test_new_key_changes_tag():
    assert observe_peer("192.0.2.1", None, K1).peer_tag != observe_peer("192.0.2.1", None, K2).peer_tag

def test_peer_changes_tag():
    assert observe_peer("192.0.2.1", None, K1).peer_tag != observe_peer("192.0.2.2", None, K1).peer_tag

def test_ipv6_canonicalized():
    assert observe_peer("2001:db8::1", None, K1).peer_tag == observe_peer("2001:0db8:0:0:0:0:0:1", None, K1).peer_tag

@pytest.mark.parametrize("header,shape", [
    (None, "absent"), ("", "empty"), ("  ", "empty"),
    ("1.2.3.4", "single_untrusted"), ("1.2.3.4, 5.6.7.8", "multiple_untrusted"),
    ("x" * 1025, "oversize")
])
def test_untrusted_header_shape_only(header, shape):
    result = observe_peer("192.0.2.1", header, K1)
    assert result.forwarded_shape == shape
    assert result.forwarded_present == (header is not None)
    assert "192.0.2.1" not in repr(result)
    assert "1.2.3.4" not in repr(result)

def test_short_key_rejected():
    with pytest.raises(ValueError):
        observe_peer("192.0.2.1", None, b"weak")

def test_invalid_peer_rejected():
    with pytest.raises(ValueError):
        observe_peer("not an ip", None, K1)
