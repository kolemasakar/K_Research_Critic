from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "gpt_store" / "actions" / "media_public_free_openapi.yaml"


def test_segment_pagination_parameters_are_inlined_for_gpt_builder() -> None:
    document = yaml.safe_load(SCHEMA.read_text(encoding="utf-8"))

    paths = [
        "/api/v1/media/youtube-gemini/transcriptions/{job_id}/segments",
        "/api/v1/media/managed/transcriptions/{job_id}/segments",
    ]

    for path in paths:
        parameters = document["paths"][path]["get"]["parameters"]
        assert all("$ref" not in parameter for parameter in parameters)
        assert [parameter["name"] for parameter in parameters] == [
            "job_id",
            "cursor",
            "limit",
        ]

    assert "parameters" not in document["components"]
