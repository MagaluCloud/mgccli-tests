from utils import run_cli
import os
import pytest

test_auth_context = {}


def test_auth_login():
    exit_code, _, _, _ = run_cli(["auth", "login"])
    assert exit_code == 0


def test_auth_access_token():
    exit_code, _, _, jsonout = run_cli(["auth", "access-token"])
    assert exit_code == 0
    assert jsonout


def test_auth_tenant_current():
    exit_code, _, _, jsonout = run_cli(["auth", "tenant", "current"])
    assert exit_code == 0
    assert "email" in jsonout
    assert "is_delegated" in jsonout
    assert "is_managed" in jsonout
    assert "legal_name" in jsonout
    assert "uuid" in jsonout


def test_auth_tenant_list():
    exit_code, _, _, jsonout = run_cli(["auth", "tenant", "list"])
    assert exit_code == 0
    assert len(jsonout) > 0


def test_auth_clients_list():
    exit_code, _, _, jsonout = run_cli(["auth", "clients", "list"])
    assert exit_code == 0
    assert isinstance(jsonout, list)


def test_auth_api_key_list():
    exit_code, _, _, jsonout = run_cli(["auth", "api-key", "list"])
    assert exit_code == 0
    assert len(jsonout) > 0

    test_auth_context["api_key"] = jsonout[0]["id"]


def test_auth_api_key_get():
    exit_code, _, _, jsonout = run_cli(
        ["auth", "api-key", "get", test_auth_context["api_key"]]
    )
    assert exit_code == 0
    assert "api_key" in jsonout
    assert "id" in jsonout
    assert "key_pair_id" in jsonout
    assert "key_pair_secret" in jsonout
    assert "name" in jsonout
    assert "scopes" in jsonout
    assert "start_validity" in jsonout
