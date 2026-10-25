import hashlib,hmac,json
from datetime import datetime,timezone
from krc_research.private_stage111 import approval_attestation,digest_profile,isolated_dispatch
from krc_research.interproject_contract import envelope,sign_envelope
KEY=b'k'*32
NOW=datetime(2026,10,25,12,tzinfo=timezone.utc)
PROFILE={'profile_id':'p1','version':'v1','protocol':'KRC Core','topic':'Concrete'}
def receipt():
 r={'profile_id':'p1','profile_version':'v1','profile_sha256':digest_profile(PROFILE),'signer_id':'owner1','approved_at':'2026-10-25T12:00:00Z'}
 r['signature']=hmac.new(KEY,json.dumps(r,sort_keys=True,separators=(',',':')).encode(),hashlib.sha256).hexdigest()
 return r
def call(op,payload,**kw):
 e=envelope(task_id='ksci-stage111-0001',operation=op,payload=payload,created_at=NOW.isoformat())
 return isolated_dispatch(e,secret=KEY,signature=sign_envelope(e,KEY),seen=set(),permitted={op},now=NOW,**kw)
def test_signature_bound(): assert approval_attestation(PROFILE,receipt(),{'owner1':KEY})=='SIGNED_BY_CONFIGURED_KEY_NOT_HUMAN_VERIFIED'
def test_wrong_profile(): assert approval_attestation({**PROFILE,'topic':'Changed'},receipt(),{'owner1':KEY})=='PROFILE_MISMATCH'
def test_wrong_signer(): assert approval_attestation(PROFILE,receipt(),{})=='UNTRUSTED_SIGNER'
def test_bad_signature():
 r=receipt();r['signature']='0'*64
 assert approval_attestation(PROFILE,r,{'owner1':KEY})=='INVALID_SIGNATURE'
def test_all_four_offline():
 gate={k:False for k in ('journal_policy_checked','search_audit_reproducible','primary_sources_inspected','novelty_reviewed','citations_validated','scientific_methods_audited','rights_and_ai_disclosure_done','human_author_approved')}
 cases=[('research.profile.validate',{'critic_profile':PROFILE}),('research.evidence.preflight',{'user_profile_approved':True,'manuscript_gate':gate}),('research.bibliography.audit',{'dois':['10.1234/test']}),('research.inspection.review',{'receipt':{'source_id':'S01','origin_id':'O01','doi':'10.1234/test','document_sha256':'a'*64,'inspected_sections':['Methods'],'passage_locators':['p1'],'checked_at':NOW.isoformat(),'inspector_id':'I','method':'FULL_TEXT','evidence_relation':'INSUFFICIENT','external_trace_id':'x'}})]
 for op,payload in cases:
  o=call(op,payload,bibliography_fn=lambda dois:{'count':len(dois)})
  assert o.get('operation')==op,o
  assert o['scientific_approval'] is False
def test_permission_denied():
 e=envelope(task_id='ksci-stage111-0002',operation='research.profile.validate',payload={'critic_profile':PROFILE},created_at=NOW.isoformat())
 o=isolated_dispatch(e,secret=KEY,signature=sign_envelope(e,KEY),seen=set(),permitted=set(),now=NOW)
 assert o['error']['code']=='OPERATION_DENIED'
