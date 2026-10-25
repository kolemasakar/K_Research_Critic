"""Isolated, fail-closed dispatch classification and hash-chain approval custody."""
from jsonschema import Draft202012Validator,FormatChecker
from .private_contract_details import sanitized_error
from .private_dispatch_adapter import _schema_for
from .private_stage111 import approval_attestation
from .interproject_contract import validate_envelope
from .science_dispatch import handle_science_request
from .inspection_receipts import append_entry,verify_chain

def approval_chain_append(chain,profile,receipt,keys):
    verdict=approval_attestation(profile,receipt,keys)
    if verdict!="SIGNED_BY_CONFIGURED_KEY_NOT_HUMAN_VERIFIED":
        raise ValueError("Unverified approval")
    return append_entry(chain,{"profile_sha256":receipt["profile_sha256"],"receipt":receipt,"assurance":verdict})

def approval_chain_verify(chain):
    return verify_chain(chain)

def dispatch_coded(message,*,secret,signature,seen,permitted,now=None,bibliography_fn=None):
    if not isinstance(message,dict):return sanitized_error("INVALID_REQUEST")
    op=message.get("operation")
    if op not in permitted:return sanitized_error("OPERATION_DENIED")
    try:
        if not Draft202012Validator(_schema_for(op),format_checker=FormatChecker()).is_valid(message.get("payload")):
            return sanitized_error("INVALID_REQUEST")
        validate_envelope(message,key=secret,signature=signature,allowed_operations=permitted,now=now)
    except (ValueError,TypeError,KeyError) as exc:
        detail=str(exc)
        if "signature" in detail.lower() or "Unauthorized route" in detail:return sanitized_error("UNAUTHORIZED")
        if "Expired or future" in detail:return sanitized_error("EXPIRED_REQUEST")
        return sanitized_error("INVALID_REQUEST")
    try:
        kw={"secret":secret,"signature":signature,"seen":seen,"permitted":permitted,"now":now}
        if bibliography_fn is not None:kw["bibliography_fn"]=bibliography_fn
        return handle_science_request(message,**kw)
    except ValueError as exc:
        if "replay" in str(exc).lower():return sanitized_error("REPLAY_REJECTED")
        return sanitized_error("HANDLER_ERROR")
    except (TypeError,KeyError):
        return sanitized_error("HANDLER_ERROR")
