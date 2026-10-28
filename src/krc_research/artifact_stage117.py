"""Stage117 isolated hardened artifact store, POSIX only; not a network service.
All read/write/cleanup operations on this class share one advisory lock.
Legacy ArtifactExchange operations MUST NOT run concurrently against same root.
"""
import fcntl
import hashlib
import os
import sqlite3
import stat
from .artifact_stream116 import StreamExchange
from .artifact_exchange import ExchangeError, MIB

class HardenedExchange(StreamExchange):
    def __init__(self, root, *, free_bytes_min=64*MIB, **kwargs):
        if not isinstance(free_bytes_min, int) or free_bytes_min<0:
            raise ExchangeError('INVALID_CONFIGURATION')
        super().__init__(root, **kwargs)
        self.free_bytes_min=free_bytes_min

    def store_stream(self, chunks, *, principal, request_id, filename, media_type='application/octet-stream'):
        def checked():
            for b in chunks:
                if not isinstance(b,bytes):
                    raise ExchangeError('INVALID_REQUEST')
                free=os.statvfs(self.data)
                available=free.f_bavail*free.f_frsize
                if available-len(b)<self.free_bytes_min:
                    raise ExchangeError('LOW_DISK_SPACE')
                yield b
        return super().store_stream(checked(),principal=principal,request_id=request_id,
                                    filename=filename,media_type=media_type)

    def read_stream(self, artifact_id, *, principal,request_id,chunk_size=256*1024):
        self._assert_scope(principal,request_id)
        if not isinstance(chunk_size,int) or not 0<chunk_size<=MIB:
            raise ExchangeError('INVALID_REQUEST')
        if not isinstance(artifact_id,str) or len(artifact_id)!=48 or any(c not in '0123456789abcdef' for c in artifact_id):
            raise ExchangeError('NOT_FOUND')
        with self._locked():
            with self._connect() as db:
                row=db.execute('SELECT principal,request_id,size,sha256,expires FROM objects WHERE id=?',(artifact_id,)).fetchone()
            if not row or (row[0],row[1])!=(principal,request_id):
                raise ExchangeError('NOT_FOUND')
            if row[4]<=self.clock():
                raise ExchangeError('ARTIFACT_EXPIRED')
            try:
                fd=os.open(self.data/artifact_id,os.O_RDONLY|os.O_NOFOLLOW)
            except OSError:
                raise ExchangeError('ARTIFACT_UNAVAILABLE') from None
            with os.fdopen(fd,'rb') as f:
                initial=os.fstat(f.fileno())
                if not stat.S_ISREG(initial.st_mode):
                    raise ExchangeError('ARTIFACT_UNAVAILABLE')
                h=hashlib.sha256(); n=0
                while True:
                    b=f.read(chunk_size)
                    if not b:break
                    n+=len(b)
                    if n>self.max_artifact:raise ExchangeError('ARTIFACT_CORRUPTED')
                    h.update(b)
                if n!=row[2] or h.hexdigest()!=row[3]:
                    raise ExchangeError('ARTIFACT_CORRUPTED')
                f.seek(0)
                while True:
                    b=f.read(chunk_size)
                    if not b:break
                    yield b
                current=os.fstat(f.fileno())
                if (current.st_size,current.st_mtime_ns,current.st_ctime_ns)!=(initial.st_size,initial.st_mtime_ns,initial.st_ctime_ns):
                    raise ExchangeError('ARTIFACT_CHANGED_DURING_READ')

    def cleanup_expired(self):
        with self._locked():
            return super().cleanup_expired()

    def reconcile_staging(self):
        with self._locked():
            with self._connect() as db:
                rows=db.execute('SELECT id FROM objects').fetchall()
                known={r[0] for r in rows}
            removed=0
            for p in self.data.iterdir():
                if p.name.startswith('.pending-') or (len(p.name)==48 and all(c in '0123456789abcdef' for c in p.name) and p.name not in known):
                    if p.is_file() or p.is_symlink():
                        p.unlink();removed+=1
            return removed
