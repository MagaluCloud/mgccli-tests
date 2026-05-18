import pytest
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import run_cli


test_members_context = {}
registry_name = f"clitestmemb{random.randint(10000, 99999)}"


def test_container_registry_members_help():
    exit_code, stdout, _, _ = run_cli(
        ["container-registry", "members", "--help"],
        is_authenticated=False,
        has_json_output=False,
    )
    assert exit_code == 0
    assert "create" in stdout
    assert "delete" in stdout
    assert "get" in stdout
    assert "list" in stdout
    assert "update" in stdout


def test_container_registry_members_list_missing_required_flag():
    exit_code, _, stderr, _ = run_cli(
        ["container-registry", "members", "list"]
    )
    assert exit_code != 0
    assert "--registry-id" in stderr


def test_container_registry_members_get_missing_required_flags():
    exit_code, _, stderr, _ = run_cli(
        ["container-registry", "members", "get"]
    )
    assert exit_code != 0
    assert "required flag" in stderr or "missing" in stderr


def test_container_registry_members_get_missing_member_id():
    exit_code, _, stderr, _ = run_cli(
        [
            "container-registry",
            "members",
            "get",
            "--registry-id=00000000-0000-0000-0000-000000000000",
        ]
    )
    assert exit_code != 0
    assert "--member-id" in stderr


def test_container_registry_members_create_missing_required_flags():
    exit_code, _, stderr, _ = run_cli(
        ["container-registry", "members", "create"]
    )
    assert exit_code != 0
    assert "required flag" in stderr or "missing" in stderr


def test_container_registry_members_create_missing_user_id():
    exit_code, _, stderr, _ = run_cli(
        [
            "container-registry",
            "members",
            "create",
            "--registry-id=00000000-0000-0000-0000-000000000000",
        ]
    )
    assert exit_code != 0
    assert "--user-id" in stderr


def test_container_registry_members_create_invalid_role_enum():
    exit_code, _, stderr, _ = run_cli(
        [
            "container-registry",
            "members",
            "create",
            "--registry-id=00000000-0000-0000-0000-000000000000",
            "--user-id=00000000-0000-0000-0000-000000000000",
            "--role=admin",
        ]
    )
    assert exit_code != 0


def test_container_registry_members_update_missing_required_flags():
    exit_code, _, stderr, _ = run_cli(
        ["container-registry", "members", "update"]
    )
    assert exit_code != 0
    assert "required flag" in stderr or "missing" in stderr


def test_container_registry_members_update_missing_role():
    exit_code, _, stderr, _ = run_cli(
        [
            "container-registry",
            "members",
            "update",
            "--registry-id=00000000-0000-0000-0000-000000000000",
            "--member-id=00000000-0000-0000-0000-000000000000",
        ]
    )
    assert exit_code != 0
    assert "--role" in stderr


def test_container_registry_members_update_invalid_role_enum():
    exit_code, _, stderr, _ = run_cli(
        [
            "container-registry",
            "members",
            "update",
            "--registry-id=00000000-0000-0000-0000-000000000000",
            "--member-id=00000000-0000-0000-0000-000000000000",
            "--role=admin",
        ]
    )
    assert exit_code != 0


def test_container_registry_members_delete_missing_required_flags():
    exit_code, _, stderr, _ = run_cli(
        ["container-registry", "members", "delete"]
    )
    assert exit_code != 0
    assert "required flag" in stderr or "missing" in stderr


def test_container_registry_members_delete_missing_member_id():
    exit_code, _, stderr, _ = run_cli(
        [
            "container-registry",
            "members",
            "delete",
            "--registry-id=00000000-0000-0000-0000-000000000000",
        ]
    )
    assert exit_code != 0
    assert "--member-id" in stderr


@pytest.mark.skip(reason="Requires a second user UUID to add as member")
def test_container_registry_members_setup_registry():
    exit_code, _, stderr, jsonout = run_cli(
        [
            "container-registry",
            "registries",
            "create",
            f"--name={registry_name}",
        ]
    )
    assert exit_code == 0, stderr
    assert "id" in jsonout
    test_members_context["registry_id"] = jsonout["id"]


@pytest.mark.skip(reason="Requires a second user UUID to add as member")
def test_container_registry_members_create():
    exit_code, _, stderr, jsonout = run_cli(
        [
            "container-registry",
            "members",
            "create",
            f"--registry-id={test_members_context['registry_id']}",
            f"--user-id={test_members_context['user_id']}",
            "--role=guest",
        ]
    )
    assert exit_code == 0, stderr
    assert "id" in jsonout
    assert "registry_id" in jsonout
    assert "user_id" in jsonout
    assert "role" in jsonout
    assert jsonout["role"] == "guest"
    assert "created_at" in jsonout
    assert "updated_at" in jsonout
    test_members_context["member_id"] = jsonout["id"]


@pytest.mark.skip(reason="Requires a second user UUID to add as member")
def test_container_registry_members_create_default_role():
    exit_code, _, stderr, jsonout = run_cli(
        [
            "container-registry",
            "members",
            "create",
            f"--registry-id={test_members_context['registry_id']}",
            f"--user-id={test_members_context['user_id_2']}",
        ]
    )
    assert exit_code == 0, stderr
    assert jsonout["role"] == "guest"


@pytest.mark.skip(reason="Requires a previously created member relationship")
def test_container_registry_members_list():
    exit_code, _, stderr, jsonout = run_cli(
        [
            "container-registry",
            "members",
            "list",
            f"--registry-id={test_members_context['registry_id']}",
        ]
    )
    assert exit_code == 0, stderr
    assert "results" in jsonout
    assert "meta" in jsonout
    assert len(jsonout["results"]) > 0


@pytest.mark.skip(reason="Requires a previously created member relationship")
def test_container_registry_members_list_with_pagination():
    exit_code, _, stderr, jsonout = run_cli(
        [
            "container-registry",
            "members",
            "list",
            f"--registry-id={test_members_context['registry_id']}",
            "--control.limit=1",
            "--control.offset=0",
        ]
    )
    assert exit_code == 0, stderr
    assert "results" in jsonout
    assert len(jsonout["results"]) <= 1


@pytest.mark.skip(reason="Requires a previously created member relationship")
def test_container_registry_members_get():
    exit_code, _, stderr, jsonout = run_cli(
        [
            "container-registry",
            "members",
            "get",
            f"--registry-id={test_members_context['registry_id']}",
            f"--member-id={test_members_context['member_id']}",
        ]
    )
    assert exit_code == 0, stderr
    assert jsonout["id"] == test_members_context["member_id"]
    assert "registry_id" in jsonout
    assert "user_id" in jsonout
    assert "role" in jsonout
    assert "created_at" in jsonout
    assert "updated_at" in jsonout


@pytest.mark.skip(reason="Requires a previously created member relationship")
def test_container_registry_members_update():
    exit_code, _, stderr, jsonout = run_cli(
        [
            "container-registry",
            "members",
            "update",
            f"--registry-id={test_members_context['registry_id']}",
            f"--member-id={test_members_context['member_id']}",
            "--role=developer",
        ]
    )
    assert exit_code == 0, stderr
    assert jsonout["role"] == "developer"


@pytest.mark.skip(reason="Requires a previously created member relationship")
def test_container_registry_members_delete():
    exit_code, _, stderr, _ = run_cli(
        [
            "container-registry",
            "members",
            "delete",
            f"--registry-id={test_members_context['registry_id']}",
            f"--member-id={test_members_context['member_id']}",
            "--no-confirm",
        ]
    )
    assert exit_code == 0, stderr


@pytest.mark.skip(reason="Cleanup test registry created during setup")
def test_container_registry_members_teardown_registry():
    exit_code, _, stderr, _ = run_cli(
        [
            "container-registry",
            "registries",
            "delete",
            f"--registry-id={test_members_context['registry_id']}",
            "--no-confirm",
        ]
    )
    assert exit_code == 0, stderr
