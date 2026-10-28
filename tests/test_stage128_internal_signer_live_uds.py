"""Isolated live UDS integration of opt-in KRC-owned science signing.

Root-ownership in these fixtures is mocked; actual host approval not claimed.
"""
import hashlib,hmac,json,os,socket,threading,time
from datetime import datetime,timezone
from pathlib import Path
from unittest.mock import patch
from test_staging_service123c import IDENTITY,KEY,SECRET,post
from test_consent_custody128 import root_dir_stat,root_file_stat
from krc_research.staging_service123c import make_staging_server
from krc_research.transport_auth123b import canonical
from krc_research.consent_custody128 import fingerprint

def signed(rid,tid,ref):
    scientific={"critic_profile":{"profile_id":"p1","version":"1","protocol":"KRC Core","topic":"Synthetic gate"}}
    payload={"task_id":tid,"profile_ref":"p1","evidence_refs":[],"consent_ref":ref,"science_payload":scientific}
    body={"version":"krc-transport/2","request_id":rid,"operation":"research.profile.validate","identity":IDENTITY,"payload":payload}
    stamp=datetime.now(timezone.utc).isoformat()
    binding={"domain":"KRC-TRANSPORT-IDENTITY/2","key_id":"stage","issued_at":stamp,"envelope":body}
    body["transport_auth"]={"alg":"HMAC-SHA256","key_id":"stage","issued_at":stamp,"mac":hmac.new(KEY,canonical(binding),hashlib.sha256).hexdigest()}
    context=dict(request_id=rid,task_id=tid,operation=body["operation"],principal="K_Science",profile_ref="p1",evidence_refs=[],payload_sha256=hashlib.sha256(json.dumps(scientific,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode()).hexdigest(),consent_ref=ref)
    return body,context

def test_optin_authorized_and_negative_replay(tmp_path):
    approvals=tmp_path/"approvals";approvals.mkdir();approvals.chmod(0o755)
    root=tmp_path/"state";root.mkdir(mode=0o700);root.chmod(0o700)
    rid="KS-"+"1"*32;tid="ks126-"+"2"*32;ref="approval-synthetic-0001"
    message,context=signed(rid,tid,ref)
    (approvals/(ref+".json")).write_text(json.dumps({"consent_ref":ref,"context_sha256":fingerprint(context),"approver":"SYNTHETIC_OWNER_FIXTURE","approved_at":int(time.time())-1,"expires_at":int(time.time())+120}))
    (approvals/(ref+".json")).chmod(0o644)
    opts={"peer_principals":{os.getuid():"K_Science"},"uid_keys":{os.getuid():{"stage":KEY}},
          "claim_allowlist":{tuple(IDENTITY.values())},"science_secret":SECRET,
          "enable_internal_science_signing":True,"consent_approvals_dir":str(approvals)}
    from krc_research import consent_custody128
    Original=consent_custody128.ConsentCustody128
    def fixture_custody(path,*,approvals_dir):\n        assert approvals_dir==str(approvals)\n        return Original(path,approvals_dir=approvals_dir)
    with patch.object(Path,"lstat",root_dir_stat),patch("os.fstat",root_file_stat),patch("krc_research.staging_service123c.ConsentCustody128",fixture_custody):
        def serve_once(data,sock_name):
            sock=tmp_path/sock_name
            server=make_staging_server(sock,root,**opts)
            thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
            try:return post(sock,data)
            finally:server.shutdown();server.server_close();thread.join();sock.unlink()
        first=serve_once(message,"backend1.sock")
        assert b"200 OK" in first
        assert b'"scientific_approval":false' in first
        # Different outer request ID cannot reuse the same grant.
        modified,_=signed("KS-"+"3"*32,tid,ref)
        second=serve_once(modified,"backend2.sock")
        assert b"409 Conflict" in second
        # Wrong/unknown consent cannot be approved even with correctly signed transport.
        other,_=signed("KS-"+"4"*32,"ks126-"+"5"*32,"approval-synthetic-9999")
        third=serve_once(other,"backend3.sock")
        assert b"409 Conflict" in third
