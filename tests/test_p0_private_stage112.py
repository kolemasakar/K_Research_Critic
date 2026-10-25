import hashlib,hmac,json
from datetime import datetime,timezone,timedelta
import pytest
from krc_research.interproject_contract import envelope,sign_envelope
from krc_research.private_stage111 import digest_profile
from krc_research.private_stage112 import approval_chain_append,approval_chain_verify,dispatch_coded
KEY=b'k'*32
NOW=datetime(2026,10,25,12,tzinfo=timezone.utc)
PROFILE={'profile_id':'p1','version':'v1','protocol':'KRC Core','topic':'Concrete'}
def receipt():
 r={'profile_id':'p1','profile_version':'v1','profile_sha256':digest_profile(PROFILE),'signer_id':'owner1','approved_at':'2026-10-25T12:00:00Z'}
 r['signature']=hmac.new(KEY,json.dumps(r,sort_keys=True,separators=(',',':')).encode(),hashlib.sha256).hexdigest()
 return r
def env(at=None):
 return envelope(task_id='ksci-stage112-0001',operation='research.profile.validate',payload={'critic_profile':PROFILE},created_at=(at or NOW).isoformat())
def call(body=None,signature=None,seen=None,permitted=None):
 b=body or env()
 return dispatch_coded(b,secret=KEY,signature=sign_envelope(b,KEY) if signature is None else signature,seen=set() if seen is None else seen,permitted={'research.profile.validate'} if permitted is None else permitted,now=NOW)
def test_success():assert call()['engine_result']['validation']=='STRUCTURE_VALID'
def test_invalid_signature():assert call(signature='0'*64)['error']['code']=='UNAUTHORIZED'
def test_expired():assert call(body=env(NOW-timedelta(hours=1)))['error']['code']=='EXPIRED_REQUEST'
def test_acl():assert call(permitted=set())['error']['code']=='OPERATION_DENIED'
def test_replay():
 seen=set();assert 'engine_result' in call(seen=seen)
 assert call(seen=seen)['error']['code']=='REPLAY_REJECTED'
def test_malformed():assert dispatch_coded(None,secret=KEY,signature='',seen=set(),permitted=set())['error']['code']=='INVALID_REQUEST'
def test_chain_tamper():
 chain=approval_chain_append([],PROFILE,receipt(),{'owner1':KEY})
 assert approval_chain_verify(chain)['status']=='INTEGRITY_OK_NOT_ATTESTED'
 chain[0]['payload']['receipt']['profile_version']='v2'
 with pytest.raises(ValueError):approval_chain_verify(chain)
def test_untrusted_signer_denied():
 with pytest.raises(ValueError):approval_chain_append([],PROFILE,receipt(),{})
