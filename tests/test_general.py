from utils import run_cli

def test_general_version():
    exit_code, stdout, stderr, _ = run_cli(["--version"])
    assert exit_code == 0, stderr
    assert "mgc version v" in stdout


# def test_invalid_param_hang_fix():
#     exit_code, stdout, stderr, _ = run_cli(["vm", "instances", "create", "-a", "whatever"])
#     assert exit_code != 0, stderr
#     assert "unknown shorthand flag" in stderr
