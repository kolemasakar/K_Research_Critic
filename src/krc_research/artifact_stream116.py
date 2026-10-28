"""Staging-only POSIX streamed artifact handling. No listener or identity provider."""
import contextlib, fcntl, hashlib, os, secrets, sqlite3, stat
from .artifact_exchange import ArtifactExchange, ExchangeError, MIB

class StreamExchange(ArtifactExchange):
    @contextlib.contextmanager
    def _locked(self):
        fd=os.open(self.root/'.writer.lock',os.O_CREAT|os.O_RDWR|os.O_NOFOLLOW,0o600)
        try:
            fcntl.flock(fd,fcntl.LOCK_EX)
            yield
        finally:
            fcntl.flock(fd,fcntl.LOCK_UN)
            os.close(fd)

    def store_stream(self,chunks,*,principal,request_id,filename,media_type='application/octet-stream'):
        self._assert_scope(principal,request_id)
        if (not isinstance(filename,str) or not filename or len(filename)>160 or
            '/' in filename or '\\' in filename or filename in ('.','..')):
            raise ExchangeError('INVALID_REQUEST')
        if not isinstance(media_type,str) or not media_type or len(media_type)>128:
            raise ExchangeError('INVALID_REQUEST')
        identifier=secrets.token_hex(24)
        pending=self.data/('.pending-'+identifier)
        final=self.data/identifier
        digest=hashlib.sha256()
        size=0
        fd=os.open(pending,os.O_CREAT|os.O_EXCL|os.O_WRONLY|os.O_NOFOLLOW,0o600)
        published=False
        try:
            with os.fdopen(fd,'wb') as output:
                for block in chunks:
                    if not isinstance(block,bytes): raise ExchangeError('INVALID_REQUEST')
                    size+=len(block)
                    if size>self.max_artifact: raise ExchangeError('ARTIFACT_TOO_LARGE')
                    digest.update(block)
                    output.write(block)
                output.flush()
                os.fsync(output.fileno())
            with self._locked():
                with self._connect() as db:
                    db.execute('BEGIN IMMEDIATE')
                    used=db.execute('SELECT COALESCE(SUM(size),0) FROM objects').fetchone()[0]
                    if used+size>self.max_total:
                        db.execute('ROLLBACK')
                        raise ExchangeError('STORAGE_QUOTA_EXCEEDED')
                    os.replace(pending,final)
                    db.execute('INSERT INTO objects VALUES (?,?,?,?,?,?,?,?)',
                        (identifier,principal,request_id,filename,media_type,size,digest.hexdigest(),self.clock()+self.ttl))
                    db.execute('COMMIT')
                    published=True
            return {'artifact_id':identifier,'size_bytes':size,'sha256':digest.hexdigest(),
                    'filename':filename,'media_type':media_type}
        finally:
            pending.unlink(missing_ok=True)
            if not published: final.unlink(missing_ok=True)

    def read_stream(self,artifact_id,*,principal,request_id,chunk_size=256*1024):
        """Two-pass hash-before-yield, bounded memory. Requires cleanup coordination."""
        self._assert_scope(principal,request_id)
        if not isinstance(chunk_size,int) or chunk_size<1 or chunk_size>MIB:
            raise ExchangeError('INVALID_REQUEST')
        if (not isinstance(artifact_id,str) or len(artifact_id)!=48 or
            any(c not in '0123456789abcdef' for c in artifact_id)):
            raise ExchangeError('NOT_FOUND')
        with self._connect() as db:
            row=db.execute('SELECT principal,request_id,size,sha256,expires FROM objects WHERE id=?',(artifact_id,)).fetchone()
        if row is None or row[0]!=principal or row[1]!=request_id: raise ExchangeError('NOT_FOUND')
        if row[4]<=self.clock(): raise ExchangeError('ARTIFACT_EXPIRED')
        try:
            fd=os.open(self.data/artifact_id,os.O_RDONLY|os.O_NOFOLLOW)
        except OSError:
            raise ExchangeError('ARTIFACT_UNAVAILABLE') from None
        with os.fdopen(fd,'rb') as f:
            if not stat.S_ISREG(os.fstat(f.fileno()).st_mode):
                raise ExchangeError('ARTIFACT_UNAVAILABLE')
            h=hashlib.sha256()
            n=0
            while True:
                block=f.read(chunk_size)
                if not block:break
                n+=len(block)
                if n>self.max_artifact:raise ExchangeError('ARTIFACT_CORRUPTED')
                h.update(block)
            if n!=row[2] or h.hexdigest()!=row[3]:
                raise ExchangeError('ARTIFACT_CORRUPTED')
            f.seek(0)
            while True:
                block=f.read(chunk_size)
                if not block:break
                yield block

    def reconcile_staging(self):
        """Manual repair only with no legacy writers and no ongoing reads."""
        with self._locked():
            count=0
            for p in self.data.glob('.pending-*'):
                if p.is_file() and not p.is_symlink():
                    p.unlink()
                    count+=1
            return count
