"""Private test-only Unix socket HTTP GET, without changing installed services."""
import hashlib
import http.client
import json
import os
import socket
import threading
from krc_research.staging_service123c import make_staging_server

class UnixConnection(http.client.HTTPConnection):
    def __init__(self,path):
        super().__init__("localhost",timeout=4)
        self.path=str(path)
    def connect(self):
        self.sock=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
        self.sock.connect(self.path)

def test_private_artifact_get_success_denial_and_sha(tmp_path):
    path=tmp_path/"backend.sock"
    server=make_staging_server(path,tmp_path/"state",peer_principals={os.getuid():"K_Science"},
        uid_keys={os.getuid():{"stage":b"K"*32}},claim_allowlist={("K_Science","K_Science","kolemasakar/K_Science","refs/heads/main")},
        science_secret=b"S"*32)
    t=threading.Thread(target=server.serve_forever,daemon=True);t.start()
    try:
        payload=b"synthetic-publicless-artifact"
        item=server.boundary.exchange.store_bytes(payload,principal="K_Science",request_id="testreq",filename="test.bin")
        def get(rid,aid):
            c=UnixConnection(path)
            try:
                c.request("GET","/v1/artifacts/"+aid,headers={"X-KRC-Request-ID":rid})
                r=c.getresponse()
                return r.status,dict(r.getheaders()),r.read()
            finally:c.close()
        code,headers,raw=get("testreq",item["artifact_id"])
        assert code==200
        assert raw==payload
        assert headers["X-Content-SHA256"]==hashlib.sha256(payload).hexdigest()
        assert int(headers["Content-Length"])==len(payload)
        assert get("wrong",item["artifact_id"])[0]==404
        assert get("testreq","not-a-valid-id")[0]==404
    finally:
        server.shutdown();server.server_close();t.join()
