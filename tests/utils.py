import json
import os
import subprocess
import shlex
from typing import List, Dict

MGC_PATH = os.environ.get("MGC_PATH") or "mgc"
MGC_API_KEY = os.environ.get("MGC_API_KEY")
MGC_PRINT_COMMAND = str(os.environ.get("MGC_PRINT_COMMAND")).lower() == "true"

def format_command_for_display(command: List[str]) -> str:
    """Format command for display, handling JSON parameters properly."""
    formatted_parts = []
    
    for part in command:
        # Check if this part contains JSON (starts with '=' and contains '{' or '[')
        if '=' in part and ('{' in part or '[' in part):
            # Split on first '=' to separate parameter name from value
            param_name, param_value = part.split('=', 1)
            
            try:
                # Try to parse as JSON and format it in a single line
                json_value = json.loads(param_value)
                formatted_json = json.dumps(json_value, separators=(',', ':'))
                # Format as single-line parameter
                formatted_part = f"{param_name}={formatted_json}"
            except json.JSONDecodeError:
                # If not valid JSON, just escape quotes for display
                formatted_part = part.replace('"', '\\"')
        else:
            formatted_part = part
        
        formatted_parts.append(formatted_part)
    
    return " ".join(formatted_parts)

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

    if (result.returncode != 0 and MGC_PRINT_COMMAND):
        print(f"Erro ao executar comando:")
        print(format_command_for_display(command))
        print()

    return result.returncode, result.stdout, result.stderr, json_output
