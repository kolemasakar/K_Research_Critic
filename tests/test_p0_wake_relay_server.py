import io
from unittest.mock import patch
from plugins.krc_migration_candidate.p0_wake_relay_server import Handler, RateGate
from plugins.krc_migration_candidate import p0_wake_relay_server as srv
from http.server import ThreadingHTTPServer
from threading import Thread
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import json

def run_one(request, *, method="POST", data=None, auth="Bearer "+"x"*40):
    Handler.token = "x"*40
    Handler.gate = RateGate()
    server=ThreadingHTTPServer(("127.0.0.1",0),Handler)
    thread=Thread(target=server.serve_forever,daemon=True)
    thread.start()
    url="http://127.0.0.1:"+str(server.server_port)+request
    try:
        req=Request(url,data=data,method=method,headers={"Authorization":auth,"Content-Type":"application/json"})
        try:
            with urlopen(req,timeout=5) as resp: return resp.status, resp.read()
        except HTTPError as e: return e.code,e.read()
    finally:
        server.shutdown()
        server.server_close()
        thread.join()

def test_deny_bad_key_even_for_known_path():
    status,body=run_one("/krc-wake/v1",data=b'{"action":"wake_voicebridge"}',auth="Bearer BAD")
    assert status==403
def test_deny_arbitrary_payload():
    status,body=run_one("/krc-wake/v1",data=b'{"action":"wake_voicebridge","url":"http://localhost"}')
    assert status==400
def test_deny_get():
    status,body=run_one("/krc-wake/v1",method="GET")
    assert status==405
def test_relay_success_only_fixed_get():
    class Opener:
        def open(self,req,timeout):
            assert req.full_url == srv._TARGET
            assert req.method=="GET" and req.get_header("Authorization") is None
            class Resp:
                status=200
                def __enter__(self): return self
                def __exit__(self,*args):pass
                def read(self,n):return b'{"status":"ok"}'
            return Resp()
    with patch.object(srv,"build_opener",return_value=Opener()):
        status,body=run_one("/krc-wake/v1",data=b'{"action":"wake_voicebridge"}')
    assert status==200 and json.loads(body)["status"]=="woken"
def test_rate_gate_prevents_back_to_back():
    g = RateGate()
    assert g.begin_or_join() == "owner"
    g.complete(False)
    assert g.begin_or_join() == "rate_limited"

def test_success_is_cached_during_cooldown():
    g = RateGate()
    assert g.begin_or_join() == "owner"
    g.complete(True)
    assert g.begin_or_join() == "ready"

def test_concurrent_join_does_not_create_second_upstream_request():
    from concurrent.futures import ThreadPoolExecutor
    from threading import Event
    started, release = Event(), Event()
    calls = []
    g = RateGate()
    def first():
        assert g.begin_or_join() == "owner"
        calls.append("upstream")
        started.set()
        assert release.wait(2)
        g.complete(True)
    def second():
        assert started.wait(2)
        return g.begin_or_join()
    with ThreadPoolExecutor(max_workers=2) as pool:
        a = pool.submit(first)
        b = pool.submit(second)
        release.set()
        a.result()
        assert b.result() == "ready"
    assert calls == ["upstream"]
