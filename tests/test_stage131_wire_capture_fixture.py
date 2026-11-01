import contextlib, hashlib, io, json, runpy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def test_reproducible_wire_capture():
    fixture=json.loads((ROOT/'tests/fixtures/stage131_uds_http_wire_capture_v1.json').read_text())
    app=runpy.run_path(str(ROOT/'tools/capture_stage131_uds_fixtures.py'),run_name='capture_module')
    output=io.StringIO()
    with contextlib.redirect_stdout(output):
        app['main']()
    observed=json.loads(output.getvalue())
    assert fixture==observed
    for row in observed['captures'].values():
        data=bytes.fromhex(row['body_hex'])
        assert len(data)==row['body_length']==int(row['headers']['content-length'])
        assert hashlib.sha256(data).hexdigest()==row['body_sha256']
