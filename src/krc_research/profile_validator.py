"""K_Science private CriticProfile shape validation, not owner attestation."""
def validate_profile(payload):
    if not isinstance(payload,dict): raise ValueError("Profile payload must be object")
    profile=payload.get("critic_profile")
    if not isinstance(profile,dict): raise ValueError("critic_profile required")
    required=("profile_id","version","protocol","topic")
    missing=[k for k in required if not isinstance(profile.get(k),str) or not profile[k].strip()]
    if missing: raise ValueError("CriticProfile missing fields: "+",".join(missing))
    if profile["protocol"] not in ("KRC Core","Scholarly Research"):
        raise ValueError("Unsupported protocol")
    approved=payload.get("user_profile_approved") is True
    return {"schema":"KRC-CRITICPROFILE-1","profile_id":profile["profile_id"],
            "profile_version":profile["version"],"protocol":profile["protocol"],
            "validation":"STRUCTURE_VALID","approval_claimed":approved,
            "approval_independently_verified":False,"scientific_approval":False}
