import time
import uuid

from utils import run_cli

dbaas_test_context = {}


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

    dbaas_test_context["engine_id"] = engine["id"]


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
    exit_code, _, stderr, jsonout = run_cli(["dbaas", "instance-types", "list"])
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

    dbaas_test_context["instance_type_id"] = instance_type["id"]


def test_dbaas_instance_types_get():
    exit_code, _, stderr, jsonout = run_cli(
        ["dbaas", "instance-types", "get", dbaas_test_context["instance_type_id"]]
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


def test_dbaas_instances_list():
    exit_code, _, stderr, jsonout = run_cli(["dbaas", "instances", "list"])

    assert exit_code == 0, stderr
    assert "results" in jsonout
    assert "meta" in jsonout


def test_dbaas_replicas_list():
    exit_code, _, stderr, jsonout = run_cli(["dbaas", "replicas", "list"])

    assert exit_code == 0, stderr
    assert "results" in jsonout
    assert "meta" in jsonout

# def test_dbaas_clusters_create():
    # assert 1 == 2

# def test_dbaas_clusters_get():
    # assert 1 == 2

def test_dbaas_clusters_list():
    exit_code, _, stderr, jsonout = run_cli(["dbaas", "clusters", "list"])

    assert exit_code == 0, stderr
    assert "results" in jsonout
    assert "meta" in jsonout

# def test_dbaas_clusters_start():
#     assert 1 == 2

# def test_dbaas_clusters_stop():
#     assert 1 == 2

# def test_dbaas_clusters_delete():
#     assert 1 == 2

