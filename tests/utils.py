import json
import logging
import subprocess
import os


mgc_api_key = os.environ.get("MGC_API_KEY", "")
mgc_cli_path = os.environ.get("MGC_PATH", "mgc")
mgc_verbose = bool(os.environ.get("MGC_VERBOSE", False))


def run_cli(commands: list[str], timeout: int = 0, is_authenticated: bool = True, has_json_output: bool = True) -> tuple[int, str, str, dict]:
    command = [mgc_cli_path] + commands
    if has_json_output:
        command = command + ["--output", "json", "--raw"]
    if is_authenticated:
        command = command + ["--api-key", mgc_api_key]
    if timeout > 0:
        command = ["timeout", str(timeout)] + command
    print(f"Running command: {command}") if mgc_verbose else None
    try:
        result = subprocess.run(command, capture_output=True, text=True)
    except Exception as e:
        logging.error(f"Error while running command: {e}")
        raise
    try:
        json_output = json.loads(result.stdout)
    except json.JSONDecodeError as e:
        json_output = {}
    if mgc_verbose:
        print(f"Finished with return code: {result.returncode}")
        print(f"Stdout: {result.stdout}")
        print(f"Stderr: {result.stderr}")
        print(f"JSON Output: {json_output}")
    return result.returncode, result.stdout, result.stderr, json_output