"""KRC cross-project envelope v1: signed, project-isolated, fail-closed.

This is a pure library. It does not authenticate or expose any HTTP listener.
Production secret provisioning and secure transport belong to Sentinel-Remote.
"""
from __future__ import annotations
import hashlib
import hmac
import json
import re
from datetime import datetime, timezone
from typing import Mapping

SCHEMA = "kscience-krc-research-v1"
CALLER = "K_Science"
AUDIENCE = "KRC"
ALLOWED = frozenset({
    "krc_capabilities",
    "krc_scholarly_preflight",
    "krc_doi_metadata",
    "krc_doi_updates",
    "krc_bibliography_audit",
    "krc_inspection_receipt_review",
})
REQUEST_RE = re.compile(r"^KS-[a-f0-9]{32}$")
MAX_BODY_BYTES = 256 * 1024

def canonical_json(obj: object) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True,
                      separators=(",",":"), allow_nan=False).encode("utf-8")

def _utc(timestamp: str) -> datetime:
    value = datetime.fromisoformat(timestamp.replace("Z","+00:00"))
    if value.utcoffset() is None:
        raise ValueError("Timestamp timezone required")
    return value.astimezone(timezone.utc)

def sign_request(*, operation: str, payload: dict, request_id: str,
                 issued_at: str, signing_key: bytes) -> dict:
    """Only for a dedicated per-project symmetric key, supplied outside Git."""
    if operation not in ALLOWED or not REQUEST_RE.fullmatch(request_id):
        raise ValueError("Unsupported operation or invalid ID")
    _utc(issued_at)
    if not isinstance(payload,dict) or len(canonical_json(payload)) > MAX_BODY_BYTES:
        raise ValueError("Invalid or oversized payload")
    if len(signing_key) < 32:
        raise ValueError("Key is too short")
    core = {
        "schema":SCHEMA,"caller":CALLER,"audience":AUDIENCE,
        "request_id":request_id,"issued_at":issued_at,
        "operation":operation,"payload":payload,
    }
    mac = hmac.new(signing_key,canonical_json(core),hashlib.sha256).hexdigest()
    return {**core, "signature_alg":"HMAC-SHA256","signature":mac}

def verify_request(envelope: Mapping, *, signing_key: bytes, now: datetime,
                   seen_ids: set[str], max_age_seconds: int = 300) -> dict:
    """Verify identity, operation ACL, HMAC, age and caller-specific replay.

    seen_ids must be a persistent, atomic replay registry in production;
    in-memory set is ONLY a unit-test fixture.
    """
    if not isinstance(envelope,Mapping):
        raise ValueError("Invalid envelope")
    expected = {
        "schema","caller","audience","request_id","issued_at",
        "operation","payload","signature_alg","signature"
    }
    if set(envelope) != expected:
        raise ValueError("Envelope fields mismatch")
    if envelope["schema"]!=SCHEMA or envelope["caller"]!=CALLER or envelope["audience"]!=AUDIENCE:
        raise ValueError("Wrong project or schema")
    if envelope["operation"] not in ALLOWED or not REQUEST_RE.fullmatch(envelope["request_id"]):
        raise ValueError("Unauthorized operation or invalid ID")
    if envelope["signature_alg"]!="HMAC-SHA256" or not re.fullmatch(r"[0-9a-f]{64}",str(envelope["signature"])):
        raise ValueError("Unsupported signature")
    if not isinstance(envelope["payload"],dict) or len(canonical_json(envelope["payload"]))>MAX_BODY_BYTES:
        raise ValueError("Payload too large")
    if len(signing_key)<32:
        raise ValueError("Signing key too short")
    core={k:v for k,v in envelope.items() if k not in ("signature_alg","signature")}
    expected_mac=hmac.new(signing_key,canonical_json(core),hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected_mac,envelope["signature"]):
        raise ValueError("Signature verification failed")
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("Verifier clock requires timezone")
    age=(now.astimezone(timezone.utc)-_utc(envelope["issued_at"])).total_seconds()
    if abs(age)>max_age_seconds:
        raise ValueError("Expired or future request")
    if envelope["request_id"] in seen_ids:
        raise ValueError("Replay detected")
    seen_ids.add(envelope["request_id"])
    return {"operation":envelope["operation"],"payload":envelope["payload"],
            "caller":CALLER,"request_id":envelope["request_id"],
            "authorized":True}

def not_ready_gate() -> dict:
    """Non-negotiable current rollout gate, until Sentinel binds the route."""
    return {"contract":SCHEMA, "transport":"NOT_CONNECTED",
            "credential_provisioned":False, "production_replay_store":False,
            "cross_project_live_calls_enabled":False,
            "reason":"Sentinel-Remote route admission and dedicated identities pending"}
