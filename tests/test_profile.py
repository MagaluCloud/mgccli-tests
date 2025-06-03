from utils import run_cli

test_profile_context = {}

PUBLIC_KEY = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIK0wmN/Cr3JXqmLW7u+g9pTh+wyqDHpSQEIQczXkVx9q not_really@a.key"


def test_profile_availability_zones_list():
    exit_code, _, _, jsonout = run_cli(["profile", "availability_zones", "list"])
    assert exit_code == 0
    assert "results" in jsonout
    assert len(jsonout["results"]) > 0


def test_profile_ssh_keys_create():
    exit_code, _, _, jsonout = run_cli(
        ["profile", "ssh-keys", "create", "--name=cli-test-key", f"--key={PUBLIC_KEY}"]
    )
    assert exit_code == 0
    assert "id" in jsonout
    test_profile_context["key_id"] = jsonout["id"]


def test_profile_ssh_keys_create_fails_with_invalid_chars():
    exit_code, _, stderr, _ = run_cli(
        ["profile", "ssh-keys", "create", "--name=key.with.dots", f"--key={PUBLIC_KEY}"]
    )
    assert exit_code != 0, stderr
    assert "Status: 422 Unprocessable Entity" in stderr


def test_profile_ssh_keys_list():
    exit_code, _, _, jsonout = run_cli(["profile", "ssh-keys", "list"])
    assert exit_code == 0


def test_profile_ssh_keys_get():
    exit_code, _, _, jsonout = run_cli(
        ["profile", "ssh-keys", "get", f"--key-id={test_profile_context['key_id']}"]
    )
    assert exit_code == 0
    assert "id" in jsonout
    assert "key" in jsonout
    assert "key_type" in jsonout
    assert "name" in jsonout


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
