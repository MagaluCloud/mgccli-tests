import random
from utils import run_cli

test_workspace_context = {}
workspace_name = f"test-workspace-{random.randint(0, 9999)}"

def test_workspace_list():
    exit_code, _, _, jsonout = run_cli(["workspace", "list"])
    assert exit_code == 0
    assert isinstance(jsonout, list)
    assert len(jsonout) > 0
    
    for workspace in jsonout:
        if workspace["name"] == "default":
            break
    test_workspace_context["initial_count"] = len(jsonout)

def test_workspace_create():
    exit_code, _, _, jsonout = run_cli(["workspace", "create", workspace_name])
    assert exit_code == 0
    assert jsonout["name"] == workspace_name

def test_workspace_set():
    exit_code, _, _, jsonout = run_cli(["workspace", "set", workspace_name])
    assert exit_code == 0
    assert jsonout["name"] == workspace_name

def test_workspace_get_created():
    exit_code, _, _, jsonout = run_cli(["workspace", "get"])
    assert exit_code == 0
    assert jsonout["name"] == workspace_name


def test_workspace_delete_fails_on_current_profile():
    exit_code, _, _, jsonout = run_cli(["workspace", "delete", workspace_name, "--no-confirm"])
    assert exit_code == 1

def test_workspace_set_default():
    exit_code, _, _, _ = run_cli(["workspace", "set", "default"])
    assert exit_code == 0

def test_workspace_delete():
    exit_code, _, _, jsonout = run_cli(["workspace", "delete", workspace_name, "--no-confirm"])
    assert exit_code == 0
    assert jsonout["name"] == workspace_name

def test_workspace_list_after_delete():
    exit_code, _, _, jsonout = run_cli(["workspace", "list"]) 
    assert exit_code == 0
    assert len(jsonout) == test_workspace_context["initial_count"]
