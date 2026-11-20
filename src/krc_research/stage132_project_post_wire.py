"""Shared Stage132 wire constants and strict bounded pilot descriptor check.

No project state, signer, provider, listener or service imports.
"""
import json
import math
import re

OP = "research.profile.validate"
IDENTITY = {"client":"K_Science","principal":"K_Science","repository":"kolemasakar/K_Science","workflow_ref":"refs/heads/main"}
MAX_EXTERNAL = 262144
RID = re.compile(r"KS-[0-9a-f]{32}\Z")

def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode("utf-8")

def denied():
    return 403, {"error":"OPERATION_DENIED"}

def conflict(rid, code="IDEMPOTENCY_CONFLICT"):
    return 409, {"request_id":rid,"status":"rejected","error":{"code":code}}

def ambiguous(rid):
    return 409, {"request_id":rid,"status":"pending_reconciliation","error":{"code":"AMBIGUOUS_REQUEST"}}

def valid_pilot_descriptor(a, *, now):
    if not isinstance(a,dict) or set(a)!={"artifact_id","filename","media_type","size_bytes","sha256","expires_at_epoch"}:return False
    expiry=a["expires_at_epoch"]
    return (isinstance(a["artifact_id"],str) and re.fullmatch(r"[0-9a-f]{48}",a["artifact_id"]) is not None
            and isinstance(a["sha256"],str) and re.fullmatch(r"[0-9a-f]{64}",a["sha256"]) is not None
            and a["filename"]=="research-result.json" and a["media_type"]=="application/json"
            and type(a["size_bytes"]) is int and 0<a["size_bytes"]<=1048576
            and type(expiry) in (int,float) and math.isfinite(expiry) and expiry>now)
