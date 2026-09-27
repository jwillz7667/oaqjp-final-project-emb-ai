#!/usr/bin/env bash
# Install project-local dependencies, record real results, then serve the lab UI.
set -euo pipefail
cd -- "$(dirname -- "$0")"
if python3 -m venv .venv; then
    project_python=.venv/bin/python
    "$project_python" -m pip install -r requirements.txt
else
    # The course image omits ensurepip; keep the fallback packages project-local.
    project_python=python3
    python3 -m pip install --target .lab-deps -r requirements.txt
    export PYTHONPATH="$PWD/.lab-deps${PYTHONPATH:+:$PYTHONPATH}"
fi
"$project_python" lab_verify.py
HOST=0.0.0.0 exec "$project_python" server.py
