import pytest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import run_cli


test_users_context = {}


def test_container_registry_users_help():
    exit_code, stdout, _, _ = run_cli(
        ["container-registry", "users", "--help"],
        is_authenticated=False,
        has_json_output=False,
    )
    assert exit_code == 0
    assert "create" in stdout
    assert "delete" in stdout
    assert "get" in stdout


def test_container_registry_users_delete_missing_required_flag():
    exit_code, _, stderr, _ = run_cli(
        ["container-registry", "users", "delete"]
    )
    assert exit_code != 0
    assert "--user-id" in stderr


def test_container_registry_users_get():
    exit_code, _, stderr, jsonout = run_cli(
        ["container-registry", "users", "get"]
    )
    if exit_code == 0:
        assert "id" in jsonout
        assert "username" in jsonout
        assert "created_at" in jsonout
        test_users_context["existing_user_id"] = jsonout["id"]
    else:
        assert "404" in stderr or "not found" in stderr.lower()


@pytest.mark.skip(reason="Creates a new container-registry user — only run when no user exists")
def test_container_registry_users_create():
    exit_code, _, stderr, jsonout = run_cli(
        ["container-registry", "users", "create"]
    )
    assert exit_code == 0, stderr
    assert "id" in jsonout
    assert "username" in jsonout
    assert "created_at" in jsonout
    test_users_context["user_id"] = jsonout["id"]


@pytest.mark.skip(reason="Subsequent create should fail because user already exists for the auth context")
def test_container_registry_users_create_duplicate_fails():
    exit_code, _, stderr, _ = run_cli(
        ["container-registry", "users", "create"]
    )
    assert exit_code != 0


@pytest.mark.skip(reason="Verifies authenticated user retrieval after create")
def test_container_registry_users_get_after_create():
    exit_code, _, stderr, jsonout = run_cli(
        ["container-registry", "users", "get"]
    )
    assert exit_code == 0, stderr
    assert jsonout["id"] == test_users_context["user_id"]
    assert "username" in jsonout
    assert "created_at" in jsonout


@pytest.mark.skip(reason="Deletes the authenticated container-registry user; impacts subsequent CR auth")
def test_container_registry_users_delete():
    exit_code, _, stderr, _ = run_cli(
        [
            "container-registry",
            "users",
            "delete",
            f"--user-id={test_users_context['user_id']}",
        ]
    )
    assert exit_code == 0, stderr


@pytest.mark.skip(reason="Deletes the authenticated container-registry user; impacts subsequent CR auth")
def test_container_registry_users_delete_positional_arg():
    exit_code, _, stderr, _ = run_cli(
        [
            "container-registry",
            "users",
            "delete",
            test_users_context["user_id"],
        ]
    )
    assert exit_code == 0, stderr
