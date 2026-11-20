"""Stage132 pilot-only POST boundary. Source candidate, no automatic activation.

Only a verified KRC transport assertion may reach this boundary. The owner
approval and durable request ledger remain in the existing private project.
No external approval operation, no caller consent boolean, no fallback.
"""
import json
import re
import sqlite3
from contextlib import closing
from krc_research.stage131_project_research_route import ProjectResearchRoute, RouteDenied, PRINCIPAL
from krc_research.stage131_n39_single_owner_chat_consent import canonical
from krc_research.stage131_project_signed_read import ProjectArtifactAuthority, ReadDenied
from krc_research.request_ledger119 import LedgerError

OP = "research.profile.validate"
IDENTITY = {"client":"K_Science","principal":"K_Science","repository":"kolemasakar/K_Science","workflow_ref":"refs/heads/main"}
MAX_EXTERNAL = 262144
RID = re.compile(r"KS-[0-9a-f]{32}\Z")
def denied():
    return 403, {"error":"OPERATION_DENIED"}

def conflict(rid, code="IDEMPOTENCY_CONFLICT"):
    return 409, {"request_id":rid,"status":"rejected","error":{"code":code}}

def ambiguous(rid):
    return 409, {"request_id":rid,"status":"pending_reconciliation","error":{"code":"AMBIGUOUS_REQUEST"}}

def validate_payload(payload):
    if not isinstance(payload,dict) or set(payload)!={"critic_profile"}:
        return False
    cp=payload["critic_profile"]
    return (isinstance(cp,dict) and set(cp)=={"profile_id","version","protocol","topic"}
            and all(isinstance(v,str) and bool(v.strip()) for v in cp.values())
            and cp["protocol"] in ("KRC Core","Scholarly Research"))

class ProjectPostBoundary:
    def __init__(self, root, *, enabled=False):
        self.root=root
        self.enabled=enabled is True
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
        if envelope["operation"]!=OP or not validate_payload(envelope["payload"]):
            return denied()
        try:
            if len(canonical({k:envelope[k] for k in ("request_id","operation","payload")}))>MAX_EXTERNAL:
                return denied()
            route=ProjectResearchRoute(self.root)
            try: proposal=route.show(rid)
            except RouteDenied as exc:
                if str(exc)=="MISSING_PROPOSAL":return denied()
                return ambiguous(rid)
            profile=proposal["profile"]
            # The approved full immutable profile, including purpose/policy, is
            # looked up by server-generated ID. Never trust a client digest.
            if profile["operation"]!=OP or profile["policy"]!="FREE_ONLY_OFFLINE":
                return denied()
            if canonical(profile["payload"])!=canonical(envelope["payload"]):
                return conflict(rid)
            status=proposal["status"]
            if status in ("PROPOSED","CANCELLED","EXPIRED","EXPIRED_RUNNING","MISSING"):
                return denied()
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
