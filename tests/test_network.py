import time
import uuid

from utils import run_cli

network_test_context = {}
random_subnet_ip = '10.{}.{}.0/24'.format(*__import__('random').sample(range(0,255),4))

def test_network_vpcs_create_required_flags_empty():
    exit_code, _, stderr, jsonout = run_cli(
        ["network", "vpcs", "create"]
    )
    assert exit_code != 0, "code should be different from 0"
    assert "missing required flag: --name=string" in stderr

def test_network_vpcs_create():
    exit_code, _, stderr, jsonout = run_cli(
        ["network", "vpcs", "create", f"--name=test-{uuid.uuid1()}", "--description", "VPC for CLI tests"]
    )
    assert exit_code == 0, stderr
    assert jsonout["id"] is not None
    assert jsonout["status"] == "pending"

    network_test_context["vpc_id"] = jsonout["id"]

def test_network_vpcs_get_required_flags_empty():
    exit_code, _, stderr, jsonout = run_cli(
        ["network", "vpcs", "get"]
    )
    assert exit_code != 0, "code should be different from 0"
    assert "missing required flag: --id=string" in stderr

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

def test_network_subnetpools_create_required_flags_empty():
    exit_code, _, stderr, jsonout = run_cli(["network", "subnetpools", "create", "--cidr", random_subnet_ip, "--type", "default"])
    assert exit_code != 0, "code should be different from 0"
    assert "missing required flags: " in stderr
    assert "--name=string" in stderr
    assert "--description=string" in stderr

def test_network_subnetpools_create():
    exit_code, _, stderr, jsonout = run_cli(["network", "subnetpools", "create", "--name", "test-subnetpool", "--description", "test-subnetpool", "--cidr", random_subnet_ip, "--type", "default"])
    assert exit_code == 0, stderr
    assert "id" in jsonout
    network_test_context["subnetpool_id"] = jsonout["id"]

def test_network_subnetpools_list():
    exit_code, _, stderr, jsonout = run_cli(["network", "subnetpools", "list"])
    assert exit_code == 0, stderr
    assert jsonout["meta"]["page"]["offset"] == 0
    assert jsonout["meta"]["page"]["limit"] == 20
    assert jsonout["results"][0]["id"] == network_test_context["subnetpool_id"]

def test_network_subnetpools_list_offset_limit():
    exit_code, _, stderr, jsonout = run_cli(["network", "subnetpools", "list", "--control.limit", "2", "--control.offset", "1"])
    assert exit_code == 0, stderr
    assert jsonout["meta"]["page"]["offset"] == 1
    assert jsonout["meta"]["page"]["limit"] == 2

def test_network_subnetpools_get_required_flags_empty():
    exit_code, _, stderr, jsonout = run_cli(["network", "subnetpools", "get"])
    assert exit_code != 0, "code should be different from 0"
    assert "missing required flag: --subnetpool-id=string" in stderr

def test_network_subnetpools_get():
    exit_code, _, stderr, jsonout = run_cli(["network", "subnetpools", "get", f"--subnetpool-id={network_test_context['subnetpool_id']}"])
    assert exit_code == 0, stderr
    assert "id" in jsonout
    assert jsonout["id"] == network_test_context["subnetpool_id"]

def test_network_vpcs_subnets_list_required_flags_empty():
    exit_code, _, stderr, jsonout = run_cli(["network", "vpcs", "subnets", "list"])
    assert exit_code != 0, "code should be different from 0"
    assert "missing required flag: --vpc-id=string" in stderr

def test_network_vpcs_subnets_list():
    exit_code, _, stderr, jsonout = run_cli(["network", "vpcs", "subnets", "list", f"--vpc-id={network_test_context['vpc_id']}"])
    assert exit_code == 0, stderr

def test_network_vpcs_subnets_create_required_flags_empty():
    exit_code, _, stderr, jsonout = run_cli(["network", "vpcs", "subnets", "create"])
    assert exit_code != 0, "code should be different from 0"
    assert "missing required flags: " in stderr
    assert "--vpc-id=string" in stderr
    assert "--name=string" in stderr
    assert "--cidr-block=string" in stderr
    assert "--ip-version=integer" in stderr

def test_network_vpcs_subnets_create():
    exit_code, _, stderr, jsonout = run_cli(["network", "vpcs", "subnets", "create", f"--vpc-id={network_test_context['vpc_id']}", "--subnetpool-id", network_test_context["subnetpool_id"], "--name", "test-subnet", "--cidr-block", random_subnet_ip, "--ip-version", "4"])
    assert exit_code == 0, stderr
    assert "id" in jsonout
    network_test_context["subnet_id"] = jsonout["id"]

def test_network_subnets_get_required_flags_empty():
    exit_code, _, stderr, jsonout = run_cli(["network", "subnets", "get"])
    assert exit_code != 0, "code should be different from 0"
    assert "missing required flag: --subnet-id=string" in stderr

def test_network_subnets_get():
    exit_code, _, stderr, jsonout = run_cli(["network", "subnets", "get", f"--subnet-id={network_test_context['subnet_id']}"])
    assert exit_code == 0, stderr
    assert "id" in jsonout
    assert jsonout["id"] == network_test_context["subnet_id"]

def test_network_subnets_update_required_flags_empty():
    exit_code, _, stderr, jsonout = run_cli(["network", "subnets", "update"])
    assert exit_code != 0, "code should be different from 0"
    assert "missing required flag: --subnet-id=string" in stderr
    
def test_network_subnets_update():
    exit_code, _, stderr, jsonout = run_cli(["network",
                                              "subnets", 
                                              "update",
                                              f"--subnet-id={network_test_context['subnet_id']}", 
                                              f"--dns-nameservers=8.8.8.8,8.8.4.4"])
    assert exit_code == 0, stderr
    assert "id" in jsonout
    assert jsonout["id"] == network_test_context["subnet_id"]

def test_network_vpcs_ports_create_required_flags_empty():
    exit_code, _, stderr, jsonout = run_cli(["network", "vpcs", "ports", "create"])
    assert exit_code != 0, "code should be different from 0"
    assert "missing required flags: " in stderr
    assert "--vpc-id=string" in stderr
    assert "--name=string" in stderr

def test_network_vpcs_ports_create():
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

def test_network_vpcs_ports_list_required_flags_empty():
    exit_code, _, stderr, jsonout = run_cli(["network", "vpcs", "ports", "list"])
    assert exit_code != 0, "code should be different from 0"
    assert "missing required flag: --vpc-id=string" in stderr

def test_network_vpcs_ports_list():
    exit_code, _, stderr, jsonout = run_cli(["network", "vpcs", "ports", "list", f"--vpc-id={network_test_context['vpc_id']}"])
    assert exit_code == 0, stderr
    assert len(jsonout["ports"]) == 1

def test_network_ports_list():
    exit_code, _, stderr, jsonout = run_cli(["network", "ports", "list"])
    assert exit_code == 0, stderr
    assert isinstance(jsonout, list)
    assert len(jsonout) > 0

def test_network_ports_update_required_flags_empty():
    exit_code, _, stderr, jsonout = run_cli(["network", "ports", "update"])
    assert exit_code != 0, "code should be different from 0"
    assert "missing required flag: --port-id=string" in stderr

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

def test_network_ports_get_required_flags_empty():
    exit_code, _, stderr, jsonout = run_cli(["network", "ports", "get"])
    assert exit_code != 0, "code should be different from 0"
    assert "missing required flag: --port-id=string" in stderr

def test_network_ports_get():
    exit_code, _, stderr, jsonout = run_cli(["network", "ports", "get", f"--port-id={network_test_context['port_id']}"])
    assert exit_code == 0, stderr
    assert "id" in jsonout
    assert jsonout["id"] == network_test_context["port_id"]

def test_network_vpcs_public_ips_create_required_flags_empty():
    exit_code, _, stderr, jsonout = run_cli(["network", "vpcs", "public-ips", "create"])
    assert exit_code != 0, "code should be different from 0"
    assert "missing required flag: --vpc-id=string" in stderr

def test_network_vpcs_public_ips_create():
    exit_code, _, stderr, jsonout = run_cli(["network", "vpcs", "public-ips", "create", f"--vpc-id={network_test_context['vpc_id']}", "--description=public-ip-test"])
    assert exit_code == 0, stderr
    assert "id" in jsonout
    network_test_context["public_ip_id"] = jsonout["id"]

def test_network_vpcs_public_ips_list_required_flags_empty():
    exit_code, _, stderr, jsonout = run_cli(["network", "vpcs", "public-ips", "list"])
    assert exit_code != 0, "code should be different from 0"
    assert "missing required flag: --vpc-id=string" in stderr

def test_network_vpcs_public_ips_list():
    exit_code, _, stderr, jsonout = run_cli(["network", "vpcs", "public-ips", "list", f"--vpc-id={network_test_context['vpc_id']}"])
    assert exit_code == 0, stderr
    assert "public_ips" in jsonout
    assert len(jsonout["public_ips"]) > 0

def test_network_public_ips_list():
    exit_code, _, stderr, jsonout = run_cli(["network", "public-ips", "list"])
    assert exit_code == 0, stderr
    assert "public_ips" in jsonout
    assert len(jsonout["public_ips"]) > 0

def test_network_public_ips_get_required_flags_empty():
    exit_code, _, stderr, jsonout = run_cli(["network", "public-ips", "get"])
    assert exit_code != 0, "code should be different from 0"
    assert "missing required flag: --public-ip-id=string" in stderr

def test_network_public_ips_get():
    exit_code, _, stderr, jsonout = run_cli(["network", "public-ips", "get", f"--public-ip-id={network_test_context['public_ip_id']}"])
    assert exit_code == 0, stderr
    assert "id" in jsonout
    assert jsonout["id"] == network_test_context["public_ip_id"]

def test_network_security_groups_create_required_flags_empty():
    exit_code, _, stderr, jsonout = run_cli(["network", "security-groups", "create"])
    assert exit_code != 0, "code should be different from 0"
    assert "missing required flag: --name=string" in stderr

def test_network_security_groups_create():
    exit_code, _, stderr, jsonout = run_cli(
        [
            "network",
            "security-groups",
            "create",
            "--name",
            f"test-security-group-{uuid.uuid1()}",
        ]
    )
    assert exit_code == 0, stderr
    assert "id" in jsonout
    network_test_context["security_group_id"] = jsonout["id"]

def test_network_security_groups_get_required_flags_empty():
    exit_code, _, stderr, jsonout = run_cli(["network", "security-groups", "get"])
    assert exit_code != 0, "code should be different from 0"
    assert "missing required flag: --security-group-id=string" in stderr

def test_network_security_groups_get():
    exit_code, _, stderr, jsonout = run_cli(["network", "security-groups", "get", f"--security-group-id={network_test_context['security_group_id']}"])
    assert exit_code == 0, stderr
    assert "id" in jsonout
    assert jsonout["id"] == network_test_context["security_group_id"]

def test_network_security_groups_list():
    exit_code, _, stderr, jsonout = run_cli(["network", "security-groups", "list"])
    assert exit_code == 0, stderr
    assert "security_groups" in jsonout
    assert len(jsonout["security_groups"]) > 0

def test_network_ports_attach_required_flags_empty():
    exit_code, _, stderr, jsonout = run_cli(["network", "ports", "attach"])
    assert exit_code != 0, "code should be different from 0"
    assert "missing required flags: " in stderr
    assert "--port-id=string" in stderr
    assert "--security-group-id=string" in stderr

def test_network_ports_attach():
    exit_code, _, stderr, jsonout = run_cli(["network", "ports", "attach", f"--port-id={network_test_context['port_id']}", f"--security-group-id={network_test_context['security_group_id']}"])
    assert exit_code == 0, stderr

def test_network_ports_detach_required_flags_empty():
    exit_code, _, stderr, jsonout = run_cli(["network", "ports", "detach"])
    assert exit_code != 0, "code should be different from 0"
    assert "missing required flags: " in stderr
    assert "--port-id=string" in stderr
    assert "--security-group-id=string" in stderr

def test_network_ports_detach():
    exit_code, _, stderr, jsonout = run_cli(["network", "ports", "detach", f"--port-id={network_test_context['port_id']}", f"--security-group-id={network_test_context['security_group_id']}"])
    assert exit_code == 0, stderr

def test_network_security_groups_delete_required_flags_empty():
    exit_code, _, stderr, jsonout = run_cli(["network", "security-groups", "delete"])
    assert exit_code != 0, "code should be different from 0"
    assert "missing required flag: --security-group-id=string" in stderr

def test_network_security_groups_delete():
    exit_code, _, stderr, jsonout = run_cli(["network", "security-groups", "delete", f"--security-group-id={network_test_context['security_group_id']}", "--no-confirm"])
    assert exit_code == 0, stderr

def test_network_natgateways_create_required_flags_empty():
    exit_code, _, stderr, jsonout = run_cli(["network", "nat-gateways", "create"])
    assert exit_code != 0, "code should be different from 0"
    assert "missing required flags: " in stderr
    assert "--name=string" in stderr
    assert "--vpc-id=string" in stderr
    assert "--zone=string" in stderr

def test_network_natgateways_create():
    exit_code, _, stderr, jsonout = run_cli(
        [
            "network",
            "nat-gateways",
            "create",
            f"--name=test-{uuid.uuid1()}",
            f"--vpc-id={network_test_context['vpc_id']}",
            "--zone=br-se1-a",
            "--description=test-natgateway",
        ]
    )

    assert exit_code == 0, stderr
    assert "id" in jsonout

    network_test_context["natgateway_id"] = jsonout["id"]

def test_network_natgateways_get_required_flags_empty():
    exit_code, _, stderr, jsonout = run_cli(["network", "nat-gateways", "get"])
    assert exit_code != 0, "code should be different from 0"
    assert "missing required flag: --id=string" in stderr

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

def test_network_natgateways_list_required_flags_empty():
    exit_code, _, stderr, jsonout = run_cli(["network", "nat-gateways", "list"])
    assert exit_code != 0, "code should be different from 0"
    assert "missing required flag: --vpc-id=string" in stderr

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

def test_network_natgateway_delete_required_flags_empty():
    exit_code, _, stderr, jsonout = run_cli(["network", "nat-gateways", "delete"])
    assert exit_code != 0, "code should be different from 0"
    assert "missing required flag: --id=string" in stderr

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

def test_network_ports_delete_required_flags_empty():
    exit_code, _, stderr, jsonout = run_cli(["network", "ports", "delete"])
    assert exit_code != 0, "code should be different from 0"
    assert "missing required flag: --port-id=string" in stderr

def test_network_ports_delete():
    exit_code, _, stderr, _ = run_cli(
        ["network", "ports", "delete", network_test_context["port_id"], "--no-confirm"]
    )
    assert exit_code == 0, stderr

def test_network_subnets_delete_required_flags_empty():
    exit_code, _, stderr, jsonout = run_cli(["network", "subnets", "delete"])
    assert exit_code != 0, "code should be different from 0"
    assert "missing required flag: --subnet-id=string" in stderr

def test_network_subnets_delete():
    exit_code, _, stderr, jsonout = run_cli(["network", "subnets", "delete", f"--subnet-id={network_test_context['subnet_id']}", "--no-confirm"])
    assert exit_code == 0, stderr

def test_network_subnetpools_delete_required_flags_empty():
    exit_code, _, stderr, jsonout = run_cli(["network", "subnetpools", "delete"])
    assert exit_code != 0, "code should be different from 0"
    assert "missing required flag: --subnetpool-id=string" in stderr

def test_network_subnetpools_delete():
    exit_code, _, stderr, jsonout = run_cli(["network", "subnetpools", "delete", f"--subnetpool-id={network_test_context['subnetpool_id']}", "--no-confirm"])
    assert exit_code == 0, stderr

def test_network_vpcs_delete_required_flags_empty():
    exit_code, _, stderr, jsonout = run_cli(["network", "vpcs", "delete"])
    assert exit_code != 0, "code should be different from 0"
    assert "missing required flag: --id=string" in stderr

def test_network_vpcs_delete():
    exit_code, _, stderr, _ = run_cli(
        ["network", "vpcs", "delete", network_test_context["vpc_id"], "--no-confirm"]
    )

    if "Status: 404 Not Found" in stderr:
        return

    assert exit_code == 0, stderr

def test_network_public_ips_delete_required_flags_empty():
    exit_code, _, stderr, jsonout = run_cli(["network", "public-ips", "delete"])
    assert exit_code != 0, "code should be different from 0"
    assert "missing required flag: --public-ip-id=string" in stderr

def test_network_public_ips_delete():
    exit_code, _, stderr, jsonout = run_cli(["network", "public-ips", "delete", f"--public-ip-id={network_test_context['public_ip_id']}", "--no-confirm"])
    assert exit_code == 0, stderr
