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


def test_worker_cap_sends_503_without_spawning_more_workers():
    with tempfile.TemporaryDirectory() as d:
        sock=Path(d)/"s.sock";srv=SignedArtifactUDSServer(sock,boundary=Boundary())
        srv._worker_slots=threading.BoundedSemaphore(2)
        th=threading.Thread(target=srv.serve_forever,daemon=True);th.start()
        clients=[]
        try:
            for _ in range(2):
                clients.append(request(sock,b"POST /v1/artifacts/read HTTP/1.1\r\nHost: x\r\n",False))
            time.sleep(.1)
            try:
                rejected=request(sock,b"POST /v1/artifacts/read HTTP/1.1\r\nHost: x\r\nContent-Type: application/json\r\nContent-Length: 2\r\n\r\n{}")
                assert b"503 Service Unavailable" in rejected
            except ConnectionResetError:
                # Linux AF_UNIX may reset while discarding unread overload bytes.
                pass
            assert srv._worker_slots._value==0
        finally:
            for client in clients:client.close()
            srv.shutdown();srv.server_close();th.join(timeout=2)

def test_absolute_deadline_closes_trickling_header():
    with tempfile.TemporaryDirectory() as d:
        sock=Path(d)/"s.sock";srv=SignedArtifactUDSServer(sock,boundary=Boundary())
        srv.request_deadline_seconds=.35
        th=threading.Thread(target=srv.serve_forever,daemon=True);th.start()
        client=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
        client.settimeout(2)
        try:
            client.connect(str(sock))
            client.sendall(b"POST /v1/artifacts/read HTTP/1.1\r\nX-Slow: ")
            started=time.monotonic()
            while time.monotonic()-started<1:
                try:
                    client.sendall(b"x")
                except OSError:
                    break
                time.sleep(.07)
            assert time.monotonic()-started<1.5
            try:
                assert client.recv(1024)==b""
            except (ConnectionResetError,BrokenPipeError):
                pass
        finally:
            client.close();srv.shutdown();srv.server_close();th.join(timeout=2)


def test_rejects_undeclared_body_bytes_before_backend_dispatch():
    class CountingBoundary:
        def __init__(self):self.calls=0
        def execute(self,*args,**kwargs):
            self.calls+=1
            return {"http_status":404,"body":{"error":"NOT_FOUND"}}
    with tempfile.TemporaryDirectory() as d:
        boundary=CountingBoundary()
        sock=Path(d)/"s.sock";srv=SignedArtifactUDSServer(sock,boundary=boundary)
        th=threading.Thread(target=srv.serve_forever,daemon=True);th.start()
        try:
            prefix=b"POST /v1/artifacts/read HTTP/1.1\r\nHost: localhost\r\nContent-Type: application/json\r\nContent-Length: 2\r\n\r\n"
            result=request(sock,prefix+b"{}EXTRA")
            assert b"400 Bad Request" in result
            assert boundary.calls==0
        finally:srv.shutdown();srv.server_close();th.join(timeout=2)


def test_actual_http_fixture_positive_and_negative_sha_contract():
    import hashlib,json
    class Stub:
        def execute(self,message,*,peer_uid):
            if message.get("artifact_id")=="ok":
                payload=b"synthetic-small-artifact"
                return {"http_status":200,"size_bytes":len(payload),
                        "sha256":hashlib.sha256(payload).hexdigest(),"body_bytes":payload}
            return {"http_status":403,"body":{"error":"FORBIDDEN"}}
    with tempfile.TemporaryDirectory() as d:
        sock=Path(d)/"s.sock";srv=SignedArtifactUDSServer(sock,boundary=Stub())
        th=threading.Thread(target=srv.serve_forever,daemon=True);th.start()
        try:
            def get(body):
                raw=json.dumps(body,separators=(",",":")).encode()
                return request(sock,b"POST /v1/artifacts/read HTTP/1.1\r\nHost: localhost\r\nContent-Type: application/json\r\nContent-Length: "+str(len(raw)).encode()+b"\r\nConnection: close\r\n\r\n"+raw)
            ok=get({"artifact_id":"ok"})
            status,body=ok.split(b"\r\n\r\n",1)
            assert b"200 OK" in status
            assert b"Content-Length: 24\r\n" in status
            assert b"X-Content-SHA256: "+hashlib.sha256(body).hexdigest().encode() in status
            assert body==b"synthetic-small-artifact"
            denied=get({"artifact_id":"deny"})
            head,data=denied.split(b"\r\n\r\n",1)
            assert b"403 Forbidden" in head
            assert json.loads(data)=={"error":"FORBIDDEN"}
            invalid=request(sock,b"POST /v1/artifacts/read HTTP/1.1\r\nHost: localhost\r\nContent-Type: application/json\r\nContent-Length: 2\r\nTransfer-Encoding: chunked\r\n\r\n{}")
            assert b"400 Bad Request" in invalid
        finally:srv.shutdown();srv.server_close();th.join(timeout=2)
