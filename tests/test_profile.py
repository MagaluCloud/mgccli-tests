from utils import run_cli
import random

test_profile_context = {}

PUBLIC_KEY = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIK0wmN/Cr3JXqmLW7u+g9pTh+wyqDHpSQEIQczXkVx9q not_really@a.key"

ssh_key_random_name = f"cli-test-key-{random.randint(1000, 9999)}"

def test_profile_availability_zones_list():
    exit_code, _, _, jsonout = run_cli(["profile", "availability_zones", "list"])
    assert exit_code == 0
    assert "results" in jsonout
    assert len(jsonout["results"]) > 0


def test_profile_ssh_keys_create():
    exit_code, _, _, jsonout = run_cli(
        ["profile", "ssh-keys", "create", f"--name=zzz_{ssh_key_random_name}", f"--key={PUBLIC_KEY}"]
    )
    assert exit_code == 0
    assert "id" in jsonout
    test_profile_context["key_id"] = jsonout["id"]


def test_profile_ssh_keys_create_empty_flags():
    exit_code, _, stderr, _ = run_cli(
        ["profile", "ssh-keys", "create"]
    )
    assert exit_code != 0
    assert "missing required flags: " in stderr
    assert "--key=string" in stderr
    assert "--name=string" in stderr

    exit_code, _, stderr, _ = run_cli(
        ["profile", "ssh-keys", "create", ssh_key_random_name, PUBLIC_KEY]
    )
    assert exit_code != 0


def test_profile_ssh_keys_create_fails_with_invalid_chars():
    exit_code, _, stderr, _ = run_cli(
        ["profile", "ssh-keys", "create", "--name=key.with.dots", f"--key={PUBLIC_KEY}"]
    )
    assert exit_code != 0, stderr
    assert "Status: 422 Unprocessable Entity" in stderr


def test_profile_ssh_keys_list():
    exit_code, _, _, jsonout = run_cli(["profile", "ssh-keys", "list"])
    assert exit_code == 0
    assert len(jsonout["results"]) >= 2


def test_profile_ssh_keys_list_with_pagination():
    exit_code, _, _, jsonout = run_cli(["profile", "ssh-keys", "list", "--control.offset=1", "--control.limit=1"])
    assert exit_code == 0
    assert len(jsonout["results"]) == 1


def test_profile_ssh_keys_list_with_sort():
    exit_code, _, _, jsonout = run_cli(
        ["profile", "ssh-keys", "create", f"--name=aaa_{ssh_key_random_name}", f"--key={PUBLIC_KEY}"]
    )
    assert exit_code == 0
    test_profile_context["key_id_2"] = jsonout["id"]

    exit_code, _, _, jsonout = run_cli(["profile", "ssh-keys", "list", "--control.sort=name:asc"])
    assert exit_code == 0
    assert "aaa_" in jsonout["results"][0]["name"]
    assert "zzz_" in jsonout["results"][-1]["name"]

    exit_code, _, _, jsonout = run_cli(["profile", "ssh-keys", "list", "--control.sort=name:desc"])
    assert exit_code == 0
    assert "zzz_" in jsonout["results"][0]["name"]
    assert "aaa_" in jsonout["results"][-1]["name"]


def test_profile_ssh_keys_get():
    exit_code, _, _, jsonout = run_cli(
        ["profile", "ssh-keys", "get", f"--key-id={test_profile_context['key_id']}"]
    )
    assert exit_code == 0
    assert "id" in jsonout
    assert "key" in jsonout
    assert "key_type" in jsonout
    assert "name" in jsonout

    exit_code, _, _, jsonout = run_cli(
        ["profile", "ssh-keys", "get", test_profile_context['key_id']]
    )
    assert exit_code == 0
    assert "id" in jsonout
    assert "key" in jsonout
    assert "key_type" in jsonout
    assert "name" in jsonout


def test_profile_ssh_keys_get_empty_flags():
    exit_code, _, stderr, _ = run_cli(
        ["profile", "ssh-keys", "get"]
    )
    assert exit_code != 0
    assert "missing required flag: --key-id=uuid" in stderr


def test_profile_ssh_keys_delete():
    exit_code, stdout, stderr, jsonout = run_cli(
        [
            "profile",
            "ssh-keys",
            "delete",
            f"--key-id={test_profile_context['key_id']}",
            "--no-confirm",
        ]
    )
    assert exit_code == 0


def test_profile_ssh_keys_delete_positional_arg():
    exit_code, stdout, stderr, jsonout = run_cli(
        [
            "profile",
            "ssh-keys",
            "delete",
            test_profile_context['key_id_2'],
            "--no-confirm",
        ]
    )
    assert exit_code == 0


def test_profile_ssh_keys_delete_empty_flags():
    exit_code, stdout, stderr, jsonout = run_cli(
        [
            "profile",
            "ssh-keys",
            "delete",
        ]
    )
    assert exit_code != 0
    assert "missing required flag: --key-id=uuid" in stderr