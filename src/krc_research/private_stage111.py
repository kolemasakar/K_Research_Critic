"""Offline only: signature-bound approval and sanitized error classification."""
import hashlib
import hmac
import json
from .private_contract_details import sanitized_error
from .private_dispatch_adapter import dispatch_validated

def digest_profile(profile):
    return hashlib.sha256(json.dumps(profile,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode()).hexdigest()

def approval_attestation(profile, receipt, trusted_signers):
    """A valid HMAC proves custody of a configured signer secret, NOT human identity by itself."""
    if not isinstance(profile,dict) or not isinstance(receipt,dict) or not isinstance(trusted_signers,dict):
        return "UNVERIFIED"
    signer=receipt.get("signer_id")
    key=trusted_signers.get(signer) if isinstance(signer,str) else None
    if not isinstance(key,bytes) or len(key)<32:
        return "UNTRUSTED_SIGNER"
    required=("profile_id","profile_version","profile_sha256","signer_id","approved_at","signature")
    if any(not isinstance(receipt.get(k),str) or not receipt[k] for k in required):
        return "INVALID_RECEIPT"
    if (receipt["profile_id"]!=profile.get("profile_id") or
        receipt["profile_version"]!=profile.get("version") or
        receipt["profile_sha256"]!=digest_profile(profile)):
        return "PROFILE_MISMATCH"
    signed={k:receipt[k] for k in required if k!="signature"}
    expected=hmac.new(key,json.dumps(signed,sort_keys=True,separators=(",",":")).encode(),hashlib.sha256).hexdigest()
    return "SIGNED_BY_CONFIGURED_KEY_NOT_HUMAN_VERIFIED" if hmac.compare_digest(expected,receipt["signature"]) else "INVALID_SIGNATURE"

def isolated_dispatch(message,*,secret,signature,seen,permitted,now=None,bibliography_fn=None):
    """Optional stricter wrapper; never exposes Python exception details."""
    if not isinstance(message,dict):
        return sanitized_error("INVALID_REQUEST")
    op=message.get("operation")
    if op not in permitted:
        return sanitized_error("OPERATION_DENIED")
    out=dispatch_validated(message,secret=secret,signature=signature,seen=seen,
        permitted=permitted,now=now,bibliography_fn=bibliography_fn)
    if isinstance(out,dict) and out.get("status")=="error":
        return out
    return out
