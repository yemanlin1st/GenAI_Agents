#!/usr/bin/env bash
set -euo pipefail

# DeepSeek Harness skill installer.
# Installs the official Python SDK into an isolated virtual environment.
# No credentials are written by this script.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${DSH_VENV_DIR:-${ROOT_DIR}/.venv}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
DSH_PY_VERSION="${DSH_PY_VERSION:-}"

command -v "$PYTHON_BIN" >/dev/null 2>&1 || {
  echo "ERROR: $PYTHON_BIN is required." >&2
  exit 1
}

"$PYTHON_BIN" - <<'PY'
import sys
if sys.version_info < (3, 10):
    raise SystemExit("ERROR: DeepSeek Harness Python SDK requires Python 3.10+.")
print(f"Python {sys.version.split()[0]}: OK")
PY

if [[ ! -d "$VENV_DIR" ]]; then
  "$PYTHON_BIN" -m venv "$VENV_DIR"
fi

# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"
python -m pip install --upgrade pip

if [[ -n "$DSH_PY_VERSION" ]]; then
  python -m pip install "deepseek-harness-sdk==${DSH_PY_VERSION}"
else
  echo "WARNING: DSH_PY_VERSION is not set. Installing the current published SDK."
  echo "For controlled environments, pin a tested version before promotion."
  python -m pip install deepseek-harness-sdk
fi

python - <<'PY'
from deepseek_harness import DeepSeekHarness
print("DeepSeek Harness Python SDK import: OK")
print("Installation path is isolated; no API credential was configured.")
PY

cat <<EOF

DeepSeek Harness skill runtime is installed in:
  $VENV_DIR

Activate it with:
  source "$VENV_DIR/bin/activate"

Configure credentials at runtime only, for example through your approved secret manager:
  DEEPSEEK_BASE_URL=<approved-endpoint>
  DEEPSEEK_API_KEY=<runtime-secret>

Optional Web UI quick start, when Node.js is available:
  npx @deepseek-ai/dsh web
EOF
