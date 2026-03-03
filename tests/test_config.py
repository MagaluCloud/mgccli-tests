from utils import run_cli

test_config_context = {}


def test_config_list():
    exit_code, _, _, jsonout = run_cli(["config", "list"])
    assert exit_code == 0, jsonout
    assert "chunkSize" in jsonout
    assert "defaultOutput" in jsonout
    assert "region" in jsonout
    assert "workers" in jsonout
    assert "x-zone" in jsonout


def test_config_get_schema():
    exit_code, _, stderr, jsonout = run_cli(["config", "get-schema", "env"])
    assert exit_code == 0, stderr
    assert jsonout["default"] == "prod"

    exit_code, _, stderr, jsonout = run_cli(["config", "get-schema", "defaultOutput"])
    assert exit_code == 0, stderr
    assert "default" not in jsonout


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
    exit_code, _, stderr, _ = run_cli(["config", "set", "workers", "5"])
    assert exit_code == 0

    exit_code, _, stderr, _ = run_cli(["config", "set", "workers", "0"])
    assert exit_code != 0
    assert "value must be greater than 1" in stderr

    exit_code, _, stderr, _ = run_cli(["config", "set", "workers", "abc"])
    assert exit_code != 0
    assert 'strconv.Atoi: parsing "abc": invalid syntax' in stderr


def test_config_set_chunk_size():
    exit_code, _, stderr, _ = run_cli(["config", "set", "chunk-size", "8"])
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


def test_config_set_default_output():
    exit_code, _, stderr, _ = run_cli(["config", "set", "default-output", "json"])
    assert exit_code == 0

    exit_code, _, stderr, _ = run_cli(["config", "set", "default-output", "table"])
    assert exit_code == 0

    exit_code, _, stderr, _ = run_cli(["config", "set", "default-output", "test"])
    assert exit_code != 0
    assert "value must be one of [json table]" in stderr


def test_config_set_region():
    exit_code, _, stderr, _ = run_cli(["config", "set", "region", "br-se1"])
    assert exit_code == 0

    exit_code, _, stderr, _ = run_cli(["config", "set", "region", "br-ne1"])
    assert exit_code == 0

    exit_code, _, stderr, _ = run_cli(["config", "set", "region", "br-mgl1"])
    assert exit_code == 0

    exit_code, _, stderr, _ = run_cli(["config", "set", "region", "test"])
    assert exit_code != 0
    assert "value must be one of [br-se1 br-ne1 br-mgl1]" in stderr


def test_config_set_env():
    exit_code, _, stderr, _ = run_cli(["config", "set", "env", "prod"])
    assert exit_code == 0

    exit_code, _, stderr, _ = run_cli(["config", "set", "env", "pre-prod"])
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


def test_config_set_raw_output():
    exit_code, _, stderr, _ = run_cli(["config", "set", "raw-output", "true"])
    assert exit_code == 0

    exit_code, _, stderr, _ = run_cli(["config", "set", "raw-output", "false"])
    assert exit_code == 0

    exit_code, _, stderr, _ = run_cli(["config", "set", "raw-output", "test"])
    assert exit_code != 0
    assert 'strconv.ParseBool: parsing "test": invalid syntax' in stderr


def test_config_set_lang():
    exit_code, _, stderr, _ = run_cli(["config", "set", "lang", "en-US"])
    assert exit_code == 0

    exit_code, _, stderr, _ = run_cli(["config", "set", "lang", "pt-BR"])
    assert exit_code == 0

    exit_code, _, stderr, _ = run_cli(["config", "set", "lang", "test"])
    assert exit_code != 0
    assert "value must be one of [en-US pt-BR]" in stderr


def test_config_set_server_url():
    exit_code, _, stderr, _ = run_cli(["config", "set", "server-url", "https://api.mgc.com.br"])
    assert exit_code == 0


def test_config_get():
    exit_code, _, stderr, jsonout = run_cli(["config", "get", "workers"])
    assert exit_code == 0, stderr
    assert jsonout == 999

    exit_code, _, stderr, jsonout = run_cli(["config", "get", "region"])
    assert exit_code == 0, stderr
    assert jsonout == "br-se1"


def test_config_delete():
    exit_code, _, stderr, jsonout = run_cli(["config", "delete", "workers"])
    assert exit_code == 0, stderr

    exit_code, _, stderr, jsonout = run_cli(["config", "get", "workers"])
    assert exit_code == 0, stderr
    assert jsonout == {}
