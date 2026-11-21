"""KRC-owned internal relay candidate. No start or deployment side effects.

Existing verified gateway (UID988) forwards only the pilot request to the
private project owner (UID1002). Separate relay key and nonce registry.
AF_UNIX only; no fallback, retry, external approval or Sentinel changes.
"""
import hashlib
import hmac
import json
import os
import re
import secrets
import socket
import socketserver
import stat
import struct
import time

from krc_research.stage132_project_post_wire import OP, IDENTITY, denied, ambiguous, canonical, valid_pilot_descriptor, OFFLINE_OPS, BIBLIOGRAPHY, DEFAULT_OPS, checked_ops
from krc_research.uds_verified123b import VerifiedStage123Handler

DOMAIN="KRC-PROJECT-PILOT-RELAY/1"
MAX_FRAME=262144
MAX_REPLY=16384
MAX_SECONDS=15
KEY_ID="stage132-project-post-relay-v1"
NONCE=re.compile(r"[0-9a-f]{48}\Z")
RID=re.compile(r"KS-[0-9a-f]{32}\Z")

def unique(pairs):
    obj=dict(pairs)
    if len(obj)!=len(pairs):raise ValueError("DUPLICATE_JSON_FIELD")
    return obj

def parse(raw):
    return json.loads(raw.decode("utf-8"),object_pairs_hook=unique)

def peer(conn):
    _,uid,gid=struct.unpack("3i",conn.getsockopt(socket.SOL_SOCKET,socket.SO_PEERCRED,12))
    return uid,gid

def budget(conn,deadline):
    remaining=deadline-time.monotonic()
    if remaining<=0:raise TimeoutError("DEADLINE")
    conn.settimeout(remaining)

def exact(conn,n,deadline):
    raw=bytearray()
    while len(raw)<n:
        budget(conn,deadline)
        part=conn.recv(n-len(raw))
        if not part:raise ValueError("TRUNCATED_FRAME")
        raw.extend(part)
    return bytes(raw)

def receive_frame(conn,deadline,limit):
    n=struct.unpack("!I",exact(conn,4,deadline))[0]
    if not 0<n<=limit:raise ValueError("FRAME_LIMIT")
    raw=exact(conn,n,deadline)
    budget(conn,deadline)
    if conn.recv(1):raise ValueError("TRAILING_FRAME")
    return parse(raw)

def send_frame(conn,value,deadline,limit):
    raw=canonical(value)
    if not 0<len(raw)<=limit:raise ValueError("FRAME_LIMIT")
    budget(conn,deadline)
    conn.sendall(struct.pack("!I",len(raw))+raw)
    conn.shutdown(socket.SHUT_WR)

def check_key(key):
    if type(key) is not bytes or len(key)!=32:raise ValueError("RELAY_KEY")

def make_message(envelope,key,*,clock=time.time):
    check_key(key)
    body={"domain":DOMAIN,"key_id":KEY_ID,"issued_at":int(clock()),
          "nonce":secrets.token_hex(24),"envelope":envelope}
    return {**body,"mac":hmac.new(key,canonical(body),hashlib.sha256).hexdigest()}

class RelayAuthority:
    def __init__(self,*,boundary,registry,key,peer_uid,peer_gid,clock=time.time):
        check_key(key)
        self.boundary,self.registry,self.key=boundary,registry,key
        self.uid,self.gid,self.clock=peer_uid,peer_gid,clock
    def accept(self,message,*,credentials):
        if credentials!=(self.uid,self.gid):return denied()
        try:
            if not isinstance(message,dict) or set(message)!={"domain","key_id","issued_at","nonce","envelope","mac"}:return denied()
            if message["domain"]!=DOMAIN or message["key_id"]!=KEY_ID:return denied()
            if type(message["issued_at"]) is not int or abs(message["issued_at"]-int(self.clock()))>300:return denied()
            if not isinstance(message["nonce"],str) or not NONCE.fullmatch(message["nonce"]):return denied()
            if not isinstance(message["mac"],str) or not re.fullmatch(r"[0-9a-f]{64}",message["mac"]):return denied()
            unsigned={k:v for k,v in message.items() if k!="mac"}
            if not hmac.compare_digest(message["mac"],hmac.new(self.key,canonical(unsigned),hashlib.sha256).hexdigest()):return denied()
            e=message["envelope"]
            if not isinstance(e,dict) or e.get("identity")!=IDENTITY or e.get("operation") not in self.boundary.enabled_operations:return denied()
            if not self.registry.claim(KEY_ID,message["nonce"],IDENTITY["principal"]):return denied()
            return self.boundary.execute(e,trusted_principal=IDENTITY["principal"])
        except Exception:return denied()

class RelayHandler(socketserver.BaseRequestHandler):
    def handle(self):
        deadline=time.monotonic()+MAX_SECONDS
        try:
            credentials=peer(self.request)
            if credentials!=(self.server.authority.uid,self.server.authority.gid):
                # No read or dispatch for a wrong kernel peer.
                return
            message=receive_frame(self.request,deadline,MAX_FRAME)
            status,body=self.server.authority.accept(message,credentials=credentials)
            send_frame(self.request,{"status":status,"body":body},deadline,MAX_REPLY)
        except (OSError,ValueError,TypeError,OverflowError):return

class RelayServer(socketserver.UnixStreamServer):
    def __init__(self,path,*,authority):
        if os.path.lexists(path):raise ValueError("SOCKET_ALREADY_EXISTS")
        self.authority=authority
        super().__init__(str(path),RelayHandler)
    def handle_error(self,*_):
        pass

def validate_reply(response,rid):
    if not isinstance(response,dict) or set(response)!={"status","body"}:raise ValueError("REPLY")
    status,b=response["status"],response["body"]
    if type(status) is not int or not isinstance(b,dict):raise ValueError("REPLY")
    if status==403 and b=={"error":"OPERATION_DENIED"}:return status,b
    if status==409 and set(b)=={"request_id","status","error"} and b["request_id"]==rid:
        if (b["status"],b["error"]) in (("rejected",{"code":"IDEMPOTENCY_CONFLICT"}),("pending_reconciliation",{"code":"AMBIGUOUS_REQUEST"})):
            return status,b
    if status==200 and set(b)=={"version","request_id","status","delivery","artifact"}:
        if (b["version"],b["request_id"],b["status"],b["delivery"])==("krc-transport/2",rid,"completed","artifact"):
            if valid_pilot_descriptor(b["artifact"],now=time.time()):
                return status,b
    raise ValueError("REPLY_NOT_CORRELATED")

class RelayClient:
    def __init__(self,path,*,key,expected_uid,expected_gid,enabled_operations=DEFAULT_OPS):
        check_key(key)
        self.path,self.key=path,key
        self.uid,self.gid=expected_uid,expected_gid
        self.enabled_operations=checked_ops(enabled_operations)
    def execute(self,envelope):
        rid=envelope.get("request_id")
        if envelope.get("identity")!=IDENTITY or envelope.get("operation") not in self.enabled_operations or not isinstance(rid,str) or not RID.fullmatch(rid):return denied()
        deadline=time.monotonic()+MAX_SECONDS
        try:
            st=os.lstat(self.path)
            if not stat.S_ISSOCK(st.st_mode) or (st.st_uid,st.st_gid,stat.S_IMODE(st.st_mode))!=(self.uid,self.gid,0o660):raise ValueError("SOCKET_CUSTODY")
            with socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) as conn:
                budget(conn,deadline);conn.connect(str(self.path))
                if peer(conn)!=(self.uid,self.gid):raise ValueError("PEER_CUSTODY")
                send_frame(conn,make_message(envelope,self.key),deadline,MAX_FRAME)
                response=receive_frame(conn,deadline,MAX_REPLY)
            return validate_reply(response,rid)
        except Exception:
            # A request might already have executed. No fallback or new attempt.
            return ambiguous(rid)

class PilotGatewayBoundary:
    """Insert AFTER existing KRC HMAC / peer / claim checks, not before."""
    def __init__(self,legacy,relay):
        self.legacy,self.relay=legacy,relay
        self.exchange=legacy.exchange
    def execute(self,envelope,*,trusted_principal):
        op=envelope.get("operation")
        if op==BIBLIOGRAPHY:
            return denied()[1]
        if op not in OFFLINE_OPS:
            return self.legacy.execute(envelope,trusted_principal=trusted_principal)
        if op not in self.relay.enabled_operations:
            return denied()[1]
        if trusted_principal!=IDENTITY["principal"]:return denied()[1]
        return self.relay.execute(envelope)[1]

class PilotGatewayHandler(VerifiedStage123Handler):
    def send_json(self,status,obj):
        # Existing handler maps non-completed documents to 409 by default.
        # Pilot denial is explicitly a generic 403; all legacy mappings stay.
        if status==409 and obj=={"error":"OPERATION_DENIED"}:status=403
        return super().send_json(status,obj)

def attach_pilot(server,relay):
    """Candidate composition for the existing authenticated UDS server.

    Operator must explicitly install a new reviewed immutable release; never
    call on a running service or expose a second network listener.
    """
    server.boundary=PilotGatewayBoundary(server.boundary,relay)
    server.RequestHandlerClass=PilotGatewayHandler
    return server
