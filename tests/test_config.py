from utils import run_cli

test_config_context = {}


def test_config_list():
    exit_code, _, _, jsonout = run_cli(["config", "list"])
    assert exit_code == 0, jsonout
    assert "chunkSize" in jsonout
    assert "defaultOutput" in jsonout
    assert "region" in jsonout
    assert "workers" in jsonout


def test_config_get_schema():
    exit_code, _, stderr, jsonout = run_cli(["config", "get-schema", "env"])
    assert exit_code == 0, stderr
    assert jsonout["default"] == "prod"


def test_config_get_schema_not_found():
    exit_code, _, stderr, jsonout = run_cli(["config", "get-schema", "test"])
    assert exit_code == 0, stderr
    assert jsonout == {}


def test_config_set():
    exit_code, _, stderr, _ = run_cli(["config", "set", "workers", "999"])
    assert exit_code == 0, stderr

    exit_code, _, stderr, _ = run_cli(["config", "set", "--key=region", "--value=br-se1"])
    assert exit_code == 0, stderr


def test_config_set_empty_flags():
    exit_code, _, stderr, _ = run_cli(["config", "set", "workers"])
    assert exit_code != 0, stderr
    assert "missing required flag: --value=" in stderr

    exit_code, _, stderr, _ = run_cli(["config", "set", "--value=0"])
    assert exit_code != 0, stderr
    assert "missing required flag: --key=string" in stderr

    exit_code, _, stderr, _ = run_cli(["config", "set"])
    assert exit_code != 0, stderr
    assert "missing required flags:" in stderr
    assert "--key=string" in stderr
    assert "--value=" in stderr


def test_config_set_workers():
    exit_code, _, stderr, _ = run_cli(["config", "set", "workers", "999"])
    assert exit_code == 0

    exit_code, _, stderr, _ = run_cli(["config", "set", "workers", "0"])
    assert exit_code != 0
    assert "number must be at least 1" in stderr

    exit_code, _, stderr, _ = run_cli(["config", "set", "workers", "abc"])
    assert exit_code != 0
    assert 'value must be an integer' in stderr

    exit_code, _, stderr, jsonout = run_cli(["config", "get", "workers"])
    assert exit_code == 0, stderr
    assert jsonout == 999


def test_config_set_chunk_size():
    exit_code, _, stderr, _ = run_cli(["config", "set", "chunkSize", "10"])
    assert exit_code == 0

    exit_code, _, stderr, _ = run_cli(["config", "set", "chunkSize", "2"])
    assert exit_code != 0
    assert "number must be at least 8" in stderr

    exit_code, _, stderr, _ = run_cli(["config", "set", "chunkSize", "5121"])
    assert exit_code != 0
    assert "number must be at most 5120" in stderr

    exit_code, _, stderr, _ = run_cli(["config", "set", "chunkSize", "abc"])
    assert exit_code != 0
    assert 'value must be an integer' in stderr

    exit_code, _, stderr, jsonout = run_cli(["config", "get", "chunkSize"])
    assert exit_code == 0, stderr
    assert jsonout == 10


def test_config_set_default_output():
    exit_code, _, stderr, _ = run_cli(["config", "set", "defaultOutput", "table"])
    assert exit_code == 0

    exit_code, _, stderr, jsonout = run_cli(["config", "get", "defaultOutput"])
    assert exit_code == 0, stderr
    assert jsonout == "table"

    exit_code, _, stderr, _ = run_cli(["config", "set", "defaultOutput", "json"])
    assert exit_code == 0


def test_config_set_region():
    exit_code, _, stderr, _ = run_cli(["config", "set", "region", "br-ne1"])
    assert exit_code == 0

    exit_code, _, stderr, _ = run_cli(["config", "set", "region", "br-mgl1"])
    assert exit_code == 0

    exit_code, _, stderr, jsonout = run_cli(["config", "get", "region"])
    assert exit_code == 0, stderr
    assert jsonout == "br-mgl1"

    exit_code, _, stderr, _ = run_cli(["config", "set", "region", "br-se1"])
    assert exit_code == 0

    exit_code, _, stderr, _ = run_cli(["config", "set", "region", "test"])
    assert exit_code != 0
    assert 'value is not one of the allowed values ["br-ne1","br-se1","br-mgl1"]' in stderr


def test_config_set_env():
    exit_code, _, stderr, _ = run_cli(["config", "set", "env", "pre-prod"])
    assert exit_code == 0

    exit_code, _, stderr, jsonout = run_cli(["config", "get", "env"])
    assert exit_code == 0, stderr
    assert jsonout == "pre-prod"

    exit_code, _, stderr, _ = run_cli(["config", "set", "env", "prod"])
    assert exit_code == 0

    exit_code, _, stderr, _ = run_cli(["config", "set", "env", "test"])
    assert exit_code != 0
    assert 'value is not one of the allowed values ["prod","pre-prod"]' in stderr


def test_config_set_server_url():
    exit_code, _, stderr, _ = run_cli(["config", "set", "serverUrl", "https://api.mgc.com.br"])
    assert exit_code == 0

    exit_code, _, stderr, jsonout = run_cli(["config", "get", "serverUrl"])
    assert exit_code == 0, stderr
    assert jsonout == "https://api.mgc.com.br"


def test_config_get_empty_flags():
    exit_code, _, stderr, jsonout = run_cli(["config", "get"])
    assert exit_code != 0
    assert "missing required flag: --key=string" in stderr


def test_config_get():
    exit_code, _, stderr, jsonout = run_cli(["config", "get", "--key=workers"])
    assert exit_code == 0, stderr
    assert jsonout == 999

    exit_code, _, stderr, jsonout = run_cli(["config", "get", "region"])
    assert exit_code == 0, stderr
    assert jsonout == "br-se1"

    exit_code, _, stderr, jsonout = run_cli(["config", "get", "serverUrl"])
    assert exit_code == 0, stderr
    assert jsonout == "https://api.mgc.com.br"


def test_config_get_invalid_config():
    exit_code, _, stderr, jsonout = run_cli(["config", "get", "test"])
    assert exit_code == 0
    assert jsonout == {}


def test_config_delete():
    exit_code, _, stderr, jsonout = run_cli(["config", "get", "workers"])
    assert exit_code == 0, stderr
    assert jsonout == 999
    
    exit_code, _, stderr, jsonout = run_cli(["config", "delete", "workers"])
    assert exit_code == 0, stderr

    exit_code, _, stderr, jsonout = run_cli(["config", "get", "workers"])
    assert exit_code == 0, stderr
    assert jsonout == {}

    exit_code, _, stderr, jsonout = run_cli(["config", "get", "chunkSize"])
    assert exit_code == 0, stderr
    assert jsonout == 10

    exit_code, _, stderr, jsonout = run_cli(["config", "delete", "--key=chunkSize"])
    assert exit_code == 0, stderr

    exit_code, _, stderr, jsonout = run_cli(["config", "get", "chunkSize"])
    assert exit_code == 0, stderr
    assert jsonout == {}

    exit_code, _, stderr, jsonout = run_cli(["config", "delete", "--key=serverUrl"])
    assert exit_code == 0, stderr


def test_config_delete_empty_flag():
    exit_code, _, stderr, jsonout = run_cli(["config", "delete"])
    assert exit_code != 0
    assert "missing required flag: --key=string" in stderr

