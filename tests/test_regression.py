import time
from utils import run_cli,run_cli_with_timeout

# Always use the following format, this should be an header for the bug:
# KF ID: 
# PR ID: 
# COMMIT ID 


# KF ID: BUG-DCC3
# PR ID: https://github.com/MagaluCloud/magalu/pull/1445
# COMMIT ID 020641dd4586b50b1dfa1036f4afd1a615a9ef0c
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


