"""Source-only Stage131 pre-dispatch authorization boundary.

No network, no grant issuance. Deliberately does NOT accept a caller boolean as consent.
"""
from .stage131_correlated_dispatch import execute_correlated

class AuthorizationGateDenied(ValueError):
    pass

def execute_with_custody(dispatch, *, authorizer, context, operation, payload, principal, request_id):
    if not callable(authorizer) or not isinstance(context,dict):
        raise AuthorizationGateDenied("TRUSTED_CUSTODY_REQUIRED")
    required=("request_id","task_id","operation","principal","profile_ref","evidence_refs","payload_sha256","consent_ref")
    if set(context)!=set(required) or context["request_id"]!=request_id or context["operation"]!=operation or context["principal"]!=principal:
        raise AuthorizationGateDenied("CONTEXT_MISMATCH")
    if not isinstance(payload,dict) or payload.get("task_id")!=context["task_id"]:
        raise AuthorizationGateDenied("TASK_MISMATCH")
    if authorizer(dict(context)) is not True:
        raise AuthorizationGateDenied("CONSENT_DENIED")
    # Authorizer must be backed by independently secured, single-use custody; no client assertions.
    return execute_correlated(dispatch,operation=operation,payload=payload,principal=principal,request_id=request_id)


def execute_with_durable_n39_custody(dispatch, *, journal, context, operation, payload, principal, request_id):
    """Source-only alternative: durable intent before single-use real consent.

    Recovered journal evidence is NEVER treated as permission to re-dispatch.
    An ambiguous crash requires a separate owner-reviewed recovery decision.
    """
    from .stage131_n39_trust_boundaries import N39ProvenanceJournal
    if not isinstance(journal,N39ProvenanceJournal):
        raise AuthorizationGateDenied("TRUSTED_PROVENANCE_JOURNAL_REQUIRED")
    if not isinstance(context,dict):
        raise AuthorizationGateDenied("CONTEXT_MISMATCH")
    required=("request_id","task_id","operation","principal","profile_ref","evidence_refs","payload_sha256","consent_ref")
    if set(context)!=set(required) or context["request_id"]!=request_id or context["operation"]!=operation or context["principal"]!=principal:
        raise AuthorizationGateDenied("CONTEXT_MISMATCH")
    if not isinstance(payload,dict) or payload.get("task_id")!=context["task_id"]:
        raise AuthorizationGateDenied("TASK_MISMATCH")
    if journal.consume_once(dict(context)) is not True:
        raise AuthorizationGateDenied("CONSENT_DENIED_OR_RECOVERY_HOLD")
    return execute_correlated(dispatch,operation=operation,payload=payload,principal=principal,request_id=request_id)
