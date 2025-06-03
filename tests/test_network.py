import time
import uuid

from utils import run_cli

# ports           Operations related to Ports
# public-ips      Operations related to Public IPs
# rules           Operations related to Rules
# security-groups Operations related to Security Groups
# subnetpools     Operations related to Subnet Pools
# subnets         Operations related to Subnets
# vpcs            Operations related to VPCs

network_test_context = {}


def test_network_vpcs_create():
    exit_code, _, stderr, jsonout = run_cli(
        ["network", "vpcs", "create", f"--name=test-{uuid.uuid1()}"]
    )
    assert exit_code == 0, stderr
    assert jsonout["id"] is not None
    assert jsonout["status"] == "pending"

    network_test_context["vpc_id"] = jsonout["id"]


def test_network_vpcs_get():
    exit_code, _, stderr, jsonout = run_cli(
        ["network", "vpcs", "get", network_test_context["vpc_id"]]
    )
    assert exit_code == 0, stderr
    assert jsonout["id"] == network_test_context["vpc_id"]

    # Wait until VPC processing is over (hoping it will be)
    while jsonout["status"] in ["pending", "processing"]:
        time.sleep(5)
        _, _, _, jsonout = run_cli(
            ["network", "vpcs", "get", network_test_context["vpc_id"]]
        )


def test_network_vpcs_list():
    exit_code, _, stderr, jsonout = run_cli(["network", "vpcs", "list"])
    assert exit_code == 0, stderr
    assert len(jsonout["vpcs"]) > 0


def test_network_ports_create():
    vpc_id = network_test_context["vpc_id"]
    exit_code, _, stderr, jsonout = run_cli(
        [
            "network",
            "vpcs",
            "ports",
            "create",
            "--vpc-id",
            vpc_id,
            "--name",
            "test-port",
        ]
    )
    assert exit_code == 0, stderr
    assert "id" in jsonout

    network_test_context["port_id"] = jsonout["id"]


def test_network_ports_list():
    exit_code, _, stderr, jsonout = run_cli(["network", "ports", "list"])
    assert exit_code == 0, stderr
    assert isinstance(jsonout, list)
    assert len(jsonout) > 0


def test_network_ports_update():
    port_id = network_test_context["port_id"]
    exit_code, _, stderr, jsonout = run_cli(
        [
            "network",
            "ports",
            "update",
            "--port-id",
            port_id,
            "--ip-spoofing-guard",
            "true",
        ]
    )
    assert exit_code == 0, stderr
    assert "teste" in jsonout, jsonout


def test_network_natgateways_create():
    exit_code, _, stderr, jsonout = run_cli(
        [
            "network",
            "nat-gateways",
            "create",
            f"--name=test-{uuid.uuid1()}",
            f"--vpc-id={network_test_context['vpc_id']}",
            "--zone=br-se1-a",
        ]
    )

    assert exit_code == 0, stderr
    assert "id" in jsonout

    network_test_context["natgateway_id"] = jsonout["id"]


def test_network_natgateways_get():
    exit_code, _, stderr, jsonout = run_cli(
        [
            "network",
            "nat-gateways",
            "get",
            f"--nat-gateway-id={network_test_context['natgateway_id']}",
        ]
    )
    assert exit_code == 0, stderr
    assert "id" in jsonout
    assert jsonout["id"] == network_test_context["natgateway_id"]


def test_network_natgateways_list():
    exit_code, _, stderr, jsonout = run_cli(
        [
            "network",
            "nat-gateways",
            "list",
            f"--vpc-id={network_test_context['vpc_id']}",
        ]
    )
    assert exit_code == 0, stderr
    assert "result" in jsonout, jsonout


def test_network_natgateway_delete():
    exit_code, _, stderr, _ = run_cli(
        [
            "network",
            "nat-gateways",
            "delete",
            network_test_context["natgateway_id"],
            "--no-confirm",
        ]
    )
    assert exit_code == 0, stderr


def test_network_ports_delete():
    exit_code, _, stderr, _ = run_cli(
        ["network", "vpcs", "delete", network_test_context["port_id"], "--no-confirm"]
    )
    assert exit_code == 0, stderr


def test_network_vpcs_delete():
    exit_code, _, stderr, _ = run_cli(
        ["network", "vpcs", "delete", network_test_context["vpc_id"], "--no-confirm"]
    )
    assert exit_code == 0, stderr
