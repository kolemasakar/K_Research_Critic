"""Stage131 mode check, isolated filesystem, no root needed."""
import os
import pytest
from krc_research.staging_entrypoint131 import _private_dir,Stage131ConfigurationError

def test_runtime_group_traverse_only(tmp_path):
    p=tmp_path/"run"
    p.mkdir(mode=0o750)
    p.chmod(0o750)
    assert _private_dir(p,os.geteuid(),allow_group_traverse=True)==p
    with pytest.raises(Stage131ConfigurationError):
        _private_dir(p,os.geteuid())
    p.chmod(0o770)
    with pytest.raises(Stage131ConfigurationError):
        _private_dir(p,os.geteuid(),allow_group_traverse=True)

def test_private_state_rejects_group_access(tmp_path):
    p=tmp_path/"state"
    p.mkdir(mode=0o700)
    p.chmod(0o700)
    assert _private_dir(p,os.geteuid())==p
    p.chmod(0o750)
    with pytest.raises(Stage131ConfigurationError):
        _private_dir(p,os.geteuid())
