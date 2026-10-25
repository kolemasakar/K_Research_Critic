"""Durable at-most-once request ID registry for authenticated KRC routes."""
import sqlite3
import os
import time
from pathlib import Path

class ReplayRegistry:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        if self.path.is_symlink():
            raise ValueError('Symlink database denied')
        old = os.umask(0o077)
        try:
            with self.connection() as db:
                db.execute('CREATE TABLE IF NOT EXISTS requests (client TEXT NOT NULL, task_id TEXT NOT NULL, created INTEGER NOT NULL, PRIMARY KEY(client,task_id))')
        finally:
            os.umask(old)

    def connection(self):
        return sqlite3.connect(str(self.path), timeout=8)

    def claim(self, client, task_id, now=None):
        if not client or not task_id:
            raise ValueError('Missing identity')
        stamp = int(time.time()) if now is None else int(now)
        try:
            with self.connection() as db:
                db.execute('INSERT INTO requests VALUES (?,?,?)', (client,task_id,stamp))
        except sqlite3.IntegrityError as exc:
            raise ValueError('Replay denied') from exc

    def prune(self, now=None, retention=86400):
        if retention < 3600:
            raise ValueError('Retention too short')
        stamp = int(time.time()) if now is None else int(now)
        with self.connection() as db:
            cur = db.execute('DELETE FROM requests WHERE created < ?', (stamp-retention,))
            return cur.rowcount
