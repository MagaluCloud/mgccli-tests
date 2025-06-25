run-all:
	MGC_API_KEY=$(MGC_API_KEY) MGC_PATH=$(MGC_PATH) poetry run pytest

run-lbaas:
	MGC_PRINT_COMMAND=True MGC_API_KEY=$(MGC_API_KEY) MGC_PATH=$(MGC_PATH) poetry run pytest tests/test_lbaas.py

run-ci: 
	MGC_API_KEY=$(MGC_API_KEY) MGC_PATH=$(MGC_PATH) poetry run pytest --tb=short --ignore=tests/test_auth.py 