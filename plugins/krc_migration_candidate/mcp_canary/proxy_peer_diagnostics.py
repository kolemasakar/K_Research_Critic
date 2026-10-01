"""Research-only, privacy-minimizing proxy diagnostics. NOT wired into VoiceBridge.

Use a fresh secret key per observation period, never log the key or raw addresses.
The socket peer is the only trusted network observation by default.
"""
import hashlib
import hmac
import ipaddress
from dataclasses import dataclass


@dataclass(frozen=True)
class PeerObservation:
    peer_tag: str
    forwarded_present: bool
    forwarded_shape: str


def observe_peer(peer: str, forwarded: str | None, key: bytes) -> PeerObservation:
    """Return non-reversible within-period peer tag and *untrusted* header shape.

    Header content is not hashed, parsed into identities, trusted or returned.
    Caller must never persist key, peer or forwarded input in logs.
    """
    if len(key) < 32:
        raise ValueError("ephemeral key must be at least 32 bytes")
    normalized = str(ipaddress.ip_address(peer))
    tag = hmac.new(key, normalized.encode("ascii"), hashlib.sha256).hexdigest()[:24]
    if forwarded is None:
        shape = "absent"
    elif not forwarded.strip():
        shape = "empty"
    elif len(forwarded) > 1024:
        shape = "oversize"
    elif "," in forwarded:
        shape = "multiple_untrusted"
    else:
        shape = "single_untrusted"
    return PeerObservation(tag, forwarded is not None, shape)
