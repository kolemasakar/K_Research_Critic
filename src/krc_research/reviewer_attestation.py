"""Independent-reviewer receipt attestation, verifiable without trusting submitted booleans.

Only a reviewer-issued HMAC tied to receipt hash, source artifact digest and reviewer
identity is accepted. It proves holder of a configured key attested the metadata,
NOT that the paper's scientific conclusions are true.
"""
from __future__ import annotations
from datetime import datetime, timezone
import hashlib
import hmac
import json
import re

HEX64 = re.compile(r"^[0-9a-f]{64}$")
MAX_AGE = 60 * 60 * 24 * 30

def canonical(body: dict) -> bytes:
    return json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
                      allow_nan=False).encode("utf-8")

def attestation_body(*, receipt_sha256: str, document_sha256: str, reviewer_id: str,
                     checked_at: str, method: str = "MANUAL_SOURCE_INSPECTION") -> dict:
    if not HEX64.fullmatch(receipt_sha256) or not HEX64.fullmatch(document_sha256):
        raise ValueError("Invalid SHA-256")
    if not isinstance(reviewer_id, str) or not reviewer_id.strip():
        raise ValueError("Reviewer identity absent")
    if method != "MANUAL_SOURCE_INSPECTION":
        raise ValueError("Unknown inspection method")
    stamp = datetime.fromisoformat(checked_at.replace("Z", "+00:00"))
    if stamp.utcoffset() is None:
        raise ValueError("Timezone required")
    return {"schema":"KRC-REVIEWER-ATTESTATION-1","receipt_sha256":receipt_sha256,
            "document_sha256":document_sha256,"reviewer_id":reviewer_id,
            "checked_at":checked_at,"method":method}

def sign_attestation(body: dict, key: bytes) -> str:
    if not isinstance(key, bytes) or len(key) < 32:
        raise ValueError("Reviewer key too short")
    return hmac.new(key, canonical(body), hashlib.sha256).hexdigest()

def verify_attestation(body: dict, signature: str, *, trusted_reviewer_keys: dict,
                       expected_receipt_sha256: str, expected_document_sha256: str,
                       researcher_id: str, now: datetime | None = None) -> dict:
    if not isinstance(body, dict):
        raise ValueError("Attestation must be object")
    expected = attestation_body(
        receipt_sha256=body["receipt_sha256"],document_sha256=body["document_sha256"],
        reviewer_id=body["reviewer_id"],checked_at=body["checked_at"],
        method=body["method"])
    if body != expected:
        raise ValueError("Attestation schema mismatch")
    reviewer = body["reviewer_id"]
    if reviewer == researcher_id or not researcher_id:
        raise ValueError("Reviewer cannot be researcher")
    key = trusted_reviewer_keys.get(reviewer)
    if key is None:
        raise ValueError("Untrusted reviewer")
    if body["receipt_sha256"] != expected_receipt_sha256 or body["document_sha256"] != expected_document_sha256:
        raise ValueError("Attested hashes mismatch")
    if not isinstance(signature,str) or not hmac.compare_digest(sign_attestation(body,key), signature):
        raise ValueError("Invalid signature")
    timestamp=datetime.fromisoformat(body["checked_at"].replace("Z","+00:00")).astimezone(timezone.utc)
    reference=(now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    delta=(reference-timestamp).total_seconds()
    if delta < 0 or delta > MAX_AGE:
        raise ValueError("Attestation outside acceptance interval")
    return {"verified":True,"reviewer_id":reviewer,"receipt_sha256":expected_receipt_sha256,
            "document_sha256":expected_document_sha256,
            "verification_scope":"REVIEWER_SIGNATURE_AND_ARTIFACT_BINDING_ONLY",
            "scientific_truth_verified":False}
