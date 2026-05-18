import pytest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import run_cli


test_scans_context = {}


def test_container_registry_scans_help():
    exit_code, stdout, _, _ = run_cli(
        ["container-registry", "scans", "--help"],
        is_authenticated=False,
        has_json_output=False,
    )
    assert exit_code == 0
    assert "get" in stdout
    assert "stop" in stdout
    assert "vulnerabilities" in stdout


def test_container_registry_scans_get_missing_required_flag():
    exit_code, _, stderr, _ = run_cli(
        ["container-registry", "scans", "get"]
    )
    assert exit_code != 0
    assert "--scan-id" in stderr


def test_container_registry_scans_stop_missing_required_flag():
    exit_code, _, stderr, _ = run_cli(
        ["container-registry", "scans", "stop"]
    )
    assert exit_code != 0
    assert "--scan-id" in stderr


def test_container_registry_scans_vulnerabilities_missing_required_flag():
    exit_code, _, stderr, _ = run_cli(
        ["container-registry", "scans", "vulnerabilities"]
    )
    assert exit_code != 0
    assert "--scan-id" in stderr


def test_container_registry_scans_vulnerabilities_help():
    exit_code, stdout, _, _ = run_cli(
        ["container-registry", "scans", "vulnerabilities", "--help"],
        is_authenticated=False,
        has_json_output=False,
    )
    assert exit_code == 0
    assert "--scan-id" in stdout
    assert "--cve-id" in stdout
    assert "--fixable" in stdout
    assert "--package-name" in stdout
    assert "--severity" in stdout


@pytest.mark.skip(reason="Requires an existing scan id (from a real image scan)")
def test_container_registry_scans_get():
    exit_code, _, stderr, jsonout = run_cli(
        [
            "container-registry",
            "scans",
            "get",
            f"--scan-id={test_scans_context['scan_id']}",
        ]
    )
    assert exit_code == 0, stderr
    assert "id" in jsonout
    assert "digest" in jsonout
    assert "status" in jsonout
    assert "created_at" in jsonout
    assert "updated_at" in jsonout


@pytest.mark.skip(reason="Requires an existing scan id (from a real image scan)")
def test_container_registry_scans_get_positional_arg():
    exit_code, _, stderr, jsonout = run_cli(
        [
            "container-registry",
            "scans",
            "get",
            test_scans_context["scan_id"],
        ]
    )
    assert exit_code == 0, stderr
    assert jsonout["id"] == test_scans_context["scan_id"]


@pytest.mark.skip(reason="Requires an existing completed scan with vulnerabilities")
def test_container_registry_scans_vulnerabilities():
    exit_code, _, stderr, jsonout = run_cli(
        [
            "container-registry",
            "scans",
            "vulnerabilities",
            f"--scan-id={test_scans_context['scan_id']}",
        ]
    )
    assert exit_code == 0, stderr
    assert "results" in jsonout
    assert "meta" in jsonout


@pytest.mark.skip(reason="Requires an existing completed scan with vulnerabilities")
def test_container_registry_scans_vulnerabilities_with_severity_filter():
    exit_code, _, stderr, jsonout = run_cli(
        [
            "container-registry",
            "scans",
            "vulnerabilities",
            f"--scan-id={test_scans_context['scan_id']}",
            '--severity=["high"]',
        ]
    )
    assert exit_code == 0, stderr
    assert "results" in jsonout
    for vuln in jsonout["results"]:
        assert vuln["severity"] == "high"


@pytest.mark.skip(reason="Requires an existing completed scan with vulnerabilities")
def test_container_registry_scans_vulnerabilities_with_fixable_filter():
    exit_code, _, stderr, jsonout = run_cli(
        [
            "container-registry",
            "scans",
            "vulnerabilities",
            f"--scan-id={test_scans_context['scan_id']}",
            "--fixable",
        ]
    )
    assert exit_code == 0, stderr
    assert "results" in jsonout
    for vuln in jsonout["results"]:
        assert vuln["fixable"] is True


@pytest.mark.skip(reason="Requires an existing completed scan with vulnerabilities")
def test_container_registry_scans_vulnerabilities_with_cve_filter():
    exit_code, _, stderr, jsonout = run_cli(
        [
            "container-registry",
            "scans",
            "vulnerabilities",
            f"--scan-id={test_scans_context['scan_id']}",
            "--cve-id=CVE-2024-0000",
        ]
    )
    assert exit_code == 0, stderr
    assert "results" in jsonout


@pytest.mark.skip(reason="Requires an existing completed scan with vulnerabilities")
def test_container_registry_scans_vulnerabilities_with_package_filter():
    exit_code, _, stderr, jsonout = run_cli(
        [
            "container-registry",
            "scans",
            "vulnerabilities",
            f"--scan-id={test_scans_context['scan_id']}",
            "--package-name=openssl",
        ]
    )
    assert exit_code == 0, stderr
    assert "results" in jsonout


@pytest.mark.skip(reason="Requires an existing completed scan with vulnerabilities")
def test_container_registry_scans_vulnerabilities_with_pagination():
    exit_code, _, stderr, jsonout = run_cli(
        [
            "container-registry",
            "scans",
            "vulnerabilities",
            f"--scan-id={test_scans_context['scan_id']}",
            "--control.limit=1",
            "--control.offset=0",
        ]
    )
    assert exit_code == 0, stderr
    assert "results" in jsonout
    assert len(jsonout["results"]) <= 1


@pytest.mark.skip(reason="Requires an existing pending/running scan to stop")
def test_container_registry_scans_stop():
    exit_code, _, stderr, _ = run_cli(
        [
            "container-registry",
            "scans",
            "stop",
            f"--scan-id={test_scans_context['scan_id']}",
        ]
    )
    assert exit_code == 0, stderr


@pytest.mark.skip(reason="Completed scans cannot be stopped — should return error")
def test_container_registry_scans_stop_completed_fails():
    exit_code, _, stderr, _ = run_cli(
        [
            "container-registry",
            "scans",
            "stop",
            f"--scan-id={test_scans_context['completed_scan_id']}",
        ]
    )
    assert exit_code != 0
