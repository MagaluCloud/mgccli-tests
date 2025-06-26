import time
import uuid

from utils import run_cli

network_test_context = {}
random_subnet_ip = '10.{}.{}.0/24'.format(*__import__('random').sample(range(0,255),4))


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


def test_network_subnetpools_create():
    exit_code, _, stderr, jsonout = run_cli(["network", "subnetpools", "create", "--name", "test-subnetpool", "--description", "test-subnetpool", "--cidr", random_subnet_ip, "--type", "default"])
    assert exit_code == 0, stderr
    assert "id" in jsonout
    network_test_context["subnetpool_id"] = jsonout["id"]

def test_network_subnetpools_list():
    exit_code, _, stderr, jsonout = run_cli(["network", "subnetpools", "list"])
    assert exit_code == 0, stderr
    assert jsonout["results"][0]["id"] == network_test_context["subnetpool_id"]


def test_network_subnetpools_get():
    exit_code, _, stderr, jsonout = run_cli(["network", "subnetpools", "get", f"--subnetpool-id={network_test_context['subnetpool_id']}"])
    assert exit_code == 0, stderr
    assert "id" in jsonout
    assert jsonout["id"] == network_test_context["subnetpool_id"]


def test_network_vpcs_subnets_list():
    exit_code, _, stderr, jsonout = run_cli(["network", "vpcs", "subnets", "list", f"--vpc-id={network_test_context['vpc_id']}"])
    assert exit_code == 0, stderr


def test_network_vpcs_subnets_create():
    exit_code, _, stderr, jsonout = run_cli(["network", "vpcs", "subnets", "create", f"--vpc-id={network_test_context['vpc_id']}", "--subnetpool-id", network_test_context["subnetpool_id"], "--name", "test-subnet", "--cidr-block", random_subnet_ip, "--ip-version", "4"])
    assert exit_code == 0, stderr
    assert "id" in jsonout
    network_test_context["subnet_id"] = jsonout["id"]


def test_network_vpcs_subnets_get():
    exit_code, _, stderr, jsonout = run_cli(["network", "subnets", "get", f"--subnet-id={network_test_context['subnet_id']}"])
    assert exit_code == 0, stderr
    assert "id" in jsonout
    assert jsonout["id"] == network_test_context["subnet_id"]


def test_network_vpcs_subnets_update():
    exit_code, _, stderr, jsonout = run_cli(["network",
                                              "subnets", 
                                              "update",
                                              f"--subnet-id={network_test_context['subnet_id']}", 
                                              f"--dns-nameservers=8.8.8.8,8.8.4.4"])
    assert exit_code == 0, stderr
    assert "id" in jsonout
    assert jsonout["id"] == network_test_context["subnet_id"]


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
            port_id,
            "--ip-spoofing-guard=true",
        ]
    )
    assert exit_code == 0, stderr


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
            network_test_context["natgateway_id"],
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
        ["network", "ports", "delete", network_test_context["port_id"], "--no-confirm"]
    )
    assert exit_code == 0, stderr

def test_network_vpcs_subnets_delete():
    exit_code, _, stderr, jsonout = run_cli(["network", "subnets", "delete", f"--subnet-id={network_test_context['subnet_id']}", "--no-confirm"])
    assert exit_code == 0, stderr

def test_network_subnetpools_delete():
    exit_code, _, stderr, jsonout = run_cli(["network", "subnetpools", "delete", f"--subnetpool-id={network_test_context['subnetpool_id']}", "--no-confirm"])
    assert exit_code == 0, stderr

def test_network_vpcs_delete():
    exit_code, _, stderr, _ = run_cli(
        ["network", "vpcs", "delete", network_test_context["vpc_id"], "--no-confirm"]
    )
    assert exit_code == 0, stderr
