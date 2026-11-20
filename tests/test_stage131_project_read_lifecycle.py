"""Source-only lifecycle tests with real isolated producer state and AF_UNIX."""
import os,socket,stat,threading,time,sqlite3
import pytest
from test_stage131_project_read_joint_fault_matrix import state,msg,wire,KEY
from krc_research.stage131_artifact_nonce_registry import ArtifactNonceRegistry
from krc_research.stage131_project_signed_read import ProjectSignedArtifactBoundary
from krc_research.stage131_project_read_lifecycle import (
    producer_preflight,existing_nonce,run_reader,notify_ready,marker_check
)

@pytest.fixture(autouse=True)
def private_umask():
    old=os.umask(0o077)
    try:yield
    finally:os.umask(old)

def test_ready_requires_valid_producer_and_existing_nonce(tmp_path):
    r,p,a=state(tmp_path)
    assert producer_preflight(r.root).root==r.root
    n=tmp_path/"nonce";n.mkdir(mode=0o700)
    with pytest.raises(FileNotFoundError):existing_nonce(n/"nonce.sqlite")
    assert not (n/"nonce.sqlite").exists()
    ArtifactNonceRegistry(n/"nonce.sqlite")
    assert existing_nonce(n/"nonce.sqlite").claim("k","n","p")
    assert not existing_nonce(n/"nonce.sqlite").claim("k","n","p")
    with sqlite3.connect(n/"nonce.sqlite") as db:db.execute("DROP TABLE used")
    with pytest.raises(ValueError,match="NONCE_SCHEMA_MISMATCH"):existing_nonce(n/"nonce.sqlite")
    with sqlite3.connect(r.root/"requests.sqlite") as db:db.execute("ALTER TABLE requests RENAME TO old_requests")
    with pytest.raises(sqlite3.Error):producer_preflight(r.root)

def test_notify_after_listen_and_restart_preserves_nonce(tmp_path):
    r,p,a=state(tmp_path)
    n=tmp_path/"nonce";n.mkdir(mode=0o700);np=n/"nonce.sqlite"
    ArtifactNonceRegistry(np)
    path=tmp_path/"backend.sock";notify=tmp_path/"notify.sock"
    message=msg(p["request_id"],a["artifact_id"])
    with socket.socket(socket.AF_UNIX,socket.SOCK_DGRAM) as listener:
        listener.bind(str(notify));listener.settimeout(4)
        for expected in (200,403):
            stop=threading.Event();errors=[]
            authority=producer_preflight(r.root);registry=existing_nonce(np)
            boundary=ProjectSignedArtifactBoundary(authority=authority,nonce_registry=registry,
                key=KEY,peer_uid=os.getuid(),enabled=True)
            def work():
                try:run_reader(path,boundary,ready=lambda:notify_ready(str(notify)),stop=stop)
                except BaseException as e:errors.append(e)
            t=threading.Thread(target=work);t.start()
            try:
                data=listener.recv(1024)
                assert data.startswith(b"READY=1\n") and path.is_socket()
                assert stat.S_IMODE(path.stat().st_mode)==0o660
                assert wire(path,message)[0]==expected
            finally:stop.set();t.join(5)
            assert not t.is_alive() and not errors and not path.exists()

def test_cannot_replace_existing_socket_or_notify_invalid_address(tmp_path):
    path=tmp_path/"occupied";path.write_text("unchanged")
    with pytest.raises(ValueError,match="SOCKET_ALREADY_EXISTS"):
        run_reader(path,None,ready=lambda:None,stop=threading.Event())
    assert path.read_text()=="unchanged"
    with pytest.raises(ValueError,match="NOTIFY_SOCKET_REQUIRED"):notify_ready("relative")
    with pytest.raises(FileNotFoundError):marker_check(tmp_path/"missing")
    path.chmod(0o644)
    with pytest.raises(ValueError,match="CONTINUOUS_RELEASE_MARKER_DENIED"):marker_check(path)
