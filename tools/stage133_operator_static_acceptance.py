"""Rootless acceptance for the reviewed Stage133 operator procedure.

Execute only the archive-extraction Python stanza in a fresh user-owned temp
directory. The root-only service installer itself is NEVER invoked here.
"""
from pathlib import Path
import hashlib
import os
import re
import stat
import subprocess
import tempfile
import tarfile

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"tools/stage133_root_operator_20261121.sh"
PACKAGE=ROOT/"stage133-release-candidate-20261121/stage133-offline-release.tar"
EXPECTED="d35541ee1f1b991354f4ddbab08f186abdfb979cc56f096c4747b65d5233bab6"

def run():
    source=SCRIPT.read_text()
    assert hashlib.sha256(PACKAGE.read_bytes()).hexdigest()==EXPECTED
    assert "ROOT_REQUIRED" in source
    assert "OPERATOR_CUSTODY" in source
    assert "sha256sum -c" in source
    assert "STAGE133_ROLLBACK_STAGE132_RESTORED_PASS" in source
    assert "UNAUTHORIZED_NOBODY_SOCKET_DENIED_PASS" in source
    assert "BROKER_UID1002_STAGE133_OPTIN_PASS" in source
    assert "GATEWAY_UID988_STAGE133_OPTIN_PASS" in source
    assert "stage133-offline-release.tar" in source
    assert "sudo " not in source
    assert source.count("systemctl daemon-reload")==2
    assert source.count("restore_stage132")>=2
    assert source.count("<<'PY'")==8, source.count("<<'PY'")
    start=source.index("/usr/bin/python3 - \"$ARCHIVE\" \"$REL\" <<'PY'\n")
    code=source[start:].split("\n",1)[1].split("\nPY\n",1)[0]
    with tempfile.TemporaryDirectory(prefix="krc-stage133-unprivileged-") as directory:
        dest=Path(directory)/"release"
        process=subprocess.run(["/usr/bin/python3","-",str(PACKAGE),str(dest)],
              input=code,text=True,capture_output=True,timeout=15)
        assert process.returncode==0,(process.stdout,process.stderr)
        assert "STAGE133_ROOT_ARCHIVE_MANIFEST_PASS" in process.stdout
        with tarfile.open(PACKAGE) as archive:
            entries={e.name:archive.extractfile(e).read() for e in archive if e.isfile()}
        actual={str(p.relative_to(dest)):p.read_bytes() for p in dest.rglob("*") if p.is_file()}
        assert actual==entries
        for p in dest.rglob("*"):
            mode=stat.S_IMODE(p.stat().st_mode)
            assert mode==0o755 if p.is_dir() else mode==0o644,(str(p),mode)
        print("EXACT_ARCHIVE_EXTRACTION_TO_UNPRIVILEGED_TEMP_PASS")
        print("PER_FILE_PARITY_SHA256_PASS")
        print("DIRECTORY_MODE_755_AND_FILE_MODE_644_PASS")
    syntax=subprocess.run(["/bin/bash","-n",str(SCRIPT)],capture_output=True,text=True)
    assert syntax.returncode==0,syntax.stderr
    print("OPERATOR_BASH_STATIC_SYNTAX_PASS")
    print("NO_LIVE_RELEASE_OR_SERVICE_CHANGED")

if __name__=="__main__":
    run()
