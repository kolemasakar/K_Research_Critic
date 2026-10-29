"""Stage131 offline read-only preinstall audit regression."""
import importlib.util
from pathlib import Path

P=Path(__file__).resolve().parents[1]/"scripts/stage131_preinstall_audit.py"
spec=importlib.util.spec_from_file_location("stage131_preinstall_audit",P)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def test_preinstall_modes_and_absent_paths(tmp_path):
    uid=__import__("os").geteuid()
    private=tmp_path/"private"
    private.mkdir(mode=0o700)
    private.chmod(0o700)
    assert mod.inspect_path(str(private),uid,directory=True,expected_mode=0o700)["status"]=="PASS"
    private.chmod(0o750)
    assert mod.inspect_path(str(private),uid,directory=True,expected_mode=0o700)["status"]=="DENIED"
    assert mod.inspect_path(str(tmp_path/"absent"),uid,directory=False,expected_mode=0o600)["status"]=="NOT_READY"

def test_preinstall_never_reads_secret_bytes(tmp_path):
    uid=__import__("os").geteuid()
    p=tmp_path/"secret.key"
    p.write_bytes(b"synthetic-do-not-read")
    p.chmod(0o600)
    assert mod.inspect_path(str(p),uid,directory=False,expected_mode=0o600)["status"]=="PASS"
    p.chmod(0o644)
    assert mod.inspect_path(str(p),uid,directory=False,expected_mode=0o600)["status"]=="DENIED"
