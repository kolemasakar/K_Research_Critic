"""Disabled-by-default in-process Artifact GET boundary; no listener or science dispatch.

Authenticates an already trusted peer identity plus signed envelope; validates the
completed request ledger and retrieves verified bytes BEFORE returning a response.
Not wired into the installed Stage131 or Stage127 transport.
"""
from .stage131_signed_artifact_read import verify_signed_read, ArtifactReadDenied
from .artifact_exchange import ExchangeError
import tempfile

class SignedArtifactReadBoundary:
    def __init__(self, *, exchange, ledger, nonce_registry, keyring, trusted_peer_identities,
                 enabled=False, max_inline_bytes=1024*1024, max_artifact_bytes=200*1024*1024):
        self.exchange=exchange
        self.ledger=ledger
        self.nonce_registry=nonce_registry
        self.keyring=keyring
        self.trusted_peer_identities=trusted_peer_identities
        self.enabled=enabled
        self.max_inline_bytes=max_inline_bytes
        self.max_artifact_bytes=max_artifact_bytes

    def execute(self, message, *, peer_uid, now_epoch=None):
        def err(status,code):
            return {"http_status":status,"content_type":"application/json","body":{"error":code}}
        if not self.enabled: return err(404,"NOT_FOUND")
        identity=self.trusted_peer_identities.get(peer_uid)
        if identity is None: return err(403,"FORBIDDEN")
        try:
            kid=message["auth"]["key_id"]
            secret=self.keyring[kid]
        except (TypeError,KeyError):
            return err(403,"FORBIDDEN")
        try:
            scope=verify_signed_read(message,trusted_identity=identity,secret=secret,
                    nonce_claim=self.nonce_registry.claim,now_epoch=now_epoch)
        except ArtifactReadDenied as exc:
            code=str(exc)
            return err(400 if code=="INVALID_REQUEST" else 403,
                       "INVALID_REQUEST" if code=="INVALID_REQUEST" else "FORBIDDEN")
        principal=scope["principal"]; request_id=scope["request_id"]
        # Read-only proof that science request was already admitted and completed.
        # Never admit or execute any new request as part of artifact retrieval.
        with self.ledger._db() as db:
            row=db.execute("SELECT state FROM requests WHERE principal=? AND request_id=?",
                           (principal,request_id)).fetchone()
        if row is None or row[0]!="COMPLETE":return err(404,"NOT_FOUND")
        # The temporary spool is private, unlinked, bounded and fully verified
        # before an HTTP adapter may send headers or the first byte.
        spool=tempfile.TemporaryFile(mode="w+b")
        size=0
        try:
            chunks=self.exchange.read_stream(scope["artifact_id"],
                    principal=principal,request_id=request_id)
            for part in chunks:
                if not isinstance(part,bytes):raise ExchangeError("ARTIFACT_CORRUPTED")
                size+=len(part)
                if size>self.max_artifact_bytes:raise ExchangeError("REQUEST_TOO_LARGE")
                spool.write(part)
            spool.flush()
            spool.seek(0)
        except ExchangeError as exc:
            spool.close()
            if exc.code=="ARTIFACT_EXPIRED":return err(410,"GONE")
            if exc.code=="REQUEST_TOO_LARGE":return err(413,"REQUEST_TOO_LARGE")
            return err(404 if exc.code in ("NOT_FOUND","ARTIFACT_UNAVAILABLE") else 502,
                       "NOT_FOUND" if exc.code in ("NOT_FOUND","ARTIFACT_UNAVAILABLE") else "UPSTREAM_INVALID_RESPONSE")
        except Exception:
            spool.close()
            return err(502,"UPSTREAM_INVALID_RESPONSE")
        if size<=self.max_inline_bytes:
            data=spool.read()
            spool.close()
            return {"http_status":200,"content_type":"application/octet-stream",
                    "body_bytes":data,"size_bytes":size,"request_id":request_id}
        # Caller MUST close spool after streamed transfer, including interrupted transfers.
        return {"http_status":200,"content_type":"application/octet-stream",
                "body_file":spool,"size_bytes":size,"request_id":request_id}
