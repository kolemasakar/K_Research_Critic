from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACTION = ROOT / "gpt_store/actions/media_managed_beta_openapi.yaml"
BUILDER = ROOT / "prompts/GPT_STORE_MEDIA_BETA_BUILDER_INSTRUCTIONS.md"
MANIFEST = ROOT / "gpt_store/media_beta_manifest.yaml"
VALIDATOR = ROOT / "scripts/validate_store_package.py"


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"anchor not found in {path}: {old[:120]!r}")
    if text.count(old) != 1:
        raise SystemExit(f"anchor not unique in {path}: {old[:120]!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


# OpenAPI version and package description.
replace_once(
    ACTION,
    '  version: 0.4.0-a9.7-c\n',
    '  version: 0.5.0-a9.9\n',
)
replace_once(
    ACTION,
    '''    Owner-only zero-client managed transcript beta for public YouTube, Instagram,
    and Facebook media. Existing Supadata native and consent-gated AI paths remain
''',
    '''    Owner-only zero-client managed transcript beta for public YouTube, Instagram,
    Facebook and supported public Telegram video posts. Existing Supadata native and
    consent-gated AI paths remain
''',
)
replace_once(
    ACTION,
    '      summary: Read managed-media beta capabilities and configured Facebook adapters\n',
    '      summary: Read managed-media beta capabilities and configured media adapters\n',
)

# Add zero-credit Telegram route before common durable job reads.
telegram_path = '''  /api/v1/media/managed/telegram:
    post:
      operationId: startManagedTelegramPublicTranscription
      summary: Retrieve one public Telegram video and transcribe it with AssemblyAI
      description: >-
        Use only for a supported public Telegram post URL. Retrieval uses the public
        Telegram embed surface and costs zero retrieval credits. No Telegram account,
        cookies, session, bot token or paid fallback is used. AssemblyAI STT may consume
        the isolated beta STT quota. Terminal unavailable jobs are not retried automatically.
      x-openai-isConsequential: false
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/TelegramPublicRequest"
      responses:
        "200":
          description: Telegram public-video job completed, failed, or reused from durable state.
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ManagedJob"
        "400":
          description: Invalid or unsupported Telegram request.
        "401":
          description: Private GPT Action authentication failed.
        "422":
          description: Public Telegram post or browser-playable video is unavailable.
        "429":
          description: Closed-beta STT quota is exhausted.
        "503":
          description: Telegram retrieval/STT pipeline is not configured.
'''
replace_once(
    ACTION,
    '  /api/v1/media/managed/transcriptions/{job_id}:\n',
    telegram_path + '  /api/v1/media/managed/transcriptions/{job_id}:\n',
)

# Capability schema.
replace_once(
    ACTION,
    '            enum: [youtube, instagram, facebook]\n',
    '            enum: [youtube, instagram, facebook, telegram]\n',
)
replace_once(
    ACTION,
    '''        facebook_stt_configured:
          type: boolean
        automatic_ai_fallback:
''',
    '''        facebook_stt_configured:
          type: boolean
        telegram_public_retrieval:
          type: boolean
        telegram_retrieval_provider:
          type: string
          const: telegram_public_web
        telegram_retrieval_credits:
          type: integer
          const: 0
        telegram_stt_provider:
          type: string
          const: assemblyai
        telegram_stt_configured:
          type: boolean
        automatic_ai_fallback:
''',
)

# Telegram request schema.
telegram_request = '''    TelegramPublicRequest:
      type: object
      additionalProperties: false
      required: [url]
      properties:
        url:
          type: string
          format: uri
          description: Public HTTPS Telegram post URL with a numeric post id.
        language_hint:
          type: string
          enum: [auto, uk, ru, en]
          default: auto
'''
replace_once(
    ACTION,
    '    NativeTranscriptRequest:\n',
    telegram_request + '    NativeTranscriptRequest:\n',
)

# Managed durable job schema.
replace_once(
    ACTION,
    '          enum: [native, generate, facebook_retrieval_stt]\n',
    '          enum: [native, generate, facebook_retrieval_stt, telegram_public_retrieval_stt]\n',
)
replace_once(
    ACTION,
    '              enum: [cobalt, scrapecreators]\n',
    '              enum: [cobalt, scrapecreators, telegram_public_web]\n',
)

# Compact Builder routing. Keep the package inside the 8000-character limit.
replace_once(
    BUILDER,
    'Live accepted: YouTube, Instagram Reel, Facebook Video/Reel.\n',
    'Live accepted in current GPT: YouTube, Instagram Reel, Facebook Video/Reel. Telegram backend is live accepted; this package adds public Telegram video routing.\n',
)
replace_once(
    BUILDER,
    '''ROUTING
YouTube/Instagram -> native managed flow first. Facebook -> `startManagedFacebookFallback`; 0 ScrapeCreators credits. COMPLETED -> segments. If free Cobalt retrieval fails, including `AWAITING_RETRIEVAL_CONSENT`, report that Facebook media retrieval is unavailable and STOP media intake. Do NOT call `preflightManagedFacebookRetrievalCredit` or `continueManagedFacebookPaidRetrieval`. Do not route Facebook through Supadata generate fallback.
''',
    '''ROUTING
YouTube/Instagram -> native managed flow first. Facebook -> `startManagedFacebookFallback`; 0 ScrapeCreators credits. COMPLETED -> segments. Cobalt failure, including `AWAITING_RETRIEVAL_CONSENT`, means unavailable; STOP. Never call paid Facebook continuation or Supadata generate fallback.
Telegram public video post -> `startManagedTelegramPublicTranscription`; no credit preflight. COMPLETED -> segments. FAILED/unavailable -> report unavailable and STOP. Never request Telegram login/cookies/session or use paid fallback.
''',
)
replace_once(
    BUILDER,
    'JOB HANDLING\nDo not expose `KRCM_...` Job IDs. PROCESSING -> bounded `getManagedMediaTranscriptionStatus` checks. COMPLETED -> retrieve ALL `getManagedMediaTranscriptSegments` pages, cursor=0, limit=50 until next_cursor=null. reused=true -> reuse. FAILED + credit_charge_uncertain=true -> no retry. Action/auth unavailable -> report unavailable. For Facebook, free retrieval failure is terminal for the active MEDIA BETA flow: do not offer any paid retrieval fallback. Do not fall back to Helper in the normal owner flow. Never invent it.\n',
    'JOB HANDLING\nDo not expose `KRCM_...` Job IDs. PROCESSING -> bounded `getManagedMediaTranscriptionStatus` checks. COMPLETED -> retrieve ALL `getManagedMediaTranscriptSegments` pages, cursor=0, limit=50 until next_cursor=null. reused=true -> reuse. FAILED + credit_charge_uncertain=true -> no retry. Action/auth unavailable -> report unavailable. Facebook free failure and Telegram unavailable are terminal: no paid fallback. Do not fall back to Helper in the normal owner flow. Never invent it.\n',
)

# Manifest: package prepared, Builder runtime not yet updated.
replace_once(MANIFEST, '  version: "0.7-beta-a9.7-i"\n', '  version: "0.8-beta-a9.9"\n')
replace_once(MANIFEST, '  builder_package_version: "0.7-beta-a9.7-i"\n', '  builder_package_version: "0.8-beta-a9.9"\n')
replace_once(MANIFEST, '  builder_target_action_schema_version: "0.4.0-a9.7-c"\n', '  builder_target_action_schema_version: "0.5.0-a9.9"\n')
replace_once(MANIFEST, '  builder_runtime_applied: true\n', '  builder_runtime_applied: false\n')
replace_once(
    MANIFEST,
    '''  public_platforms_in_progress: []
  public_platforms_not_started:
    - telegram
''',
    '''  public_platforms_in_progress:
    - telegram
  public_platforms_not_started: []
''',
)
replace_once(
    MANIFEST,
    '  managed_facebook_live_accepted: true\n',
    '''  managed_facebook_live_accepted: true
  managed_telegram_code_ready: true
  managed_telegram_backend_live_accepted: true
  managed_telegram_public_retrieval_provider: telegram_public_web
  managed_telegram_retrieval_credits: 0
  managed_telegram_stt_provider: assemblyai
  managed_telegram_action_schema_ready: true
  managed_telegram_builder_runtime_applied: false
  managed_telegram_private_gpt_e2e_complete: false
''',
)
replace_once(
    MANIFEST,
    '  rollout_state: A9_7_I_PRIVATE_GPT_E2E_ACCEPTED\n',
    '  rollout_state: A9_9_TELEGRAM_PACKAGE_READY_BUILDER_PENDING\n',
)
replace_once(
    MANIFEST,
    '  a9_7_i_private_gpt_e2e_complete: true\n',
    '''  a9_7_i_private_gpt_e2e_complete: true
  a9_9_telegram_backend_complete: true
  a9_9_telegram_action_package_complete: true
  a9_9_telegram_builder_runtime_applied: false
  a9_9_telegram_private_gpt_e2e_complete: false
''',
)
replace_once(MANIFEST, '  gpt_builder_private_update_required: false\n', '  gpt_builder_private_update_required: true\n')

# Validator follows the new explicit package state.
replace_once(
    VALIDATOR,
    '    _require(instructions.get("version") == "0.7-beta-a9.7-i", "A9.7-I instruction version must be 0.7-beta-a9.7-i")\n',
    '    _require(instructions.get("version") == "0.8-beta-a9.9", "A9.9 instruction version must be 0.8-beta-a9.9")\n',
)
replace_once(
    VALIDATOR,
    '    _require(instructions.get("builder_package_version") == "0.7-beta-a9.7-i", "A9.7-I Builder package version must be 0.7-beta-a9.7-i")\n',
    '    _require(instructions.get("builder_package_version") == "0.8-beta-a9.9", "A9.9 Builder package version must be 0.8-beta-a9.9")\n',
)
replace_once(
    VALIDATOR,
    '    _require(instructions.get("builder_runtime_applied") is True, "A9.7-I Builder package must record runtime application")\n',
    '    _require(instructions.get("builder_runtime_applied") is False, "A9.9 Builder package must remain pending until private GPT Builder is updated")\n',
)
replace_once(
    VALIDATOR,
    '    _require(beta.get("public_platforms_in_progress") == [], "No public platform may remain in progress after Facebook Cobalt live acceptance")\n',
    '    _require(beta.get("public_platforms_in_progress") == ["telegram"], "Telegram must remain in progress until private-GPT E2E acceptance")\n',
)
replace_once(
    VALIDATOR,
    '    _require(beta.get("public_platforms_not_started") == ["telegram"], "Telegram must remain not started")\n',
    '    _require(beta.get("public_platforms_not_started") == [], "No public platform may remain not started after A9.9 backend acceptance")\n',
)
replace_once(
    VALIDATOR,
    '    _require(beta.get("managed_facebook_live_accepted") is True, "Facebook free Cobalt path must be marked live accepted after H1 evidence")\n',
    '''    _require(beta.get("managed_facebook_live_accepted") is True, "Facebook free Cobalt path must be marked live accepted after H1 evidence")
    _require(beta.get("managed_telegram_code_ready") is True, "A9.9 Telegram managed path must be code-ready")
    _require(beta.get("managed_telegram_backend_live_accepted") is True, "A9.9 Telegram backend must record isolated live acceptance")
    _require(beta.get("managed_telegram_public_retrieval_provider") == "telegram_public_web", "Telegram retrieval provider must be public web")
    _require(beta.get("managed_telegram_retrieval_credits") == 0, "Telegram retrieval credits must remain zero")
    _require(beta.get("managed_telegram_stt_provider") == "assemblyai", "Telegram STT provider must be AssemblyAI")
    _require(beta.get("managed_telegram_action_schema_ready") is True, "Telegram Action schema must be package-ready")
    _require(beta.get("managed_telegram_builder_runtime_applied") is False, "Telegram Builder runtime must remain pending")
    _require(beta.get("managed_telegram_private_gpt_e2e_complete") is False, "Telegram private-GPT E2E must remain pending")
''',
)
replace_once(
    VALIDATOR,
    '    _require(release.get("rollout_state") == "A9_7_I_PRIVATE_GPT_E2E_ACCEPTED", "rollout state must record accepted A9.7-I owner private-GPT E2E")\n',
    '    _require(release.get("rollout_state") == "A9_9_TELEGRAM_PACKAGE_READY_BUILDER_PENDING", "rollout state must record A9.9 package-ready Builder-pending state")\n',
)
replace_once(
    VALIDATOR,
    '    _require(release.get("a9_7_i_private_gpt_e2e_complete") is True, "A9.7-I owner private-GPT E2E must be accepted")\n',
    '''    _require(release.get("a9_7_i_private_gpt_e2e_complete") is True, "A9.7-I owner private-GPT E2E must remain accepted")
    _require(release.get("a9_9_telegram_backend_complete") is True, "A9.9 Telegram backend acceptance must be complete")
    _require(release.get("a9_9_telegram_action_package_complete") is True, "A9.9 Telegram Action package must be complete")
    _require(release.get("a9_9_telegram_builder_runtime_applied") is False, "A9.9 Telegram Builder runtime must remain pending")
    _require(release.get("a9_9_telegram_private_gpt_e2e_complete") is False, "A9.9 Telegram private-GPT E2E must remain pending")
    _require(release.get("gpt_builder_private_update_required") is True, "A9.9 must require private Builder package update")
''',
)
replace_once(
    VALIDATOR,
    '            "startManagedFacebookFallback",\n',
    '            "startManagedFacebookFallback",\n            "startManagedTelegramPublicTranscription",\n',
)
replace_once(
    VALIDATOR,
    '            "A9.7-I Builder instructions",\n',
    '            "A9.9 Builder instructions",\n',
)
replace_once(
    VALIDATOR,
    '            "version: 0.4.0-a9.7-c",\n',
    '            "version: 0.5.0-a9.9",\n',
)
replace_once(
    VALIDATOR,
    '            "operationId: startManagedFacebookFallback",\n',
    '            "operationId: startManagedFacebookFallback",\n            "operationId: startManagedTelegramPublicTranscription",\n',
)
replace_once(
    VALIDATOR,
    '            "facebook_retrieval_stt",\n',
    '            "facebook_retrieval_stt",\n            "telegram_public_retrieval_stt",\n            "telegram_public_web",\n',
)
replace_once(
    VALIDATOR,
    '        "A9.7-C managed Action schema",\n',
    '        "A9.9 managed Action schema",\n',
)

print("A9.9 Telegram private-GPT Action package patch applied")
