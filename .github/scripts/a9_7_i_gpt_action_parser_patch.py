from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = ROOT / "gpt_store" / "actions" / "media_managed_beta_openapi.yaml"
TEST = ROOT / "tests" / "test_media_beta_managed_package.py"
NEW_TEST = ROOT / "tests" / "test_media_action_parser_compat.py"

schema_text = SCHEMA.read_text(encoding="utf-8")

old_description = '''      description: >-\n        Public Facebook media only. This operation attempts configured Cobalt\n        retrieval first. It never invokes the paid ScrapeCreators fallback. If\n        free retrieval is unavailable, the returned durable job stops at\n        AWAITING_RETRIEVAL_CONSENT. If retrieval succeeds, AssemblyAI STT completes\n        the durable KRCM transcript and segments subject to the closed-beta STT quota.\n'''
new_description = '''      description: >-\n        Try configured Cobalt for a public Facebook URL. Never call ScrapeCreators\n        here. If free retrieval fails, stop at AWAITING_RETRIEVAL_CONSENT. If it\n        succeeds, run AssemblyAI STT and persist durable KRCM transcript segments.\n'''
if old_description not in schema_text:
    raise SystemExit("facebook description anchor not found")
schema_text = schema_text.replace(old_description, new_description, 1)

ref_line = '        - $ref: "#/components/parameters/JobId"\n'
inline_job_id = '''        - name: job_id\n          in: path\n          required: true\n          schema:\n            type: string\n            pattern: ^KRCM_[A-Za-z0-9-]+$\n'''
ref_count = schema_text.count(ref_line)
if ref_count != 6:
    raise SystemExit(f"expected 6 JobId operation refs, found {ref_count}")
schema_text = schema_text.replace(ref_line, inline_job_id)

# Remove the now-unused reusable parameter. GPT Builder currently parses operation
# parameters more reliably when path parameters are fully inline.
component_parameter = '''  parameters:\n    JobId:\n      name: job_id\n      in: path\n      required: true\n      schema:\n        type: string\n        pattern: ^KRCM_[A-Za-z0-9-]+$\n'''
if component_parameter not in schema_text:
    raise SystemExit("components JobId anchor not found")
schema_text = schema_text.replace(component_parameter, "", 1)
SCHEMA.write_text(schema_text, encoding="utf-8")

# Update the existing regression expectation from reusable-ref to inline path parameter.
test_text = TEST.read_text(encoding="utf-8")
old_assertion = '''    for operation in job_operations:\n        assert operation["parameters"][0] == {"$ref": "#/components/parameters/JobId"}\n'''
new_assertion = '''    for operation in job_operations:\n        job_id = operation["parameters"][0]\n        assert job_id["name"] == "job_id"\n        assert job_id["in"] == "path"\n        assert job_id["required"] is True\n        assert job_id["schema"]["type"] == "string"\n        assert job_id["schema"]["pattern"] == "^KRCM_[A-Za-z0-9-]+$"\n        assert "$ref" not in job_id\n'''
if old_assertion not in test_text:
    raise SystemExit("existing JobId test assertion anchor not found")
test_text = test_text.replace(old_assertion, new_assertion, 1)
TEST.write_text(test_text, encoding="utf-8")

NEW_TEST.write_text('''from __future__ import annotations\n\nfrom pathlib import Path\n\nimport yaml\n\nROOT = Path(__file__).resolve().parents[1]\nSCHEMA_PATH = ROOT / "gpt_store" / "actions" / "media_managed_beta_openapi.yaml"\n\n\ndef _operations(schema: dict):\n    for path, path_item in schema["paths"].items():\n        for method in ("get", "post", "put", "patch", "delete"):\n            operation = path_item.get(method)\n            if isinstance(operation, dict):\n                yield path, method, operation\n\n\ndef test_gpt_builder_operation_descriptions_fit_limit() -> None:\n    schema = yaml.safe_load(SCHEMA_PATH.read_text(encoding="utf-8"))\n    for path, method, operation in _operations(schema):\n        description = operation.get("description")\n        if description is not None:\n            assert len(description) <= 300, (path, method, len(description))\n\n\ndef test_gpt_builder_job_id_parameters_are_inline() -> None:\n    text = SCHEMA_PATH.read_text(encoding="utf-8")\n    schema = yaml.safe_load(text)\n    assert "#/components/parameters/JobId" not in text\n    for path, method, operation in _operations(schema):\n        if "{job_id}" not in path:\n            continue\n        params = operation.get("parameters", [])\n        job = next((p for p in params if p.get("name") == "job_id"), None)\n        assert job is not None, (path, method)\n        assert "$ref" not in job\n        assert job["in"] == "path"\n        assert job["required"] is True\n        assert job["schema"]["type"] == "string"\n        assert job["schema"]["pattern"] == "^KRCM_[A-Za-z0-9-]+$"\n''', encoding="utf-8")

# Static safety check before CI proper.
schema = yaml.safe_load(schema_text)
for path, path_item in schema["paths"].items():
    for method in ("get", "post", "put", "patch", "delete"):
        operation = path_item.get(method)
        if not isinstance(operation, dict):
            continue
        description = operation.get("description")
        if description is not None and len(description) > 300:
            raise SystemExit(f"operation description too long: {path} {method} {len(description)}")
        if "{job_id}" in path:
            params = operation.get("parameters", [])
            if not any(
                p.get("name") == "job_id"
                and p.get("in") == "path"
                and p.get("required") is True
                and "$ref" not in p
                for p in params
                if isinstance(p, dict)
            ):
                raise SystemExit(f"job_id not inline: {path} {method}")

print("A9.7-I GPT Action parser compatibility patch: PASS")
