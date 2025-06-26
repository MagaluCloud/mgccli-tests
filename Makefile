test-all:
	MGC_API_KEY=$(MGC_API_KEY) MGC_PATH=$(MGC_PATH) poetry run pytest

test-lbaas:
	MGC_PRINT_COMMAND=True MGC_API_KEY=$(MGC_API_KEY) MGC_PATH=$(MGC_PATH) poetry run pytest tests/test_lbaas.py

test-dbaas:
	MGC_PRINT_COMMAND=True MGC_API_KEY=$(MGC_API_KEY) MGC_PATH=$(MGC_PATH) poetry run pytest tests/test_dbaas.py

test-network:
	MGC_PRINT_COMMAND=True MGC_API_KEY=$(MGC_API_KEY) MGC_PATH=$(MGC_PATH) poetry run pytest tests/test_network.py -v

test-ci: 
	MGC_API_KEY=$(MGC_API_KEY) MGC_PATH=$(MGC_PATH) poetry run pytest --tb=short --ignore=tests/test_auth.py 