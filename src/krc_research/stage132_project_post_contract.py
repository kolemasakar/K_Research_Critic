"""Stage132 pilot-only POST boundary. Source candidate, no automatic activation.

Only a verified KRC transport assertion may reach this boundary. The owner
approval and durable request ledger remain in the existing private project.
No external approval operation, no caller consent boolean, no fallback.
"""
import sqlite3
from contextlib import closing
from krc_research.stage131_project_research_route import ProjectResearchRoute, RouteDenied, PRINCIPAL
from krc_research.stage131_n39_single_owner_chat_consent import canonical
from krc_research.stage131_project_signed_read import ProjectArtifactAuthority, ReadDenied, ro
from krc_research.request_ledger119 import LedgerError

from krc_research.stage132_project_post_wire import (OP,IDENTITY,MAX_EXTERNAL,RID,denied,conflict,ambiguous,valid_pilot_descriptor)
import time
from jsonschema import Draft202012Validator, FormatChecker
from krc_research.private_dispatch_adapter import _schema_for
from krc_research.stage132_project_post_wire import PREFLIGHT, INSPECTION, DEFAULT_OPS, checked_ops

def valid_operation_payload(op, payload):
    if op == OP:
        return validate_payload(payload)
    if not isinstance(payload, dict):
        return False
    if op == PREFLIGHT:
        if "user_profile_approved" in payload:
            return False
        candidate = {**payload, "user_profile_approved": True}
    elif op == INSPECTION:
        receipt = payload.get("receipt")
        if not isinstance(receipt, dict) or receipt.get("trace_verified", False) is not False:
            return False
        candidate = payload
    else:
        return False
    return Draft202012Validator(_schema_for(op), format_checker=FormatChecker()).is_valid(candidate)

def validate_payload(payload):
    if not isinstance(payload,dict) or set(payload)!={"critic_profile"}:
        return False
    cp=payload["critic_profile"]
    return (isinstance(cp,dict) and set(cp)=={"profile_id","version","protocol","topic"}
            and all(isinstance(v,str) and bool(v.strip()) for v in cp.values())
            and cp["protocol"] in ("KRC Core","Scholarly Research"))

class ProjectPostBoundary:
    def __init__(self, root, *, enabled=False, enabled_operations=DEFAULT_OPS):
        self.root=root
        self.enabled=enabled is True
        self.enabled_operations=checked_ops(enabled_operations)
    def execute(self, envelope, *, trusted_principal):
        if not self.enabled or trusted_principal!=PRINCIPAL:
            return denied()
        if not isinstance(envelope,dict) or set(envelope)!={"version","identity","request_id","operation","payload"}:
            return denied()
        if envelope["version"]!="krc-transport/2" or envelope["identity"]!=IDENTITY:
            return denied()
        rid=envelope["request_id"]
        if not isinstance(rid,str) or not RID.fullmatch(rid):
            return denied()
        op=envelope["operation"]
        if not isinstance(op,str) or op not in self.enabled_operations or not valid_operation_payload(op,envelope["payload"]):
            return denied()
        try:
            if len(canonical({k:envelope[k] for k in ("request_id","operation","payload")}))>MAX_EXTERNAL:
                return denied()
            # Fail closed if existing authority is missing; do not provision
            # or repair private databases through an external request.
            root=ProjectArtifactAuthority(self.root).root
            for name,tables in (("consent.sqlite",("approvals","project_profiles","artifacts")),
                                ("requests.sqlite",("requests",)),
                                ("artifacts/index.sqlite3",("objects",)),
                                ("science-replay.sqlite",("requests",))):
                with closing(ro(root/name)) as db:
                    for table in tables:
                        db.execute("SELECT * FROM "+table+" LIMIT 0")
            route=ProjectResearchRoute(root)
            try: proposal=route.show(rid)
            except RouteDenied as exc:
                if str(exc)=="MISSING_PROPOSAL":return denied()
                return ambiguous(rid)
            profile=proposal["profile"]
            # The approved full immutable profile, including purpose/policy, is
            # looked up by server-generated ID. Never trust a client digest.
            if profile["operation"]!=op or profile["policy"]!="FREE_ONLY_OFFLINE":
                return denied()
            status=proposal["status"]
            if status in ("PROPOSED","CANCELLED","EXPIRED","EXPIRED_RUNNING","MISSING"):
                return denied()
            if canonical(profile["payload"])!=canonical(envelope["payload"]):
                return conflict(rid)
            if status in ("RUNNING","COMPLETED"):
                return ambiguous(rid)
            if status!="APPROVED":
                return denied()
            # run re-reads approved state, admits in the durable RequestLedger,
            # claims exactly once and checks cancellation/expiry before dispatch.
            try:
                result=route.run(rid,proposal["profile_sha256"])
            except (RouteDenied,LedgerError):
                # A race or lost response may already have consumed the grant.
                # Never dispatch again or return a cached success.
                return ambiguous(rid)
            if not isinstance(result,dict) or set(result)!={"version","request_id","status","delivery","artifact"}:
                return ambiguous(rid)
            if (result["version"],result["request_id"],result["status"],result["delivery"])!=("krc-transport/2",rid,"completed","artifact"):
                return ambiguous(rid)
            a=result["artifact"]
            if not valid_pilot_descriptor(a,now=time.time()):return ambiguous(rid)
            authority=ProjectArtifactAuthority(route.root)
            d=authority.descriptor({"request_id":rid,"artifact_id":a["artifact_id"],"principal":PRINCIPAL})
            if d!={**a,"request_id":rid}:
                return ambiguous(rid)
            # The existing GET authority uses this same producer state and
            # rechecks consent and TTL independently; POST never grants GET.
            return 200,result
        except ReadDenied as exc:
            return denied() if exc.status==403 else ambiguous(rid)
        except (ValueError,OSError,sqlite3.Error,KeyError,TypeError,LedgerError):
            return ambiguous(rid)
        except Exception:
            return ambiguous(rid)
