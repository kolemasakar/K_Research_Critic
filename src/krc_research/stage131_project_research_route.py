"""Private single-owner STAGING project command route.

Trust: existing authorized remote command session as the dedicated OS user.
No HTTP endpoint, no new identity check, no deployed service changes.
One proposal contains the complete execution payload; approval is a separate
invocation after the owner has seen that exact profile. No paid/network work.
"""
import argparse
import hashlib
import json
import os
import re
import secrets
import sqlite3
import stat
import time
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker
from .stage131_n39_project_channel_consent import ProjectChannelVerifier, TrustedProjectConsentAdapter
from .stage131_n39_single_owner_chat_consent import SingleOwnerConsentLedger, canonical, profile_hash
from .science_signer127 import KRCInternalScienceSigner
from .science_adapter122 import ScienceAdapter122
from .private_dispatch_adapter import _schema_for
from .stage131_consumer_boundary_checks import validate_science_result
from .request_ledger119 import RequestLedger
from .replay_registry import ReplayRegistry
from .artifact_stage117 import HardenedExchange

PRINCIPAL="K_Science"
CHANNEL="KRC-personal-project"
OPS=frozenset(("research.profile.validate","research.evidence.preflight","research.inspection.review"))
MAX_PROFILE=512*1024
class RouteDenied(ValueError):
    pass

def private_root(path):
    p=Path(path)
    if not p.is_absolute() or p.is_symlink():
        raise RouteDenied("UNSAFE_STATE")
    p.mkdir(mode=0o700,parents=True,exist_ok=True)
    st=p.lstat()
    if not stat.S_ISDIR(st.st_mode) or st.st_uid!=os.geteuid() or st.st_mode & 0o077:
        raise RouteDenied("UNSAFE_STATE")
    return p

class ProjectResearchRoute:
    def __init__(self, root):
        self.root=private_root(root)
        self.verifier=ProjectChannelVerifier()
        self.consent=SingleOwnerConsentLedger(self.root/"consent.sqlite",verifier=self.verifier,authorized_principal=PRINCIPAL)
        self.adapter=TrustedProjectConsentAdapter(ledger=self.consent,verifier=self.verifier)
        self.requests=RequestLedger(self.root/"requests.sqlite")
        self.exchange=HardenedExchange(self.root/"artifacts")
        with self.consent._db() as db:
            db.execute("""CREATE TABLE IF NOT EXISTS project_profiles (
                request_id TEXT PRIMARY KEY, profile_json TEXT NOT NULL)""")

    def propose(self, profile):
        if not isinstance(profile,dict) or set(profile)!={"purpose","operation","payload","policy"}:
            raise RouteDenied("INVALID_PROFILE")
        if not isinstance(profile["purpose"],str) or not profile["purpose"].strip() or profile["policy"]!="FREE_ONLY_OFFLINE":
            raise RouteDenied("INVALID_POLICY")
        op=profile["operation"]
        if op not in OPS:
            raise RouteDenied("OFFLINE_OPERATION_NOT_ENABLED")
        if not Draft202012Validator(_schema_for(op),format_checker=FormatChecker()).is_valid(profile["payload"]):
            raise RouteDenied("INVALID_PAYLOAD")
        raw=canonical(profile)
        if len(raw)>MAX_PROFILE: raise RouteDenied("PROFILE_TOO_LARGE")
        rid="KS-"+secrets.token_hex(16)
        # Publish the complete proposal and its authoritative digest atomically.
        with self.consent._db() as db:
            db.execute("BEGIN IMMEDIATE")
            db.execute("INSERT INTO approvals(request_id,chat_id,profile_sha256,status) VALUES(?,?,?,'PROPOSED')",
                       (rid,CHANNEL,profile_hash(profile)))
            db.execute("INSERT INTO project_profiles VALUES(?,?)",(rid,raw.decode()))
            db.execute("COMMIT")
        return self.show(rid)

    def show(self,rid):
        if not isinstance(rid,str) or not re.fullmatch(r"KS-[0-9a-f]{32}",rid):
            raise RouteDenied("INVALID_REQUEST_ID")
        with self.consent._db() as db:
            row=db.execute("""SELECT a.profile_sha256,p.profile_json
                FROM approvals a JOIN project_profiles p USING(request_id)
                WHERE a.request_id=? AND a.chat_id=?""",(rid,CHANNEL)).fetchone()
        if not row: raise RouteDenied("MISSING_PROPOSAL")
        profile=json.loads(row[1])
        if profile_hash(profile)!=row[0]: raise RouteDenied("PROFILE_MISMATCH")
        return {"request_id":rid,"profile_sha256":row[0],"profile":profile,
                "status":self.consent.status(rid)}

    def decide(self,rid,digest,decision):
        proposal=self.show(rid)
        if digest!=proposal["profile_sha256"]: raise RouteDenied("PROFILE_MISMATCH")
        if not self.adapter.confirm_profile(request_id=rid,chat_id=CHANNEL,
                   profile=proposal["profile"],decision=decision):
            raise RouteDenied("DECISION_DENIED")
        return self.show(rid)

    def run(self,rid,digest):
        proposal=self.show(rid)
        if proposal["profile_sha256"]!=digest: raise RouteDenied("PROFILE_MISMATCH")
        if proposal["status"]!="APPROVED": raise RouteDenied("APPROVAL_REQUIRED_OR_ALREADY_USED")
        profile=proposal["profile"]
        op,payload=profile["operation"],profile["payload"]
        if op not in OPS: raise RouteDenied("OFFLINE_OPERATION_NOT_ENABLED")
        admitted=self.requests.admit(principal=PRINCIPAL,request_id=rid,operation=op,payload=profile)
        if admitted["decision"]!="EXECUTE": raise RouteDenied("REQUEST_ALREADY_ADMITTED")
        task=rid+"-task"
        key=secrets.token_bytes(32) # local ephemeral internal key; never exposed
        science=ScienceAdapter122(secret=key,allowed_principals={PRINCIPAL})
        science.seen=ReplayRegistry(self.root/"science-replay.sqlite")
        expected={"request_id":rid,"task_id":task,"operation":op,"principal":PRINCIPAL,
                  "profile_ref":digest,"evidence_refs":[],"payload_sha256":hashlib.sha256(canonical(payload)).hexdigest(),"consent_ref":rid}
        def authorize(context):
            return context==expected and self.consent.claim_execution(rid)
        def dispatch(operation,envelope,principal):
            if not self.consent.can_continue(rid): raise RouteDenied("CANCELLED_OR_EXPIRED")
            return science(operation,envelope,principal)
        signer=KRCInternalScienceSigner(science_key=key,authorizer=authorize,dispatcher=dispatch)
        result=signer.execute(request_id=rid,task_id=task,operation=op,payload=payload,
            principal=PRINCIPAL,profile_ref=digest,evidence_refs=[],consent_ref=rid)
        if validate_science_result(result,expected_task_id=task,expected_operation=op)!="VALID_SHAPE_ONLY":
            raise RouteDenied("INVALID_SCIENCE_RESULT")
        if not self.consent.can_continue(rid): raise RouteDenied("CANCELLED_OR_EXPIRED")
        artifact=self.exchange.store_bytes(canonical(result),principal=PRINCIPAL,request_id=rid,
            filename="research-result.json",media_type="application/json")
        output={"version":"krc-transport/2","request_id":rid,"status":"completed","delivery":"artifact","artifact":artifact}
        self.requests.complete(principal=PRINCIPAL,request_id=rid,operation=op,payload=profile,result=output)
        # Record artifact association and close execution together. If cancelled
        # or expired in the meantime, fail closed: bytes remain inaccessible.
        with self.consent._db() as db:
            db.execute("BEGIN IMMEDIATE")
            now=int(time.time())
            changed=db.execute("""UPDATE approvals SET status='COMPLETED',completed_at=?
                WHERE request_id=? AND status='RUNNING' AND expires_at>?""",(now,rid,now))
            if changed.rowcount!=1:
                db.execute("ROLLBACK")
                raise RouteDenied("CANCELLED_OR_EXPIRED")
            db.execute("INSERT INTO artifacts VALUES(?,?)",(artifact["artifact_id"],rid))
            db.execute("COMMIT")
        return output

    def read(self,rid):
        proposal=self.show(rid)
        if proposal["status"]!="COMPLETED": raise RouteDenied("READ_DENIED")
        with self.requests._db() as db:
            row=db.execute("SELECT state,result FROM requests WHERE principal=? AND request_id=?",
                           (PRINCIPAL,rid)).fetchone()
        if not row or row[0]!="COMPLETE": raise RouteDenied("READ_DENIED")
        output=json.loads(row[1])
        art=output["artifact"]
        if not self.consent.is_authorized(principal=PRINCIPAL,request_id=rid,artifact_id=art["artifact_id"]):
            raise RouteDenied("READ_DENIED")
        raw=b"".join(self.exchange.read_stream(art["artifact_id"],principal=PRINCIPAL,request_id=rid))
        if hashlib.sha256(raw).hexdigest()!=art["sha256"] or len(raw)!=art["size_bytes"]:
            raise RouteDenied("ARTIFACT_MISMATCH")
        if not self.consent.is_authorized(principal=PRINCIPAL,request_id=rid,artifact_id=art["artifact_id"]):
            raise RouteDenied("READ_DENIED")
        return {"descriptor":output,"result":json.loads(raw)}

def main(argv=None):
    os.umask(0o077)
    parser=argparse.ArgumentParser(description="Private offline staging project route")
    parser.add_argument("--state",required=True)
    sub=parser.add_subparsers(dest="cmd",required=True)
    p=sub.add_parser("propose");p.add_argument("profile_file")
    for cmd in ("show","read","approve","cancel","run"):
        p=sub.add_parser(cmd);p.add_argument("request_id")
        if cmd in ("approve","cancel","run"):p.add_argument("profile_sha256")
    a=parser.parse_args(argv)
    try:
        route=ProjectResearchRoute(a.state)
        if a.cmd=="propose":
            with open(a.profile_file,"rb") as f: raw=f.read(MAX_PROFILE+1)
            if len(raw)>MAX_PROFILE: raise RouteDenied("PROFILE_TOO_LARGE")
            result=route.propose(json.loads(raw))
        elif a.cmd in ("approve","cancel"):
            result=route.decide(a.request_id,a.profile_sha256,a.cmd.upper())
        elif a.cmd=="run": result=route.run(a.request_id,a.profile_sha256)
        else: result=getattr(route,a.cmd)(a.request_id)
        print(json.dumps(result,ensure_ascii=False,sort_keys=True))
    except (ValueError,OSError,sqlite3.Error) as exc:
        print(json.dumps({"status":"DENIED","error":str(exc) if isinstance(exc,RouteDenied) else type(exc).__name__}))
        return 1
    return 0

if __name__=="__main__":
    raise SystemExit(main())
