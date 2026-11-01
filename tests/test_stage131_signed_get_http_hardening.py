import os,socket,tempfile,threading,time
from pathlib import Path
from krc_research.stage131_signed_artifact_uds import SignedArtifactUDSServer
class Boundary:
    def execute(self,*a,**kw):raise RuntimeError("synthetic database failure")
def request(sock,raw,read=True):
    s=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
    s.settimeout(3);s.connect(str(sock));s.sendall(raw)
    if not read:return s
    data=b""
    while True:
        x=s.recv(4096)
        if not x:break
        data+=x
    s.close()
    return data
def test_framing_rejects_duplicates_te_and_backend_errors():
    with tempfile.TemporaryDirectory() as d:
        sock=Path(d)/"s.sock";srv=SignedArtifactUDSServer(sock,boundary=Boundary())
        th=threading.Thread(target=srv.serve_forever,daemon=True);th.start()
        try:
            def req(headers,body=b"{}"):
                return request(sock,b"POST /v1/artifacts/read HTTP/1.1\r\nHost: localhost\r\nContent-Type: application/json\r\n"+headers+b"\r\n\r\n"+body)
            assert b"400 Bad Request" in req(b"Content-Length: 2\r\nContent-Length: 2")
            assert b"400 Bad Request" in req(b"Content-Length: 2\r\nTransfer-Encoding: chunked")
            assert b"400 Bad Request" in req(b"Content-Length: 2, 2")
            assert b"503 Service Unavailable" in req(b"Content-Length: 2")
            assert b"BACKEND_UNAVAILABLE" in req(b"Content-Length: 2")
        finally:srv.shutdown();srv.server_close();th.join(timeout=2)
def test_slow_client_does_not_block_concurrent_request():
    with tempfile.TemporaryDirectory() as d:
        sock=Path(d)/"s.sock";srv=SignedArtifactUDSServer(sock,boundary=Boundary())
        th=threading.Thread(target=srv.serve_forever,daemon=True);th.start()
        try:
            slow=request(sock,b"POST /v1/artifacts/read HTTP/1.1\r\nHost: localhost\r\nContent-Type: application/json\r\nContent-Length: 100\r\n\r\n{",False)
            started=time.monotonic()
            fast=request(sock,b"POST /v1/artifacts/read HTTP/1.1\r\nHost: localhost\r\nContent-Type: application/json\r\nContent-Length: 2\r\n\r\n{}")
            assert b"503 Service Unavailable" in fast
            assert time.monotonic()-started<3
            slow.close()
        finally:srv.shutdown();srv.server_close();th.join(timeout=2)
