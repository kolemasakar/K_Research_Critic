"""Reference internal descriptor client for Sentinel's admitted read route.

No new public endpoint. Accept only the server-derived, signed read envelope
from the trusted machine admission path; derive a DIFFERENT signed nonce for
the descriptor request. Then compare the independently sourced descriptor
with the binary read response via Sentinel's verified_spool.
"""
import json
import re
import secrets
import socket
import struct
import time

from .stage131_signed_artifact_read import verify_signed_read, sign_fixture
from .stage131_consumer_boundary_checks import validate_artifact_descriptor
from .stage131_project_signed_read import IDENTITY, KEY_ID

MAX_HEADER=16384
MAX_BODY=4096
ALLOWED_ERRORS={403,404,410,413,502,503,504}

class DescriptorDenied(ValueError):
    def __init__(self,status,code):
        self.status,self.code=status,code
        super().__init__(code)

def fail(status,code):raise DescriptorDenied(status,code)

def describe_envelope(original,key):
    # This is a client-side check only, NOT server nonce admission.
    scope=verify_signed_read(original,trusted_identity=IDENTITY,secret=key,
        nonce_claim=lambda *_: True)
    if original["auth"]["key_id"]!=KEY_ID:fail(403,"FORBIDDEN")
    m=json.loads(json.dumps(original));m["operation"]="artifact.describe"
    m["auth"]["issued_at_epoch"]=int(time.time())
    m["auth"]["nonce"]=secrets.token_hex(24)
    if m["auth"]["nonce"]==original["auth"]["nonce"]:fail(503,"BACKEND_UNAVAILABLE")
    return sign_fixture(m,key),scope

def fetch_descriptor(socket_path,original,*,key,expected_uid=1002,expected_gid=984,timeout=20):
    if not isinstance(key,bytes) or len(key)!=32 or type(timeout) not in (int,float) or not 0<timeout<=25:
        fail(503,"BACKEND_UNAVAILABLE")
    try:m,scope=describe_envelope(original,key)
    except DescriptorDenied:raise
    except (ValueError,TypeError,KeyError):fail(403,"FORBIDDEN")
    data=json.dumps(m,sort_keys=True,separators=(",",":")).encode()
    if not 0<len(data)<=262144:fail(400,"INVALID_REQUEST")
    deadline=time.monotonic()+timeout
    with socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) as s:
        def remaining():
            left=deadline-time.monotonic()
            if left<=0:fail(504,"UPSTREAM_TIMEOUT")
            s.settimeout(left)
        def read(n):
            remaining()
            return s.recv(n)
        try:
            remaining();s.connect(str(socket_path))
            _,uid,gid=struct.unpack("3i",s.getsockopt(socket.SOL_SOCKET,socket.SO_PEERCRED,12))
            if (uid,gid)!=(expected_uid,expected_gid):fail(403,"FORBIDDEN")
            remaining()
            s.sendall(b"POST /v1/artifacts/describe HTTP/1.1\r\nHost: localhost\r\nContent-Type: application/json\r\nContent-Length: "+str(len(data)).encode()+b"\r\nConnection: close\r\n\r\n"+data)
            s.shutdown(socket.SHUT_WR)
            buf=bytearray()
            while b"\r\n\r\n" not in buf:
                if len(buf)>=MAX_HEADER:fail(502,"UPSTREAM_INVALID_RESPONSE")
                b=read(min(4096,MAX_HEADER-len(buf)))
                if not b:fail(502,"UPSTREAM_INVALID_RESPONSE")
                buf.extend(b)
            header,body=bytes(buf).split(b"\r\n\r\n",1)
            lines=header.split(b"\r\n")
            match=re.fullmatch(rb"HTTP/1\.[01] ([1-5][0-9]{2})(?: [\x20-\x7e]*)?",lines[0])
            if match is None:fail(502,"UPSTREAM_INVALID_RESPONSE")
            status=int(match.group(1));headers={}
            for line in lines[1:]:
                name,sep,value=line.partition(b":");name=name.lower()
                if not sep or not re.fullmatch(rb"[!#$%&'*+.^_`|~0-9A-Za-z-]+",name) or name in headers or any(x<32 and x!=9 or x==127 for x in value):
                    fail(502,"UPSTREAM_INVALID_RESPONSE")
                headers[name]=value.strip()
            length=headers.get(b"content-length",b"")
            if (not re.fullmatch(rb"[0-9]{1,5}",length) or int(length)>MAX_BODY or len(body)>int(length)
                or b"transfer-encoding" in headers or headers.get(b"content-type")!=b"application/json"
                or headers.get(b"connection",b"").lower()!=b"close" or headers.get(b"cache-control")!=b"no-store"
                or headers.get(b"x-content-type-options")!=b"nosniff"):
                fail(502,"UPSTREAM_INVALID_RESPONSE")
            while len(body)<int(length):
                b=read(int(length)-len(body))
                if not b:fail(502,"UPSTREAM_INVALID_RESPONSE")
                body+=b
            if read(1):fail(502,"UPSTREAM_INVALID_RESPONSE")
            if status!=200:
                if status in ALLOWED_ERRORS:fail(status,"UPSTREAM_DENIED_"+str(status))
                fail(502,"UPSTREAM_INVALID_RESPONSE")
            try:out=json.loads(body)
            except (ValueError,UnicodeError):fail(502,"UPSTREAM_INVALID_RESPONSE")
            if (not isinstance(out,dict) or set(out)!={"request_id","artifact_id","filename","media_type","sha256","size_bytes","expires_at_epoch"}
                or out["request_id"]!=scope["request_id"] or out["artifact_id"]!=scope["artifact_id"]
                or validate_artifact_descriptor(out)!="DESCRIPTOR_VALID_NOT_AUTHORIZED"):
                fail(502,"UPSTREAM_INVALID_RESPONSE")
            return out
        except DescriptorDenied:raise
        except (socket.timeout,TimeoutError):fail(504,"UPSTREAM_TIMEOUT")
        except (FileNotFoundError,ConnectionRefusedError):fail(503,"BACKEND_UNAVAILABLE")
        except OSError:fail(502,"UPSTREAM_INVALID_RESPONSE")
