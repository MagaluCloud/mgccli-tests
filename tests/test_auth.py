import pytest
import uuid
from datetime import date, timedelta
from utils import run_cli


test_auth_context = {}
pytest.skip("Skipping ", allow_module_level=True)


def test_version():
    exit_code, _, _, jsonout = run_cli(["--version"], is_authenticated=False, has_json_output=False)
    assert exit_code == 0
    assert jsonout


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


def test_auth_api_key_create_with_validity():
    exp = (date.today() + timedelta(days=1)).isoformat()
    name = str(uuid.uuid4())
    exit_code, _, _, jsonout = run_cli(
        [
            "auth",
            "api-key",
            "create",
            "--description",
            "Automated testing from MGC CLI",
            "--expiration",
            exp,
            "--name",
            name,
            "--scopes",
            '["dbaas.read"]',
        ]
    )
    assert exit_code == 0
    assert "uuid" in jsonout
    test_auth_context["api_key_uuid_with_validity"] = jsonout["uuid"]


def test_auth_api_key_create_without_validity():
    name = str(uuid.uuid4())
    exit_code, _, _, jsonout = run_cli(
        [
            "auth",
            "api-key",
            "create",
            "--description",
            "Automated testing from MGC CLI",
            "--name",
            name,
            "--scopes",
            '["dbaas.read"]',
        ]
    )
    assert exit_code == 0
    assert "uuid" in jsonout
    test_auth_context["api_key_uuid_without_validity"] = jsonout["uuid"]


def test_auth_api_key_create_without_validity_and_description():
    name = str(uuid.uuid4())
    exit_code, _, _, jsonout = run_cli(
        [
            "auth",
            "api-key",
            "create",
            "--name",
            name,
            "--scopes",
            '["dbaas.read"]',
        ]
    )
    assert exit_code == 0
    assert "uuid" in jsonout
    test_auth_context["api_key_uuid_without_validity_and_description"] = jsonout["uuid"]


def test_auth_api_key_list_with_validity():
    exit_code, _, _, jsonout = run_cli(["auth", "api-key", "list"])
    assert exit_code == 0
    assert len(jsonout) > 0
    api_key_with_validity = next((item for item in jsonout if item.get("id") == test_auth_context.get("api_key_uuid_with_validity")), None)
    assert api_key_with_validity
    assert "id" in api_key_with_validity
    assert "name" in api_key_with_validity
    assert "start_validity" in api_key_with_validity
    assert "description" in api_key_with_validity
    assert "end_validity" in api_key_with_validity


def test_auth_api_key_list_without_validity():
    exit_code, _, _, jsonout = run_cli(["auth", "api-key", "list"])
    assert exit_code == 0
    assert len(jsonout) > 0
    api_key_without_validity = next((item for item in jsonout if item.get("id") == test_auth_context.get("api_key_uuid_without_validity")), None)
    assert api_key_without_validity
    assert "id" in api_key_without_validity
    assert "name" in api_key_without_validity
    assert "start_validity" in api_key_without_validity
    assert "description" in api_key_without_validity
    assert "end_validity" not in api_key_without_validity


def test_auth_api_key_list_without_validity_and_description():
    exit_code, _, _, jsonout = run_cli(["auth", "api-key", "list"])
    assert exit_code == 0
    assert len(jsonout) > 0
    api_key_without_validity = next((item for item in jsonout if item.get("id") == test_auth_context.get("api_key_uuid_without_validity_and_description")), None)
    assert api_key_without_validity
    assert "id" in api_key_without_validity
    assert "name" in api_key_without_validity
    assert "start_validity" in api_key_without_validity
    assert "description" not in api_key_without_validity
    assert "end_validity" not in api_key_without_validity


def test_auth_api_key_get():
    exit_code, _, _, jsonout = run_cli(
        ["auth", "api-key", "get", test_auth_context["api_key_uuid_with_validity"]]
    )
    assert exit_code == 0
    assert "api_key" in jsonout
    assert "id" in jsonout
    assert "key_pair_id" in jsonout
    assert "key_pair_secret" in jsonout
    assert "name" in jsonout
    assert "scopes" in jsonout
    assert "start_validity" in jsonout
