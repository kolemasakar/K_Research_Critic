"""KRC-SCIENCE-1 private research exchange contract (offline validation).
No network, no implicit trust, no execution of research from unverified requests.
"""
from __future__ import annotations
import hashlib, hmac, json, re
from datetime import datetime, timezone

VERSION="krc-science/1"
CLIENT="K_Science"
PROVIDER="K_Research_Critic"
ALLOWED={"research.profile.validate","research.evidence.preflight",
         "research.bibliography.audit","research.inspection.review"}
ID=re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_.:-]{7,119}$")

def _canonical(obj):
    return json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False).encode("utf-8")

def envelope(*, task_id:str, operation:str, payload:dict, created_at:str,
             client:str=CLIENT, provider:str=PROVIDER, version:str=VERSION)->dict:
    if not ID.fullmatch(task_id) or operation not in ALLOWED:
        raise ValueError("Invalid task id or operation")
    if not isinstance(payload,dict) or len(_canonical(payload))>262144:
        raise ValueError("Invalid payload or too large")
    parsed=datetime.fromisoformat(created_at.replace("Z","+00:00"))
    if parsed.utcoffset() is None:
        raise ValueError("Timezone missing")
    body={"version":version,"task_id":task_id,"client":client,"provider":provider,
          "operation":operation,"created_at":created_at,"payload":payload}
    return {**body,"payload_sha256":hashlib.sha256(_canonical(payload)).hexdigest()}

def sign_envelope(body:dict, key:bytes)->str:
    if not isinstance(key,bytes) or len(key)<32: raise ValueError("Weak or absent key")
    return hmac.new(key,_canonical(body),hashlib.sha256).hexdigest()

def validate_envelope(body:dict,*, key:bytes, signature:str, allowed_client=CLIENT,
                      allowed_operations=ALLOWED, max_age_seconds=600, now=None)->dict:
    if set(body)!={"version","task_id","client","provider","operation","created_at","payload","payload_sha256"}:
        raise ValueError("Envelope fields mismatch")
    rebuilt=envelope(task_id=body["task_id"],operation=body["operation"],
                    payload=body["payload"],created_at=body["created_at"],
                    client=body["client"],provider=body["provider"],version=body["version"])
    if body!=rebuilt: raise ValueError("Envelope checksum mismatch")
    if body["version"]!=VERSION or body["provider"]!=PROVIDER or body["client"]!=allowed_client:
        raise ValueError("Unauthorized route")
    if body["operation"] not in allowed_operations: raise ValueError("Operation denied")
    expected=sign_envelope(body,key)
    if not isinstance(signature,str) or not hmac.compare_digest(expected,signature):
        raise ValueError("Invalid signature")
    instant=datetime.fromisoformat(body["created_at"].replace("Z","+00:00")).astimezone(timezone.utc)
    current=now or datetime.now(timezone.utc)
    if abs((current-instant).total_seconds())>max_age_seconds:
        raise ValueError("Expired or future request")
    return {"route":"KS->KRC","task_id":body["task_id"],"operation":body["operation"],
            "authenticated":True,"author_approval_provided":False,
            "replay_protection":"REQUIRES_SERVER_SIDE_TASK_ID_REGISTRY"}

def check_replay(task_id:str,seen:set[str])->None:
    if task_id in seen: raise ValueError("Replayed task id")
    seen.add(task_id)
