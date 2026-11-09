#!/usr/bin/env bash
set -euo pipefail

# Unix/macOS bootstrap. Windows users: follow README.md instead.

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

python3 -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r server/requirements.txt

python server/manage.py migrate
python server/manage.py populate_data
python server/manage.py runserver
