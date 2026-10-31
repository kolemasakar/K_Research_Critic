"""Source-only signed artifact.read validation; never starts a UDS listener."""
import hashlib,hmac,json,math,time
from .stage131_consumer_boundary_checks import validate_artifact_descriptor

VERSION="krc-artifact-get/1"
PATH="/v1/artifacts/read"
METHOD="POST"
class ArtifactReadDenied(ValueError): pass
def canonical_bytes(message):
    if not isinstance(message,dict):raise ArtifactReadDenied("INVALID_REQUEST")
    unsigned=json.loads(json.dumps(message))
    try: del unsigned["auth"]["mac_sha256"]
    except (KeyError,TypeError):raise ArtifactReadDenied("INVALID_REQUEST") from None
    try:return json.dumps(unsigned,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode("utf-8")
    except (TypeError,ValueError):raise ArtifactReadDenied("INVALID_REQUEST") from None

def verify_signed_read(message,*,trusted_identity,secret,nonce_claim,now_epoch=None,skew_seconds=300):
    """Caller owns trusted SO_PEERCRED/OIDC derivation, scoped key and durable atomic nonce_claim."""
    if not isinstance(message,dict) or set(message)!={"version","operation","request_id","artifact_id","identity","auth"}:
        raise ArtifactReadDenied("INVALID_REQUEST")
    if message["version"]!=VERSION or message["operation"]!="artifact.read":
        raise ArtifactReadDenied("OPERATION_DENIED")
    a=message["auth"]; i=message["identity"]
    if not isinstance(a,dict) or set(a)!={"key_id","issued_at_epoch","nonce","mac_sha256"} or not isinstance(i,dict) or set(i)!={"principal","repository","workflow_ref"}:
        raise ArtifactReadDenied("INVALID_REQUEST")
    if not isinstance(trusted_identity,dict) or i!=trusted_identity:
        raise ArtifactReadDenied("FORBIDDEN")
    if not all(isinstance(i[k],str) and i[k] for k in i):raise ArtifactReadDenied("INVALID_REQUEST")
    if not isinstance(message["request_id"],str) or not message["request_id"] or not isinstance(message["artifact_id"],str) or len(message["artifact_id"])!=48 or any(c not in "0123456789abcdef" for c in message["artifact_id"]):
        raise ArtifactReadDenied("INVALID_REQUEST")
    if type(a["issued_at_epoch"]) is not int or not isinstance(a["key_id"],str) or not a["key_id"] or not isinstance(a["nonce"],str) or len(a["nonce"])<16 or not isinstance(a["mac_sha256"],str) or len(a["mac_sha256"])!=64:
        raise ArtifactReadDenied("INVALID_REQUEST")
    now=time.time() if now_epoch is None else now_epoch
    if type(now) not in (int,float) or not math.isfinite(now) or not 0<skew_seconds<=300 or abs(now-a["issued_at_epoch"])>skew_seconds:
        raise ArtifactReadDenied("STALE_SIGNATURE")
    if not isinstance(secret,bytes) or len(secret)<16:raise ArtifactReadDenied("TRUSTED_KEY_REQUIRED")
    expected=hmac.new(secret,canonical_bytes(message),hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected,a["mac_sha256"]):raise ArtifactReadDenied("BAD_SIGNATURE")
    if not callable(nonce_claim) or nonce_claim(a["key_id"],a["nonce"],i["principal"]) is not True:
        raise ArtifactReadDenied("REPLAY_DENIED")
    return {"artifact_id":message["artifact_id"],"request_id":message["request_id"],"principal":i["principal"]}

def sign_fixture(message,secret):
    out=json.loads(json.dumps(message))
    out["auth"]["mac_sha256"]=hmac.new(secret,canonical_bytes(out),hashlib.sha256).hexdigest()
    return out
