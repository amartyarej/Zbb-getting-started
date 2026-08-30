#!/usr/bin/env bash
# Environment Setup & Requirements Installer for Part 3 Analysis Tutorial

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REQ_FILE="$SCRIPT_DIR/requirements.txt"

echo "============================================================"
echo "Part 3 Detector-Level Analysis: Environment Setup"
echo "============================================================"

# Check Python binary
if command -v python3 &>/dev/null; then
    PYTHON_BIN="python3"
elif command -v python &>/dev/null; then
    PYTHON_BIN="python"
else
    echo "[Error]: Python 3 is not installed or not available in PATH."
    exit 1
fi

echo "Using Python binary: $($PYTHON_BIN --version)"

# Check if pip is available
if ! $PYTHON_BIN -m pip --version &>/dev/null; then
    echo "[Error]: pip is not installed for $($PYTHON_BIN --version)."
    exit 1
fi

# Detect virtual environment (venv, conda) vs system python
IS_VENV=$($PYTHON_BIN -c "import sys; print(sys.prefix != sys.base_prefix)" 2>/dev/null || echo "False")

if [ -n "$VIRTUAL_ENV" ] || [ -n "$CONDA_PREFIX" ] || [ "$IS_VENV" = "True" ]; then
    echo "Environment: Virtual Environment / Conda detected."
    PIP_USER_FLAG=""
else
    echo "Environment: System Python detected. Using '--user' mode for non-sudo compatibility."
    PIP_USER_FLAG="--user"
fi

# Install dependencies
echo "Installing/updating dependencies from requirements.txt..."
$PYTHON_BIN -m pip install $PIP_USER_FLAG -r "$REQ_FILE"

echo ""
echo "============================================================"
echo "Verification: Testing installed HEP packages..."
echo "============================================================"

$PYTHON_BIN -c "
import numpy
import matplotlib
import uproot
import awkward
import scipy
import mplhep
import dcor

print('  [✓] numpy version:      ', numpy.__version__)
print('  [✓] matplotlib version: ', matplotlib.__version__)
print('  [✓] uproot version:     ', uproot.__version__)
print('  [✓] awkward version:    ', awkward.__version__)
print('  [✓] scipy version:      ', scipy.__version__)
print('  [✓] mplhep version:     ', mplhep.__version__)
print('  [✓] dcor version:       ', dcor.__version__)
"

echo "============================================================"
echo "Setup complete! You can now run Part 3 tutorial exercises."
echo "============================================================"
