"""Stage127 KRC-owned internal science signer. Not deployed, fail closed.

The authorizer must be a KRC-controlled trusted verifier of user consent,
not a field or boolean supplied by K_Science/Sentinel. No network signing API.
"""
import hashlib
import json
from datetime import datetime,timezone
from jsonschema import Draft202012Validator,FormatChecker
from .interproject_contract import envelope,sign_envelope
from .private_dispatch_adapter import _schema_for
from .staging_backend114 import OPS

class ScienceAuthorizationDenied(ValueError): pass

def _canonical(data):
    return json.dumps(data,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode("utf-8")

class KRCInternalScienceSigner:
    def __init__(self, *, science_key, authorizer, dispatcher, bibliography_enabled=False):
        if not isinstance(science_key,bytes) or len(science_key)<32:
            raise ScienceAuthorizationDenied("INVALID_KEY")
        if not callable(authorizer) or not callable(dispatcher):
            raise ScienceAuthorizationDenied("MISSING_TRUSTED_COMPONENT")
        self._key=science_key
        self._authorizer=authorizer
        self._dispatcher=dispatcher
        self._bibliography_enabled=bibliography_enabled

    def execute(self, *, request_id, task_id, operation, payload, principal,
                profile_ref, evidence_refs, consent_ref):
        if (not isinstance(request_id,str) or not request_id.startswith("KS-")
            or not isinstance(task_id,str) or not isinstance(principal,str)
            or not principal or operation not in OPS
            or not isinstance(profile_ref,str) or not profile_ref
            or not isinstance(consent_ref,str) or not consent_ref
            or not isinstance(evidence_refs,list)
            or any(not isinstance(x,str) or not x for x in evidence_refs)
            or operation=="research.bibliography.audit" and not self._bibliography_enabled):
            raise ScienceAuthorizationDenied("DENIED")
        try:
            valid=Draft202012Validator(_schema_for(operation),format_checker=FormatChecker()).is_valid(payload)
            digest=hashlib.sha256(_canonical(payload)).hexdigest()
        except (ValueError,TypeError,OverflowError):
            raise ScienceAuthorizationDenied("INVALID_PAYLOAD") from None
        if not valid:
            raise ScienceAuthorizationDenied("INVALID_PAYLOAD")
        context={"request_id":request_id,"task_id":task_id,"operation":operation,
                 "principal":principal,"profile_ref":profile_ref,
                 "evidence_refs":list(evidence_refs),"payload_sha256":digest,
                 "consent_ref":consent_ref}
        # Authorizer MUST validate against independent, KRC-held approval custody,
        # rejecting stale/replayed/forged consent and unauthorized science actions.
        if self._authorizer(dict(context)) is not True:
            raise ScienceAuthorizationDenied("CONSENT_DENIED")
        body=envelope(task_id=task_id,operation=operation,payload=payload,
                      created_at=datetime.now(timezone.utc).isoformat())
        sig=sign_envelope(body,self._key)
        # Signature never crosses this boundary. Only authorized KRC dispatch.
        return self._dispatcher(operation,{"science_envelope":body,"science_signature":sig},principal)
