"""KRC Public Research MCP — experimental SDK-backed server.

One FIFO worker; no video/providers; guests use per-job opaque capabilities.
Never expose directly to internet before review of operational controls.
"""
import base64
import hashlib
import json
import os
import secrets
import sqlite3
import threading
import time
import uuid
from contextlib import contextmanager
from pathlib import Path

TEN_HOURS = 36000
MIN_FREE = 0.10
MAX_DOC = 16 * 1024 * 1024
MAX_CHUNK = 160 * 1024
MAX_PAYLOAD = 256 * 1024
MAX_DOCUMENTS = 32
TOOLS = ("research_profile_validate", "claim_evidence_audit", "research_report_validate")
RISK = {"LOW": 0, "MEDIUM": 1, "HIGH": 2, "CRITICAL": 3}
FLOORS = {"medicine": ("CRITICAL", 3), "law": ("HIGH", 2), "finance": ("HIGH", 2),
          "construction": ("HIGH", 2), "geodesy": ("HIGH", 2),
          "military": ("HIGH", 2), "software": ("MEDIUM", 1)}


def analyze(tool: str, payload: dict) -> dict:
    if not isinstance(payload, dict):
        raise ValueError("payload must be an object")
    if tool == "research_profile_validate":
        domain = str(payload.get("domain", "general")).lower()
        floor, n = FLOORS.get(domain, ("MEDIUM", 1))
        proposed = str(payload.get("risk_level", floor)).upper()
        count = payload.get("required_cross_checks", 0)
        if proposed not in RISK or type(count) is not int or count < 0:
            raise ValueError("invalid risk level or cross checks")
        risk = max(proposed, floor, key=lambda x: RISK[x])
        return {"risk_level": risk, "required_cross_checks": max(count, n, RISK[risk]),
                "approved": False, "domain": domain,
                "notice": "CriticProfile approval must be obtained from the human user"}
    if tool == "claim_evidence_audit":
        origins = payload.get("evidence_origins", [])
        required = payload.get("required", 1)
        if not isinstance(origins, list) or len(origins) > 1000 or type(required) is not int or required < 0:
            raise ValueError("invalid evidence ledger")
        if any(not isinstance(x, str) or not x.strip() or len(x) > 256 for x in origins):
            raise ValueError("invalid origin identifier")
        unique = set(x.strip().casefold() for x in origins)
        return {"required": required, "achieved_independent": len(unique),
                "duplicate_origins": len(origins) - len(unique),
                "status": "PASS" if len(unique) >= required else "SHORTFALL",
                "notice": "Evidence origin independence must be verified externally"}
    if tool == "research_report_validate":
        report = payload.get("report", "")
        if not isinstance(report, str):
            raise ValueError("report must be a string")
        headings = ["ФІНАЛЬНИЙ ЗВІТ", "ПЕРЕВІРКА ТВЕРДЖЕНЬ",
                    "ПРОТОКОЛ ПЕРЕВІРКИ", "ПІДСУМОК ЗА ТВЕРДЖЕННЯМИ"]
        missing = [heading for heading in headings if heading not in report.upper()]
        return {"valid_structure": not missing, "missing_sections": missing,
                "notice": "This validates structure, not factual accuracy"}
    raise ValueError("unknown research tool")


def digest(token: str) -> str:
    if not isinstance(token, str) or len(token) < 32 or len(token) > 200:
        raise ValueError("invalid guest capability")
    return hashlib.sha256(token.encode()).hexdigest()


class QueueStore:
    def __init__(self, root: str):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True, mode=0o700)
        self.docs = self.root / "docs"
        self.docs.mkdir(exist_ok=True, mode=0o700)
        self.db = self.root / "queue.sqlite3"
        self.lock = threading.RLock()
        self.wake = threading.Event()
        self.stop = threading.Event()
        self._init_db()

    @contextmanager
    def connect(self):
        c = sqlite3.connect(str(self.db), isolation_level=None, timeout=15)
        try:
            c.execute("PRAGMA busy_timeout=15000")
            c.execute("PRAGMA journal_mode=WAL")
            yield c
        finally:
            c.close()

    def _init_db(self):
        with self.connect() as c:
            c.execute("CREATE TABLE IF NOT EXISTS jobs("
                      "seq INTEGER PRIMARY KEY AUTOINCREMENT, id TEXT UNIQUE NOT NULL,"
                      "owner TEXT NOT NULL, kind TEXT NOT NULL, payload TEXT NOT NULL,"
                      "doc TEXT, state TEXT NOT NULL, result TEXT, created REAL NOT NULL,"
                      "completed REAL, delivered REAL, expires REAL)")
            c.execute("CREATE TABLE IF NOT EXISTS documents("
                      "id TEXT PRIMARY KEY, owner TEXT NOT NULL, path TEXT NOT NULL,"
                      "length INTEGER NOT NULL, complete INTEGER NOT NULL,"
                      "created REAL NOT NULL, expires REAL)")
            c.execute("UPDATE jobs SET state='queued' WHERE state='running'")

    def disk_guard(self, n: int):
        stat = os.statvfs(self.root)
        available = stat.f_bavail * stat.f_frsize
        reserve = (stat.f_blocks * stat.f_frsize + 9) // 10
        if available - n < reserve:
            raise ValueError("storage_reserve_exhausted: must retain 10% free disk")

    def create_guest(self):
        return secrets.token_urlsafe(32)

    def submit(self, guest: str, kind: str, payload: dict, doc: str = "") -> dict:
        owner = digest(guest)
        if kind not in TOOLS:
            raise ValueError("unsupported research tool")
        if not isinstance(payload, dict):
            raise ValueError("payload must be an object")
        body = json.dumps(payload, ensure_ascii=False)
        if len(body.encode("utf-8")) > MAX_PAYLOAD:
            raise ValueError("payload too large; upload document in chunks")
        now = time.time()
        with self.lock, self.connect() as c:
            self.disk_guard(len(body.encode()) + 4096)
            if doc:
                d = c.execute("SELECT owner, complete FROM documents WHERE id=?", (doc,)).fetchone()
                if d is None or d[0] != owner or d[1] != 1:
                    raise ValueError("document not found, not complete or not owned")
            ident = uuid.uuid4().hex
            c.execute("INSERT INTO jobs(id,owner,kind,payload,doc,state,created)"
                      " VALUES(?,?,?,?,?,'queued',?)",
                      (ident, owner, kind, body, doc or None, now))
            position = c.execute("SELECT COUNT(*) FROM jobs WHERE state='queued'").fetchone()[0]
        self.wake.set()
        return {"job_id": ident, "state": "queued", "queue_position": position,
                "message": "Запит поставлено до черги FIFO"}

    def status(self, guest: str, job_id: str, acknowledge: bool = False) -> dict:
        owner = digest(guest)
        with self.lock, self.connect() as c:
            r = c.execute("SELECT state,result,completed,delivered,expires,doc FROM jobs"
                          " WHERE id=? AND owner=?", (job_id, owner)).fetchone()
            if r is None:
                return {"status": "not_found_or_expired"}
            state, result, completed, delivered, expiry, doc = r
            now = time.time()
            if expiry is not None and expiry <= now:
                return {"status": "expired"}
            if acknowledge and state in ("done", "failed"):
                if delivered is None:
                    delivered, expiry = now, now + TEN_HOURS
                    c.execute("UPDATE jobs SET delivered=?,expires=? WHERE id=?",
                              (delivered, expiry, job_id))
                    if doc:
                        c.execute("UPDATE documents SET expires=? WHERE id=?",
                                  (expiry, doc))
            position = 0
            if state == "queued":
                seq = c.execute("SELECT seq FROM jobs WHERE id=?", (job_id,)).fetchone()[0]
                position = c.execute("SELECT COUNT(*) FROM jobs WHERE state='queued' AND seq<=?",
                                     (seq,)).fetchone()[0]
            return {"status": state, "queue_position": position,
                    "result": json.loads(result) if result is not None else None,
                    "expires": expiry}

    def upload(self, guest: str, chunk_b64: str, document_id: str = "",
               final: bool = False) -> dict:
        owner = digest(guest)
        if len(chunk_b64) > MAX_CHUNK * 2:
            raise ValueError("chunk too large")
        try:
            data = base64.b64decode(chunk_b64, validate=True)
        except Exception as e:
            raise ValueError("invalid base64") from e
        if len(data) > MAX_CHUNK:
            raise ValueError("chunk too large")
        now = time.time()
        with self.lock, self.connect() as c:
            self.disk_guard(len(data) + 4096)
            if document_id:
                row = c.execute("SELECT owner,path,length,complete FROM documents WHERE id=?",
                                (document_id,)).fetchone()
                if row is None or row[0] != owner or row[3]:
                    raise ValueError("document not found, owned by other guest or complete")
                path, length = Path(row[1]), row[2]
            else:
                self._evict_if_needed(c)
                document_id = uuid.uuid4().hex
                path = self.docs / (document_id + ".tmp")
                length = 0
                c.execute("INSERT INTO documents(id,owner,path,length,complete,created,expires)"
                          " VALUES(?,?,?,?,0,?,?)",
                          (document_id, owner, str(path), 0, now, now + TEN_HOURS))
            if length + len(data) > MAX_DOC:
                raise ValueError("document exceeds 16 MiB")
            with open(path, "ab") as handle:
                os.chmod(path, 0o600)
                handle.write(data)
            c.execute("UPDATE documents SET length=?,complete=?,expires=? WHERE id=?",
                      (length + len(data), int(final), now + TEN_HOURS, document_id))
        return {"document_id": document_id, "bytes": length + len(data), "complete": final}

    def _evict_if_needed(self, c):
        count = c.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
        if count < MAX_DOCUMENTS:
            return
        row = c.execute(
            "SELECT d.id,d.path FROM documents d WHERE NOT EXISTS("
            " SELECT 1 FROM jobs j WHERE j.doc=d.id AND j.state IN ('queued','running'))"
            " ORDER BY d.created,d.id LIMIT 1").fetchone()
        if row is None:
            raise ValueError("all documents protected; cannot safely evict")
        Path(row[1]).unlink(missing_ok=True)
        c.execute("DELETE FROM documents WHERE id=?", (row[0],))

    def run_one(self) -> bool:
        with self.lock, self.connect() as c:
            row = c.execute("SELECT id,kind,payload,doc FROM jobs WHERE state='queued'"
                            " ORDER BY seq LIMIT 1").fetchone()
            if row is None:
                return False
            jid, kind, raw, doc = row
            c.execute("UPDATE jobs SET state='running' WHERE id=?", (jid,))
        try:
            payload = json.loads(raw)
            if doc:
                with self.connect() as c:
                    r = c.execute("SELECT path,complete FROM documents WHERE id=?", (doc,)).fetchone()
                if not r or not r[1]:
                    raise ValueError("document unavailable")
                raw_doc = Path(r[0]).read_bytes()
                if len(raw_doc) > MAX_DOC:
                    raise ValueError("document exceeds limit")
                payload = dict(payload)
                if kind == "research_report_validate":
                    payload["report"] = raw_doc.decode("utf-8")
                else:
                    obj = json.loads(raw_doc.decode("utf-8"))
                    if not isinstance(obj, dict):
                        raise ValueError("document must contain JSON object")
                    payload.update(obj)
            result, state = analyze(kind, payload), "done"
        except Exception as e:
            result, state = {"error": str(e)}, "failed"
        now = time.time()
        with self.lock, self.connect() as c:
            c.execute("UPDATE jobs SET state=?,result=?,completed=?,expires=? WHERE id=?",
                      (state, json.dumps(result, ensure_ascii=False), now, now + TEN_HOURS, jid))
            if doc:
                c.execute("UPDATE documents SET expires=? WHERE id=?", (now + TEN_HOURS, doc))
        return True

    def cleanup(self):
        now = time.time()
        with self.lock, self.connect() as c:
            files = c.execute(
                "SELECT d.id,d.path FROM documents d WHERE d.expires<=? AND NOT EXISTS("
                " SELECT 1 FROM jobs j WHERE j.doc=d.id AND j.state IN ('queued','running'))",
                (now,)).fetchall()
            for ident, path in files:
                Path(path).unlink(missing_ok=True)
                c.execute("DELETE FROM documents WHERE id=?", (ident,))
            c.execute("DELETE FROM jobs WHERE expires<=? AND state IN ('done','failed')", (now,))
            # Never expire jobs still queued: owner requires FIFO without
            # queue-time deadline. Cleanup applies after completion only.

    def background(self):
        def work():
            while not self.stop.is_set():
                if not self.run_one():
                    self.wake.wait(0.5)
                    self.wake.clear()
        def sweep():
            while not self.stop.wait(60):
                self.cleanup()
        self.worker = threading.Thread(target=work, daemon=True, name="krc-fifo-worker")
        self.sweeper = threading.Thread(target=sweep, daemon=True, name="krc-ttl-sweeper")
        self.worker.start()
        self.sweeper.start()


def app():
    from mcp.server.fastmcp import FastMCP

    host = os.environ.get("KRC_HOST", "127.0.0.1")
    port = int(os.environ.get("KRC_PORT", "9013"))
    root = os.environ.get("KRC_STATE", "/tmp/krc-public-mcp-dev")
    store = QueueStore(root)
    store.background()
    mcp = FastMCP("KRC Public Research", host=host, port=port,
                  stateless_http=True, json_response=True)

    @mcp.tool()
    def guest_session() -> dict:
        """Create a no-login private capability for a temporary guest job."""
        return {"guest_token": store.create_guest()}

    @mcp.tool()
    def research_submit(guest_token: str, tool: str, payload: dict,
                        document_id: str = "") -> dict:
        """Enqueue a research check (FIFO); return queue status and job id."""
        return store.submit(guest_token, tool, payload, document_id)

    @mcp.tool()
    def research_status(guest_token: str, job_id: str,
                        acknowledge_delivery: bool = False) -> dict:
        """Check FIFO position or result; optionally acknowledge delivery."""
        return store.status(guest_token, job_id, acknowledge_delivery)

    @mcp.tool()
    def research_document_upload(guest_token: str, chunk_base64: str,
                                 document_id: str = "", final: bool = False) -> dict:
        """Upload part of a temporary document; max 160 KiB decoded per chunk."""
        return store.upload(guest_token, chunk_base64, document_id, final)

    @mcp.tool()
    def research_profile_validate(payload: dict, guest_token: str = "") -> dict:
        """Enqueue CriticProfile validation in FIFO; return private guest capability."""
        token = guest_token or store.create_guest()
        return {"guest_token": token, **store.submit(token, "research_profile_validate", payload)}

    @mcp.tool()
    def claim_evidence_audit(payload: dict, guest_token: str = "") -> dict:
        """Enqueue evidence-origin quality check; no truth determination."""
        token = guest_token or store.create_guest()
        return {"guest_token": token, **store.submit(token, "claim_evidence_audit", payload)}

    @mcp.tool()
    def research_report_validate(payload: dict, guest_token: str = "") -> dict:
        """Enqueue Ukrainian report structure check in FIFO."""
        token = guest_token or store.create_guest()
        return {"guest_token": token, **store.submit(token, "research_report_validate", payload)}

    return mcp


if __name__ == "__main__":
    app().run(transport="streamable-http")
