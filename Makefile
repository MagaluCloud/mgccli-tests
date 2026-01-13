.PHONY: ensure-deps test test-auth test-block test-dbaas test-lbaas test-network test-object test-profile test-regression test-vm test-workspace

ensure-deps:
	@command -v python3 >/dev/null 2>&1 || { echo "python3 not found. Please install python3 and re-run."; exit 1; }
	@command -v curl >/dev/null 2>&1 || { echo "curl not found. Install curl to allow automatic installation of 'uv'."; exit 1; }
	@command -v uv >/dev/null 2>&1 || ( \
		echo "uv not found — installing via curl..."; \
		mkdir -p ~/.local/bin; \
		UV_URL=$${UV_URL:-https://github.com/uv/uv/releases/latest/download/uv}; \
		if curl -fL "$$UV_URL" -o ~/.local/bin/uv; then \
			chmod +x ~/.local/bin/uv; \
			echo "uv installed at ~/.local/bin/uv"; \
		else \
			echo "Failed to download 'uv' via curl. Please install 'uv' manually."; exit 1; \
		fi )

test: ensure-deps
	@MGC_API_KEY=$(MGC_API_KEY) MGC_PATH=$(MGC_PATH) uv run pytest --html=report.html --self-contained-html

test-auth: ensure-deps
	@MGC_VERBOSE=True MGC_API_KEY=$(MGC_API_KEY) MGC_PATH=$(MGC_PATH) uv run pytest tests/test_auth.py

test-block: ensure-deps
	@MGC_VERBOSE=True MGC_API_KEY=$(MGC_API_KEY) MGC_PATH=$(MGC_PATH) uv run pytest tests/test_block.py

test-dbaas: ensure-deps
	@MGC_VERBOSE=True MGC_API_KEY=$(MGC_API_KEY) MGC_PATH=$(MGC_PATH) uv run pytest tests/test_dbaas.py

test-lbaas: ensure-deps
	@MGC_VERBOSE=True MGC_API_KEY=$(MGC_API_KEY) MGC_PATH=$(MGC_PATH) uv run pytest tests/test_lbaas.py

test-network: ensure-deps
	@MGC_VERBOSE=True MGC_API_KEY=$(MGC_API_KEY) MGC_PATH=$(MGC_PATH) uv run pytest tests/test_network.py

test-object: ensure-deps
	@MGC_VERBOSE=True MGC_API_KEY=$(MGC_API_KEY) MGC_PATH=$(MGC_PATH) uv run pytest tests/test_object.py

test-profile: ensure-deps
	@MGC_VERBOSE=True MGC_API_KEY=$(MGC_API_KEY) MGC_PATH=$(MGC_PATH) uv run pytest tests/test_profile.py

test-regression: ensure-deps
	@MGC_VERBOSE=True MGC_API_KEY=$(MGC_API_KEY) MGC_PATH=$(MGC_PATH) uv run pytest tests/test_regression.py

test-vm: ensure-deps
	@MGC_VERBOSE=True MGC_API_KEY=$(MGC_API_KEY) MGC_PATH=$(MGC_PATH) uv run pytest tests/test_vm.py

test-workspace: ensure-deps
	@MGC_VERBOSE=True MGC_API_KEY=$(MGC_API_KEY) MGC_PATH=$(MGC_PATH) uv run pytest tests/test_workspace.py
