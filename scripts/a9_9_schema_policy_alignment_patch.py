from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "gpt_store/actions/media_managed_beta_openapi.yaml"
TEST = ROOT / "tests/test_media_beta_builder_a9_7_i.py"


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if old not in text or text.count(old) != 1:
        raise SystemExit(f"A9.9 schema policy anchor mismatch in {path}: {old[:140]!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


replace_once(
    SCHEMA,
    '''    consent-gated AI paths remain
    available. Facebook retrieval/STT uses a free Cobalt attempt first; if that
    cannot retrieve the public media, a separate local preflight and a new explicit
    one-credit ScrapeCreators approval are required before any paid retrieval.
    AssemblyAI STT runs only after media retrieval. Action bearer and owner
    admission credentials remain server-side.
''',
    '''    consent-gated AI paths remain available. Facebook retrieval/STT uses the free
    Cobalt path. If Cobalt cannot retrieve the public media, Facebook retrieval is
    unavailable and media intake stops. ScrapeCreators is reserved compatibility
    surface only and is not active or offerable. AssemblyAI STT runs only after
    successful media retrieval. Action bearer and owner admission credentials remain
    server-side.
''',
)

replace_once(
    SCHEMA,
    '''        Try configured Cobalt for a public Facebook URL. Never call ScrapeCreators
        here. If free retrieval fails, stop at AWAITING_RETRIEVAL_CONSENT. If it
        succeeds, run AssemblyAI STT and persist durable KRCM transcript segments.
''',
    '''        Try configured Cobalt for a public Facebook URL. Never call ScrapeCreators
        here. If free retrieval fails, treat Facebook retrieval as terminal unavailable
        and stop media intake. If it succeeds, run AssemblyAI STT and persist durable
        KRCM transcript segments.
''',
)

replace_once(
    SCHEMA,
    '          description: Facebook fallback completed or stopped before paid retrieval.\n',
    '          description: Facebook Cobalt path completed or stopped terminally unavailable.\n',
)

replace_once(
    SCHEMA,
    '      summary: Read the local one-credit ceiling before paid Facebook retrieval\n',
    '      summary: "Reserved compatibility: inspect legacy Facebook paid-retrieval ceiling"\n',
)

replace_once(
    SCHEMA,
    '''        Call only after the same job returns AWAITING_RETRIEVAL_CONSENT. This is a
        local policy quote: it does not call ScrapeCreators and performs no provider
        balance lookup. It does not authorize paid retrieval.
''',
    '''        Reserved compatibility only for historical durable jobs. Active MEDIA BETA
        Builder must not call or offer this operation after Cobalt failure. This local
        quote does not call ScrapeCreators and does not authorize paid retrieval.
''',
)

replace_once(
    SCHEMA,
    '      summary: Run exactly one explicitly approved ScrapeCreators retrieval attempt\n',
    '      summary: "Reserved compatibility: legacy explicitly approved Facebook retrieval"\n',
)

replace_once(
    SCHEMA,
    '''        Call only after the local Facebook retrieval preflight and a NEW explicit
        user approval. The hard maximum is exactly one ScrapeCreators credit.
        Automatic retries are forbidden. If charge outcome is uncertain, the job
        records credit_charge_uncertain=true and must never be replayed automatically.
''',
    '''        Reserved compatibility only for historical durable jobs. Active MEDIA BETA
        Builder must not call this operation after Cobalt failure. If legacy use is ever
        separately authorized, the hard maximum remains one ScrapeCreators credit and
        uncertain-charge operations must never be replayed automatically.
''',
)

replace_once(
    TEST,
    '''    paths = schema["paths"]
    assert paths["/api/v1/media/managed/facebook-fallback"]["post"]["operationId"] == (
''',
    '''    action_text = (
        ROOT / "gpt_store" / "actions" / "media_managed_beta_openapi.yaml"
    ).read_text(encoding="utf-8")
    assert "ScrapeCreators is reserved compatibility" in action_text
    assert "treat Facebook retrieval as terminal unavailable" in action_text
    assert "Active MEDIA BETA Builder must not call this operation after Cobalt failure" in action_text
    assert "separate local preflight and a new explicit" not in action_text
    assert "stop at AWAITING_RETRIEVAL_CONSENT" not in action_text

    paths = schema["paths"]
    assert paths["/api/v1/media/managed/facebook-fallback"]["post"]["operationId"] == (
''',
)

print("A9.9 Action schema aligned with terminal Facebook failure policy")
