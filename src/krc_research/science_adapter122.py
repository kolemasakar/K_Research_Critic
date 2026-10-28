"""Staging adapter for KRC's real four-operation offline dispatcher.

This is NOT the deployed transport bridge. A persistent replay registry and
trusted UDS identity binding are still required.
"""
from .private_stage112 import dispatch_coded
from .staging_backend114 import OPS

class ScienceAdapter122:
    def __init__(self, *, secret, allowed_principals, bibliography_fn=None):
        if not isinstance(secret,bytes) or len(secret)<32:
            raise ValueError("Invalid secret")
        self.secret=secret
        self.allowed_principals=frozenset(allowed_principals)
        self.bibliography_fn=bibliography_fn
        self.seen=set()  # Offline tests only; not durable across restart.

    def __call__(self,operation,payload,principal):
        if principal not in self.allowed_principals:
            raise PermissionError("UNAUTHORIZED")
        if operation not in OPS:
            raise PermissionError("OPERATION_DENIED")
        if not isinstance(payload,dict):
            raise ValueError("INVALID_REQUEST")
        body=payload.get("science_envelope")
        signature=payload.get("science_signature")
        if not isinstance(body,dict) or body.get("operation")!=operation:
            raise ValueError("INVALID_REQUEST")
        if operation=="research.bibliography.audit" and self.bibliography_fn is None:
            raise PermissionError("OPERATION_DENIED")
        result=dispatch_coded(body,secret=self.secret,signature=signature,
                              seen=self.seen,permitted=OPS,
                              bibliography_fn=self.bibliography_fn)
        if result.get("status")=="error":
            raise ValueError(result["error"]["code"])
        return result
