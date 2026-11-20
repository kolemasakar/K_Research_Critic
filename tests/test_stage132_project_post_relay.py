"""Actual isolated wire chain, synthetic verified OIDC/Tailnet identities.

Sentinel runtime and client verifier are from separately pinned companion
repositories. No live listener, key, approval, state or provider is used.
"""
import contextlib
import copy
import hashlib
import http.client
import json
import os
import threading
import time
import uuid
import pytest
from krc_research.stage132_project_post_contract import OP,IDENTITY,ProjectPostBoundary
from krc_research.stage132_project_post_relay import (
    RelayAuthority,RelayServer,RelayClient,attach_pilot,make_message)
from krc_research.stage131_artifact_nonce_registry import ArtifactNonceRegistry
from krc_research.stage131_project_research_route import ProjectResearchRoute
from krc_research.replay_registry import ReplayRegistry
from krc_research.stage131_project_signed_read import ProjectArtifactAuthority,ProjectSignedArtifactBoundary,KEY_ID
from krc_research.stage131_signed_artifact_uds import SignedArtifactUDSServer
from krc_research.staging_service123c import make_staging_server
from test_stage132_project_post_contract import PROFILE,count,approve

TRANS=b"t"*32
RELAY=b"r"*32
READ=b"g"*32
UID=os.getuid()
GID=os.getgid()
KEY_ID_POST="stage126-v1"

@contextlib.contextmanager
def running(server):
    t=threading.Thread(target=server.serve_forever,daemon=True)
    t.start()
    try:yield server
    finally:
        server.shutdown();server.server_close();t.join(5)
        assert not t.is_alive()

@pytest.fixture
def chain(tmp_path):
    # The installed companion sources are deliberately an explicit dependency,
    # supplied via PYTHONPATH by the isolated integration test runner.
    auth=pytest.importorskip("authenticated_admission123d")
    runtime=pytest.importorskip("stage127_get_runtime")
    from artifact_get_stage127_release_candidate import Stage127RetrievalAdmission,EXPECTED_STAGE127
    from artifact_get_project_adapter127 import ProjectReadAdapter
    from claims_bridge127 import krc_identity_from_verified_claims
    from oidc_replay123e import DurableOIDCReplay
    from krc_uds_client import create_pinned_staging_client
    old=os.umask(0o077)
    try:
        r=ProjectResearchRoute(tmp_path/"private")
        ReplayRegistry(r.root/"science-replay.sqlite")
        p=r.propose(copy.deepcopy(PROFILE))
        registry=ArtifactNonceRegistry(tmp_path/"relay-nonce.sqlite")
        relay=RelayAuthority(boundary=ProjectPostBoundary(r.root,enabled=True),
                             registry=registry,key=RELAY,peer_uid=UID,peer_gid=GID)
        relay_path=tmp_path/"relay.sock"
        relay_srv=RelayServer(relay_path,authority=relay)
        os.chmod(relay_path,0o660)
        relay_client=RelayClient(relay_path,key=RELAY,expected_uid=UID,expected_gid=GID)
        legacy_path=tmp_path/"legacy.sock"
        claims={tuple(IDENTITY[k] for k in ("client","principal","repository","workflow_ref"))}
        gateway=make_staging_server(legacy_path,tmp_path/"legacy",
                peer_principals={UID:"K_Science"},uid_keys={UID:{KEY_ID_POST:TRANS}},
                claim_allowlist=claims,science_secret=b"s"*32,enable_internal_science_signing=False)
        attach_pilot(gateway,relay_client)
        os.chmod(legacy_path,0o660)
        backend=create_pinned_staging_client(str(legacy_path),expected_uid=UID,expected_gid=GID,
                                            expected_socket_gid=GID)
        reader_path=tmp_path/"read.sock"
        reader=SignedArtifactUDSServer(reader_path,boundary=ProjectSignedArtifactBoundary(
            authority=ProjectArtifactAuthority(r.root),nonce_registry=ArtifactNonceRegistry(tmp_path/"read-nonce.sqlite"),
            key=READ,peer_uid=UID,enabled=True))
        os.chmod(reader_path,0o660)
        class OIDC:
            expected_claims=EXPECTED_STAGE127
            def verify(self,token):
                if token=="bad":raise auth.AdmissionDenied("DENIED")
                return {**EXPECTED_STAGE127,"jti":token,"exp":int(time.time())+180}
        class Tailnet:
            def verify(self,ip):
                assert ip=="127.0.0.1"
                return "test-peer"
        oidc,tailnet=OIDC(),Tailnet()
        replay=DurableOIDCReplay(str(tmp_path/"oidc.sqlite"))
        signer=auth.AuthenticatedStagingSigner(oidc_verifier=oidc,tailnet_verifier=tailnet,
            key=TRANS,key_id=KEY_ID_POST,allowed_peer_ids=set(),replay_registry=replay,
            identity_projector=lambda claims,pid,ids:krc_identity_from_verified_claims(
                claims,peer_stable_id=pid,allowed_peer_ids=ids,expected_claims=EXPECTED_STAGE127,
                ephemeral_tag_oidc_policy=True),ephemeral_tag_oidc_policy=True)
        admission=Stage127RetrievalAdmission(oidc=oidc,tailnet=tailnet,replay=replay,key=READ,key_id=KEY_ID)
        adapter=ProjectReadAdapter(socket_path=str(reader_path),key=READ,expected_uid=UID,
                                   expected_gid=GID,enabled=True)
        http=runtime.RuntimeStage127Server(("127.0.0.1",0),signer=signer,backend=backend,
                enabled=True,admission=admission,adapter=adapter,allow_loopback_fixture=True,audit=lambda _:None)
        def http_call(method,path,body=None,token=None,headers=None):
            hh={"Authorization":"Bearer "+(token or uuid.uuid4().hex),"Connection":"close",**(headers or {})}
            if body is not None:hh["Content-Type"]="application/json";body=json.dumps(body).encode()
            c=http.client.HTTPConnection("127.0.0.1",http.server_address[1],timeout=20)
            try:
                c.request(method,path,body=body,headers=hh)
                out=c.getresponse();return out.status,dict(out.getheaders()),out.read()
            finally:c.close()
        request={"request_id":p["request_id"],"operation":OP,"payload":copy.deepcopy(PROFILE["payload"])}
        with running(relay_srv),running(gateway),running(reader),running(http):
            yield r,p,request,http_call,relay,relay_client
    finally:os.umask(old)

def test_complete_post_get_science_receiver(chain):
    pilot=pytest.importorskip("stage127_science_pilot")
    r,p,req,http,_,_=chain
    assert http("POST","/staging/v2/execute",req)[0]==403
    proposal=approve(r,p)
    prepared=pilot.prepare_post(proposal,displayed_profile=PROFILE,expected_request_id=p["request_id"])
    assert prepared["request"]==req and prepared["sent"] is False
    status,_,raw=http("POST","/staging/v2/execute",prepared["request"],token="post-one")
    assert status==200
    d=json.loads(raw)
    assert http("POST","/staging/v2/execute",req,token="post-one")[0]==403
    assert http("POST","/staging/v2/execute",req,token="post-two")[0]==409
    a=d["artifact"];get_path="/staging/v2/artifacts/"+a["artifact_id"]
    st,h,b=http("GET",get_path,headers={"X-KRC-Request-ID":p["request_id"]})
    out=pilot.accept_profile_result(d,b,displayed_profile=PROFILE,expected_request_id=p["request_id"],
        expected_task_id=p["request_id"]+"-task",now_epoch=time.time(),headers=h,http_status=st)
    assert out["status"]=="PILOT_RESULT_SHAPE_VERIFIED" and out["scientific_approval"] is False
    assert hashlib.sha256(b).hexdigest()==a["sha256"] and count(r)==1
    r.decide(p["request_id"],p["profile_sha256"],"CANCEL")
    assert http("GET",get_path,headers={"X-KRC-Request-ID":p["request_id"]})[0]==403
    assert count(r)==1

def test_auth_and_no_fallback(chain):
    r,p,req,http,relay,client=chain;approve(r,p)
    assert http("POST","/staging/v2/execute",req,token="bad")[0]==403
    changed=copy.deepcopy(req);changed["payload"]["critic_profile"]["topic"]="foreign"
    st,_,raw=http("POST","/staging/v2/execute",changed)
    assert st==409 and json.loads(raw)["error"]["code"]=="IDEMPOTENCY_CONFLICT"
    assert http("POST","/staging/v2/execute",dict(req,payload={**req["payload"],"user_profile_approved":True}))[0]==403
    old=client.path;client.path=str(r.root/"absent.sock")
    st,_,raw=http("POST","/staging/v2/execute",req)
    assert st==409 and json.loads(raw)["error"]["code"]=="AMBIGUOUS_REQUEST"
    client.path=old
    # Transport-only probe preserves the previous rejection.
    assert http("POST","/staging/v2/execute",{"request_id":"KS-"+uuid.uuid4().hex,"operation":"transport.probe","payload":{}})[0]==403
    assert count(r)==0

def test_relay_peer_mac_nonce_before_owner_approval(chain):
    r,p,req,http,relay,_=chain
    e={"version":"krc-transport/2","identity":dict(IDENTITY),**req}
    m=make_message(e,RELAY)
    assert relay.accept(m,credentials=(UID+1,GID))[0]==403
    bad=copy.deepcopy(m);bad["mac"]="0"*64
    assert relay.accept(bad,credentials=(UID,GID))[0]==403
    assert relay.accept(m,credentials=(UID,GID))[0]==403
    approve(r,p)
    # Previously denied valid signed relay message cannot become an execution.
    assert relay.accept(m,credentials=(UID,GID))[0]==403 and count(r)==0
    assert relay.accept(make_message(e,RELAY),credentials=(UID,GID))[0]==200 and count(r)==1
