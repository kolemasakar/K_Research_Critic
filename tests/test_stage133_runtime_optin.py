"""Source-only opt-in gate tests. No actual root marker or service mutation."""
import stat
from types import SimpleNamespace
import pytest
from krc_research import stage132_project_post_runtime as runtime
from krc_research.stage132_project_post_wire import DEFAULT_OPS, OFFLINE_OPS

class Stub:
    def __init__(self, uid,mode=0o600,links=1):
        self.uid,self.mode,self.links=uid,mode,links
    def lstat(self):
        return SimpleNamespace(st_uid=self.uid,st_mode=stat.S_IFREG|self.mode,st_nlink=self.links)

def test_default_off_remains_profile_only():
    assert runtime.reviewed_offline_operations(False)==DEFAULT_OPS
    assert OFFLINE_OPS > DEFAULT_OPS

@pytest.mark.parametrize("uid,mode,links",[(1002,0o600,1),(0,0o644,1),(0,0o600,2)])
def test_broken_root_marker_denied(monkeypatch,uid,mode,links):
    monkeypatch.setattr(runtime,"STAGE133_MARKER",Stub(uid,mode,links))
    with pytest.raises(ValueError,match="STAGE133_MARKER_CUSTODY"):
        runtime.reviewed_offline_operations(True)

def test_only_explicit_flag_and_valid_root_marker_enables(monkeypatch):
    monkeypatch.setattr(runtime,"STAGE133_MARKER",Stub(0,0o600,1))
    assert runtime.reviewed_offline_operations(False)==DEFAULT_OPS
    assert runtime.reviewed_offline_operations(True)==OFFLINE_OPS
