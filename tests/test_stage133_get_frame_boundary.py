"""UDS strict framing regression on an isolated socket; no real consent."""
import socket
import tempfile
import threading
from pathlib import Path
from krc_research.stage131_signed_artifact_uds import SignedArtifactUDSServer

class SyntheticBoundary:
    def __init__(self):
        self.calls=0
    def execute(self,*args,**kwargs):
        self.calls+=1
        raise RuntimeError("synthetic backend failure")

def exchange(sock,body,declared=2,check_no_early_reply=False):
    with socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) as s:
        s.settimeout(4)
        s.connect(str(sock))
        request=(b"POST /v1/artifacts/read HTTP/1.1\r\n"
            b"Host: localhost\r\nContent-Type: application/json\r\n"
            + b"Content-Length: "+str(declared).encode()
            + b"\r\nConnection: close\r\n\r\n"+body)
        s.sendall(request)
        if check_no_early_reply:
            s.settimeout(0.15)
            try: premature=s.recv(1)
            except socket.timeout:premature=None
            assert premature is None, "server dispatched before explicit EOF"
            s.settimeout(4)
        s.shutdown(socket.SHUT_WR)
        chunks=[]
        while True:
            part=s.recv(4096)
            if not part:break
            chunks.append(part)
        return b"".join(chunks)

def test_get_refuses_overlong_body_before_dispatch():
    with tempfile.TemporaryDirectory() as d:
        socket_path=Path(d)/"strict.sock"
        boundary=SyntheticBoundary()
        server=SignedArtifactUDSServer(socket_path,boundary=boundary)
        worker=threading.Thread(target=server.serve_forever,daemon=True)
        worker.start()
        try:
            out=exchange(socket_path,b"{}x")
            assert b"400 Bad Request" in out
            assert boundary.calls==0
        finally:
            server.shutdown()
            server.server_close()
            worker.join(3)

def test_get_waits_for_write_half_close_and_dispatches_once():
    with tempfile.TemporaryDirectory() as d:
        socket_path=Path(d)/"strict.sock"
        boundary=SyntheticBoundary()
        server=SignedArtifactUDSServer(socket_path,boundary=boundary)
        worker=threading.Thread(target=server.serve_forever,daemon=True)
        worker.start()
        try:
            out=exchange(socket_path,b"{}",check_no_early_reply=True)
            assert b"503 Service Unavailable" in out
            assert boundary.calls==1
        finally:
            server.shutdown()
            server.server_close()
            worker.join(3)
