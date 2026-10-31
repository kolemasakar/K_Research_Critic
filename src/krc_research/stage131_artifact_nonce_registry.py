"""Isolated durable atomic replay protection for signed artifact reads. No listener."""
import os,sqlite3,time
from pathlib import Path

class ArtifactNonceRegistry:
    def __init__(self,path,*,clock=time.time,ttl_seconds=900):
        self.path=Path(path)
        self.clock=clock
        if not 300<=ttl_seconds<=3600:raise ValueError("INVALID_TTL")
        self.ttl=ttl_seconds
        if self.path.is_symlink():raise ValueError("UNSAFE_STATE")
        self.path.parent.mkdir(parents=True,exist_ok=True)
        with self._db() as db:
            db.execute("CREATE TABLE IF NOT EXISTS used (key_id TEXT NOT NULL,nonce TEXT NOT NULL,principal TEXT NOT NULL,created REAL NOT NULL,PRIMARY KEY(key_id,nonce,principal))")
    def _db(self):
        db=sqlite3.connect(str(self.path),timeout=5,isolation_level=None)
        db.execute("PRAGMA busy_timeout=5000")
        db.execute("PRAGMA journal_mode=WAL")
        db.execute("PRAGMA synchronous=FULL")
        return db
    def claim(self,key_id,nonce,principal):
        if not all(isinstance(x,str) and x for x in (key_id,nonce,principal)):return False
        with self._db() as db:
            try:
                db.execute("BEGIN IMMEDIATE")
                now=self.clock()
                db.execute("DELETE FROM used WHERE created < ?",(now-self.ttl,))
                db.execute("INSERT INTO used(key_id,nonce,principal,created) VALUES(?,?,?,?)",(key_id,nonce,principal,now))
                db.execute("COMMIT")
                return True
            except sqlite3.IntegrityError:
                db.execute("ROLLBACK")
                return False
            except Exception:
                db.execute("ROLLBACK")
                raise
