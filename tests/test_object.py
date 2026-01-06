import pytest
import os
from utils import run_cli

object_test_context = {}

bucket_name = "mgc-cli-tests-temp"

MGC_API_KEY = os.environ.get("MGC_API_KEY")


@pytest.mark.skip
def test_objs_api_key_list():
    if not MGC_API_KEY:
        exit_code, _, stderr, jsonout = run_cli(["object-storage", "api-key", "list"])
        assert exit_code == 0, stderr
        assert len(jsonout) > 0
        object_test_context["keys"] = jsonout

@pytest.mark.skip
def test_objs_api_key_set():
    if not MGC_API_KEY:
        exit_code, _, stderr, _ = run_cli(
            ["os", "api-key", "set", object_test_context["keys"][0]["uuid"]]
        )
        assert exit_code == 0, stderr

@pytest.mark.skip
def test_objs_buckets_create():
    exit_code, _, stderr, jsonout = run_cli(["object-storage", "buckets", "create", bucket_name])
    assert exit_code == 0, stderr
    assert "bucket" in jsonout
    assert "bucket_is_prefix" in jsonout
    assert "enable_versioning" in jsonout

@pytest.mark.skip
def test_objs_buckets_list():
    exit_code, _, stderr, jsonout = run_cli(["object-storage", "buckets", "list"])
    assert exit_code == 0, stderr
    assert len(jsonout["Buckets"]) > 0

@pytest.mark.skip
def test_objs_buckets_delete():
    exit_code, _, stderr, jsonout = run_cli(
        ["os", "buckets", "delete", f"--bucket={bucket_name}", "--no-confirm"]
    )
    assert exit_code == 0, stderr
