import hashlib
import json
import socket
import sys
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"))
from stage131_isolated_real_components import isolated_real_components

def request(sock, message):
    raw=json.dumps(message,separators=(",",":")).encode()
    with socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) as s:
        s.settimeout(3)
        s.connect(sock)
        s.sendall(b"POST /v1/artifacts/read HTTP/1.1\r\nHost: localhost\r\nContent-Type: application/json\r\nContent-Length: "+str(len(raw)).encode()+b"\r\n\r\n"+raw)
        s.shutdown(socket.SHUT_WR)
        result=b""
        while True:
            x=s.recv(65536)
            if not x:break
            result+=x
        return result.split(b"\r\n\r\n",1)

def test_reusable_real_component_fixture():
    with isolated_real_components() as f:
        desc=f.descriptor()
        assert hashlib.sha256(b"stage131-real-component-fixture-v1").hexdigest()==desc["sha256"]
        request_msg=f.signed_request()
        head,body=request(str(f.socket_path),request_msg)
        assert b"200 OK" in head
        assert hashlib.sha256(body).hexdigest()==desc["sha256"]
        assert int(desc["size_bytes"])==len(body)
        head,_=request(str(f.socket_path),request_msg)
        assert b"403 Forbidden" in head
        head,_=request(str(f.socket_path),f.signed_request("fixture-nonce-00000002",artifact_id="b"*48))
        assert b"404 Not Found" in head
