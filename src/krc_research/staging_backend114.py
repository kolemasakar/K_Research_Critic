"""KRC stage114 staging-only four-operation backend adapter; no network listener."""
from .private_stage112 import dispatch_coded
from .private_contract_details import sanitized_error
OPS=frozenset(("research.profile.validate","research.evidence.preflight","research.bibliography.audit","research.inspection.review"))

def execute_staging_request(message, *, secret, signature, replay_registry, now=None,
                            bibliography_fn=None, allow_provider_network=False):
    """Restricted signed operation handler; external bibliography disabled by default."""
    if not isinstance(message,dict):
        return sanitized_error("INVALID_REQUEST")
    operation=message.get("operation")
    if operation not in OPS:
        return sanitized_error("OPERATION_DENIED")
    if operation=="research.bibliography.audit" and not allow_provider_network and bibliography_fn is None:
        return sanitized_error("OPERATION_DENIED")
    result=dispatch_coded(message,secret=secret,signature=signature,seen=replay_registry,
                          permitted=OPS,now=now,bibliography_fn=bibliography_fn)
    if not isinstance(result,dict):
        return sanitized_error("HANDLER_ERROR")
    return result

def staging_capabilities():
    """Static local inventory; never creates a job or calls research providers."""
    return {"contract":"krc-science/1","stage":"STAGING_ONLY",
            "operations":sorted(OPS),"network_listener":False,
            "production_enabled":False,"scientific_approval":False,
            "bibliography_default_external_access":False}
