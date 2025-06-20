import random
import time

from utils import run_cli

dbaas_test_context = {}


def _get_instance(instance_id):
    return run_cli(["dbaas", "instances", "get", instance_id])


def _wait_for_instance_running_state(instance_id):
    _, _, _, jsonout = _get_instance(instance_id)
    while jsonout["status"] not in ["ACTIVE", "ERROR"]:
        time.sleep(5)
        _, _, _, jsonout = _get_instance(instance_id)

    assert jsonout["status"] == "ACTIVE"


def test_dbaas_engines_list():
    exit_code, _, stderr, jsonout = run_cli(["dbaas", "engines", "list"])
    assert exit_code == 0, stderr
    assert "results" in jsonout
    assert len(jsonout["results"]) > 0

    engine = jsonout["results"][0]
    assert "id" in engine
    assert "name" in engine
    assert "status" in engine
    assert "version" in engine

    for eng in jsonout["results"]:
        if eng["status"] == "ACTIVE":
            dbaas_test_context["engine_id"] = eng["id"]

    assert dbaas_test_context["engine_id"]


def test_dbaas_engines_get():
    exit_code, _, stderr, jsonout = run_cli(
        ["dbaas", "engines", "get", dbaas_test_context["engine_id"]]
    )
    assert exit_code == 0, stderr

    assert "id" in jsonout
    assert "name" in jsonout
    assert "status" in jsonout
    assert "version" in jsonout


def test_dbaas_instance_types_list():
    exit_code, _, stderr, jsonout = run_cli(["dbaas", "instance-types", "list", "--status=ACTIVE"])
    assert exit_code == 0, stderr
    assert "results" in jsonout
    assert len(jsonout["results"]) > 0

    instance_type = jsonout["results"][0]
    assert "id" in instance_type
    assert "family_description" in instance_type
    assert "family_slug" in instance_type
    assert "label" in instance_type
    assert "name" in instance_type
    assert "ram" in instance_type
    assert "size" in instance_type
    assert "vcpu" in instance_type

    for it in jsonout["results"]:
        dbaas_test_context["engine_id"] = it["engine_id"]
        if it["compatible_product"] == "SINGLE_INSTANCE":
            dbaas_test_context["single_instance_type_id"] = it["id"]
        if it["compatible_product"] == "CLUSTER":
            dbaas_test_context["cluster_instance_type_id"] = it["id"]
    
    assert dbaas_test_context["single_instance_type_id"]
    # assert dbaas_test_context["cluster_instance_type_id"]


def test_dbaas_instance_types_get():
    exit_code, _, stderr, jsonout = run_cli(
        [
            "dbaas",
            "instance-types",
            "get",
            dbaas_test_context["single_instance_type_id"],
        ]
    )
    assert exit_code == 0, stderr

    assert "id" in jsonout
    assert "family_description" in jsonout
    assert "family_slug" in jsonout
    assert "label" in jsonout
    assert "name" in jsonout
    assert "ram" in jsonout
    assert "size" in jsonout
    assert "vcpu" in jsonout


def test_dbaas_instances_create():
    exit_code, _, stderr, jsonout = run_cli(
        [
            "dbaas",
            "instances",
            "create",
            f"--engine-id={dbaas_test_context['engine_id']}",
            f"--instance-type-id={dbaas_test_context['single_instance_type_id']}",
            "--user=some-user",
            "--password=some-passwd",
            "--volume.size=10",
            "--volume.type=CLOUD_NVME15K",
            f"--name=cli-test-{random.randint(0, 9999)}",
        ]
    )

    assert exit_code == 0, stderr
    assert "id" in jsonout

    dbaas_test_context["instance_id"] = jsonout["id"]

    _wait_for_instance_running_state(jsonout["id"])


def test_dbaas_instances_list():
    exit_code, _, stderr, jsonout = run_cli(["dbaas", "instances", "list"])

    assert exit_code == 0, stderr
    assert "results" in jsonout
    assert "meta" in jsonout

    assert len(jsonout["results"]) > 0


def test_dbaas_instances_get():
    exit_code, _, stderr, jsonout = run_cli(
        ["dbaas", "instances", "get", dbaas_test_context["instance_id"]]
    )

    assert exit_code == 0, stderr

    assert "addresses" in jsonout
    assert "apply_parameters_pending" in jsonout
    assert "availability_zone" in jsonout
    assert "backup_retention_days" in jsonout
    assert "created_at" in jsonout
    assert "engine_id" in jsonout
    assert "generation" in jsonout
    assert "id" in jsonout
    assert "instance_type_id" in jsonout
    assert "name" in jsonout
    assert "parameter_group_id" in jsonout
    assert "status" in jsonout
    assert "updated_at" in jsonout
    assert "volume" in jsonout


def test_dbaas_replicas_list():
    exit_code, _, stderr, jsonout = run_cli(["dbaas", "replicas", "list"])

    assert exit_code == 0, stderr
    assert "results" in jsonout
    assert "meta" in jsonout


def test_dbaas_clusters_list():
    exit_code, _, stderr, jsonout = run_cli(["dbaas", "clusters", "list"])

    assert exit_code == 0, stderr
    assert "results" in jsonout
    assert "meta" in jsonout


# def test_dbaas_instances_delete():
#     exit_code, _, stderr, jsonout = run_cli(
#         [
#             "dbaas",
#             "instances",
#             "delete",
#             dbaas_test_context["instance_id"],
#             "--no-confirm",
#         ]
#     )

#     assert exit_code == 0, stderr
