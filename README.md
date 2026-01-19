# mgc-cli-tests

Functional tests for Magalu Cloud CLI.

## Requirements

- Python 3.10 or higher
- uv (Astral's package manager)
- Make
- [MGC CLI](https://github.com/MagaluCloud/mgccli/) in PATH (or configure via the `MGC_PATH` environment variable)

## Installation and setup

Option A — Manual:
1. Install uv following the official instructions: https://github.com/astral-sh/uv
   - Example (Linux/Mac):
     ```
     curl -LsSf https://astral.sh/uv/install.sh | sh
     ```
   - Restart your terminal after installation.
2. In the project directory, run:
   ```
   uv sync
   uv run pytest --html=report.html --self-contained-html
   ```
3. To run individual test targets:
   ```
   uv run pytest tests/test_auth.py
   uv run pytest tests/test_block.py
   ...
   ```

Option B — Automatic (using the Makefile):
1. Run:
   ```
   make test
   ```
   - The Makefile checks for python3 and curl and attempts to install `uv` via curl into `~/.local/bin/uv` if not present.
   - If the Makefile installs `uv` to `~/.local/bin`, ensure `~/.local/bin` is in your PATH, e.g.:
     ```
     export PATH=$HOME/.local/bin:$PATH
     ```
2. To run individual test targets:
   ```
   make test-auth
   make test-block
   ...
   ```

## HTML report

- The `make test` target generates a self-contained HTML report named `report.html`.
- Open `report.html` in your browser after the run to review results.

## How to run without the Makefile

To run all tests:
```
uv run pytest
```

To run a specific test file:
```
uv run pytest tests/test_lbaas.py
```

## Modules tested

Settings:
- General
- Authorization
- Config
- Profile
- Workspaces

Products:
- Block Storage
- DBaaS
- Network
- Virtual machines
