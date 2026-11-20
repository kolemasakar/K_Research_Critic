"""Single-owner project-channel consent adapter (source-only).

The current personal KRC workflow is accessed through the owner's logged-in
ChatGPT project. No second KRC login, owner identification prompt, external
account, or HMAC on each human chat answer is required.

SECURITY BOUNDARY: only an already trusted internal project-channel handler
may hold/invoke this adapter. This module does NOT authenticate internet
clients, infer ChatGPT identity, or expose an HTTP endpoint. Direct network
use without an authenticated frontend boundary is NOT authorized.
"""
import secrets
import time

from .stage131_n39_single_owner_chat_consent import (
    ConsentDenied, SingleOwnerConsentLedger, profile_hash
)

class ProjectChannelVerifier:
    """Identity of the invoking *internal handler*, not reauthentication of owner.

    The private unexported marker must be passed by Python object identity;
    ordinary incoming JSON/user text cannot express this marker.
    """
    def __init__(self, *, owner_ref="single-chatgpt-project-owner",
                 clock=time.time):
        if not isinstance(owner_ref,str) or not owner_ref:
            raise ConsentDenied("INVALID_PROJECT_OWNER")
        self.owner_ref=owner_ref
        self.clock=clock
        self._marker=object()

    def _internal_event(self, *, decision, request_id, chat_id, digest):
        return dict(
            decision=decision, request_id=request_id, chat_id=chat_id,
            profile_sha256=digest, received_at=int(self.clock()),
            event_ref="project-action-"+secrets.token_hex(16),
            _channel_marker=self._marker
        )

    def verify(self, event, *, request_id, chat_id, expected_profile_hash):
        return (
            type(event) is dict
            and event.get("_channel_marker") is self._marker
            and event.get("decision") in ("APPROVE","CANCEL")
            and event.get("request_id")==request_id
            and event.get("chat_id")==chat_id
            and event.get("profile_sha256")==expected_profile_hash
            and type(event.get("received_at")) is int
            and isinstance(event.get("event_ref"),str)
            and len(event["event_ref"])>=16
        )

class TrustedProjectConsentAdapter:
    """Wraps consent decisions, invoked ONLY by the trusted internal handler."""
    def __init__(self, *, ledger, verifier):
        if not isinstance(ledger,SingleOwnerConsentLedger):
            raise ConsentDenied("CONSENT_LEDGER_REQUIRED")
        if not isinstance(verifier,ProjectChannelVerifier) or ledger.verifier is not verifier:
            raise ConsentDenied("PROJECT_CHANNEL_VERIFIER_REQUIRED")
        self._ledger=ledger
        self._verifier=verifier

    def confirm_profile(self, *, request_id, chat_id, profile, decision):
        """Used after the profile has been displayed in the logged-in project.

        No identity challenge. Refuses stale/changed profile and duplicate
        approval via the durable ledger. Revoke supports same request/profile.
        """
        if decision not in ("APPROVE","CANCEL"):
            raise ConsentDenied("INVALID_DECISION")
        digest=profile_hash(profile)
        event=self._verifier._internal_event(
            decision=decision,request_id=request_id,
            chat_id=chat_id,digest=digest)
        return self._ledger.decide(request_id=request_id,chat_id=chat_id,event=event)
