"""KRC-owned Stage123-B independent verifier for Sentinel's transport assertion.
No OIDC issuer validation occurs here: Sentinel must verify upstream first.
"""
import hashlib,hmac,json,re
from datetime import datetime,timezone

class TransportAuthError(ValueError):
    pass

def canonical(value):
    try:
        return json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode("utf-8")
    except (TypeError,ValueError,OverflowError) as e:
        raise TransportAuthError("INVALID_ASSERTION") from e

def verify(message,*,peer_uid,uid_keys,claim_allowlist,now=None):
    if not isinstance(message,dict) or set(message)!={"version","request_id","operation","identity","payload","transport_auth"}:
        raise TransportAuthError("INVALID_ASSERTION")
    auth=message["transport_auth"]
    if not isinstance(auth,dict) or set(auth)!={"alg","key_id","issued_at","mac"} or auth.get("alg")!="HMAC-SHA256":
        raise TransportAuthError("INVALID_ASSERTION")
    key_id=auth["key_id"]
    if not isinstance(key_id,str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,64}",key_id):
        raise TransportAuthError("INVALID_ASSERTION")
    peer_keys=uid_keys.get(peer_uid)
    key=peer_keys.get(key_id) if isinstance(peer_keys,dict) else None
    if not isinstance(key,bytes) or len(key)<32:
        raise TransportAuthError("UNAUTHORIZED")
    try:
        stamp=datetime.fromisoformat(auth["issued_at"].replace("Z","+00:00"))
        current=now or datetime.now(timezone.utc)
        if stamp.utcoffset() is None or abs((current-stamp).total_seconds())>300:
            raise TransportAuthError("EXPIRED_ASSERTION")
    except (AttributeError,TypeError,ValueError) as e:
        if isinstance(e,TransportAuthError):raise
        raise TransportAuthError("INVALID_ASSERTION") from e
    envelope={k:v for k,v in message.items() if k!="transport_auth"}
    if envelope["version"]!="krc-transport/2" or not isinstance(envelope["payload"],dict):
        raise TransportAuthError("INVALID_ASSERTION")
    identity=envelope["identity"]
    needed=("client","principal","repository","workflow_ref")
    if not isinstance(identity,dict) or set(identity)!=set(needed) or any(not isinstance(identity[k],str) or not identity[k] for k in needed):
        raise TransportAuthError("UNAUTHORIZED")
    if not isinstance(envelope["request_id"],str) or not envelope["request_id"]:
        raise TransportAuthError("INVALID_ASSERTION")
    if len(canonical(message))>262144:
        raise TransportAuthError("REQUEST_TOO_LARGE")
    binding={"domain":"KRC-TRANSPORT-IDENTITY/2","key_id":key_id,"issued_at":auth["issued_at"],"envelope":envelope}
    if not isinstance(auth["mac"],str) or not re.fullmatch("[a-f0-9]{64}",auth["mac"]):
        raise TransportAuthError("INVALID_ASSERTION")
    expected=hmac.new(key,canonical(binding),hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected,auth["mac"]):
        raise TransportAuthError("INVALID_ASSERTION")
    if tuple(identity[k] for k in needed) not in claim_allowlist:
        raise TransportAuthError("UNAUTHORIZED")
    return envelope
