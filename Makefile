test-all:
	@MGC_API_KEY=$(MGC_API_KEY) MGC_PATH=$(MGC_PATH) poetry run pytest --tb=short -v

test-lbaas:
	@MGC_PRINT_COMMAND=True MGC_API_KEY=$(MGC_API_KEY) MGC_PATH=$(MGC_PATH) poetry run pytest tests/test_lbaas.py --tb=short -v

test-dbaas:
	@MGC_PRINT_COMMAND=True MGC_API_KEY=$(MGC_API_KEY) MGC_PATH=$(MGC_PATH) poetry run pytest tests/test_dbaas.py --tb=short -v

test-network:
	@MGC_PRINT_COMMAND=True MGC_API_KEY=$(MGC_API_KEY) MGC_PATH=$(MGC_PATH) poetry run pytest tests/test_network.py --tb=short -v

test-object:
	@MGC_PRINT_COMMAND=True MGC_API_KEY=$(MGC_API_KEY) MGC_PATH=$(MGC_PATH) poetry run pytest tests/test_object.py --tb=short -v

test-profile:
	@MGC_PRINT_COMMAND=True MGC_API_KEY=$(MGC_API_KEY) MGC_PATH=$(MGC_PATH) poetry run pytest tests/test_profile.py --tb=short -v

test-vm:
	@MGC_PRINT_COMMAND=True MGC_API_KEY=$(MGC_API_KEY) MGC_PATH=$(MGC_PATH) poetry run pytest tests/test_vm.py --tb=short -v

test-workspace:
	@MGC_PRINT_COMMAND=True MGC_API_KEY=$(MGC_API_KEY) MGC_PATH=$(MGC_PATH) poetry run pytest tests/test_workspace.py --tb=short -v

test-regression:
	@MGC_PRINT_COMMAND=True MGC_API_KEY=$(MGC_API_KEY) MGC_PATH=$(MGC_PATH) poetry run pytest tests/test_regression.py --tb=short -v

test-ci: 
	@MGC_API_KEY=$(MGC_API_KEY) MGC_PATH=$(MGC_PATH) poetry run pytest --ignore=tests/test_auth.py --tb=short -v