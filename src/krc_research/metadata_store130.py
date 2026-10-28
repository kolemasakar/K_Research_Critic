"""Local, bounded metadata cache and append-only query accounting, staging only.

SQLite lives in the KRC private state root. Stores public DOI, URLs and metadata,
never OIDC credentials, Transport MAC, Science key or unpublished manuscripts.
"""
import json,sqlite3,time
from pathlib import Path

class MetadataStore130:
    def __init__(self,path,*,ttl_seconds=86400,clock=None):
        self.path=str(Path(path))
        if not Path(path).is_absolute() or not 60<=ttl_seconds<=604800:raise ValueError("INVALID_CONFIG")
        self.ttl=ttl_seconds;self.clock=clock or time.time
        with sqlite3.connect(self.path) as db:
            db.execute("CREATE TABLE IF NOT EXISTS cache(provider TEXT NOT NULL,url TEXT NOT NULL,expires REAL NOT NULL,body TEXT NOT NULL,PRIMARY KEY(provider,url))")
            db.execute("CREATE TABLE IF NOT EXISTS audit(time REAL NOT NULL,provider TEXT NOT NULL,url TEXT NOT NULL,outcome TEXT NOT NULL)")
    def load(self,provider,url):
        with sqlite3.connect(self.path) as db:
            r=db.execute("SELECT body,expires FROM cache WHERE provider=? AND url=?",(provider,url)).fetchone()
            if r and r[1]>self.clock():
                db.execute("INSERT INTO audit VALUES(?,?,?,?)",(self.clock(),provider,url,"CACHE_HIT"))
                return json.loads(r[0])
        return None
    def put(self,provider,url,obj):
        raw=json.dumps(obj,separators=(",",":"),ensure_ascii=False)
        if len(raw.encode())>2_000_000:raise ValueError("OVERSIZED_METADATA")
        with sqlite3.connect(self.path) as db:
            db.execute("INSERT OR REPLACE INTO cache VALUES(?,?,?,?)",(provider,url,self.clock()+self.ttl,raw))
            db.execute("INSERT INTO audit VALUES(?,?,?,?)",(self.clock(),provider,url,"FETCH_OK"))
    def error(self,provider,url):
        with sqlite3.connect(self.path) as db:db.execute("INSERT INTO audit VALUES(?,?,?,?)",(self.clock(),provider,url,"FETCH_ERROR"))
