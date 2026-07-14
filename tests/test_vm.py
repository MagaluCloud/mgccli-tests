import ipaddress
import json
import time
import random
import uuid
from utils import run_cli

vm_test_context = {}

# One /24 per VPC, so each vNIC gets a private IP from a distinct network.
subnet_a_cidr, subnet_b_cidr = (
    "10.{}.1.0/24".format(octet) for octet in random.sample(range(0, 255), 2)
)

POLL_INTERVAL = 5
CREATE_TIMEOUT = 900
DELETE_TIMEOUT = 900


def _get_vm(vm_id):
    return run_cli(["vm", "instances", "get", vm_id])


def _get_snapshot(snapshot_id):
    return run_cli(["vm", "snapshots", "get", snapshot_id])


def _get_vpc(vpc_id):
    return run_cli(["network", "vpcs", "get", vpc_id])


def _interface(vpc_id, subnet_id, tag, associate_public_ip):
    return {
        "associate_public_ip": associate_public_ip,
        "subnets": [{"id": subnet_id}],
        "tag": tag,
        "vpc": {"id": vpc_id},
    }


def _wait_for_vpc(vpc_id):
    deadline = time.monotonic() + CREATE_TIMEOUT
    _, _, _, jsonout = _get_vpc(vpc_id)
    while jsonout["status"] in ["pending", "processing"]:
        assert time.monotonic() < deadline, f"vpc {vpc_id} still {jsonout['status']}"
        time.sleep(POLL_INTERVAL)
        _, _, _, jsonout = _get_vpc(vpc_id)
    return jsonout


def _wait_for_vm_deletion(vm_id):
    deadline = time.monotonic() + DELETE_TIMEOUT
    while time.monotonic() < deadline:
        exit_code, _, _, jsonout = _get_vm(vm_id)
        if exit_code != 0 or jsonout.get("status") == "deleted":
            return
        time.sleep(POLL_INTERVAL)
    raise AssertionError(f"vm {vm_id} was not deleted within {DELETE_TIMEOUT}s")


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
    assert jsonout["meta"]["page"]["limit"] == 50
    assert jsonout["meta"]["page"]["offset"] == 0


def test_vm_images_list_limit_offset():
    exit_code, _, stderr, jsonout = run_cli(["vm", "images", "list", "--control.limit=1", "--control.offset=1"])
    assert exit_code == 0, stderr
    assert "images" in jsonout
    assert len(jsonout["images"]) == 1
    assert jsonout["meta"]["page"]["limit"] == 1
    assert jsonout["meta"]["page"]["offset"] == 1


def test_vm_machine_types_list():
    exit_code, _, stderr, jsonout = run_cli(["vm", "machine-types", "list"])
    assert exit_code == 0, stderr
    assert "machine_types" in jsonout
    assert len(jsonout["machine_types"]) > 0
    assert jsonout["meta"]["page"]["limit"] == 200
    assert jsonout["meta"]["page"]["offset"] == 0


def test_vm_machine_types_list_limit_offset():
    exit_code, _, stderr, jsonout = run_cli(["vm", "machine-types", "list", "--control.limit=1", "--control.offset=1"])
    assert exit_code == 0, stderr
    assert "machine_types" in jsonout
    assert len(jsonout["machine_types"]) == 1
    assert jsonout["meta"]["page"]["limit"] == 1
    assert jsonout["meta"]["page"]["offset"] == 1


def test_vm_instances_create():
    name = f"test_vm_{uuid.uuid1()}"

    exit_code, _, stderr, jsonout = run_cli(
        [
            "vm",
            "instances",
            "create",
            f"--name={name}",
            "--image.name='cloud-ubuntu-24.04 LTS'",
            "--machine-type.name=BV1-1-10",
            f"--ssh-key-name={vm_test_context['key_name']}",
        ]
    )
    assert exit_code == 0, stderr
    assert "id" in jsonout

    vm_test_context["vm_name"] = name
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
            f"--name={vm_test_context['vm_name']}",
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


def test_vm_snapshots_create_required_flags_empty():
    exit_code, _, stderr, jsonout = run_cli(
        [
            "vm",
            "snapshots",
            "create",
        ]
    )
    assert exit_code != 0, "code should be different from 0"
    assert "missing required flags: " in stderr
    assert "--name=string" in stderr
    assert "--instance=object" in stderr


def test_vm_snapshots_create():
    exit_code, _, stderr, jsonout = run_cli(
        [
            "vm",
            "snapshots",
            "create",
            f"--name=test_snapshot_{uuid.uuid1()}",
            f"--instance.id={vm_test_context['vm_id']}",
        ]
    )
    assert exit_code == 0, stderr
    assert "id" in jsonout

    vm_test_context["snapshot_id"] = jsonout["id"]

    # Wait until snapshot creation is over (hoping it will be)
    _, _, _, jsonout = _get_snapshot(vm_test_context["snapshot_id"])
    while jsonout["status"] in ["provisioning", "creating"]:
        time.sleep(5)
        _, _, _, jsonout = _get_snapshot(vm_test_context["snapshot_id"])

    assert jsonout["status"] == "completed"


def test_vm_snapshots_list():
    exit_code, _, stderr, jsonout = run_cli(["vm", "snapshots", "list"])
    assert exit_code == 0, stderr
    assert "snapshots" in jsonout
    assert jsonout["meta"]["page"]["limit"] == 200
    assert jsonout["meta"]["page"]["offset"] == 0


def test_vm_snapshots_list_limit_offset():
    exit_code, _, stderr, jsonout = run_cli(["vm", "snapshots", "list", "--control.limit=1", "--control.offset=1"])
    assert exit_code == 0, stderr
    assert "snapshots" in jsonout
    assert jsonout["meta"]["page"]["limit"] == 1
    assert jsonout["meta"]["page"]["offset"] == 1


def test_vm_snapshots_get_required_flags_empty():
    exit_code, _, stderr, jsonout = run_cli(
        [
            "vm",
            "snapshots",
            "get",
        ]
    )
    assert exit_code != 0, "code should be different from 0"
    assert "missing required flag: --id=string" in stderr


def test_vm_snapshots_get():
    exit_code, _, stderr, jsonout = run_cli(
        ["vm", "snapshots", "get", vm_test_context["snapshot_id"]]
    )
    assert exit_code == 0, stderr
    assert "id" in jsonout
    assert jsonout["id"] == vm_test_context["snapshot_id"]
    assert "name" not in jsonout["instance"]["image"]
    assert "name" not in jsonout["instance"]["machine_type"]


def test_vm_snapshots_get_expand_image():
    exit_code, _, stderr, jsonout = run_cli(
        ["vm", "snapshots", "get", vm_test_context["snapshot_id"], "--expand=image"]
    )
    assert exit_code == 0, stderr
    assert "id" in jsonout
    assert jsonout["id"] == vm_test_context["snapshot_id"]
    assert "name" in jsonout["instance"]["image"]
    assert jsonout["instance"]["image"]["name"] == "cloud-ubuntu-24.04 LTS"


def test_vm_snapshots_get_expand_machine_type():
    exit_code, _, stderr, jsonout = run_cli(
        ["vm", "snapshots", "get", vm_test_context["snapshot_id"], "--expand=machine-type"]
    )
    assert exit_code == 0, stderr
    assert "id" in jsonout
    assert jsonout["id"] == vm_test_context["snapshot_id"]
    assert "name" in jsonout["instance"]["machine_type"]
    assert jsonout["instance"]["machine_type"]["name"] == "BV1-1-10"


def test_vm_snapshots_rename_required_flags_empty():
    exit_code, _, stderr, jsonout = run_cli(
        [
            "vm",
            "snapshots",
            "rename",
        ]
    )
    assert exit_code != 0, "code should be different from 0"
    assert "missing required flags: " in stderr
    assert "--id=string" in stderr
    assert "--name=string" in stderr


def test_vm_snapshots_rename():
    exit_code, _, stderr, jsonout = run_cli(
        ["vm", "snapshots", "rename", vm_test_context["snapshot_id"], "--name=test_snapshot_renamed"]
    )
    assert exit_code == 0, stderr


def test_vm_snapshots_delete_required_flags_empty():
    exit_code, _, stderr, jsonout = run_cli(
        [
            "vm",
            "snapshots",
            "delete",
        ]
    )
    assert exit_code != 0, "code should be different from 0"
    assert "missing required flag: --id=uuid" in stderr


def test_vm_snapshots_delete():
    exit_code, _, stderr, jsonout = run_cli(
        ["vm", "snapshots", "delete", vm_test_context["snapshot_id"], "--no-confirm"]
    )
    assert exit_code == 0, stderr


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


def test_vnics_vpcs_create():
    for vpc in ["vpc_a", "vpc_b"]:
        exit_code, _, stderr, jsonout = run_cli(
            [
                "network",
                "vpcs",
                "create",
                f"--name=test-vnics-{uuid.uuid1()}",
                "--description",
                "VPC for CLI multiple vNICs tests",
            ]
        )
        assert exit_code == 0, stderr
        assert "id" in jsonout

        vm_test_context[f"{vpc}_id"] = jsonout["id"]
        _wait_for_vpc(jsonout["id"])


def test_vnics_subnetpools_create():
    for pool, cidr in [("pool_a", subnet_a_cidr), ("pool_b", subnet_b_cidr)]:
        exit_code, _, stderr, jsonout = run_cli(
            [
                "network",
                "subnetpools",
                "create",
                "--name",
                f"test-vnics-{uuid.uuid1()}",
                "--description",
                "subnetpool for CLI multiple vNICs tests",
                "--cidr",
                cidr,
                "--type",
                "default",
            ]
        )
        assert exit_code == 0, stderr
        assert "id" in jsonout

        vm_test_context[f"{pool}_id"] = jsonout["id"]


def test_vnics_subnets_create():
    subnets = [
        ("subnet_a", "vpc_a_id", "pool_a_id", subnet_a_cidr),
        ("subnet_b", "vpc_b_id", "pool_b_id", subnet_b_cidr),
    ]
    for subnet, vpc_key, pool_key, cidr in subnets:
        exit_code, _, stderr, jsonout = run_cli(
            [
                "network",
                "vpcs",
                "subnets",
                "create",
                f"--vpc-id={vm_test_context[vpc_key]}",
                "--subnetpool-id",
                vm_test_context[pool_key],
                "--name",
                f"test-vnics-{subnet}",
                "--cidr-block",
                cidr,
                "--ip-version",
                "4",
            ]
        )
        assert exit_code == 0, stderr
        assert "id" in jsonout

        vm_test_context[f"{subnet}_id"] = jsonout["id"]


def test_vm_instances_create_multiple_vnics():
    name = f"test_vm_vnics_{uuid.uuid1()}"
    interfaces = [
        _interface(
            vm_test_context["vpc_a_id"],
            vm_test_context["subnet_a_id"],
            "primary",
            True,
        ),
        _interface(
            vm_test_context["vpc_b_id"],
            vm_test_context["subnet_b_id"],
            "secondary",
            False,
        ),
    ]

    exit_code, _, stderr, jsonout = run_cli(
        [
            "vm",
            "instances",
            "create",
            f"--name={name}",
            "--image.name='cloud-ubuntu-24.04 LTS'",
            "--machine-type.name=BV1-1-10",
            f"--ssh-key-name={vm_test_context['key_name']}",
            f"--network-profile.interfaces={json.dumps(interfaces)}",
        ]
    )
    assert exit_code == 0, stderr
    assert "id" in jsonout

    vm_test_context["vnics_vm_id"] = jsonout["id"]

    # Wait until vm creation is over
    deadline = time.monotonic() + CREATE_TIMEOUT
    _, _, _, jsonout = _get_vm(vm_test_context["vnics_vm_id"])
    while jsonout["status"] in ["provisioning", "creating"]:
        assert time.monotonic() < deadline, f"vm still {jsonout['status']}"
        time.sleep(POLL_INTERVAL)
        _, _, _, jsonout = _get_vm(vm_test_context["vnics_vm_id"])

    assert jsonout["status"] == "completed"


def test_vm_instances_delete_multiple_vnics():
    exit_code, _, stderr, _ = run_cli(
        [
            "vm",
            "instances",
            "delete",
            vm_test_context["vnics_vm_id"],
            "--delete-public-ip",
            "--no-confirm",
        ]
    )
    assert exit_code == 0, stderr

    # The subnets below can only be deleted once the ports of the instance are gone.
    _wait_for_vm_deletion(vm_test_context["vnics_vm_id"])


def test_vnics_subnets_delete():
    for subnet in ["subnet_a", "subnet_b"]:
        exit_code, _, stderr, _ = run_cli(
            [
                "network",
                "subnets",
                "delete",
                f"--subnet-id={vm_test_context[f'{subnet}_id']}",
                "--no-confirm",
            ]
        )
        assert exit_code == 0, stderr


def test_vnics_subnetpools_delete():
    for pool in ["pool_a", "pool_b"]:
        exit_code, _, stderr, _ = run_cli(
            [
                "network",
                "subnetpools",
                "delete",
                f"--subnetpool-id={vm_test_context[f'{pool}_id']}",
                "--no-confirm",
            ]
        )
        assert exit_code == 0, stderr


def test_vnics_vpcs_delete():
    for vpc in ["vpc_a", "vpc_b"]:
        exit_code, _, stderr, _ = run_cli(
            [
                "network",
                "vpcs",
                "delete",
                vm_test_context[f"{vpc}_id"],
                "--no-confirm",
            ]
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