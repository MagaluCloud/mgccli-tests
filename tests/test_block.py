import random
import time
from utils import run_cli

block_test_context = {}


def _get_volume(volume_id):
    return run_cli(["bs", "volumes", "get", volume_id])


def _get_snapshot(snap_id):
    return run_cli(["bs", "snapshots", "get", snap_id])


def test_bs_volume_types_list():
    exit_code, _, stderr, jsonout = run_cli(["bs", "volume-types", "list"])
    assert exit_code == 0, stderr
    assert len(jsonout["types"]) > 0


def test_bs_volumes_create():
    exit_code, _, stderr, jsonout = run_cli(
        [
            "bs",
            "volumes",
            "create",
            f"--name=test-volume-{random.randint(0, 9999)}",
            "--size=10",
            "--type.name=cloud_nvme10k",
        ]
    )
    assert exit_code == 0, stderr
    assert "id" in jsonout

    block_test_context["volume_id"] = jsonout["id"]

    # Wait until volume creation is over (hoping it will be)
    _, _, _, jsonout = _get_volume(block_test_context["volume_id"])
    while jsonout["status"] == "creating":
        time.sleep(5)
        _, _, _, jsonout = _get_volume(block_test_context["volume_id"])


def test_bs_volumes_get():
    exit_code, _, stderr, jsonout = _get_volume(block_test_context["volume_id"])
    assert exit_code == 0, stderr
    assert "availability_zone" in jsonout
    assert "encrypted" in jsonout
    assert "id" in jsonout
    assert "name" in jsonout
    assert "size" in jsonout
    assert "state" in jsonout
    assert "status" in jsonout
    assert "type" in jsonout


def test_bs_snapshots_create():
    exit_code, _, stderr, jsonout = run_cli(
        [
            "bs",
            "snapshots",
            "create",
            f"--name=test-snapshot-{random.randint(0, 9999)}",
            "--description='just for testing'",
            f"--volume.id={block_test_context["volume_id"]}",
        ]
    )
    assert exit_code == 0, stderr
    assert "id" in jsonout

    block_test_context["snapshot_id"] = jsonout["id"]

    # Wait until snapshot creation is over (hoping it will be)
    _, _, _, jsonout = _get_snapshot(block_test_context["snapshot_id"])
    while jsonout["status"] == "creating":
        time.sleep(5)
        _, _, _, jsonout = _get_snapshot(block_test_context["snapshot_id"])


def test_bs_snapshots_list():
    exit_code, _, stderr, jsonout = run_cli(["bs", "snapshots", "list"])
    assert exit_code == 0, stderr
    assert len(jsonout["snapshots"]) > 0


def test_bs_snapshots_get():
    exit_code, _, stderr, jsonout = run_cli(
        ["bs", "snapshots", "get", block_test_context["snapshot_id"]]
    )
    assert exit_code == 0, stderr
    assert "availability_zones" in jsonout
    assert "description" in jsonout
    assert "id" in jsonout
    assert "name" in jsonout
    assert "size" in jsonout
    assert "state" in jsonout
    assert "status" in jsonout
    assert "type" in jsonout
    assert "volume" in jsonout


def test_bs_snapshots_delete():
    exit_code, _, stderr, jsonout = run_cli(
        ["bs", "snapshots", "delete", block_test_context["snapshot_id"], "--no-confirm"]
    )
    assert exit_code == 0, stderr
    # Extra wait to relieve snapshot count for volume
    time.sleep(10)


def test_bs_volumes_delete():
    exit_code, _, stderr, jsonout = run_cli(
        ["bs", "volumes", "delete", block_test_context["volume_id"], "--no-confirm"]
    )
    assert exit_code == 0, stderr
