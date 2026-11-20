"""Separate process uses the exact old gateway source and only new wire/runtime overlay."""
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
import pytest
from krc_research.stage132_project_post_relay import RelayAuthority,RelayServer
from krc_research.stage132_project_post_contract import ProjectPostBoundary,OP,IDENTITY
from krc_research.stage131_artifact_nonce_registry import ArtifactNonceRegistry
from krc_research.stage131_project_research_route import ProjectResearchRoute
from krc_research.replay_registry import ReplayRegistry
from test_stage132_project_post_contract import PROFILE,approve,count
from test_stage132_project_post_relay import running,UID,GID,TRANS,RELAY,KEY_ID_POST

def test_exact_installed_gateway_factory(tmp_path):
    legacy=os.getenv("KRC_STAGE132_LEGACY_SRC")
    if not legacy:pytest.skip("Installed legacy gateway source is an explicit dependency")
    from krc_uds_client import create_pinned_staging_client,IPCError
    from identity_assertion import sign_assertion
    old=os.umask(0o077)
    try:
        route=ProjectResearchRoute(tmp_path/"private")
        ReplayRegistry(route.root/"science-replay.sqlite")
        proposal=route.propose(PROFILE)
        approve(route,proposal)
        path=tmp_path/"relay.sock"
        relay=RelayServer(path,authority=RelayAuthority(boundary=ProjectPostBoundary(route.root,enabled=True),
            registry=ArtifactNonceRegistry(tmp_path/"relay.sqlite"),key=RELAY,peer_uid=UID,peer_gid=GID))
        os.chmod(path,0o660)
        overlay=tmp_path/"overlay";pkg=overlay/"krc_research";pkg.mkdir(parents=True)
        import krc_research.stage132_project_post_relay as mod
        for name in ("stage132_project_post_wire.py","stage132_project_post_relay.py","stage132_project_post_runtime.py"):
            shutil.copyfile(Path(mod.__file__).parent/name,pkg/name)
        sock=tmp_path/"gateway.sock"
        c={"peer_uid":UID,"principal":"K_Science","client":"K_Science","repository":"kolemasakar/K_Science","workflow_ref":"refs/heads/main","key_id":KEY_ID_POST,"socket_path":str(sock),"state_root":str(tmp_path/"legacy")}
        script="""import os,sys,json,threading
from pathlib import Path
import krc_research.staging_service123c as original
from krc_research.stage132_project_post_runtime import compose_gateway,serve
from krc_research.stage132_project_post_relay import RelayClient
assert Path(original.__file__).is_relative_to(Path(sys.argv[1]))
c=json.loads(sys.argv[2])
relay=RelayClient(sys.argv[3],key=b'r'*32,expected_uid=os.getuid(),expected_gid=os.getgid())
serve(compose_gateway(c,transport=b't'*32,science=b's'*32,relay=relay),Path(c['socket_path']),stop=threading.Event())
"""
        env={**os.environ,"PYTHONPATH":str(overlay)+os.pathsep+legacy,"PYTHONNOUSERSITE":"1"}
        with running(relay):
            proc=subprocess.Popen([sys.executable,"-s","-c",script,legacy,json.dumps(c),str(path)],env=env)
            try:
                for _ in range(200):
                    if proc.poll() is not None:raise AssertionError("GATEWAY_EXITED")
                    if sock.exists() and os.stat(sock).st_mode & 0o777==0o660:break
                    time.sleep(.025)
                else:raise AssertionError("GATEWAY_NOT_READY")
                client=create_pinned_staging_client(str(sock),expected_uid=UID,expected_gid=GID)
                envelope={"version":"krc-transport/2","request_id":proposal["request_id"],"identity":dict(IDENTITY),"operation":OP,"payload":PROFILE["payload"]}
                result=client.execute(sign_assertion(envelope,key=TRANS,key_id=KEY_ID_POST))
                assert result["status"]=="completed" and result["request_id"]==proposal["request_id"]
                assert count(route)==1
                with pytest.raises(IPCError) as err:
                    client.execute(sign_assertion(envelope,key=TRANS,key_id=KEY_ID_POST))
                assert err.value.code=="AMBIGUOUS_REQUEST" and count(route)==1
            finally:
                proc.terminate();proc.wait(timeout=10)
    finally:os.umask(old)
