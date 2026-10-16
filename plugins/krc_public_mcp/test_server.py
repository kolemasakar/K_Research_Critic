"""Regression tests for KRC Public MCP server core. Run: python3 -m unittest -v."""
import base64
import json
import os
import sqlite3
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest.mock import patch
from server import QueueStore, analyze, TEN_HOURS


class TestResearch(unittest.TestCase):
    def test_risk_floor(self):
        v = analyze("research_profile_validate", {"domain": "medicine", "risk_level": "LOW"})
        self.assertEqual((v["risk_level"], v["required_cross_checks"]), ("CRITICAL", 3))
        self.assertFalse(v["approved"])

    def test_evidence_duplicates(self):
        v = analyze("claim_evidence_audit", {"required": 2, "evidence_origins": ["Source A", "source a"]})
        self.assertEqual(v["status"], "SHORTFALL")
        self.assertEqual(v["duplicate_origins"], 1)

    def test_report_heading_check(self):
        self.assertFalse(analyze("research_report_validate", {"report": "Текст"})["valid_structure"])


class TestQueue(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.s = QueueStore(self.tmp.name)
        self.token = self.s.create_guest()

    def tearDown(self):
        self.tmp.cleanup()

    def enqueue(self, token=None, doc=""):
        return self.s.submit(token or self.token, "claim_evidence_audit",
                             {"evidence_origins": ["one", "two"], "required": 2}, doc)

    def test_fifo_and_result(self):
        ids = [self.enqueue()["job_id"] for _ in range(3)]
        self.assertEqual(self.s.status(self.token, ids[-1])["queue_position"], 3)
        for jid in ids:
            self.assertTrue(self.s.run_one())
            self.assertEqual(self.s.status(self.token, jid)["status"], "done")
        self.assertFalse(self.s.run_one())

    def test_cross_guest_isolation(self):
        job = self.enqueue()
        self.assertEqual(self.s.status(self.s.create_guest(), job["job_id"])["status"],
                         "not_found_or_expired")

    def test_ten_parallel_submissions(self):
        out = []
        lock = threading.Lock()
        def submit():
            result = self.enqueue()
            with lock:
                out.append(result["job_id"])
        threads = [threading.Thread(target=submit) for _ in range(10)]
        for t in threads: t.start()
        for t in threads: t.join()
        self.assertEqual(len(set(out)), 10)
        for i in range(10):
            self.assertTrue(self.s.run_one())
        self.assertTrue(all(self.s.status(self.token, j)["status"] == "done" for j in out))

    def test_pending_survives_restart_and_ttl(self):
        j = self.enqueue()["job_id"]
        with self.s.connect() as c:
            c.execute("UPDATE jobs SET created=? WHERE id=?", (time.time()-TEN_HOURS*2, j))
        self.s.cleanup()
        self.assertEqual(self.s.status(self.token, j)["status"], "queued")
        reopened = QueueStore(self.tmp.name)
        self.assertEqual(reopened.status(self.token, j)["status"], "queued")

    def test_unclaimed_expiry_ten_hours(self):
        j = self.enqueue()["job_id"]
        self.s.run_one()
        with self.s.connect() as c:
            c.execute("UPDATE jobs SET expires=? WHERE id=?", (time.time()-1, j))
        self.s.cleanup()
        self.assertEqual(self.s.status(self.token, j)["status"], "not_found_or_expired")

    def test_ack_extends_retention_ten_hours(self):
        j = self.enqueue()["job_id"]
        self.s.run_one()
        x = self.s.status(self.token, j, acknowledge=True)
        self.assertGreaterEqual(x["expires"] - time.time(), TEN_HOURS-2)

    def test_document_content(self):
        data = json.dumps({"required": 3, "evidence_origins": ["A", "B"]}).encode()
        d = self.s.upload(self.token, base64.b64encode(data).decode(), final=True)["document_id"]
        j = self.enqueue(doc=d)["job_id"]
        self.s.run_one()
        v = self.s.status(self.token, j)
        self.assertEqual(v["result"]["status"], "SHORTFALL")
        self.assertEqual(v["result"]["required"], 3)

    def test_document_result_cleanup(self):
        d = self.s.upload(self.token, base64.b64encode(b"{}").decode(), final=True)["document_id"]
        j = self.enqueue(doc=d)["job_id"]
        self.s.run_one()
        self.s.status(self.token, j, acknowledge=True)
        with self.s.connect() as c:
            c.execute("UPDATE jobs SET expires=? WHERE id=?", (time.time()-1,j))
            c.execute("UPDATE documents SET expires=? WHERE id=?", (time.time()-1,d))
            path = c.execute("SELECT path FROM documents WHERE id=?", (d,)).fetchone()[0]
        self.s.cleanup()
        self.assertFalse(Path(path).exists())

    def test_disk_guard(self):
        class Fake:
            f_bavail = 10
            f_frsize = 100
            f_blocks = 100
        with patch("server.os.statvfs", return_value=Fake()):
            with self.assertRaisesRegex(ValueError, "storage_reserve_exhausted"):
                self.s.disk_guard(1)


if __name__ == "__main__":
    unittest.main()
