"""Build and independently verify a source-only Stage133 STAGING package.

Rootless. Never writes /opt, /etc, /run, systemd, or private state.
Does not create markers, credentials, approvals, or network/provider traffic.
"""
from __future__ import annotations
import hashlib
import io
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tarfile

ROOT = Path(__file__).resolve().parents[1]
BASE_TAR = Path("/home/krcops/stage132-post-candidate-20261120/stage132-post-release-candidate-v2.tar")
BASE_SHA256 = "e1e03b5afd04d22f033711c02272e9c4b3160fc1c8c642a73988bc5c5c750993"
OUT = ROOT / "stage133-release-candidate-20261121"
PKG = OUT / "stage133-offline-release.tar"
BASENAME = "/opt/krc-stage133-offline/current"
SRC_FILES = (
    "stage132_project_post_contract.py",
    "stage132_project_post_relay.py",
    "stage132_project_post_runtime.py",
    "stage132_project_post_wire.py",
    "stage131_project_research_route.py",
    "stage131_science_semantic_contract.py",
    "stage133_science_input.py",
)
GATEWAY_FILES = (
    "stage132_project_post_relay.py",
    "stage132_project_post_runtime.py",
    "stage132_project_post_wire.py",
)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def source(path):
    raw = (ROOT / path).read_bytes()
    if not raw or len(raw) > 65536:
        raise ValueError("UNSAFE_SOURCE_BYTES "+path)
    return raw

def read_stage132_template(archive, path):
    name = "./" + path
    members = [m for m in archive.getmembers() if m.name == name]
    if len(members) != 1 or not members[0].isfile() or members[0].size > 65536:
        raise ValueError("INVALID_STAGE132_TEMPLATE")
    return archive.extractfile(members[0]).read().decode("utf-8")

def templates():
    if sha(BASE_TAR.read_bytes()) != BASE_SHA256:
        raise ValueError("STAGE132_BASE_ARCHIVE_MISMATCH")
    with tarfile.open(BASE_TAR, "r:") as archive:
        broker = read_stage132_template(archive, "deploy/krc-project-n39-post.service.example")
        gateway = read_stage132_template(archive, "deploy/20-project-pilot-post.conf.example")
    broker = broker.replace("/opt/krc-stage132-post/current", BASENAME)
    gateway = gateway.replace("/opt/krc-stage132-post/current", BASENAME)
    for name, body in (("broker", broker), ("gateway", gateway)):
        if " --enable-reviewed-staging-post" not in body or " --enable-stage133-offline-operations" in body:
            raise ValueError("UNEXPECTED_STAGE132_TEMPLATE_"+name)
    broker_on = broker.replace(" --enable-reviewed-staging-post",
        " --enable-reviewed-staging-post --enable-stage133-offline-operations")
    gateway_on = gateway.replace(" --enable-reviewed-staging-post",
        " --enable-reviewed-staging-post --enable-stage133-offline-operations")
    broker_on = broker_on.replace(
        "ConditionPathExists=/etc/krc-stage132-post/enable-reviewed-staging-post",
        "ConditionPathExists=/etc/krc-stage132-post/enable-reviewed-staging-post\n"
        "ConditionPathExists=/etc/krc-stage132-post/enable-reviewed-stage133-offline")
    return {
        "deploy/stage133-broker-default-off.service": broker.encode(),
        "deploy/stage133-gateway-default-off.conf": gateway.encode(),
        "deploy/stage133-broker-reviewed-optin.service": broker_on.encode(),
        "deploy/stage133-gateway-reviewed-optin.conf": gateway_on.encode(),
    }

def filemap():
    out = {f"src/krc_research/{name}":source(f"src/krc_research/{name}") for name in SRC_FILES}
    out.update({f"gateway-src/krc_research/{name}":source(f"src/krc_research/{name}")
                for name in GATEWAY_FILES})
    out["schemas/stage133/external_offline_payloads_v1.schema.json"] = source(
        "schemas/stage133/external_offline_payloads_v1.schema.json")
    out.update(templates())
    return out

def verify_archive(path, expected):
    with tarfile.open(path, "r:") as archive:
        members = archive.getmembers()
        names = [m.name for m in members]
        if len(set(names)) != len(names) or set(names) != set(expected) | {"SHA256SUMS"}:
            raise ValueError("ARCHIVE_ALLOWLIST_MISMATCH")
        payload = {}
        for member in members:
            name = member.name
            if (name.startswith("/") or ".." in Path(name).parts
                or not member.isfile() or member.size > 65536
                or member.mode != 0o644 or member.mtime != 0):
                raise ValueError("ARCHIVE_CUSTODY_FAILURE")
            payload[name] = archive.extractfile(member).read()
    if payload["SHA256SUMS"].decode("ascii") != "".join(
        f"{sha(expected[name])}  {name}\n" for name in sorted(expected)):
        raise ValueError("ARCHIVE_MANIFEST_MISMATCH")
    for name, raw in expected.items():
        if payload[name] != raw:
            raise ValueError("ARCHIVE_CONTENT_MISMATCH")
    return sha(path.read_bytes())

def create():
    if OUT.exists():
        raise ValueError("ALREADY_BUILT; refuse implicit overwrite")
    os.umask(0o077)
    OUT.mkdir(mode=0o700)
    expected = filemap()
    manifest = "".join(f"{sha(expected[name])}  {name}\n" for name in sorted(expected)).encode()
    with tarfile.open(PKG, "w", format=tarfile.USTAR_FORMAT) as archive:
        for name, body in sorted({**expected, "SHA256SUMS": manifest}.items()):
            item = tarfile.TarInfo(name)
            item.size = len(body)
            item.mode = 0o644
            item.mtime = 0
            item.uid = item.gid = 0
            item.uname = item.gname = "root"
            archive.addfile(item, io.BytesIO(body))
    os.chmod(PKG,0o600)
    result=verify_archive(PKG, expected)
    (OUT / "archive.sha256").write_text(result+"  stage133-offline-release.tar\n",encoding="ascii")
    print("STAGE133_ARCHIVE_ALLOWLIST_SHA256_PASS")
    print("STAGE133_ARCHIVE_SHA256="+result)
    print("STAGE133_ARCHIVE_MEMBERS="+str(len(expected)+1))
    for role,which in (("broker","src"),("gateway","gateway-src")):
        dep="/opt/krc-project-n39-read/549d44868f188c6f6715bd9224c6fa4de29b05cf/src" if role=="broker" else "/opt/krc-research-v2/src"
        target=OUT / ("audit-"+role)
        target.mkdir()
        for name,raw in expected.items():
            if name.startswith(which+"/"):
                p=target/name.removeprefix(which+"/")
                p.parent.mkdir(parents=True,exist_ok=True)
                p.write_bytes(raw)
        env=os.environ.copy()
        env["PYTHONPATH"]=str(target)+":"+dep
        env["PYTHONNOUSERSITE"]="1"
        env["PYTHONDONTWRITEBYTECODE"]="1"
        cmd=[sys.executable,"-s","-c",
             "from krc_research.stage132_project_post_runtime import reviewed_offline_operations;"
             "assert reviewed_offline_operations()==frozenset({'research.profile.validate'});"
             "from krc_research.stage132_project_post_wire import OFFLINE_OPS;"
             "assert len(OFFLINE_OPS)==3;"
             "print('DEFAULT_OFF_AND_IMPORTS_PASS')"]
        subprocess.run(cmd,env=env,check=True,timeout=15)
        print("ROLE_IMPORT_"+role.upper()+"_PASS")
    assert b"--enable-stage133-offline-operations" not in expected["deploy/stage133-broker-default-off.service"]
    assert b"--enable-stage133-offline-operations" not in expected["deploy/stage133-gateway-default-off.conf"]
    assert b"--enable-stage133-offline-operations" in expected["deploy/stage133-broker-reviewed-optin.service"]
    assert b"--enable-stage133-offline-operations" in expected["deploy/stage133-gateway-reviewed-optin.conf"]
    assert b"ConditionPathExists=/etc/krc-stage132-post/enable-reviewed-stage133-offline" in expected["deploy/stage133-broker-reviewed-optin.service"]
    print("TWO_ROLE_OPTIN_TEMPLATES_PASS")
    print("NO_INSTALL_NO_SERVICE_MUTATION")

if __name__ == "__main__":
    create()
