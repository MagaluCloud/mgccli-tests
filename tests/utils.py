import json
import os
import subprocess
from typing import List, Dict

MGC_PATH = os.environ.get("MGC_PATH") or "mgc"
MGC_API_KEY = os.environ.get("MGC_API_KEY")

def run_cli(args: List[str]) -> tuple[int, str, str, Dict]:
    """Run CLI command and return exit code, plain text output and parsed JSON output."""
    if MGC_API_KEY:
        command = [MGC_PATH] + args + ["--output=json", "--raw", "--api-key", MGC_API_KEY]
    else:
        command = [MGC_PATH] + args + ["--output=json", "--raw"]
        
    result = subprocess.run(command, capture_output=True, text=True)

    try:
        json_output = json.loads(result.stdout)
    except json.JSONDecodeError:
        json_output = {}

    return result.returncode, result.stdout, result.stderr, json_output
