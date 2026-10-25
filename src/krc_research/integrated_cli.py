"""KRC integrated scholarly CLI, fail-closed: NO attestation from input JSON.

Usage: PYTHONPATH=src python -m krc_research.integrated_cli input.json output.json
Only a separate trusted execution host may supply attestations in code.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from .integrated_research import execute_research

def run_file(source:Path,destination:Path)->dict:
    inp=source.read_bytes()
    if len(inp)>524288: raise ValueError("Input exceeds 512KiB limit")
    package=json.loads(inp.decode("utf-8"))
    if "attested_receipt_hashes" in package or "trusted_attestations" in package:
        raise ValueError("Attestations cannot come from user input")
    report=execute_research(package)
    result={"input_sha256":hashlib.sha256(inp).hexdigest(),
            "execution_mode":"OFFLINE_UNATTESTED","output":report}
    destination.write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    return result

def main():
    p=argparse.ArgumentParser()
    p.add_argument("input",type=Path)
    p.add_argument("output",type=Path)
    args=p.parse_args()
    run_file(args.input,args.output)

if __name__=="__main__":main()
