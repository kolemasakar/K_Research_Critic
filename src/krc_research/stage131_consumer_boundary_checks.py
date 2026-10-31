"""Read-only KRC boundary validation for science result and artifact manifests.

This module never signs, dispatches, fetches or grants access.
"""
import time

OPS=frozenset(("research.profile.validate","research.evidence.preflight","research.bibliography.audit","research.inspection.review"))

def validate_science_result(result, *, expected_task_id, expected_operation):
    if not isinstance(result,dict) or set(result)!={"task_id","operation","status","engine_result","scientific_approval"}:
        return "INVALID_SCIENCE_RESULT"
    if not isinstance(expected_task_id,str) or not expected_task_id or expected_operation not in OPS:
        return "INVALID_EXPECTED_CONTEXT"
    if result["task_id"]!=expected_task_id or result["operation"]!=expected_operation:
        return "CORRELATION_MISMATCH"
    if result["status"] not in ("PENDING","REVISE") or result["scientific_approval"] is not False:
        return "INVALID_SCIENCE_RESULT"
    if not isinstance(result["engine_result"],dict):
        return "INVALID_SCIENCE_RESULT"
    return "VALID_SHAPE_ONLY"

def validate_artifact_descriptor(descriptor, *, now_epoch=None):
    if not isinstance(descriptor,dict):
        return "INVALID_ARTIFACT"
    required={"artifact_id","filename","media_type","size_bytes","sha256","expires_at_epoch"}
    if not required.issubset(descriptor):
        return "INVALID_ARTIFACT"
    a=descriptor
    if not (isinstance(a["artifact_id"],str) and len(a["artifact_id"])==48 and all(ch in "0123456789abcdef" for ch in a["artifact_id"])):
        return "INVALID_ARTIFACT"
    if not (isinstance(a["sha256"],str) and len(a["sha256"])==64 and all(ch in "0123456789abcdef" for ch in a["sha256"])):
        return "INVALID_ARTIFACT"
    if not (isinstance(a["filename"],str) and a["filename"] and isinstance(a["media_type"],str) and a["media_type"]):
        return "INVALID_ARTIFACT"
    if type(a["size_bytes"]) is not int or a["size_bytes"]<0:
        return "INVALID_ARTIFACT"
    expiry=a["expires_at_epoch"]
    if type(expiry) not in (int,float) or not 0<expiry<float("inf"):
        return "INVALID_ARTIFACT"
    now=time.time() if now_epoch is None else now_epoch
    if type(now) not in (int,float) or not 0<=now<float("inf"):
        return "INVALID_CLOCK"
    return "EXPIRED" if expiry<=now else "DESCRIPTOR_VALID_NOT_AUTHORIZED"
