"""Capture deterministic, normalized real AF_UNIX HTTP fixtures (synthetic boundary)."""
import hashlib
import json
import socket
import tempfile
import threading
from pathlib import Path
from krc_research.stage131_signed_artifact_uds import SignedArtifactUDSServer

class SyntheticBoundary:
    def execute(self, message, *, peer_uid):
        if message.get("artifact_id") == "allow":
            body=b"fixture-artifact-v1"
            return {"http_status":200,"body_bytes":body,"size_bytes":len(body),
                    "sha256":hashlib.sha256(body).hexdigest()}
        return {"http_status":403,"body":{"error":"FORBIDDEN"}}

def capture(path, body, *, extra=b""):
    client=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
    client.settimeout(3)
    client.connect(str(path))
    req=b"POST /v1/artifacts/read HTTP/1.1\r\nHost: local\r\nContent-Type: application/json\r\nContent-Length: "+str(len(body)).encode()+b"\r\nConnection: close\r\n\r\n"+body+extra
    client.sendall(req)
    client.shutdown(socket.SHUT_WR)
    wire=b""
    while True:
        chunk=client.recv(65536)
        if not chunk:break
        wire+=chunk
    client.close()
    header,payload=wire.split(b"\r\n\r\n",1)
    lines=header.decode("ascii").split("\r\n")
    headers={}
    for line in lines[1:]:
        k,v=line.split(":",1)
        if k.lower() not in ("date","server"): headers[k.lower()]=v.strip()
    return {"status_line":lines[0],"headers":headers,"body_hex":payload.hex(),
            "body_length":len(payload),"body_sha256":hashlib.sha256(payload).hexdigest()}

def main():
    with tempfile.TemporaryDirectory() as d:
        sock=Path(d)/"socket"
        server=SignedArtifactUDSServer(sock,boundary=SyntheticBoundary())
        worker=threading.Thread(target=server.serve_forever,daemon=True)
        worker.start()
        try:
            ok=capture(sock,b'{"artifact_id":"allow"}')
            denied=capture(sock,b'{"artifact_id":"deny"}')
            extra=capture(sock,b'{"artifact_id":"deny"}',extra=b"EXTRA")
            assert ok["status_line"].startswith("HTTP/1.1 200")
            assert denied["status_line"].startswith("HTTP/1.1 403")
            assert extra["status_line"].startswith("HTTP/1.1 400")
            out={"schema":"KRC_STAGE131_UDS_CAPTURE_V1",
                 "protocol":"request write-half-close required; no dispatch without EOF",
                 "source_kind":"synthetic isolated actual AF_UNIX HTTP",
                 "captures":{"success_200":ok,"forbidden_403":denied,"trailing_400":extra}}
            print(json.dumps(out,sort_keys=True,indent=2))
        finally:
            server.shutdown();server.server_close();worker.join(timeout=3)
if __name__=="__main__":
    main()
