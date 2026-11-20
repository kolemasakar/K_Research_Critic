"""Synthetic isolated state; existing project producer used without mocks."""
import copy
import hashlib
import os
import sqlite3
import threading
from concurrent.futures import ThreadPoolExecutor
import pytest
from krc_research.stage131_project_research_route import ProjectResearchRoute
from krc_research.stage131_project_signed_read import ProjectArtifactAuthority,ReadDenied
from krc_research.replay_registry import ReplayRegistry
from krc_research.stage132_project_post_contract import ProjectPostBoundary,IDENTITY,OP

PROFILE={"purpose":"Synthetic test only","operation":OP,"policy":"FREE_ONLY_OFFLINE",
         "payload":{"critic_profile":{"profile_id":"test-pilot","version":"v1",
             "protocol":"KRC Core","topic":"Synthetic concrete NDT"}}}

@pytest.fixture
def fixture(tmp_path):
    old=os.umask(0o077)
    try:
        route=ProjectResearchRoute(tmp_path/"private")
        ReplayRegistry(route.root/"science-replay.sqlite")
        proposal=route.propose(copy.deepcopy(PROFILE))
        envelope={"version":"krc-transport/2","identity":dict(IDENTITY),
                  "request_id":proposal["request_id"],"operation":OP,
                  "payload":copy.deepcopy(PROFILE["payload"])}
        yield route,proposal,envelope
    finally:os.umask(old)

def count(route):
    with sqlite3.connect(route.root/"science-replay.sqlite") as c:
        return c.execute("select count(*) from requests").fetchone()[0]

def call(route,envelope,enabled=True,principal="K_Science"):
    return ProjectPostBoundary(route.root,enabled=enabled).execute(envelope,trusted_principal=principal)

def approve(route,p):
    return route.decide(p["request_id"],p["profile_sha256"],"APPROVE")

def test_actual_result_and_shared_get_authority(fixture):
    r,p,e=fixture;approve(r,p)
    status,out=call(r,e); assert status==200
    assert out["request_id"]==p["request_id"] and out["status"]=="completed"
    a=out["artifact"];scope={"request_id":p["request_id"],"artifact_id":a["artifact_id"],"principal":"K_Science"}
    f,d=ProjectArtifactAuthority(r.root).spool(scope)
    with f:raw=f.read()
    assert d=={**a,"request_id":p["request_id"]}
    assert len(raw)==a["size_bytes"] and hashlib.sha256(raw).hexdigest()==a["sha256"]
    assert r.read(p["request_id"])["result"]["task_id"]==p["request_id"]+"-task"
    assert r.read(p["request_id"])["result"]["scientific_approval"] is False
    assert call(r,e)[0]==409 and count(r)==1
    r.decide(p["request_id"],p["profile_sha256"],"CANCEL")
    assert call(r,e)[0]==403
    with pytest.raises(ReadDenied) as exc:ProjectArtifactAuthority(r.root).descriptor(scope)
    assert exc.value.status==403 and count(r)==1

@pytest.mark.parametrize("kind",["default_off","proposed","wrong_principal","wrong_identity","wrong_id","fake_approval","other_operation","cancelled","expired","mismatch","untrusted_extra","missing_db"])
def test_denials_no_execution(fixture,kind):
    r,p,e=fixture
    if kind!="proposed":approve(r,p)
    principal="K_Science";enabled=True;expected=403
    if kind=="default_off":enabled=False
    elif kind=="wrong_principal":principal="OTHER"
    elif kind=="wrong_identity":e["identity"]["repository"]="other/repo"
    elif kind=="wrong_id":e["request_id"]="KS-"+"f"*32
    elif kind=="fake_approval":e["payload"]["user_profile_approved"]=True
    elif kind=="other_operation":e["operation"]="research.bibliography.audit"
    elif kind=="cancelled":r.decide(p["request_id"],p["profile_sha256"],"CANCEL")
    elif kind=="expired":
        with r.consent._db() as db:db.execute("update approvals set expires_at=1 where request_id=?",(p["request_id"],))
    elif kind=="mismatch":e["payload"]["critic_profile"]["topic"]="changed";expected=409
    elif kind=="untrusted_extra":e["consent"]=True
    elif kind=="missing_db":
        (r.root/"science-replay.sqlite").rename(r.root/"science-replay.offline");expected=409
    assert call(r,e,enabled,principal)[0]==expected
    if kind=="missing_db":assert not (r.root/"science-replay.sqlite").exists()
    else:assert count(r)==0

def test_concurrent_admission(fixture):
    r,p,e=fixture;approve(r,p)
    barrier=threading.Barrier(6)
    def run(_):barrier.wait();return call(r,e)[0]
    with ThreadPoolExecutor(max_workers=6) as pool: statuses=list(pool.map(run,range(6)))
    assert statuses.count(200)==1 and all(s==409 for s in statuses if s!=200)
    assert count(r)==1

def test_ambiguous_existing_admission_no_redispatch(fixture):
    r,p,e=fixture;approve(r,p)
    r.requests.admit(principal="K_Science",request_id=p["request_id"],operation=OP,payload=p["profile"])
    status,body=call(r,e)
    assert status==409 and body["error"]["code"]=="AMBIGUOUS_REQUEST"
    assert count(r)==0
