import time
from utils import run_cli,run_cli_with_timeout
import os

# Always use the following format, this should be an header for the bug:
# KF ID: 
# PR ID: 

# KF ID: BUG-DCC3
# PR ID: https://github.com/MagaluCloud/magalu/pull/1445

def test_invalid_param_hang_fix_1_0():
    exit_code, stdout, stderr, _ = run_cli_with_timeout(["vm", "instances", "create", "-a", "whatever"], timeout=2)
    assert exit_code == 1, stderr
    assert "unknown shorthand flag" in stderr

def test_invalid_param_hang_fix_1_1():
    exit_code, stdout, stderr, _ = run_cli_with_timeout(["vm", "instances", "create", "-awhatever"], timeout=2)
    assert exit_code == 1, stderr
    assert "unknown shorthand flag" in stderr


def test_invalid_param_hang_fix_2_0():
    _, _, stderr, _ = run_cli_with_timeout(["--debug=teste"], timeout=2)
    assert "invalid argument \"teste\"" in stderr 

def test_invalid_param_hang_fix_2_1():
    _, _, stderr, _ = run_cli_with_timeout(["--debug=teste"], timeout=2)
    assert "Command execution timed out" not in stderr


# KF ID: BUG-33F5
# PR ID: https://github.com/MagaluCloud/magalu/pull/1452 

def test_refresh_token_not_set_3_0():
    try:
        os.remove(os.path.expanduser("~/.config/magalu"))
    except FileNotFoundError:
        pass
    api_key = os.environ.get("MGC_API_KEY")
    os.environ["MGC_API_KEY"] = ""
    exit_code, _, stderr, _ = run_cli(["vm", "instances", "list", "--api-key", api_key])
    os.environ["MGC_API_KEY"] = api_key
    assert exit_code == 0, stderr
    assert "Error: RefreshToken is not set" not in stderr

def test_debug_flag_is_working_4_0():
    exit_code, _, stderr, _ = run_cli(["vm", "instances", "list", "--debug"])
    assert exit_code == 0, stderr
    assert "github.com/MagaluCloud/magalu/mgc/core/http" in stderr

def test_region_flag_is_working_5_0():
    exit_code, _, stderr, _ = run_cli(["vm", "instances", "list","--debug", "--region", "br-ne1"])
    assert exit_code == 0, stderr
    assert "api.magalu.cloud/br-ne1" in stderr


def test_region_flag_is_working_5_1():
    exit_code, _, stderr, _ = run_cli(["vm", "instances", "list","--debug", "--region", "br-se1"])
    assert exit_code == 0, stderr
    assert "api.magalu.cloud/br-se1" in stderr

def test_no_confirm_flag_6_0():
    _, stdout, _, _ = run_cli(["vm", "instances", "delete", "1234567890"])
    assert "\x1b[?25l\x1b[?2004h" in stdout

def test_no_confirm_flag_6_1():
    exit_code, _, stderr, _ = run_cli(["vm", "instances", "delete", "1234567890", "--no-confirm"])
    assert exit_code == 1, stderr
    assert "Unprocessable Entity"  in stderr
