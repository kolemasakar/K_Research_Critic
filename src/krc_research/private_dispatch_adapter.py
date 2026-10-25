"""Isolated contract-checked KRC dispatcher. No server listener and no network side effects implied."""
from jsonschema import Draft202012Validator, FormatChecker
from .private_contract_schemas import contracts
from .private_contract_details import CLAIM, RECEIPT, sanitized_error
from .science_dispatch import handle_science_request

def _schema_for(op):
    spec=contracts()["operations"].get(op)
    if spec is None: raise ValueError("Unsupported operation")
    schema=dict(spec["inputSchema"])
    schema["additionalProperties"]=False
    properties=dict(schema.get("properties",{}))
    if op=="research.evidence.preflight":
        properties["claims"]={"type":"array","items":CLAIM}
    elif op=="research.inspection.review":
        properties["receipt"]=RECEIPT
    schema["properties"]=properties
    return schema

def dispatch_validated(message, *, secret, signature, seen, permitted, now=None,
                       bibliography_fn=None):
    """Never expose internal exception strings; preserve signed-envelope ACL and replay."""
    try:
        if not isinstance(message,dict): return sanitized_error("INVALID_REQUEST")
        op=message.get("operation")
        schema=_schema_for(op)
        payload=message.get("payload")
        if not Draft202012Validator(schema,format_checker=FormatChecker()).is_valid(payload):
            return sanitized_error("INVALID_REQUEST")
        kw={"secret":secret,"signature":signature,"seen":seen,"permitted":permitted,"now":now}
        if bibliography_fn is not None: kw["bibliography_fn"]=bibliography_fn
        return handle_science_request(message,**kw)
    except (ValueError,TypeError,KeyError):
        return sanitized_error("HANDLER_ERROR")
