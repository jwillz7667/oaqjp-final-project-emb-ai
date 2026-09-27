#!/usr/bin/env bash
# Install project-local dependencies, record real results, then serve the lab UI.
set -euo pipefail
cd -- "$(dirname -- "$0")"
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python lab_verify.py
HOST=0.0.0.0 exec .venv/bin/python server.py
