"""Stage131 safe composition checks. No listener, no grants, no dispatch by default."""
from .stage131_correlated_dispatch import execute_correlated
from .stage131_consumer_boundary_checks import validate_artifact_descriptor
from .stage131_bibliography_adapter import lookup_doi_metadata
from .stage131_bibliography_http import fetch_json_metadata

class Stage131GateDenied(ValueError):
    pass

def science_result_gate(dispatch, *, operation, payload, principal, request_id, consent_verified=False):
    if consent_verified is not True:
        raise Stage131GateDenied("OWNER_CONSENT_REQUIRED")
    return execute_correlated(dispatch,operation=operation,payload=payload,
                              principal=principal,request_id=request_id)

def artifact_read_gate(exchange, descriptor, *, authenticated_principal,
                       expected_principal, request_id, now_epoch):
    """Internal scoped read only. Not an external GET handler or authorization issuer."""
    if not authenticated_principal or authenticated_principal!=expected_principal:
        raise Stage131GateDenied("UNAUTHORIZED")
    if not isinstance(request_id,str) or not request_id:
        raise Stage131GateDenied("INVALID_SCOPE")
    if validate_artifact_descriptor(descriptor,now_epoch=now_epoch)!="DESCRIPTOR_VALID_NOT_AUTHORIZED":
        raise Stage131GateDenied("INVALID_OR_EXPIRED_ARTIFACT")
    # Exchange re-verifies principal, request_id, clock and SHA against stored bytes.
    return exchange.get_bytes(descriptor["artifact_id"],principal=authenticated_principal,request_id=request_id)

def bibliography_metadata_gate(doi, *, provider_approved=False, allow_network=False, fetcher=fetch_json_metadata):
    if provider_approved is not True or allow_network is not True:
        return {"status":"PROVIDER_DISABLED","doi":doi,"sources":{}}
    return lookup_doi_metadata(doi,allow_network=True,fetch_json=fetcher)
