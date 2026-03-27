#!/usr/bin/env bash
# run_project.sh - self-contained helper script for Weather-Driven-Electricity-Price-Forecasting
# Usage:
#   ./run_project.sh install    # setup Python environment and install dependencies
#   ./run_project.sh start      # launch Streamlit app
#   ./run_project.sh docker     # docker-compose up (build if needed)
#   ./run_project.sh help       # this help message

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

function command_help() {
  cat <<EOF
Usage: $0 <command>

Commands:
  install   Create virtual environment and install Python dependencies
  start     Start the Streamlit app at http://localhost:8501
  docker    Start service via Docker Compose
  check     Validate required model files are present
  help      Show this message

Examples:
  $0 install
  $0 start
  $0 docker
EOF
}

function command_check() {
  echo "Checking required files..."
  local missing=0
  local files_to_check=(
    "src/app.py"
    "requirements.txt"
    "models/lgbm_model.joblib"
    "models/scaler.joblib"
  )
  for f in "${files_to_check[@]}"; do
    if [[ ! -f "$f" ]]; then
      echo "⛔ Missing file: $f"
      missing=1
    else
      echo "✅ Found: $f"
    fi
  done
  if [[ $missing -ne 0 ]]; then
    echo "Please ensure all required files are in place."
    exit 1
  fi
  echo "All required files present."
}

function command_install() {
  command_check
  local venv_dir="${SCRIPT_DIR}/.venv"

  if [[ ! -d "$venv_dir" ]]; then
    echo "Creating virtual environment at $venv_dir"
    python3 -m venv "$venv_dir"
  else
    echo "Using existing virtual environment at $venv_dir"
  fi

  echo "Activating virtual environment..."
  # shellcheck source=/dev/null
  source "$venv_dir/bin/activate"

  echo "Upgrading pip and installing requirements..."
  pip install --upgrade pip
  pip install -r requirements.txt

  echo "Install complete. Activate with: source $venv_dir/bin/activate" 
}

function command_start() {
  command_check
  local venv_dir="${SCRIPT_DIR}/.venv"

  if [[ -f "$venv_dir/bin/activate" ]]; then
    # shellcheck source=/dev/null
    source "$venv_dir/bin/activate"
  else
    echo "Virtualenv not found. Run '$0 install' first."
    exit 1
  fi

  echo "Starting Streamlit app..."
  echo "Open in browser: http://localhost:8501"
  streamlit run src/app.py
}

function command_docker() {
  echo "Starting Docker Compose..."
  docker-compose up --build
}

if [[ $# -lt 1 ]]; then
  command_help
  exit 1
fi

case "$1" in
  help|-h|--help)
    command_help
    ;;
  check)
    command_check
    ;;
  install)
    command_install
    ;;
  start)
    command_start
    ;;
  docker)
    command_docker
    ;;
  *)
    echo "Unknown command: $1" >&2
    command_help
    exit 1
    ;;
esac
