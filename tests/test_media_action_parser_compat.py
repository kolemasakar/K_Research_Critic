from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "gpt_store" / "actions" / "media_managed_beta_openapi.yaml"


def _operations(schema: dict):
    for path, path_item in schema["paths"].items():
        for method in ("get", "post", "put", "patch", "delete"):
            operation = path_item.get(method)
            if isinstance(operation, dict):
                yield path, method, operation


def test_gpt_builder_operation_descriptions_fit_limit() -> None:
    schema = yaml.safe_load(SCHEMA_PATH.read_text(encoding="utf-8"))
    for path, method, operation in _operations(schema):
        description = operation.get("description")
        if description is not None:
            assert len(description) <= 300, (path, method, len(description))


def test_gpt_builder_job_id_parameters_are_inline() -> None:
    text = SCHEMA_PATH.read_text(encoding="utf-8")
    schema = yaml.safe_load(text)
    assert "#/components/parameters/JobId" not in text
    for path, method, operation in _operations(schema):
        if "{job_id}" not in path:
            continue
        params = operation.get("parameters", [])
        job = next((p for p in params if p.get("name") == "job_id"), None)
        assert job is not None, (path, method)
        assert "$ref" not in job
        assert job["in"] == "path"
        assert job["required"] is True
        assert job["schema"]["type"] == "string"
        assert job["schema"]["pattern"] == "^KRCM_[A-Za-z0-9-]+$"
