import time
import random
from utils import run_cli

vm_test_context = {}


def _get_vm(vm_id):
    return run_cli(["vm", "instances", "get", vm_id])


def test_create_ssh_key():
    key = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIK0wmN/Cr3JXqmLW7u+g9pTh+wyqDHpSQEIQczXkVx9q not_really@a.key"
    key_name = f"cli-test-key-{random.randint(1000, 9999)}"
    exit_code, _, stderr, jsonout = run_cli(
        ["profile", "ssh-keys", "create", f"--name={key_name}", f"--key={key}"]
    )
    assert exit_code == 0, stderr
    assert "id" in jsonout
    vm_test_context["key_id"] = jsonout["id"]
    vm_test_context["key_name"] = key_name


def test_vm_images_list():
    exit_code, _, stderr, jsonout = run_cli(["vm", "images", "list"])
    assert exit_code == 0, stderr
    assert "images" in jsonout
    assert len(jsonout["images"]) > 0


def test_vm_machine_types_list():
    exit_code, _, stderr, jsonout = run_cli(["vm", "machine-types", "list"])
    assert exit_code == 0, stderr
    assert "machine_types" in jsonout
    assert len(jsonout["machine_types"]) > 0


def test_vm_snapshots_list():
    exit_code, _, stderr, jsonout = run_cli(["vm", "snapshots", "list"])
    assert exit_code == 0, stderr
    assert "snapshots" in jsonout


def test_vm_instances_create():
    exit_code, _, stderr, jsonout = run_cli(
        [
            "vm",
            "instances",
            "create",
            "--name=test_vm",
            "--image.name='cloud-ubuntu-24.04 LTS'",
            "--machine-type.name=BV1-1-10",
            f"--ssh-key-name={vm_test_context['key_name']}",
        ]
    )
    assert exit_code == 0, stderr
    assert "id" in jsonout

    vm_test_context["vm_id"] = jsonout["id"]

    # Wait until vm creation is over (hoping it will be)
    _, _, _, jsonout = _get_vm(vm_test_context["vm_id"])
    while jsonout["status"] in ["provisioning", "creating"]:
        time.sleep(5)
        _, _, _, jsonout = _get_vm(vm_test_context["vm_id"])

    assert jsonout["status"] == "completed"


def test_vm_instances_create_with_error():
    exit_code, _, stderr, jsonout = run_cli(
        [
            "vm",
            "instances",
            "create",
            "--name=test_vm",
            "--image.name='cloud-ubuntu-24.04 LTS'",
            "--machine-type.name=BV1-1-10",
            f"--ssh-key-name={vm_test_context['key_name']}",
        ]
    )
    assert exit_code != 0

    assert "Error:" in stderr
    assert "Request ID" in stderr
    assert "MGC Trace ID" in stderr
    assert "Status" in stderr


def test_vm_instances_list():
    exit_code, _, stderr, jsonout = run_cli(["vm", "instances", "list"])
    assert exit_code == 0, stderr
    assert "instances" in jsonout


def test_vm_instances_get():
    exit_code, _, stderr, jsonout = run_cli(
        ["vm", "instances", "get", vm_test_context["vm_id"]]
    )
    assert exit_code == 0, stderr
    assert "id" in jsonout
    assert "availability_zone" in jsonout
    assert "image" in jsonout
    assert "name" in jsonout
    assert "machine_type" in jsonout
    assert "network" in jsonout
    assert "interfaces" in jsonout["network"]
    assert "ssh_key_name" in jsonout
    assert "state" in jsonout
    assert "status" in jsonout


def test_vm_instances_init_logs():
    exit_code, _, _, jsonout = run_cli(
        ["vm", "instances", "init-logs", vm_test_context["vm_id"]]
    )
    assert exit_code == 0
    assert "logs" in jsonout
    assert len(jsonout["logs"]) > 0


def test_vm_instances_delete():
    exit_code, _, stderr, _ = run_cli(
        ["vm", "instances", "delete", vm_test_context["vm_id"], "--no-confirm"]
    )
    assert exit_code == 0, stderr


def test_profile_ssh_keys_delete():
    exit_code, stdout, stderr, _ = run_cli(
        [
            "profile",
            "ssh-keys",
            "delete",
            f"--key-id={vm_test_context['key_id']}",
            "--no-confirm",
        ]
    )
    assert exit_code == 0, stderr
