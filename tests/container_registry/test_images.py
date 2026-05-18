import pytest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import run_cli


test_images_context = {}


def test_container_registry_images_scans_help():
    exit_code, stdout, _, _ = run_cli(
        ["container-registry", "images", "scans", "--help"],
        is_authenticated=False,
        has_json_output=False,
    )
    assert exit_code == 0
    assert "list" in stdout
    assert "schedule" in stdout


def test_container_registry_images_scans_list_missing_required_flags():
    exit_code, _, stderr, _ = run_cli(
        ["container-registry", "images", "scans", "list"]
    )
    assert exit_code != 0
    assert "required flag" in stderr or "missing" in stderr


def test_container_registry_images_scans_list_missing_repository_id():
    exit_code, _, stderr, _ = run_cli(
        [
            "container-registry",
            "images",
            "scans",
            "list",
            "--registry-id=00000000-0000-0000-0000-000000000000",
            "--digest-or-tag=latest",
        ]
    )
    assert exit_code != 0
    assert "--repository-id" in stderr


def test_container_registry_images_scans_list_missing_digest_or_tag():
    exit_code, _, stderr, _ = run_cli(
        [
            "container-registry",
            "images",
            "scans",
            "list",
            "--registry-id=00000000-0000-0000-0000-000000000000",
            "--repository-id=00000000-0000-0000-0000-000000000000",
        ]
    )
    assert exit_code != 0
    assert "--digest-or-tag" in stderr


def test_container_registry_images_scans_list_invalid_status_enum():
    exit_code, _, stderr, _ = run_cli(
        [
            "container-registry",
            "images",
            "scans",
            "list",
            "--registry-id=00000000-0000-0000-0000-000000000000",
            "--repository-id=00000000-0000-0000-0000-000000000000",
            "--digest-or-tag=latest",
            "--status=invalid_status",
        ]
    )
    assert exit_code != 0


def test_container_registry_images_scans_schedule_help():
    exit_code, stdout, _, _ = run_cli(
        ["container-registry", "images", "scans", "schedule", "--help"],
        is_authenticated=False,
        has_json_output=False,
    )
    assert exit_code == 0
    assert "--registry-id" in stdout
    assert "--repository-id" in stdout
    assert "--digest-or-tag" in stdout


def test_container_registry_images_scans_schedule_missing_required_flags():
    exit_code, _, stderr, _ = run_cli(
        ["container-registry", "images", "scans", "schedule"]
    )
    assert exit_code != 0
    assert "required flag" in stderr or "missing" in stderr


def test_container_registry_images_scans_schedule_missing_digest_or_tag():
    exit_code, _, stderr, _ = run_cli(
        [
            "container-registry",
            "images",
            "scans",
            "schedule",
            "--registry-id=00000000-0000-0000-0000-000000000000",
            "--repository-id=00000000-0000-0000-0000-000000000000",
        ]
    )
    assert exit_code != 0
    assert "--digest-or-tag" in stderr


@pytest.mark.skip(reason="Requires a pre-existing registry with a pushed image")
def test_container_registry_images_scans_list_for_existing_image():
    exit_code, _, stderr, jsonout = run_cli(
        [
            "container-registry",
            "images",
            "scans",
            "list",
            f"--registry-id={test_images_context.get('registry_id')}",
            f"--repository-id={test_images_context.get('repository_id')}",
            f"--digest-or-tag={test_images_context.get('digest_or_tag', 'latest')}",
        ]
    )
    assert exit_code == 0, stderr
    assert "results" in jsonout
    assert "meta" in jsonout


@pytest.mark.skip(reason="Requires a pre-existing registry with a pushed image")
def test_container_registry_images_scans_list_with_status_filter():
    exit_code, _, stderr, jsonout = run_cli(
        [
            "container-registry",
            "images",
            "scans",
            "list",
            f"--registry-id={test_images_context.get('registry_id')}",
            f"--repository-id={test_images_context.get('repository_id')}",
            f"--digest-or-tag={test_images_context.get('digest_or_tag', 'latest')}",
            "--status=completed",
        ]
    )
    assert exit_code == 0, stderr
    assert "results" in jsonout
    for scan in jsonout["results"]:
        assert scan["status"] == "completed"


@pytest.mark.skip(reason="Requires a pre-existing registry with a pushed image")
def test_container_registry_images_scans_list_with_pagination():
    exit_code, _, stderr, jsonout = run_cli(
        [
            "container-registry",
            "images",
            "scans",
            "list",
            f"--registry-id={test_images_context.get('registry_id')}",
            f"--repository-id={test_images_context.get('repository_id')}",
            f"--digest-or-tag={test_images_context.get('digest_or_tag', 'latest')}",
            "--control.limit=1",
            "--control.offset=0",
        ]
    )
    assert exit_code == 0, stderr
    assert "results" in jsonout
    assert len(jsonout["results"]) <= 1


@pytest.mark.skip(reason="Requires a pre-existing registry with a pushed image")
def test_container_registry_images_scans_schedule_for_existing_image():
    exit_code, _, stderr, jsonout = run_cli(
        [
            "container-registry",
            "images",
            "scans",
            "schedule",
            f"--registry-id={test_images_context.get('registry_id')}",
            f"--repository-id={test_images_context.get('repository_id')}",
            f"--digest-or-tag={test_images_context.get('digest_or_tag', 'latest')}",
        ]
    )
    assert exit_code == 0, stderr
    assert "id" in jsonout
    assert "digest" in jsonout
    assert "registry_id" in jsonout
    assert "repository_id" in jsonout
    assert "status" in jsonout
    assert "created_at" in jsonout
    assert "updated_at" in jsonout
    test_images_context["scheduled_scan_id"] = jsonout["id"]
