import hashlib
import pytest
from krc_research.artifact_stage117 import HardenedExchange
from krc_research.artifact_exchange import ExchangeError

def test_secure_read_and_hash(tmp_path):
 s=HardenedExchange(tmp_path/'store',free_bytes_min=0)
 item=s.store_stream([b'a'*1000,b'b'],principal='P',request_id='R',filename='m.pdf')
 assert b''.join(s.read_stream(item['artifact_id'],principal='P',request_id='R',chunk_size=127))==b'a'*1000+b'b'

def test_disk_guard(tmp_path):
 s=HardenedExchange(tmp_path/'store',free_bytes_min=10**18)
 with pytest.raises(ExchangeError,match='LOW_DISK_SPACE'):
  s.store_stream([b'x'],principal='p',request_id='r',filename='f')

def test_scope(tmp_path):
 s=HardenedExchange(tmp_path/'store',free_bytes_min=0)
 a=s.store_stream([b'x'],principal='p',request_id='r',filename='f')
 with pytest.raises(ExchangeError,match='NOT_FOUND'):
  list(s.read_stream(a['artifact_id'],principal='q',request_id='r'))

def test_expired_and_cleanup(tmp_path):
 now=[100.]
 s=HardenedExchange(tmp_path/'store',free_bytes_min=0,ttl=1,clock=lambda:now[0])
 a=s.store_stream([b'x'],principal='p',request_id='r',filename='f')
 now[0]=102.
 with pytest.raises(ExchangeError,match='ARTIFACT_EXPIRED'):
  list(s.read_stream(a['artifact_id'],principal='p',request_id='r'))
 assert s.cleanup_expired()==1

def test_recovery_orphan(tmp_path):
 s=HardenedExchange(tmp_path/'store',free_bytes_min=0)
 (s.data/('a'*48)).write_bytes(b'orphan')
 (s.data/'.pending-x').write_bytes(b'temp')
 a=s.store_stream([b'valid'],principal='p',request_id='r',filename='f')
 assert s.reconcile_staging()==2
 assert b''.join(s.read_stream(a['artifact_id'],principal='p',request_id='r'))==b'valid'

def test_corrupt_file(tmp_path):
 s=HardenedExchange(tmp_path/'store',free_bytes_min=0)
 a=s.store_stream([b'x'],principal='p',request_id='r',filename='f')
 (s.data/a['artifact_id']).write_bytes(b'y')
 with pytest.raises(ExchangeError,match='ARTIFACT_CORRUPTED'):
  list(s.read_stream(a['artifact_id'],principal='p',request_id='r'))
