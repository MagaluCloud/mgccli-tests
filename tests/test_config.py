from utils import run_cli

test_config_context = {}


def test_config_list():
    exit_code, _, _, jsonout = run_cli(["config", "list"])
    assert exit_code == 0, jsonout
    assert "chunk-size" in jsonout
    assert "debug" in jsonout
    assert "default-output" in jsonout
    assert "env" in jsonout
    assert "lang" in jsonout
    assert "raw-output" in jsonout
    assert "region" in jsonout
    assert "server-url" in jsonout
    assert "workers" in jsonout


def test_config_get_schema():
    exit_code, _, stderr, jsonout = run_cli(["config", "get-schema", "env"])
    assert exit_code == 0, stderr
    assert jsonout["default"] == "prod"

    exit_code, _, stderr, jsonout = run_cli(["config", "get-schema", "--key=default-output"])
    assert exit_code == 0, stderr
    assert jsonout["default"] == "json"

def test_config_get_schema_not_found():
    exit_code, _, stderr, jsonout = run_cli(["config", "get-schema", "test"])
    assert exit_code != 0, stderr
    assert 'config "test" not found' in stderr


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
    assert "value must be greater than 1" in stderr

    exit_code, _, stderr, _ = run_cli(["config", "set", "workers", "abc"])
    assert exit_code != 0
    assert 'strconv.Atoi: parsing "abc": invalid syntax' in stderr

    exit_code, _, stderr, jsonout = run_cli(["config", "get", "workers"])
    assert exit_code == 0, stderr
    assert jsonout["workers"] == 999


def test_config_set_chunk_size():
    exit_code, _, stderr, _ = run_cli(["config", "set", "chunk-size", "10"])
    assert exit_code == 0

    exit_code, _, stderr, _ = run_cli(["config", "set", "chunk-size", "2"])
    assert exit_code != 0
    assert "value must be greater than 8" in stderr

    exit_code, _, stderr, _ = run_cli(["config", "set", "chunk-size", "5121"])
    assert exit_code != 0
    assert "value must be less than 5120" in stderr

    exit_code, _, stderr, _ = run_cli(["config", "set", "chunk-size", "abc"])
    assert exit_code != 0
    assert 'strconv.Atoi: parsing "abc": invalid syntax' in stderr

    exit_code, _, stderr, jsonout = run_cli(["config", "get", "chunk-size"])
    assert exit_code == 0, stderr
    assert jsonout["chunk-size"] == 10


def test_config_set_default_output():
    exit_code, _, stderr, _ = run_cli(["config", "set", "default-output", "table"])
    assert exit_code == 0

    exit_code, _, stderr, jsonout = run_cli(["config", "get", "default-output"])
    assert exit_code == 0, stderr
    assert jsonout["default-output"] == "table"

    exit_code, _, stderr, _ = run_cli(["config", "set", "default-output", "json"])
    assert exit_code == 0

    exit_code, _, stderr, _ = run_cli(["config", "set", "default-output", "test"])
    assert exit_code != 0
    assert "value must be one of [json table]" in stderr


def test_config_set_region():
    exit_code, _, stderr, _ = run_cli(["config", "set", "region", "br-ne1"])
    assert exit_code == 0

    exit_code, _, stderr, _ = run_cli(["config", "set", "region", "br-mgl1"])
    assert exit_code == 0

    exit_code, _, stderr, jsonout = run_cli(["config", "get", "region"])
    assert exit_code == 0, stderr
    assert jsonout["region"] == "br-mgl1"

    exit_code, _, stderr, _ = run_cli(["config", "set", "region", "br-se1"])
    assert exit_code == 0

    exit_code, _, stderr, _ = run_cli(["config", "set", "region", "test"])
    assert exit_code != 0
    assert "value must be one of [br-se1 br-ne1 br-mgl1]" in stderr


def test_config_set_env():
    exit_code, _, stderr, _ = run_cli(["config", "set", "env", "pre-prod"])
    assert exit_code == 0

    exit_code, _, stderr, jsonout = run_cli(["config", "get", "env"])
    assert exit_code == 0, stderr
    assert jsonout["env"] == "pre-prod"

    exit_code, _, stderr, _ = run_cli(["config", "set", "env", "prod"])
    assert exit_code == 0

    exit_code, _, stderr, _ = run_cli(["config", "set", "env", "test"])
    assert exit_code != 0
    assert "value must be one of [prod pre-prod]" in stderr


def test_config_set_debug():
    exit_code, _, stderr, _ = run_cli(["config", "set", "debug", "true"])
    assert exit_code == 0

    exit_code, _, stderr, _ = run_cli(["config", "set", "debug", "false"])
    assert exit_code == 0

    exit_code, _, stderr, _ = run_cli(["config", "set", "debug", "test"])
    assert exit_code != 0
    assert 'strconv.ParseBool: parsing "test": invalid syntax' in stderr

    exit_code, _, stderr, jsonout = run_cli(["config", "get", "debug"])
    assert exit_code == 0, stderr
    assert jsonout["debug"] == False


def test_config_set_raw_output():
    exit_code, _, stderr, _ = run_cli(["config", "set", "raw-output", "true"])
    assert exit_code == 0

    exit_code, _, stderr, _ = run_cli(["config", "set", "raw-output", "false"])
    assert exit_code == 0

    exit_code, _, stderr, _ = run_cli(["config", "set", "raw-output", "test"])
    assert exit_code != 0
    assert 'strconv.ParseBool: parsing "test": invalid syntax' in stderr

    exit_code, _, stderr, jsonout = run_cli(["config", "get", "raw-output"])
    assert exit_code == 0, stderr
    assert jsonout["raw-output"] == False


def test_config_set_lang():
    exit_code, _, stderr, _ = run_cli(["config", "set", "lang", "pt-BR"])
    assert exit_code == 0

    exit_code, _, stderr, jsonout = run_cli(["config", "get", "lang"])
    assert exit_code == 0, stderr
    assert jsonout["lang"] == "pt-BR"

    exit_code, _, stderr, _ = run_cli(["config", "set", "lang", "en-US"])
    assert exit_code == 0

    exit_code, _, stderr, _ = run_cli(["config", "set", "lang", "test"])
    assert exit_code != 0
    assert "value must be one of [en-US pt-BR]" in stderr


def test_config_set_server_url():
    exit_code, _, stderr, _ = run_cli(["config", "set", "server-url", "https://api.mgc.com.br"])
    assert exit_code == 0

    exit_code, _, stderr, jsonout = run_cli(["config", "get", "server-url"])
    assert exit_code == 0, stderr
    assert jsonout["server-url"] == "https://api.mgc.com.br"


def test_config_get_empty_flags():
    exit_code, _, stderr, jsonout = run_cli(["config", "get"])
    assert exit_code != 0
    assert "missing required flag: --key=string" in stderr


def test_config_get():
    exit_code, _, stderr, jsonout = run_cli(["config", "get", "--key=workers"])
    assert exit_code == 0, stderr
    assert jsonout["workers"] == 999

    exit_code, _, stderr, jsonout = run_cli(["config", "get", "region"])
    assert exit_code == 0, stderr
    assert jsonout["region"] == "br-se1"

    exit_code, _, stderr, jsonout = run_cli(["config", "get", "server_url"])
    assert exit_code == 0, stderr
    assert jsonout["server_url"] == "https://api.mgc.com.br"


def test_config_get_invalid_config():
    exit_code, _, stderr, jsonout = run_cli(["config", "get", "test"])
    assert exit_code != 0
    assert "config test not found" in stderr


def test_config_delete():
    exit_code, _, stderr, jsonout = run_cli(["config", "get", "workers"])
    assert exit_code == 0, stderr
    assert jsonout["workers"] == 999
    
    exit_code, _, stderr, jsonout = run_cli(["config", "delete", "workers"])
    assert exit_code == 0, stderr

    exit_code, _, stderr, jsonout = run_cli(["config", "get", "workers"])
    assert exit_code == 0, stderr
    assert jsonout["workers"] == 5

    exit_code, _, stderr, jsonout = run_cli(["config", "get", "chunk-size"])
    assert exit_code == 0, stderr
    assert jsonout["chunk-size"] == 10

    exit_code, _, stderr, jsonout = run_cli(["config", "delete", "--key=chunk-size"])
    assert exit_code == 0, stderr

    exit_code, _, stderr, jsonout = run_cli(["config", "get", "chunk-size"])
    assert exit_code == 0, stderr
    assert jsonout["chunk-size"] == 8

    exit_code, _, stderr, jsonout = run_cli(["config", "delete", "--key=server-url"])
    assert exit_code == 0, stderr


def test_config_delete_empty_flag():
    exit_code, _, stderr, jsonout = run_cli(["config", "delete"])
    assert exit_code != 0
    assert "missing required flag: --key=string" in stderr

