#!/usr/bin/env python3
"""Read-only, redacted Cobalt configuration/log summary. Run with existing Docker access."""
import json, subprocess, sys
def docker(*args):
    p = subprocess.run(["docker", *args], capture_output=True, text=True, timeout=20)
    if p.returncode:
        raise RuntimeError("docker_read_failed")
    return p.stdout + (p.stderr if args and args[0] == "logs" else "")
try:
    ids = docker("ps", "-q").split()
    found = []
    for cid in ids:
        obj = json.loads(docker("inspect", cid))[0]
        if "cobalt" in obj.get("Config", {}).get("Image", "").lower():
            found.append(obj)
    if len(found) != 1:
        print(json.dumps({"status":"container_selection_required","candidate_count":len(found)}))
        sys.exit(2)
    obj = found[0]
    env = dict(item.split("=",1) for item in obj.get("Config",{}).get("Env",[]) if "=" in item)
    configured = {key:bool(env.get(key,"").strip()) for key in [
        "COOKIE_PATH","API_KEY_URL","HTTP_PROXY","HTTPS_PROXY","http_proxy","https_proxy","API_EXTERNAL_PROXY"
    ]}
    configured["API_AUTH_REQUIRED_enabled"] = env.get("API_AUTH_REQUIRED") == "1"
    logs = docker("logs", "--since", "2h", "--tail", "300", obj["Id"])
    # Never print raw logs or values. These fixed messages reflect only observed log markers.
    markers = {
        "cookies_loaded_marker":"cookies loaded successfully!" in logs,
        "cookies_load_failed_marker":"failed to load cookies." in logs,
        "api_keys_loaded_marker":"api keys loaded successfully!" in logs,
        "api_keys_load_failed_marker":"Failed loading API keys" in logs
    }
    print(json.dumps({"status":"read_only_summary","configured":configured,"log_markers":markers,
      "stage_http_status":"not_available_without_stage_instrumentation",
      "cookie_validity":"not_verified","note":"Absence of a recent marker does not prove unconfigured state."}))
except Exception:
    print(json.dumps({"status":"diagnostic_unavailable","raw_error_suppressed":True}))
    sys.exit(1)
