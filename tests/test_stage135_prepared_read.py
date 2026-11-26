import copy
import hashlib
import hmac
import os
import socket
import tempfile
import threading
import unittest
from pathlib import Path
from krc_research.stage135_prepared_read import (
    Registry, Reader, Denied, VERSION, OPERATION, KEY_ID, canonical, digest, signing_bytes)
from krc_research.stage135_prepared_uds import PreparedServer, PATH

RID="KS-"+"a"*32
WF="kolemasakar/K_Science/.github/workflows/synthetic.yml@refs/heads/main"
IDENT=dict(principal="K_Science",repository="kolemasakar/K_Science",
    workflow_ref="refs/heads/main",workflow_file_ref=WF,run_id="12345",run_attempt=1)
KEY=bytes(range(32))
NOW=1795636800
PROFILE={"operation":"research.bibliography.audit","payload":{"synthetic":True}}
BODY=canonical(dict(request_id=RID,operation=PROFILE["operation"],payload=PROFILE["payload"]))

class Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        self.reg=Registry(self.root)
        self.reg.prepare(RID,IDENT,digest(canonical(PROFILE)),digest(BODY),len(BODY))
        self.path=self.root/(RID+".json")
        self.path.write_bytes(BODY)
        self.path.chmod(0o600)
        self.now=NOW
        self.state="PROPOSED"
        self.profile=copy.deepcopy(PROFILE)
        self.reader=self.make_reader()
    def make_reader(self,**overrides):
        opts=dict(key=KEY,peer_uid=os.getuid(),allowed_workflow=WF,
            profile_lookup=lambda rid:(self.profile,self.state),enabled=True,clock=lambda:self.now)
        opts.update(overrides)
        return Reader(self.reg,**opts)
    def approve(self,ttl=900):
        self.reg.authorize(RID,decision="synthetic-only",now=NOW,ttl=ttl)
    def message(self,nonce="1"*32,**changes):
        m=dict(version=VERSION,operation=OPERATION,request_id=RID,
            identity=copy.deepcopy(IDENT),auth=dict(key_id=KEY_ID,issued_at_epoch=NOW,nonce=nonce))
        m.update(changes)
        m["auth"]["mac_sha256"]=hmac.new(KEY,signing_bytes(m),hashlib.sha256).hexdigest()
        return m
    def read(self,m=None,**kw):
        return self.reader.read(canonical(self.message() if m is None else m),peer_uid=kw.get("uid",os.getuid()))
    def reject(self,status,call):
        with self.assertRaises(Denied) as ctx:call()
        self.assertEqual(ctx.exception.status,status)
    def test_disabled(self):
        self.reader=self.make_reader(enabled=False)
        self.reject(404,self.read)
    def test_unapproved(self):
        self.reject(403,self.read)
    def test_success(self):
        self.approve()
        self.assertEqual(self.read(),BODY)
        self.assertEqual(self.state,"PROPOSED")
    def test_replay_restart(self):
        self.approve()
        self.read()
        self.reg=Registry(self.root)
        self.reader=self.make_reader()
        self.reject(403,self.read)
    def test_fresh_nonce(self):
        self.approve()
        self.read()
        self.assertEqual(self.read(self.message("2"*32)),BODY)
    def test_wrong_peer(self):
        self.approve()
        self.reject(403,lambda:self.read(uid=os.getuid()+1))
    def test_bad_mac_no_nonce_consumption(self):
        self.approve()
        m=self.message()
        m["auth"]["mac_sha256"]="0"*64
        self.reject(403,lambda:self.read(m))
        self.assertEqual(self.read(),BODY)
    def test_wrong_workflow(self):
        self.approve()
        self.reject(403,lambda:self.read(self.message(identity=dict(IDENT,workflow_file_ref=WF.replace("synthetic","other")))))
    def test_wrong_run(self):
        self.approve()
        self.reject(403,lambda:self.read(self.message(identity=dict(IDENT,run_id="999"))))
    def test_wrong_attempt(self):
        self.approve()
        self.reject(400,lambda:self.read(self.message(identity=dict(IDENT,run_attempt=2))))
    def test_wrong_purpose(self):
        self.approve()
        self.reject(403,lambda:self.read(self.message(operation="artifact.read")))
    def test_v1_denied(self):
        self.approve()
        self.reject(403,lambda:self.read(self.message(version="krc-prepared-read/1")))
    def test_wrong_rid(self):
        self.approve()
        self.reject(403,lambda:self.read(self.message(request_id="KS-"+"b"*32)))
    def test_path_traversal(self):
        self.approve()
        self.reject(400,lambda:self.read(self.message(request_id="../private")))
    def test_expiry(self):
        self.approve(10)
        self.now=NOW+10
        self.reject(410,self.read)
    def test_stale_signature(self):
        self.approve()
        self.now=NOW+61
        self.reject(403,self.read)
    def test_revoke(self):
        self.approve()
        self.reg.revoke(RID)
        self.reject(403,self.read)
    def test_terminal(self):
        self.approve()
        self.state="COMPLETED"
        self.reject(403,self.read)
    def test_profile_change(self):
        self.approve()
        self.profile["payload"]["synthetic"]=False
        self.reject(502,self.read)
    def test_body_change(self):
        self.approve()
        self.path.write_bytes(b"x"*len(BODY))
        self.reject(502,self.read)
    def test_public_file(self):
        self.approve()
        self.path.chmod(0o644)
        self.reject(502,self.read)
    def test_symlink(self):
        self.approve()
        self.path.unlink()
        self.path.symlink_to("/dev/null")
        self.reject(503,self.read)
    def test_duplicate_json(self):
        self.approve()
        raw=canonical(self.message())[:-1]+b',"version":"duplicate"}'
        self.reject(400,lambda:self.reader.read(raw,peer_uid=os.getuid()))
    def test_limit(self):
        self.reject(413,lambda:self.reader.read(b"x"*4097,peer_uid=os.getuid()))
    def test_ttl_limit(self):
        with self.assertRaises(ValueError):self.approve(901)
    def test_revoke_during_read(self):
        self.approve()
        def lookup(rid):
            self.reg.revoke(RID)
            return self.profile,self.state
        self.reader=self.make_reader(profile_lookup=lookup)
        self.reject(403,self.read)
    def test_uds(self):
        self.approve()
        p=self.root/"s.sock"
        srv=PreparedServer(p,reader=self.reader)
        th=threading.Thread(target=srv.serve_forever,daemon=True)
        th.start()
        try:
            def exchange(raw,extra=b"",path=PATH):
                with socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) as s:
                    s.settimeout(5)
                    s.connect(str(p))
                    s.sendall(("POST "+path+" HTTP/1.1\r\nHost: local\r\nContent-Type: application/json\r\nContent-Length: "+str(len(raw))+"\r\n\r\n").encode()+raw+extra)
                    s.shutdown(socket.SHUT_WR)
                    parts=[]
                    while True:
                        b=s.recv(65536)
                        if not b:break
                        parts.append(b)
                    return b"".join(parts)
            raw=canonical(self.message())
            out=exchange(raw)
            head,body=out.split(b"\r\n\r\n",1)
            self.assertIn(b" 200 ",head)
            self.assertIn(digest(BODY).encode(),head)
            self.assertEqual(body,BODY)
            self.assertIn(b" 403 ",exchange(raw))
            self.assertIn(b" 400 ",exchange(canonical(self.message("2"*32)),b"x"))
            self.assertIn(b" 404 ",exchange(raw,path="/v1/artifacts/read"))
        finally:
            srv.shutdown()
            srv.server_close()
            th.join(3)

if __name__=="__main__":
    unittest.main()
