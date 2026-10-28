"""Stage126: interrupted download does not terminate the isolated UDS handler."""
import os,socket,threading
from krc_research.uds_stage123 import Stage123Server
from krc_research.research_boundary120 import ResearchBoundary
from krc_research.request_ledger119 import RequestLedger
from krc_research.artifact_stage117 import HardenedExchange

def test_disconnected_client_then_health(tmp_path):
    store=HardenedExchange(tmp_path/"artifacts",free_bytes_min=0)
    manifest=store.store_stream([b"x"*32768 for _ in range(40)],principal="client",request_id="req",filename="test.bin")
    boundary=ResearchBoundary(ledger=RequestLedger(tmp_path/"ledger.sqlite"),exchange=store,dispatch=lambda o,p,who:{"ok":True})
    sock=tmp_path/"backend.sock"
    srv=Stage123Server(sock,boundary=boundary,peer_principals={os.getuid():"client"})
    t=threading.Thread(target=srv.serve_forever,daemon=True);t.start()
    try:
        client=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
        client.connect(str(sock))
        aid=manifest["artifact_id"]
        client.sendall((f"GET /v1/artifacts/{aid} HTTP/1.1\r\nHost: local\r\nX-KRC-Request-ID: req\r\nConnection: close\r\n\r\n").encode())
        client.recv(512)
        client.close()
        # This test checks service availability after a client disconnect;
        # it does NOT claim interruption-safe resume or complete content delivery.
        follow=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
        follow.settimeout(4)
        follow.connect(str(sock))
        follow.sendall(b"GET /healthz HTTP/1.1\r\nHost: local\r\nConnection: close\r\n\r\n")
        data=follow.recv(4096)
        follow.close()
        assert b"200 OK" in data
    finally:
        srv.shutdown();srv.server_close();t.join()
