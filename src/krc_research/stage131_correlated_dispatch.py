"""Fail-closed staging adapter: validate actual inner result against request context.

Not installed or registered with running Stage131. No scientific dispatch here.
"""
from .stage131_consumer_boundary_checks import validate_science_result

class ScienceResultContractError(ValueError):
    pass

def execute_correlated(dispatch, *, operation, payload, principal, request_id):
    """Adapter for a reviewed signer-enabled InternalAuthorizedDispatch only.

    Requires an independently trusted task_id from the already admitted request.
    The call cannot grant consent or authorize execution; dispatch must enforce these.
    """
    if not callable(dispatch):
        raise ScienceResultContractError("DISPATCH_UNAVAILABLE")
    if not isinstance(payload,dict) or not isinstance(payload.get("task_id"),str) or not payload["task_id"]:
        raise ScienceResultContractError("INVALID_REQUEST")
    result=dispatch(operation,payload,principal,request_id=request_id)
    decision=validate_science_result(result,expected_task_id=payload["task_id"],expected_operation=operation)
    if decision!="VALID_SHAPE_ONLY":
        raise ScienceResultContractError(decision)
    return result
